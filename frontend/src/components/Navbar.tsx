interface NavbarProps {
  activePhase: 'router' | 'content' | 'combat';
  setActivePhase: (phase: 'router' | 'content' | 'combat') => void;
}

export default function Navbar({ activePhase, setActivePhase }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <div className="brand-icon"></div>
        <span>GRID07</span>
      </div>
      
      <div className="nav-tabs">
        <button
          className={`tab ${activePhase === 'router' ? 'active' : ''}`}
          onClick={() => setActivePhase('router')}
        >
          <span className="tab-num">01</span>
          <span className="tab-name">Router</span>
        </button>
        <button
          className={`tab ${activePhase === 'content' ? 'active' : ''}`}
          onClick={() => setActivePhase('content')}
        >
          <span className="tab-num">02</span>
          <span className="tab-name">Content</span>
        </button>
        <button
          className={`tab ${activePhase === 'combat' ? 'active' : ''}`}
          onClick={() => setActivePhase('combat')}
        >
          <span className="tab-num">03</span>
          <span className="tab-name">Combat</span>
        </button>
      </div>
      
      <div className="api-status">
        <div className="status-dot"></div>
        <span>ONLINE</span>
      </div>
    </nav>
  );
}
