# vector_store.py
import asyncio
from dataclasses import dataclass
from qdrant_client import AsyncQdrantClient as QdrantClient
from qdrant_client.http.models import PointStruct, Filter
from qdrant_client.http.models import ScoredPoint

from models import Chunk

@dataclass
class SearchResult:
    id: str
    text: str
    score: float
    metadata: dict  # must include at least documentid, sourcefile, chunk_index

# Initialize the Qdrant client (async wrapper)
qdrant = QdrantClient(url="http://localhost:6333")  # async supported

COLLECTION_NAME = "my_collection"
EMBDENING_DIM = 10  # Example dimension, adjust as needed
async def init_collection():
    # Create collection if it doesn't exist
    if  not await qdrant.collection_exists(COLLECTION_NAME):
        await qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={"size": EMBDENING_DIM, "distance": "Cosine"}
        )

async def upsert_chunks(chunks: list[Chunk]):
    points = [
        PointStruct(
            id=chunk.id, 
            vector=chunk.embedding, 
            payload={"metadata": chunk.metadata, "text": chunk.text})
        for chunk in chunks
    ]
    await qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

async def searchsimilar(queryembedding: list[float], top_k: int = 5) -> list[SearchResult]:
    result = await qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=queryembedding,
        limit=top_k
    )
    res =  [
        SearchResult(
            id= p.id,
            text=p.payload.get("text", ""),
            score=p.score,
            metadata=p.payload.get("metadata", {})
        )
        for p in result.points
    ]
    print(res)
    return res

# Example usage
async def main():
    await init_collection()
    

if __name__ == "__main__":
    asyncio.run(main())
