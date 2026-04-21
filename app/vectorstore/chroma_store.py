# ChromaDB setup
# app/vectorstore/chroma_store.py

from __future__ import annotations
from functools import lru_cache
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma

from app.config.settings import CHROMA_DIR, CHROMA_NAME
from app.embeddings.embedding_model import get_embedding_model
from app.personas.bot_personas import ALL_BOTS, BotPersona

@lru_cache(maxsize=1)
def get_client() -> chromadb.ClientAPI:
    """Return a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))


def build_store(bots: List[BotPersona] = ALL_BOTS) -> Chroma:
    """Build a Chroma vector store for the given bots."""
    embedding_model = get_embedding_model()
    client = get_client()

    try:
        client.delete_collection(CHROMA_NAME)
    except Exception:
        pass

    vectorStore = Chroma(
        client=client,
        collection_name=CHROMA_NAME,
        embedding_function=embedding_model
    )

    desc = [bot.description for bot in bots]
    metadatas = [{"bot_id": bot.id, "bot_name": bot.name} for bot in bots]
    ids = [bot.id for bot in bots]

    vectorStore.add(documents=desc, metadatas=metadatas, ids=ids)
    print(f"[ChromaDB] Built vector store with {len(bots)} bot personas.")
    return vectorStore

def query_similar_bots(
        vectorStore: Chroma,
        post: str,
        top_k: int = 3,
    ) -> List[Tuple[BotPersona, float]]:

    """Query the vector store for bots similar to the given post."""

    results = vectorStore.similarity_search_with_relevance_scores(post, k=top_k)

    hits: List[Tuple[str, str, float]] = []

    for doc, score in results:
        bot_id = doc.metadata.get("bot_id")
        bot_name = doc.metadata.get("bot_name")
        hits.append((bot_id, bot_name, round(score,4)))

    return sorted(hits, key=lambda x: x[2], reverse=True)





