from pydantic import BaseModel, Field
from uuid import uuid4

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    metadata: dict
    embedding: list[float] = Field(default_factory=list)


if __name__ == "__main__":
    sample_chunk = Chunk(
        text="This is a sample chunk.",
        metadata={"documentid": "doc1", "sourcefile": "file1.txt", "chunk_index": 0},
        embedding=[0.1, 0.2, 0.3]
    )
    print(sample_chunk)