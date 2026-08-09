from typing import List, Tuple
import numpy as np
from app.personas.bot_personas import ALL_BOTS
from app.embeddings.embedding_model import get_embedding_model


def cosine_similarity(a: List[float], b: List[float]) -> float:
    a_np = np.array(a)
    b_np = np.array(b)
    return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))


def serverless_semantic_routing(post_content: str, threshold: float = 0.25) -> List[Tuple[str, str, float]]:
    try:
        embedding_model = get_embedding_model()
        
        post_embedding = embedding_model.embed_query(post_content)
        
        results = []
        for bot in ALL_BOTS:
            bot_embedding = embedding_model.embed_query(bot.description)
            similarity = cosine_similarity(post_embedding, bot_embedding)
            
            if similarity >= threshold:
                results.append((bot.id, bot.name, similarity))
        
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results
    
    except Exception as e:
        print(f"Serverless semantic routing failed: {e}")
        raise
