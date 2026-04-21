# Mock search tool

def mock_searxng_search(query: str):
    if "crypto" in query.lower():
        return ["Bitcoin hits new all-time high"]
    elif "ai" in query.lower():
        return ["New AI model released"]
    return ["General news headline"]
