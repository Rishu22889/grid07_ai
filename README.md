# Grid07 AI – Cognitive Routing & RAG System

[![CI/CD Pipeline](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/ci.yml)
[![Docker Publish](https://github.com/Rishu22889/grid07_ai/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/docker-publish.yml)
[![Vercel Deploy](https://github.com/Rishu22889/grid07_ai/actions/workflows/vercel-deploy.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/vercel-deploy.yml)
[![LLM Evaluation](https://github.com/Rishu22889/grid07_ai/actions/workflows/evaluation.yml/badge.svg)](https://github.com/Rishu22889/grid07_ai/actions/workflows/evaluation.yml)

**Live Demo:** https://grid07ai.vercel.app

An AI-powered chatbot system featuring three distinct AI personas with vector-based routing, RAG-enhanced conversations, and prompt injection defense. Built with Flask, LangChain, and deployed on Vercel.

**📚 [Quick Start Guide](./QUICKSTART.md)** | **🧪 [Evaluation Docs](./eval/README.md)**

## Screenshots

### Phase 1: Vector Persona Router
![Phase 1 - Router](./static/phase-1.png)
Semantic routing using vector similarity to match messages with relevant AI personas.

### Phase 2: Autonomous Content Engine
![Phase 2 - Content](./static/phase-2.png)
LangGraph-powered content generation with personality-driven topic selection.

### Phase 3: RAG Combat Defense
![Phase 3 - Combat](./static/phase-3.png)
Prompt injection resistance testing with full conversational context.

---

## Overview

This project demonstrates a production-ready AI system that routes user queries to specialized AI personas, maintains context across multi-turn conversations, and defends against prompt injection attacks. The system combines semantic routing, retrieval-augmented generation, and autonomous content creation.

### What It Does

- Chat with three distinct AI personas, each with unique viewpoints and expertise
- Automatically route messages to relevant personas using vector similarity
- Maintain conversation context across multiple turns using RAG
- Detect and neutralize prompt injection attempts
- Generate autonomous content based on personality traits

---

## Features

### Three AI Personas

**Tech Maximalist**
An optimistic futurist who believes technological advancement, especially in AI, crypto, and space exploration, will solve humanity's challenges. Influenced by Silicon Valley thinking and supportive of visionary entrepreneurs.

**Doomer**
A critical observer who questions late-stage capitalism, big tech monopolies, and unchecked AI development. Values decentralization, privacy, and sustainability while highlighting systemic risks.

**Finance Bro**
A market-obsessed analyst who evaluates everything through the lens of money, risk, and returns. Focused on trading, macroeconomics, and financial systems with an emphasis on ROI.

### Smart Routing

The system uses semantic understanding to match incoming messages with the most relevant personas. In local development, this uses vector embeddings and ChromaDB. On Vercel, it falls back to keyword-based routing to work within serverless constraints.

### RAG-Enhanced Conversations

Rather than treating each message in isolation, the system maintains full conversation history and context. This allows for coherent multi-turn discussions where the AI remembers what was said earlier and builds upon it logically.

### Prompt Injection Defense

The system treats all user input as potentially malicious. It includes detection mechanisms for common injection patterns like "ignore all previous instructions" and maintains persona consistency even when users attempt to manipulate the AI's behavior.

---

## Architecture

The system is built in three main phases, each handling a specific aspect of the AI interaction:

### Phase 1: Cognitive Routing

Instead of broadcasting every message to all personas, the system uses semantic embeddings to determine relevance. Each persona has an embedded representation of their expertise and interests. Incoming messages are embedded using the same model, and cosine similarity determines which personas are most relevant.

In production on Vercel, vector operations are replaced with keyword matching to avoid serverless limitations, but the core concept remains the same.

### Phase 2: Autonomous Content Engine

Personas can generate content autonomously using LangGraph state machines. The process involves:

1. Deciding on a topic based on the persona's interests
2. Gathering relevant context through search
3. Drafting content that aligns with their viewpoint

This demonstrates how AI agents can operate independently while maintaining consistent character.

### Phase 3: RAG with Security

The most critical component handles actual conversations. For each user message, the system:

1. Retrieves full conversation context including parent posts and comment history
2. Constructs a comprehensive prompt with all relevant information
3. Generates a response that's both contextually appropriate and consistent with the persona
4. Monitors for injection attempts and ignores malicious instructions

This ensures conversations feel natural and coherent while maintaining security.

---

## Technical Stack

### Backend
- **Python 3.13**: Core language
- **Flask**: REST API framework
- **Flask-CORS**: Cross-origin requests
- **LangChain**: LLM orchestration
- **LangGraph**: State machine workflows
- **Groq API**: Fast LLM inference (Llama 3.3 70B)
- **Google Gemini**: Embedding generation
- **ChromaDB**: Vector database (local only)

### Frontend
- **React 19**: UI framework
- **TypeScript 6**: Type safety
- **Vite 8**: Build tool and dev server
- **CSS3**: Custom styling (professional dark theme)
- **Responsive Design**: Mobile and desktop support

### Infrastructure & DevOps
- **Docker & Docker Compose**: Containerization and orchestration
- **Nginx**: Reverse proxy for production
- **Vercel**: Serverless deployment with automatic HTTPS
- **GitHub Actions**: CI/CD pipelines
- **GitHub Container Registry**: Docker image hosting

### Development Tools
- **Ruff**: Python linting
- **Black**: Python code formatting
- **oxlint**: TypeScript/JavaScript linting
- **Trivy**: Security vulnerability scanning

### Evaluation & Testing
- **Groq API (Llama 3.3 70B)**: LLM-as-Judge evaluation
- **Custom Test Suite**: 30 curated test cases
- **Automated CI/CD Testing**: Weekly evaluation runs

---

## Deployment

### Quick Start with Docker

The easiest way to run the entire stack:

```bash
# Clone the repository
git clone https://github.com/Rishu22889/grid07_ai.git
cd grid07_ai

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run with Docker Compose
docker-compose up --build
```

Access the application:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5001

See [DOCKER.md](./DOCKER.md) for detailed Docker documentation.

### Deploy to Vercel

1. Clone the repository:
```bash
git clone <your-repository>
cd grid07_ai
```

2. Deploy using Vercel CLI:
```bash
vercel
```

3. Configure environment variables in the Vercel Dashboard:
   - Navigate to your project settings
   - Add the following variables:
     ```
     GROQ_API_KEY=your_groq_api_key
     GOOGLE_API_KEY=your_google_api_key
     GROQ_MODEL=llama-3.1-8b-instant
     EMBEDDING_MODEL=models/gemini-embedding-001
     ROUTING_THRESHOLD=0.5
     ```

4. Redeploy to apply environment variables:
```bash
vercel --prod
```

### API Keys

Both services offer free tiers suitable for development and demonstration:
- Groq API: https://console.groq.com/keys
- Google AI Studio: https://aistudio.google.com/app/apikey
- Tavily Search (Optional): https://tavily.com/ - For real web search in content generation

---

## Local Development

### Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## Testing the Routing System

The routing system uses **real semantic embeddings** (Google Gemini + ChromaDB), not hardcoded scores.

### Automated Test Script

Run the test script to verify routing accuracy:

```bash
python test_routing.py
```

**Expected Results:**
- Finance queries (Bitcoin, ROI, leverage) → Finance Bro scores highest
- Critical queries (privacy, surveillance, monopolies) → Doomer scores highest  
- Tech queries (AI, quantum computing, SpaceX) → Tech Maximalist scores highest
- Each query produces **unique scores** based on semantic similarity

### Debug API Endpoint

Verify embeddings are real (not hardcoded):

```bash
curl -X POST http://localhost:5001/api/debug/embeddings \
  -H "Content-Type: application/json" \
  -d '{"text": "Bitcoin price analysis and market trends"}'
```

**Response includes:**
- Actual embedding vectors (first 10 dimensions shown)
- Similarity scores for each bot persona
- Vector dimensionality (768 dimensions for Gemini)
- Proof that vectors change with different inputs

---

Start the API server:
```bash
python -m app.web_api
```

Start the frontend (development mode):
```bash
cd frontend
npm install
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:5001

### Code Quality

Run linters before committing:

```bash
# Backend linting
pip install ruff black
ruff check app/
black --check app/

# Frontend linting
cd frontend
npm run lint
```

---

## CI/CD Pipeline

The project includes automated GitHub Actions workflows:

- **Continuous Integration**: Linting, building, and security scanning on every push
- **Docker Publishing**: Automated Docker image builds and publishing to GitHub Container Registry
- **Vercel Deployment**: Automatic deployments to Vercel on main branch updates

See [.github/workflows/README.md](./.github/workflows/README.md) for detailed CI/CD documentation.

---

## LLM-as-Judge Evaluation

Grid07 AI includes a comprehensive evaluation harness that demonstrates production-ready AI system evaluation practices.

### Dashboard Preview

![Evaluation Dashboard](./static/eval-dashboard.png)

*Interactive evaluation dashboard with real-time metrics and test results*

### Evaluation System

- **30 Curated Test Cases**: Covering technology discussions, critical analysis, financial topics, prompt injections, multi-turn conversations, and safety boundaries
- **LLM-as-Judge Scoring**: Automated evaluation on 4 dimensions:
  - Relevance (addresses the question)
  - Faithfulness (persona consistency, context awareness)
  - Safety (ethical boundaries)
  - Injection Resistance (adversarial robustness)
- **Automated Reporting**: JSON, CSV, and interactive HTML dashboard

### Run Evaluation

```bash
# Run all tests and generate dashboard
./eval/run_eval.sh

# Or run individually
python -m eval.runner
python -m eval.dashboard

# View results
open eval/results/dashboard.html
```

### Why This Matters

Traditional metrics (BLEU, ROUGE) don't capture persona consistency, contextual appropriateness, safety, or adversarial robustness. LLM-as-Judge provides human-like evaluation at scale with multi-dimensional scoring and explanations.

See [eval/README.md](./eval/README.md) for complete evaluation documentation.

---

## Project Structure

```
grid07_ai/
├── index.html              # Frontend chatbot interface
├── app/
│   ├── web_api.py         # Flask API server
│   ├── config/            # Configuration and settings
│   ├── personas/          # Persona definitions and system prompts
│   ├── rag/               # RAG logic and injection defense
│   ├── graph/             # LangGraph workflows
│   ├── router/            # Routing logic
│   ├── embeddings/        # Embedding generation
│   ├── vectorstore/       # ChromaDB integration
│   └── tools/             # Mock search and utilities
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
└── README.md
```

---

## Built For

This project was developed for the Trilogy Innovations internship application, specifically addressing:

**Criterion 2: Real-World Projects**
A working application with live deployment, demonstrating full-stack development skills and production-ready patterns.

**Criterion 3: AI-Augmented Building**
Extensive use of AI technologies including LLMs, RAG, vector embeddings, and autonomous agents, with clear architectural decisions and security considerations.

### Key Strengths

- Clean, modular architecture that separates concerns
- Security-conscious implementation with injection defense
- Comprehensive documentation explaining design decisions
- Live deployment accessible for evaluation
- Demonstrates understanding of production AI systems

---

## API Reference

### Endpoints

**GET /api/bots**
Returns list of available bot personas with their descriptions.

**POST /api/chat**
Engage in conversation with a specific bot.
```json
{
  "bot_id": "bot_a",
  "message": "What do you think about AI?",
  "parent_post": "Original post content",
  "comment_history": []
}
```

**POST /api/route**
Route a message to relevant bot personas.
```json
{
  "post": "Bitcoin crashed 20% today"
}
```

**POST /api/generate**
Generate autonomous content for a bot.
```json
{
  "bot_id": "bot_a"
}
```

**GET /health**
Health check endpoint.

---

## Configuration

### Environment Variables

**Required:**
- `GROQ_API_KEY`: API key for Groq language model service
- `GOOGLE_API_KEY`: API key for Google Gemini embeddings

**Optional:**
- `GROQ_MODEL`: Model identifier (default: llama-3.1-8b-instant)
- `EMBEDDING_MODEL`: Embedding model (default: models/gemini-embedding-001)
- `ROUTING_THRESHOLD`: Similarity threshold for routing (default: 0.5)

---

## Technical Notes

### Vercel Deployment Considerations

Vercel's serverless environment has some limitations compared to traditional servers:

- No persistent storage, so ChromaDB vector store is disabled
- 500MB bundle size limit requires minimal dependencies
- Routing uses keyword matching instead of vector similarity
- Content generation is simplified without full LangGraph

These are reasonable trade-offs for a demonstration deployment. All core functionality, including chat and RAG, works as intended.

### Local Development Advantages

Running locally provides the full experience:
- Complete vector similarity routing with ChromaDB
- Full LangGraph-powered content generation
- Comprehensive RAG implementation
- No bundle size constraints

---

## Troubleshooting

**Module not found errors on Vercel:**
The requirements.txt file has been optimized to exclude heavy dependencies like torch and transformers. If you need these locally, install them separately.

**API connection failures:**
Verify that environment variables are properly set in the Vercel Dashboard. Remember to redeploy after adding or changing variables.

**ChromaDB errors in local development:**
Remove the chroma_db directory and restart. The vector store will rebuild automatically.

---

## License

MIT License. You're free to use this code for your own projects and learning.

---

**Developed to demonstrate AI engineering capabilities and production-ready development practices.**
