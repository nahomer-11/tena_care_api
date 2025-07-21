import os
from huggingface_hub import InferenceClient

# Load token and initialize client
HF_TOKEN = os.getenv("HF_API_TOKEN")  # Make sure this is in your .env
MODEL = "intfloat/multilingual-e5-base"

client = InferenceClient(
    model=MODEL,
    token=HF_TOKEN,
)

def get_hf_embedding(text: str) -> list[float]:
    """
    Returns a 768-dimensional embedding vector for the given input text
    using the intfloat/multilingual-e5-base model via Hugging Face Inference API.
    """
    try:
        return client.feature_extraction(
            text,
            normalize=True,
            prompt_name="query",  # Automatically adds "query: " to text
        )
    except Exception as e:
        raise RuntimeError(f"HuggingFace API error: {e}")
