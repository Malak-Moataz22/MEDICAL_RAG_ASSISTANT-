from fastapi import APIRouter, HTTPException
from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.services.retrieval import query_rag_pipeline

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    try:
        result = query_rag_pipeline(request.question)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))