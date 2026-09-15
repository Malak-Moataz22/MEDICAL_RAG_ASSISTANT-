from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.query import router as query_router
from backend.app.services.retrieval import get_vector_store
from backend.app.utils.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="Medical RAG API",
    version="1.0.0"
)

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    get_vector_store()


app.include_router(query_router, prefix="/api", tags=["RAG Query"])


@app.get("/")
def root():
    return {"message": "Welcome to the Medical RAG Assistant API!"}


@app.get("/health")
def health():
    return {"status": "ok"}