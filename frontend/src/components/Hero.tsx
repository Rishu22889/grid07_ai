interface HeroProps {
  openChat: (botId: string) => void;
}

export default function Hero({ openChat }: HeroProps) {
  const bots = [
    {
      id: 'bot_a',
      avatar: 'A',
      name: 'Agent Alpha',
      role: 'Tech Optimist',
    },
    {
      id: 'bot_b',
      avatar: 'B',
      name: 'Agent Beta',
      role: 'Critical Skeptic',
    },
    {
      id: 'bot_c',
      avatar: 'C',
      name: 'Agent Gamma',
      role: 'Market Analyst',
    },
  ];

  return (
    <header>
      {/* your existing Hero content */}

      <div className="bot-cards">
        {bots.map((bot) => (
          <div
            key={bot.id}
            className="bot-card"
            onClick={() => openChat(bot.id)}
          >
            <div className="bot-avatar">
              {bot.avatar}
            </div>

            <div className="bot-info">
              <div className="bot-name">
                {bot.name}
              </div>

              <div className="bot-role">
                {bot.role}
              </div>
            </div>
          </div>
        ))}
      </div>
    </header>
  );
}