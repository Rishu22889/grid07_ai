import { useState } from 'react';
import './App.css';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import RouterPhase from './components/RouterPhase';
import ContentPhase from './components/ContentPhase';
import CombatPhase from './components/CombatPhase';
import ChatInterface from './components/ChatInterface';

type Phase = 'router' | 'content' | 'combat';

type Bot = {
  id: string;
  avatar: string;
  name: string;
  role: string;
};

const bots: Bot[] = [
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

function App() {
  const [activePhase, setActivePhase] =
    useState<Phase>('router');

  const [selectedBotId, setSelectedBotId] =
    useState<string | null>(null);

  const openChat = (botId: string) => {
    setSelectedBotId(botId);
  };

  const closeChat = () => {
    setSelectedBotId(null);
  };

  const selectedBot = bots.find(
    (bot) => bot.id === selectedBotId
  );

  // ================= CHAT SCREEN =================
  if (selectedBot) {
    return (
      <ChatInterface
        bot={selectedBot}
        onBack={closeChat}
      />
    );
  }

  // ================= HOME SCREEN =================
  return (
    <div className="app">

      <Navbar activePhase={activePhase} setActivePhase={setActivePhase}/>

      <main className="container">

        <Hero openChat={openChat} />

        {activePhase === 'router' && <RouterPhase />}
        {activePhase === 'content' && <ContentPhase />}
        {activePhase === 'combat' && <CombatPhase />}

      </main>

    </div>
  );
}

export default App;