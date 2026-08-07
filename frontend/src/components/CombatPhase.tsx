import { useState } from 'react';

const API_BASE = import.meta.env.DEV ? 'http://localhost:5001/api' : '/api';

interface Comment {
  role: 'human' | 'agent';
  text: string;
}

export default function CombatPhase() {
  const [botId, setBotId] = useState<'bot_a' | 'bot_b' | 'bot_c'>('bot_a');
  const [parentPost, setParentPost] = useState('');
  const [comments, setComments] = useState<Comment[]>([
    { role: 'human', text: "That's statistically false. Modern EV batteries retain 90% capacity after 8 years." },
    { role: 'agent', text: 'Where are you getting your data from? Corporate propaganda.' },
  ]);
  const [reply, setReply] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [newCommentRole, setNewCommentRole] = useState<'human' | 'agent'>('human');
  const [newCommentText, setNewCommentText] = useState('');

  const handleTest = async () => {
    if (!reply.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bot_id: botId,
          message: reply,
          parent_post: parentPost || 'Electric Vehicles are a complete scam.',
          comment_history: comments.map(c => ({ role: c.role, message: c.text })),
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const addComment = () => {
    if (newCommentText.trim()) {
      setComments([...comments, { role: newCommentRole, text: newCommentText }]);
      setNewCommentText('');
      setShowModal(false);
    }
  };

  const removeComment = (index: number) => {
    setComments(comments.filter((_, i) => i !== index));
  };

  return (
    <section className="phase active">
      <div className="phase-header">
        <span className="phase-label">PHASE 03</span>
        <h2>RAG Combat Defense</h2>
        <p>Prompt injection resistance testing with full conversational context and persona enforcement.</p>
      </div>

      <div className="combat-grid">
        <div className="combat-control">
          <div className="control-section">
            <label htmlFor="combat-bot">SELECT AGENT</label>
            <select
              id="combat-bot"
              className="combat-select"
              value={botId}
              onChange={(e) => setBotId(e.target.value as any)}
            >
              <option value="bot_a">Agent Alpha — Tech Optimist</option>
              <option value="bot_b">Agent Beta — Critical Skeptic</option>
              <option value="bot_c">Agent Gamma — Market Analyst</option>
            </select>
          </div>

          <div className="control-section">
            <label htmlFor="parent-post">PARENT POST</label>
            <textarea
              id="parent-post"
              rows={3}
              value={parentPost}
              onChange={(e) => setParentPost(e.target.value)}
              placeholder="Enter the original post that started the conversation..."
            />
          </div>

          <div className="control-section">
            <label htmlFor="comment-thread">COMMENT THREAD</label>
            <div className="comment-thread" id="comment-thread">
              {comments.map((comment, idx) => (
                <div key={idx} className="thread-item">
                  <div className="thread-header">
                    <span className="thread-badge">{comment.role.toUpperCase()}</span>
                    <button className="thread-remove" onClick={() => removeComment(idx)}>
                      ×
                    </button>
                  </div>
                  <div className="thread-text">{comment.text}</div>
                </div>
              ))}
            </div>
            <button className="add-comment-btn" onClick={() => setShowModal(true)}>
              Add Comment
            </button>
          </div>

          <div className="control-section">
            <label htmlFor="combat-reply">
              TEST INPUT <span className="injection-label">INJECTION TEST</span>
            </label>
            <textarea
              id="combat-reply"
              rows={3}
              value={reply}
              onChange={(e) => setReply(e.target.value)}
              placeholder="Enter your message or injection attempt..."
            />
          </div>

          <button className="run-btn" onClick={handleTest} disabled={loading}>
            <span className="btn-icon">▶</span>
            {loading ? 'Testing...' : 'Test Defense'}
          </button>
        </div>

        <div className="combat-display">
          {!result ? (
            <div className="display-placeholder">
              <div className="shield-icon">◈</div>
              <p>Defense response will appear here</p>
            </div>
          ) : (
            <div className="combat-result visible">
              <div className="defense-response">
                <div className="response-header">
                  <div className="response-bot">
                    <div className="response-bot-avatar">
                      {result.bot_id === 'bot_a' ? 'A' : result.bot_id === 'bot_b' ? 'B' : 'C'}
                    </div>
                    <div className="response-bot-name">{result.bot_name}</div>
                  </div>
                </div>
                <div className="response-text">{result.reply}</div>
                <div className="defense-status">
                  <div className={`status-indicator ${result.injection_detected ? 'detected' : 'safe'}`}>
                    {result.injection_detected ? 'INJECTION DETECTED' : 'CLEAN INPUT'}
                  </div>
                  <span style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
                    Defense system active
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {showModal && (
        <div className="modal active" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Comment</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label htmlFor="comment-role">ROLE</label>
                <select
                  id="comment-role"
                  className="modal-select"
                  value={newCommentRole}
                  onChange={(e) => setNewCommentRole(e.target.value as any)}
                >
                  <option value="human">Human</option>
                  <option value="agent">Agent</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="comment-text">COMMENT TEXT</label>
                <textarea
                  id="comment-text"
                  rows={4}
                  value={newCommentText}
                  onChange={(e) => setNewCommentText(e.target.value)}
                  placeholder="Enter comment text..."
                />
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn-secondary" onClick={() => setShowModal(false)}>
                Cancel
              </button>
              <button className="btn-primary" onClick={addComment}>
                Add Comment
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
