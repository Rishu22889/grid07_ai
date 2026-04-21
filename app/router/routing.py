# Routing logic (Phase 1)
# app/router/routing.py

from __future__ import annotations
from typing import List, Tuple

from app.config.settings import ROUTING_THRESHOLD
from app.utils.helpers import print_section, print_table_row
from app.vectorstore.chroma_store import query_similar_bots, build_store, Chroma


personas_store: Chroma | None = None

def get_store() -> Chroma:
    """Get the Chroma vector store, building it if it doesn't exist."""
    global personas_store
    if personas_store is None:
        print_section("Initializing vector store...")
        personas_store = build_store()
    return personas_store

def reset_store() -> None:
    """Reset the Chroma vector store (for testing)."""
    global personas_store
    personas_store = None
    print("[Routing] Vector store reset.")


def route_post_to_bots(post_content: str, threshold: float = ROUTING_THRESHOLD) -> List[Tuple[str, str, float]]:
    """Route a social media post to relevant bot personas based on similarity."""

    print_section("Routing post to bots...")
    print(f"Post content: {post_content}")
    print(f"Routing threshold: {threshold}\n")

    vectorStore = get_store()
    top_results = query_similar_bots(vectorStore, post_content, top_k=5)

    print(f" {'Bot ID':<12} {'Bot Name':<22} {'Score':>10} {'Routed':>7}")
    print(f" {'-'*12} {'-'*22} {'-'*10} {'-'*7}")

    routed_bots: List[Tuple[str, str, float]] = []
    for bot_id, bot_name, score in top_results:
        is_routed = score>=threshold
        print_table_row(bot_id, bot_name, f"{score:.4f}", "Yes" if is_routed else "No")
        if is_routed:
            routed_bots.append((bot_id, bot_name, score))

    print()
    if routed_bots:
        print(f"Post routed to {len(routed_bots)} bot(s).")
    else:
        print("No bots met the routing threshold. Post will not be routed.")
        
    return routed_bots