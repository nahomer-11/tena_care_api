import os
from typing import List
from pydantic import Field
from qdrant_client import QdrantClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from .embedding import get_hf_embedding

# Load environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# ✅ Custom Retriever (must subclass BaseRetriever and declare fields with Pydantic)
class HFQdrantRetriever(BaseRetriever):
    client: QdrantClient = Field()
    collection: str = Field()

    def _get_relevant_documents(self, query: str) -> List[Document]:
        vector = get_hf_embedding(query)
        results = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=5,
        )
        return [
            Document(page_content=hit.payload["text"])
            for hit in results
        ]

# Create retriever instance
retriever = HFQdrantRetriever(client=client, collection=COLLECTION_NAME)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Create RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
)
