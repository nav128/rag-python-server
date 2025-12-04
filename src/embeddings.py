from openai import OpenAI
from config import EMBEDDINGS_MODEL, OPENAIAPIKEY
client = OpenAI(api_key=OPENAIAPIKEY)

def get_embedding(text: str, dim: int = 10) -> list[float]:
     """Get embedding for the given text using OpenAI API."""
     emb = client.embeddings.create(
            model=EMBEDDINGS_MODEL, 
            input=text,
            dimensions=dim
          )
     return emb.data[0].embedding


if __name__ == "__main__":
    sample_text = "Hello, world!"
    embedding = get_embedding(sample_text)
    print(f"Embedding for '{sample_text}': {embedding}")