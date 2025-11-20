import numpy as np
import openai

EMBED = openai.Embedding

def embed(text:str)->np.array:
    EMBED.create(
        input = text,
        model = "text-embedding-ada-002"
    )
    return EMBED["data"]['embedding']


    