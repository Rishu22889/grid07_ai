# Mock search tool
# app/tools/mock_search.py
# Currently using tag-based classification for simplicity.
# This can be extended using embedding similarity for better semantic matching.

TAGS_DB = {
    "finance": [
        "finance", "market", "markets", "trading", "stocks", "equity",
        "interest rate", "rates", "fed", "federal reserve",
        "inflation", "recession", "bond", "yield",
        "liquidity", "macro", "monetary policy",
        "arbitrage", "hedge", "alpha", "risk reward",
        "portfolio", "returns", "pnl",
        "china", "debt", "real estate", "default",
        "economic slowdown"
    ],

    "crypto": [
        "crypto", "bitcoin", "ethereum", "blockchain",
        "web3", "defi", "nft",
        "token", "mining", "staking",
        "crypto market", "exchange", "wallet"
    ],

    "ai": [
        "ai", "artificial intelligence", "machine learning",
        "deep learning", "llm", "gpt", "model",
        "automation", "neural network",
        "ai agents", "generative ai", "chatbot"
    ],

    "privacy": [
        "privacy", "data", "surveillance",
        "tracking", "user data", "personal data",
        "cybersecurity", "data breach",
        "regulation", "gdpr", "compliance"
    ]
}

def detect_categories(query: str):
    query = query.lower()
    matched = []

    for category, tags in TAGS_DB.items():
        if any(tag in query for tag in tags):
            matched.append(category)

    return matched if matched else ["general"]

def mock_searxng_search(query: str):
    """This function returns mock search results based on simple keyword matching."""
    query = query.lower().replace("'", "")

    category = detect_categories(query)

    if category == "finance":
        return [
            "Federal Reserve signals pause in rate hikes amid slowing inflation",
            "China property sector faces liquidity crisis and rising defaults",
            "Markets react as bond yields stabilize globally"
        ]

    elif category == "crypto":
        return [
            "Bitcoin hits new all-time high amid ETF inflows",
            "Crypto market sees increased institutional adoption"
        ]

    elif category == "ai":
        return [
            "New AI model replaces junior developer tasks",
            "AI startups attract billions in funding"
        ]

    elif category == "privacy":
        return [
            "Big tech faces backlash over data privacy violations",
            "New regulations target surveillance practices"
        ]

    return [
            "Big tech data centers consume massive energy despite green claims",
            "AI infrastructure expansion increases carbon footprint"
    ]