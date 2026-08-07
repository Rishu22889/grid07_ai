import { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import RouterPhase from './components/RouterPhase';
import ContentPhase from './components/ContentPhase';
import CombatPhase from './components/CombatPhase';

type Phase = 'router' | 'content' | 'combat';

function App() {
  const [activePhase, setActivePhase] = useState<Phase>('router');

  return (
    <div className="app">
      <Navbar activePhase={activePhase} setActivePhase={setActivePhase} />
      
      <main className="container">
        <Hero />
        
        {activePhase === 'router' && <RouterPhase />}
        {activePhase === 'content' && <ContentPhase />}
        {activePhase === 'combat' && <CombatPhase />}
      </main>
    </div>
  );
}

export default App;
