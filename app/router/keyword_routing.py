from typing import List, Tuple
from app.personas.bot_personas import ALL_BOTS

KEYWORD_WEIGHTS = {
    'bot_a': {
        'ai': 0.9, 'artificial intelligence': 0.95, 'machine learning': 0.9, 'neural network': 0.9,
        'crypto': 0.85, 'cryptocurrency': 0.9, 'bitcoin': 0.8, 'blockchain': 0.85, 'web3': 0.85,
        'space': 0.8, 'spacex': 0.9, 'rocket': 0.8, 'quantum': 0.85, 'quantum computing': 0.9,
        'startup': 0.7, 'silicon valley': 0.85, 'tech': 0.6, 'innovation': 0.7, 'future': 0.6,
        'breakthrough': 0.75, 'revolutionary': 0.7, 'exponential': 0.75, 'automation': 0.7,
        'autonomous': 0.7, 'metaverse': 0.8, 'disruption': 0.7, 'vc': 0.7, 'venture capital': 0.75
    },
    'bot_b': {
        'privacy': 0.9, 'surveillance': 0.95, 'monopoly': 0.85, 'monopolies': 0.85,
        'capitalism': 0.8, 'inequality': 0.85, 'exploitation': 0.85, 'crisis': 0.7,
        'climate': 0.8, 'environmental': 0.75, 'doom': 0.8, 'dystopian': 0.85,
        'authoritarian': 0.85, 'corruption': 0.8, 'greed': 0.75, 'bias': 0.7,
        'manipulation': 0.8, 'censorship': 0.8, 'scandal': 0.75, 'breach': 0.8,
        'abuse': 0.85, 'violation': 0.85, 'threat': 0.7, 'risk': 0.6, 'danger': 0.7,
        'harm': 0.75, 'failure': 0.65, 'collapse': 0.8, 'decline': 0.7
    },
    'bot_c': {
        'trading': 0.9, 'trade': 0.8, 'market': 0.85, 'stock': 0.9, 'investment': 0.9,
        'roi': 0.95, 'profit': 0.85, 'loss': 0.8, 'leverage': 0.9, 'margin': 0.85,
        'portfolio': 0.85, 'hedge': 0.8, 'fund': 0.75, 'alpha': 0.9, 'beta': 0.8,
        'valuation': 0.85, 'earnings': 0.8, 'dividend': 0.85, 'yield': 0.8, 'bond': 0.8,
        'forex': 0.9, 'options': 0.85, 'futures': 0.85, 'commodity': 0.8, 'bull': 0.75,
        'bear': 0.75, 'volatility': 0.8, 'liquidity': 0.8, 'interest rate': 0.85,
        'inflation': 0.8, 'gdp': 0.75, 'fed': 0.8, 'federal reserve': 0.85, 'treasury': 0.8
    }
}


def keyword_based_routing(post_content: str, threshold: float = 0.25) -> List[Tuple[str, str, float]]:
    post_lower = post_content.lower()
    
    scores = {}
    for bot in ALL_BOTS:
        bot_keywords = KEYWORD_WEIGHTS.get(bot.id, {})
        total_score = 0.0
        matches = 0
        
        for keyword, weight in bot_keywords.items():
            if keyword in post_lower:
                total_score += weight
                matches += 1
        
        if matches > 0:
            avg_score = total_score / matches
            match_bonus = min(0.1 * (matches - 1), 0.2)
            normalized_score = min(avg_score + match_bonus, 1.0)
        else:
            normalized_score = 0.3
        
        scores[bot.id] = (bot.id, bot.name, normalized_score)
    
    sorted_bots = sorted(scores.values(), key=lambda x: x[2], reverse=True)
    routed = [(bot_id, bot_name, score) for bot_id, bot_name, score in sorted_bots if score >= threshold]
    
    return routed
