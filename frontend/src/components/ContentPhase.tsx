import { useState } from 'react';

const API_BASE = import.meta.env.DEV ? 'http://localhost:5001/api' : '/api';

export default function ContentPhase() {
  const [selectedBot, setSelectedBot] = useState<'bot_a' | 'bot_b' | 'bot_c'>('bot_a');
  const [result, setResult] = useState<{ topic: string; post_content: string; note?: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const bots = [
    { id: 'bot_a' as const, avatar: 'A', name: 'Agent Alpha' },
    { id: 'bot_b' as const, avatar: 'B', name: 'Agent Beta' },
    { id: 'bot_c' as const, avatar: 'C', name: 'Agent Gamma' },
  ];

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: selectedBot }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="phase active">
      <div className="phase-header">
        <span className="phase-label">PHASE 02</span>
        <h2>Autonomous Content Engine</h2>
        <p>LangGraph state machine: topic selection, contextual search, and persona-driven content generation.</p>
      </div>

      <div className="bot-selector">
        {bots.map((bot) => (
          <button
            key={bot.id}
            className={`bot-select-btn ${selectedBot === bot.id ? 'active' : ''}`}
            onClick={() => setSelectedBot(bot.id)}
          >
            <div className="select-avatar">{bot.avatar}</div>
            <span>{bot.name}</span>
          </button>
        ))}
      </div>

      <div className="content-output">
        {!result ? (
          <div className="content-placeholder">
            <div className="placeholder-icon">◈</div>
            <p>Select an agent and generate autonomous content</p>
          </div>
        ) : (
          <div className="content-card">
            <div className="content-topic">{result.topic}</div>
            <div className="content-text">{result.post_content}</div>
            {result.note && (
              <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: 'var(--text-dim)' }}>
                {result.note}
              </div>
            )}
          </div>
        )}
      </div>

      <button className="run-btn centered" onClick={handleGenerate} disabled={loading}>
        <span className="btn-icon">▶</span>
        {loading ? 'Generating...' : 'Generate'}
      </button>
    </section>
  );
}
