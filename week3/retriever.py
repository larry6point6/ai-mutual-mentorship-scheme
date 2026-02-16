from haystack_integrations.document_stores.opensearch import OpenSearchDocumentStore
from haystack_integrations.components.retrievers.opensearch import (
    OpenSearchBM25Retriever,
    OpenSearchEmbeddingRetriever,
    OpenSearchHybridRetriever,
)
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder


OPENSEARCH = {
    "hosts": ["https://localhost:9200"],
    "index": "public_texts",
    "embedding_dim": 768,
    "use_ssl": True,
    "verify_certs": False,
    "http_auth": ("admin", "OSPassword246"),
}

EMBED_MODEL = "nomic-embed-text"
OLLAMA_ENDPOINT = "http://localhost:11434"
TOP_K = 5


doc_store = OpenSearchDocumentStore(**OPENSEARCH)

query_embedder = OllamaTextEmbedder(
    model=EMBED_MODEL,
    url=OLLAMA_ENDPOINT,
)

os_bm25 = OpenSearchBM25Retriever(
    document_store=doc_store,
    top_k=TOP_K,
)

os_emb = OpenSearchEmbeddingRetriever(
    document_store=doc_store,
    top_k=TOP_K,
)

os_hybrid = OpenSearchHybridRetriever(
    document_store=doc_store,
    embedder=query_embedder,
    top_k=TOP_K,
)


def retrieve(query: str, mode: str = "hybrid") -> str:
    query = query.strip()
    if not query:
        return "Please enter a query."

    # ---- Select retriever ----
    if mode == "bm25":
        result = os_bm25.run(query=query)

    elif mode == "embedding":
        # Explicit query-time embedding
        q_emb = query_embedder.run(text=query)["embedding"]
        result = os_emb.run(query_embedding=q_emb)

    elif mode == "hybrid":
        # Hybrid does embedding internally
        result = os_hybrid.run(query=query)

    else:
        return f"Unknown retrieval mode: {mode}"

    documents = result.get("documents", [])
    if not documents:
        return "No relevant documents found."

    lines = []
    for i, doc in enumerate(documents, start=1):
        snippet = doc.content[:400].strip()
        source = doc.meta.get("source", "unknown")
        lines.append(f"{i}. {snippet}\n   source: {source}")

    return {"text": "\n\n".join(lines), "documents": documents}
