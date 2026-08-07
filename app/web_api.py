import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS

from app.config.settings import validate_settings
from app.personas.bot_personas import ALL_BOTS, BOTS_BY_ID

try:
    from app.rag.defense import generate_defense_reply
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

try:
    from app.graph.langgraph_flow import run_agent
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

app = Flask(__name__)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=ALLOWED_ORIGINS)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

try:
    validate_settings()
    print("✅ Settings validated successfully")
except ValueError as e:
    print(f"❌ Invalid settings: {e}")
    sys.exit(1)


@app.route('/api/bots', methods=['GET'])
def get_bots():
    """Get list of all available bot personas"""
    bots_info = [
        {
            'id': bot.id,
            'name': bot.name,
            'description': bot.description
        }
        for bot in ALL_BOTS
    ]
    return jsonify({'bots': bots_info})


@app.route('/api/route', methods=['POST'])
def route_post():
    """Route a post to relevant bot personas"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    post_content = data.get('post', '').strip()
    
    if not post_content:
        return jsonify({'error': 'Post content is required'}), 400
    
    if len(post_content) > 5000:
        return jsonify({'error': 'Post content too long (max 5000 characters)'}), 400
    
    post_lower = post_content.lower()
    routed = []
    
    if any(word in post_lower for word in ['ai', 'tech', 'innovation', 'crypto', 'space', 'future']):
        routed.append({'bot_id': 'bot_a', 'bot_name': 'Tech Maximalist', 'similarity_score': 0.85})
    
    if any(word in post_lower for word in ['problem', 'monopoly', 'privacy', 'surveillance', 'capitalism']):
        routed.append({'bot_id': 'bot_b', 'bot_name': 'Doomer', 'similarity_score': 0.82})
    
    if any(word in post_lower for word in ['market', 'stock', 'price', 'money', 'trade', 'invest', 'bitcoin']):
        routed.append({'bot_id': 'bot_c', 'bot_name': 'Finance Bro', 'similarity_score': 0.88})
    
    if not routed:
        routed = [
            {'bot_id': 'bot_a', 'bot_name': 'Tech Maximalist', 'similarity_score': 0.55},
            {'bot_id': 'bot_b', 'bot_name': 'Doomer', 'similarity_score': 0.52},
            {'bot_id': 'bot_c', 'bot_name': 'Finance Bro', 'similarity_score': 0.50}
        ]
    
    return jsonify({
        'post': post_content,
        'routed_bots': routed,
        'count': len(routed),
        'note': 'Using keyword-based routing (ChromaDB disabled for Vercel deployment)'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with a specific bot persona"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    bot_id = data.get('bot_id', '').strip()
    message = data.get('message', '').strip()
    parent_post = data.get('parent_post', '').strip()
    comment_history = data.get('comment_history', [])
    
    if not bot_id:
        return jsonify({'error': 'bot_id is required'}), 400
    
    if not message:
        return jsonify({'error': 'message is required'}), 400
    
    if len(message) > 5000:
        return jsonify({'error': 'Message too long (max 5000 characters)'}), 400
    
    if bot_id not in BOTS_BY_ID:
        return jsonify({'error': f'Invalid bot_id: {bot_id}'}), 404
    
    try:
        bot = BOTS_BY_ID[bot_id]
        
        if RAG_AVAILABLE:
            bot_reply, injection_detected = generate_defense_reply(
                bot_persona=bot,
                parent_post=parent_post or message,
                comment_history=comment_history,
                human_reply=message
            )
        else:
            bot_reply = f"[{bot.name}] I received your message about: {message[:50]}..."
            injection_detected = False
        
        return jsonify({
            'bot_id': bot_id,
            'bot_name': bot.name,
            'reply': bot_reply,
            'injection_detected': injection_detected
        })
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate autonomous content for a bot"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    bot_id = data.get('bot_id', '').strip()
    
    if not bot_id:
        return jsonify({'error': 'bot_id is required'}), 400
    
    if bot_id not in BOTS_BY_ID:
        return jsonify({'error': f'Invalid bot_id: {bot_id}'}), 404
    
    bot = BOTS_BY_ID[bot_id]
    
    if LANGGRAPH_AVAILABLE:
        try:
            result = run_agent(bot)
            return jsonify({
                'bot_id': result['bot_id'],
                'topic': result['topic'],
                'post_content': result['post_content'],
                'note': 'Generated using LangGraph autonomous pipeline'
            })
        except Exception as e:
            app.logger.error(f"LangGraph error: {str(e)}")
            return jsonify({'error': 'Content generation failed'}), 500
    else:
        import random
        topics = {
            'bot_a': ['AI Breakthrough', 'Crypto Adoption', 'Space Technology', 'Future of Work'],
            'bot_b': ['Tech Monopolies', 'Privacy Crisis', 'Surveillance State', 'Climate Impact'],
            'bot_c': ['Market Volatility', 'Interest Rates', 'Investment Strategy', 'Economic Trends']
        }
        
        topic = random.choice(topics.get(bot_id, ['Technology Update']))
        
        responses = {
            'bot_a': f"The future is here! {topic} is accelerating faster than anyone predicted. This is massive.",
            'bot_b': f"Another day, another problem. {topic} shows exactly what's wrong with unchecked growth.",
            'bot_c': f"From a market perspective, {topic} presents interesting alpha opportunities. Watch the spreads."
        }
        
        return jsonify({
            'bot_id': bot_id,
            'topic': topic,
            'post_content': responses.get(bot_id, 'Content generated.'),
            'note': 'Using simplified generation (LangGraph disabled for Vercel)'
        })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Grid07 AI API'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


app_vercel = app


def handler(event, context):
    return app(event, context)


if __name__ == '__main__':
    print("\n🚀 Starting Grid07 AI Web API...")
    print("📡 API will be available at: http://localhost:5001")
    print("🤖 Available endpoints:")
    print("   - GET  /api/bots      - List all bot personas")
    print("   - POST /api/route     - Route posts to bots")
    print("   - POST /api/chat      - Chat with a bot")
    print("   - POST /api/generate  - Generate autonomous content")
    print("   - GET  /health        - Health check")
    print("\n")
    
    is_production = os.getenv('FLASK_ENV') == 'production'
    app.run(
        host='127.0.0.1' if not is_production else '0.0.0.0',
        port=5001,
        debug=not is_production
    )
