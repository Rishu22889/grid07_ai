export default function Hero() {
  const bots = [
    { id: 'bot_a', avatar: 'A', name: 'Agent Alpha', role: 'Tech Optimist' },
    { id: 'bot_b', avatar: 'B', name: 'Agent Beta', role: 'Critical Skeptic' },
    { id: 'bot_c', avatar: 'C', name: 'Agent Gamma', role: 'Market Analyst' },
  ];

  return (
    <header className="hero">
      <div className="hero-badge">AUTONOMOUS SYSTEM</div>
      <h1>
        Multi-Agent
        <br />
        <span className="gradient">Orchestration Platform</span>
      </h1>
      <p className="subtitle">
        Persona-based routing with vector similarity | Autonomous content generation | Injection-resistant defense
      </p>

      <div className="bot-cards">
        {bots.map((bot) => (
          <div key={bot.id} className="bot-card">
            <div className="bot-avatar">{bot.avatar}</div>
            <div className="bot-info">
              <div className="bot-name">{bot.name}</div>
              <div className="bot-role">{bot.role}</div>
            </div>
          </div>
        ))}
      </div>
    </header>
  );
}
