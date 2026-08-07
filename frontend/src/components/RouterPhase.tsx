import { useState } from 'react';

const API_BASE = import.meta.env.DEV ? 'http://localhost:5001/api' : '/api';

export default function RouterPhase() {
  const [input, setInput] = useState('');
  const [threshold, setThreshold] = useState(0.25);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleRoute = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/route`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ post: input, threshold }),
      });
      const data = await response.json();
      setResults(data.routed_bots || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="phase active">
      <div className="phase-header">
        <span className="phase-label">PHASE 01</span>
        <h2>Vector Persona Router</h2>
        <p>Semantic embedding using all-MiniLM-L6-v2 model with ChromaDB cosine similarity matching.</p>
      </div>

      <div className="demo-grid">
        <div className="input-panel">
          <label htmlFor="router-input">INPUT MESSAGE</label>
          <textarea
            id="router-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your social media post or message here..."
          />

          <div className="controls">
            <div className="threshold-control">
              <label htmlFor="threshold">THRESHOLD</label>
              <input
                type="range"
                id="threshold"
                min="0"
                max="100"
                value={threshold * 100}
                onChange={(e) => setThreshold(Number(e.target.value) / 100)}
              />
              <span>{threshold.toFixed(2)}</span>
            </div>
            <button className="run-btn" onClick={handleRoute} disabled={loading}>
              <span className="btn-icon">▶</span>
              Execute
            </button>
          </div>
        </div>

        <div className="output-panel">
          <div className="output-header">Routing Results</div>
          <div className="results-list">
            {loading ? (
              <div className="loading">Processing...</div>
            ) : results.length > 0 ? (
              results.map((bot, idx) => (
                <div key={idx} className="result-item">
                  <div className="result-bot">
                    <div className="result-avatar">{bot.bot_id === 'bot_a' ? 'A' : bot.bot_id === 'bot_b' ? 'B' : 'C'}</div>
                    <div className="result-name">{bot.bot_name}</div>
                  </div>
                  <div className="result-score">{bot.similarity_score.toFixed(2)}</div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', color: 'var(--text-dim)' }}>
                Enter a message and click Execute
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
