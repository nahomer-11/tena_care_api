# core/web_embedding.py

import os
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = "thenlper/gte-large"

client = InferenceClient(
    model=MODEL,
    token=HF_TOKEN,
)

def get_hf_embedding(text: str) -> list[float]:
    """
    Returns a 1024-dimensional embedding vector using gte-large via Hugging Face API.
    """
    try:
        return client.feature_extraction(
            text,
            normalize=True
        )
    except Exception as e:
        raise RuntimeError(f"HuggingFace API error: {e}")
