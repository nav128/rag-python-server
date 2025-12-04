from datetime import time
from pydantic import BaseModel, Field
from uuid import uuid4

# Rag models
class Chunk(BaseModel):
    """Result from RAG search."""
    chunk_id: str
    text: str
    relevance_score: float
    source_file: str

class SearchResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    metadata: dict
    embedding: list[float] = Field(default_factory=list)


# Agent models
class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str | None = time().isoformat()

class AgentState(BaseModel):
    """Agent execution state."""
    conversation_history: list[ChatMessage]
    search_results: list[SearchResult] = []

class MyOutput(BaseModel):
    message: str
