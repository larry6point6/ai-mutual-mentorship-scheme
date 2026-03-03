from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from .pipelines import build_pipelines

app = FastAPI(title="RAG Service (Ingest + Query)", version="1.0.0")

PIPELINES = None


class IngestRequest(BaseModel):
    urls: List[HttpUrl]


class IngestResponse(BaseModel):
    urls_received: int
    status: str


class QueryRequest(BaseModel):
    query: str


@app.on_event("startup")
def startup():
    global PIPELINES
    PIPELINES = build_pipelines()

@app.get("/")
def root():
    return {"message": "Welcome to the Haystack RAG Service! Use /ingest to add documents and /query to ask questions."}

@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    if PIPELINES is None:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        ingestion = PIPELINES["ingestion"]
        ingestion.run(
            {"fetcher": {"urls": [str(u) for u in req.urls]}}
        )
        return IngestResponse(
            urls_received=len(req.urls),
            status="ok",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(req: QueryRequest):
    if PIPELINES is None:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        retrieval = PIPELINES["retrieval"]
        result = retrieval.run(
            {
                "query_embedder": {"text": req.query},
                "prompt_builder": {"query": req.query},
            },
            include_outputs_from={"retriever"},
        )

        replies = result.get("response_generator", {}).get("replies") or []
        answer = replies[0] if replies else ""

        docs = result.get("retriever", {}).get("documents") or []
        returned_docs = [{"content": d.content, "meta": d.meta} for d in docs]

        return {
            "answer": answer,
            "documents": returned_docs,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))