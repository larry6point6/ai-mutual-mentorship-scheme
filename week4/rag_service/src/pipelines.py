import os
from haystack import Pipeline
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.writers import DocumentWriter
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.builders import PromptBuilder

from haystack_integrations.document_stores.opensearch import OpenSearchDocumentStore
from haystack_integrations.components.embedders.ollama import (
    OllamaDocumentEmbedder,
    OllamaTextEmbedder,
)
from haystack_integrations.components.retrievers.opensearch import (
    OpenSearchEmbeddingRetriever,
)
from haystack_integrations.components.generators.ollama import OllamaGenerator


DEFAULT_TEMPLATE = """You are a helpful assistant. Use the following documents as context.
If the answer isn't in the documents, say you don't know.

Query: {{ query }}

Documents:
{% for doc in documents %}
- {{ doc.content }}
{% endfor %}

Answer:"""


def _document_store() -> OpenSearchDocumentStore:
    """
    OpenSearch runs with security disabled in docker-compose,
    so we connect over plain HTTP with no auth.
    """
    opensearch_url = os.getenv("OPENSEARCH_URL", "http://opensearch:9200")
    index_name = os.getenv("INDEX_NAME", "documents")

    return OpenSearchDocumentStore(
        hosts=opensearch_url,
        index=index_name,
        use_ssl=True,
        verify_certs=False,
        http_auth=("admin", "OSPassword246"),
    )


def build_ingestion_pipeline(document_store: OpenSearchDocumentStore) -> Pipeline:
    user_agent = os.getenv(
        "FETCHER_USER_AGENT",
        "ai-mutual-mentorship/0.1 (https://github.com/larry6point6/ai-mutual-mentorship-scheme)",
    )

    fetcher = LinkContentFetcher(user_agents=[user_agent])
    converter = HTMLToDocument()
    cleaner = DocumentCleaner()
    splitter = DocumentSplitter(
        split_by="word",
        split_length=200,
        split_overlap=15,
    )

    ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
    embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    doc_embedder = OllamaDocumentEmbedder(
        model=embed_model,
        url=ollama_url,
    )

    writer = DocumentWriter(
        document_store=document_store,
        policy=DuplicatePolicy.SKIP,
    )

    p = Pipeline()
    p.add_component(instance=fetcher, name="fetcher")
    p.add_component(instance=converter, name="converter")
    p.add_component(instance=cleaner, name="cleaner")
    p.add_component(instance=splitter, name="splitter")
    p.add_component(instance=doc_embedder, name="doc_embedder")
    p.add_component(instance=writer, name="writer")

    p.connect("fetcher.streams", "converter")
    p.connect("converter", "cleaner")
    p.connect("cleaner", "splitter")
    p.connect("splitter", "doc_embedder")
    p.connect("doc_embedder", "writer")

    return p


def build_retrieval_pipeline(document_store: OpenSearchDocumentStore) -> Pipeline:
    ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")

    embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    llm_model = os.getenv("OLLAMA_LLM_MODEL", "llama3.2")
    top_k = int(os.getenv("TOP_K", "5"))

    query_embedder = OllamaTextEmbedder(
        model=embed_model,
        url=ollama_url,
    )

    retriever = OpenSearchEmbeddingRetriever(
        document_store=document_store,
        top_k=top_k,
    )

    prompt_template = os.getenv("PROMPT_TEMPLATE", DEFAULT_TEMPLATE)
    prompt_builder = PromptBuilder(template=prompt_template)

    generator = OllamaGenerator(
        model=llm_model,
        url=ollama_url,
    )

    p = Pipeline()
    p.add_component("query_embedder", query_embedder)
    p.add_component("retriever", retriever)
    p.add_component("prompt_builder", prompt_builder)
    p.add_component("response_generator", generator)

    p.connect("query_embedder.embedding", "retriever.query_embedding")
    p.connect("retriever.documents", "prompt_builder.documents")
    p.connect("prompt_builder", "response_generator")

    return p


def build_pipelines():
    ds = _document_store()
    return {
        "document_store": ds,
        "ingestion": build_ingestion_pipeline(ds),
        "retrieval": build_retrieval_pipeline(ds),
    }