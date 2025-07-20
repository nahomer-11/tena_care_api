import requests
import os

HF_TOKEN = os.getenv("HF_API_TOKEN")  # put in .env
MODEL = "intfloat/multilingual-e5-base"

def get_hf_embedding(text: str):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    json_data = {
        "inputs": f"query: {text.strip()}"
    }
    response = requests.post(
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL}",
        headers=headers,
        json=json_data
    )
    if response.status_code != 200:
        raise Exception(f"HF API failed: {response.text}")
    return response.json()[0]  # Returns the vector
