import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS

from app.router.routing import route_post_to_bots

from app.config.settings import validate_settings, ROUTING_THRESHOLD
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


@app.route("/api/route", methods=["POST"])
def route_post():
    """Route a post to relevant bot personas using semantic similarity."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    post_content = data.get("post", "").strip()
    threshold = float(data.get("threshold", ROUTING_THRESHOLD))

    if not post_content:
        return jsonify({"error": "Post content is required"}), 400

    if len(post_content) > 5000:
        return jsonify({"error": "Post content too long (max 5000 characters)"}), 400

    print(f"\n{'='*70}")
    print(f"🎯 ROUTING REQUEST (Timestamp: {__import__('time').time()})")
    print(f"{'='*70}")
    print(f"📝 Post: {post_content[:100]}...")
    print(f"🎚️  Threshold: {threshold}")
    print(f"🔧 Using: Semantic Embeddings (Google Gemini + ChromaDB)")

    routed_bots = []
    routing_method = "unknown"
    routing_model = "unknown"
    
    try:
        # Try semantic routing with ChromaDB (works locally with persistent storage)
        routed = route_post_to_bots(post_content, threshold=threshold)
        routed_bots = [
            {
                "bot_id": bot_id,
                "bot_name": bot_name,
                "similarity_score": round(score, 4)
            }
            for bot_id, bot_name, score in routed
        ]
        routing_method = "semantic_embeddings_chromadb"
        routing_model = "Google Gemini embeddings + ChromaDB vector store"
        
        print(f"\n📊 CHROMADB ROUTING RESULTS:")
        for bot in routed_bots:
            print(f"   ✓ {bot['bot_name']:20} Score: {bot['similarity_score']:.4f}")

    except Exception as e:
        print(f"\n⚠️  ChromaDB routing failed: {e}")
        print(f"🔄 Trying serverless semantic routing (on-demand embeddings)...")
        
        # Try serverless semantic routing (no vector DB, compute on each request)
        try:
            from app.router.serverless_routing import serverless_semantic_routing
            routed = serverless_semantic_routing(post_content, threshold=threshold)
            routed_bots = [
                {
                    "bot_id": bot_id,
                    "bot_name": bot_name,
                    "similarity_score": round(score, 4)
                }
                for bot_id, bot_name, score in routed
            ]
            routing_method = "semantic_embeddings_serverless"
            routing_model = "Google Gemini embeddings (computed on-demand, no vector DB)"
            
            print(f"\n📊 SERVERLESS SEMANTIC ROUTING RESULTS:")
            for bot in routed_bots:
                print(f"   ✓ {bot['bot_name']:20} Score: {bot['similarity_score']:.4f}")
                
        except Exception as serverless_error:
            print(f"\n⚠️  Serverless semantic routing failed: {serverless_error}")
            print(f"🔄 Falling back to keyword-based routing...")
            
            # Final fallback: keyword-based routing (no API calls, pure logic)
            try:
                from app.router.keyword_routing import keyword_based_routing
                routed = keyword_based_routing(post_content, threshold=threshold)
                routed_bots = [
                    {
                        "bot_id": bot_id,
                        "bot_name": bot_name,
                        "similarity_score": round(score, 4)
                    }
                    for bot_id, bot_name, score in routed
                ]
                routing_method = "keyword_matching"
                routing_model = "Weighted keyword dictionary (fallback)"
                
                print(f"\n📊 KEYWORD ROUTING RESULTS:")
                for bot in routed_bots:
                    print(f"   ✓ {bot['bot_name']:20} Score: {bot['similarity_score']:.4f}")
                    
            except Exception as keyword_error:
                print(f"\n❌ All routing methods failed!")
                import traceback
                traceback.print_exc()
                
                return jsonify({
                    "error": "Routing system unavailable",
                    "details": {
                        "chromadb": str(e),
                        "serverless": str(serverless_error),
                        "keyword": str(keyword_error)
                    },
                    "type": "RoutingFailure"
                }), 500

    # Add real-time context if available
    context = None
    try:
        from app.tools.real_search import search_web
        print(f"\n🔍 Enriching with Tavily search...")
        search_results = search_web(post_content, max_results=2)
        context = [
            {'title': r.get('title', ''), 'snippet': r.get('content', '')[:150]}
            for r in search_results
        ]
        print(f"✓ Added {len(context)} context items")
    except Exception as e:
        print(f"⚠️  Tavily search skipped: {e}")

    print(f"\n✅ Successfully routed to {len(routed_bots)} bot(s)")
    print(f"{'='*70}\n")

    return jsonify({
        "post": post_content,
        "routed_bots": routed_bots,
        "count": len(routed_bots),
        "threshold": threshold,
        "context": context,
        "method": routing_method,
        "model": routing_model,
        "note": f"Using {routing_method}" + (" + Tavily context" if context else "")
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

    if not parent_post:
        parent_post = ""
    
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


@app.route('/api/debug/embeddings', methods=['POST'])
def debug_embeddings():
    """Debug endpoint to show actual embedding vectors and prove they're not hardcoded"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    try:
        from app.embeddings.embedding_model import get_embedding_model
        from app.router.routing import get_store
        from app.vectorstore.chroma_store import query_similar_bots
        
        embedding_model = get_embedding_model()
        
        # Generate embedding for the input text
        input_embedding = embedding_model.embed_query(text)
        
        # Get the vector store
        store = get_store()
        
        # Query for similar bots
        results = query_similar_bots(store, text, top_k=3)
        
        # Get embeddings for each bot description
        from app.personas.bot_personas import BOTS_BY_ID
        bot_embeddings = {}
        for bot_id, bot_name, score in results:
            bot = BOTS_BY_ID[bot_id]
            bot_embedding = embedding_model.embed_query(bot.description)
            bot_embeddings[bot_id] = {
                "name": bot_name,
                "score": score,
                "embedding_preview": bot_embedding[:10],  # First 10 dimensions
                "embedding_length": len(bot_embedding)
            }
        
        return jsonify({
            "input_text": text,
            "input_embedding_preview": input_embedding[:10],  # First 10 dimensions
            "embedding_length": len(input_embedding),
            "embedding_model": "Google Gemini (models/embedding-001)",
            "bot_results": bot_embeddings,
            "note": "These are REAL embeddings, not hardcoded. Each query generates unique vectors."
        })
    
    except Exception as e:
        return jsonify({
            "error": "Debug failed",
            "details": str(e)
        }), 500


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
