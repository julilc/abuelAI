import numpy as np
from config import openai_client

EMBED_MODEL = "nomic-embed-text"

def embed(text: str) -> np.ndarray:
    response = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    embedding = response.data[0].embedding
    return np.array(embedding, dtype=np.float32)
