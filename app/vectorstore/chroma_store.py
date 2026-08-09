# ChromaDB setup
# app/vectorstore/chroma_store.py

from __future__ import annotations
from functools import lru_cache
from typing import List, Tuple
import os

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config.settings import CHROMA_DIR, CHROMA_NAME
from app.embeddings.embedding_model import get_embedding_model
from app.personas.bot_personas import ALL_BOTS, BotPersona

@lru_cache(maxsize=1)
def _get_client() -> chromadb.ClientAPI:
    """
    Get ChromaDB client - hosted or local based on environment.
    
    For hosted ChromaDB (Vercel/production):
    - Set CHROMA_HOST (e.g., 'api.trychroma.com' or 'your-instance.trychroma.com')
    - Set CHROMA_API_KEY (your API token)
    
    For local ChromaDB (development):
    - Don't set CHROMA_HOST
    - Uses persistent local storage in ./chroma_db/
    """
    chroma_host = os.getenv('CHROMA_HOST')
    chroma_api_key = os.getenv('CHROMA_API_KEY')
    
    if chroma_host:
        # Use hosted ChromaDB for serverless environments
        print(f"[ChromaDB] Connecting to hosted instance: {chroma_host}")
        
        headers = {}
        if chroma_api_key:
            headers["Authorization"] = f"Bearer {chroma_api_key}"
            print(f"[ChromaDB] Using API key authentication")
        
        # Parse host and port if specified
        if ':' in chroma_host:
            host, port = chroma_host.rsplit(':', 1)
            port = int(port)
        else:
            host = chroma_host
            port = 443  # Default HTTPS port
        
        return chromadb.HttpClient(
            host=host,
            port=port,
            ssl=True,
            headers=headers,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=False
            )
        )
    else:
        # Use local persistent ChromaDB for development
        print(f"[ChromaDB] Using local persistent storage: {CHROMA_DIR}")
        return chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False)
        )


def build_store(bots: List[BotPersona] = ALL_BOTS) -> Chroma:
    """Build a Chroma vector store for the given bots."""
    embedding_model = get_embedding_model()
    client = _get_client()

    try:
        client.delete_collection(CHROMA_NAME)
        print(f"[ChromaDB] Deleted existing collection: {CHROMA_NAME}")
    except Exception:
        pass

    vectorStore = Chroma(
        client=client,
        collection_name=CHROMA_NAME,
        embedding_function=embedding_model
    )
    
    ids = [bot.id for bot in bots]

    documents = [
        Document(page_content=bot.description, metadata={"bot_id": bot.id, "bot_name": bot.name})
            for bot in bots
    ] 

    vectorStore.add_documents(documents=documents, ids=ids)
    print(f"[ChromaDB] Built vector store with {len(bots)} bot personas.")
    return vectorStore

def query_similar_bots(
        vectorStore: Chroma,
        post: str,
        top_k: int = 3,
    ) -> List[Tuple[str, str, float]]:

    """Query the vector store for bots similar to the given post."""
    
    print(f"\n🔍 Querying ChromaDB vector store...")
    print(f"   Query: '{post[:80]}...'")
    print(f"   Top K: {top_k}")

    results = vectorStore.similarity_search_with_relevance_scores(post, k=top_k)

    hits: List[Tuple[str, str, float]] = []

    print(f"\n📊 Raw similarity scores from embeddings:")
    for doc, score in results:
        bot_id = doc.metadata.get("bot_id")
        bot_name = doc.metadata.get("bot_name")
        print(f"   {bot_name:20} | Score: {score:.4f}")
        hits.append((bot_id, bot_name, round(score,4)))

    return sorted(hits, key=lambda x: x[2], reverse=True)
