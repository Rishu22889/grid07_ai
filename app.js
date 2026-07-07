const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5001/api' 
    : '/api';

let selectedBot = 'bot_a';

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initRouter();
    initContent();
    initCombat();
    loadPersonas();
});

function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const phases = document.querySelectorAll('.phase');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.phase;
            
            tabs.forEach(t => t.classList.remove('active'));
            phases.forEach(p => p.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(`${target}-phase`).classList.add('active');
        });
    });
}

function initRouter() {
    const runBtn = document.getElementById('run-router');
    const input = document.getElementById('router-input');
    const threshold = document.getElementById('threshold');
    const thresholdValue = document.getElementById('threshold-value');
    const results = document.getElementById('router-results');
    
    threshold.addEventListener('input', (e) => {
        thresholdValue.textContent = (e.target.value / 100).toFixed(2);
    });
    
    runBtn.addEventListener('click', async () => {
        const post = input.value.trim();
        if (!post) {
            results.innerHTML = '<div style="text-align: center; color: var(--text-dim);">Enter a post first</div>';
            return;
        }
        
        results.innerHTML = '<div class="loading">Routing...</div>';
        
        try {
            const response = await fetch(`${API_BASE}/route`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ post, threshold: parseFloat(thresholdValue.textContent) })
            });
            
            const data = await response.json();
            
            if (data.routed_bots && data.routed_bots.length > 0) {
                results.innerHTML = data.routed_bots.map(bot => `
                    <div class="result-item">
                        <div class="result-bot">
                            <span>${getBotIcon(bot.bot_id)}</span>
                            <div>
                                <div class="result-name">${bot.bot_name}</div>
                            </div>
                        </div>
                        <div class="result-score">${bot.similarity_score.toFixed(2)}</div>
                    </div>
                `).join('');
            } else {
                results.innerHTML = '<div style="text-align: center; color: var(--text-dim);">No bots matched</div>';
            }
        } catch (err) {
            results.innerHTML = `<div style="color: #ff0064;">Error: ${err.message}</div>`;
        }
    });
}

function initContent() {
    const generateBtn = document.getElementById('generate-content');
    const botBtns = document.querySelectorAll('.bot-select-btn');
    const placeholder = document.querySelector('.content-placeholder');
    const result = document.getElementById('content-result');
    
    botBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            botBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedBot = btn.dataset.bot;
        });
    });
    
    generateBtn.addEventListener('click', async () => {
        placeholder.style.display = 'none';
        result.style.display = 'block';
        result.innerHTML = '<div class="loading">Generating content...</div>';
        
        try {
            const response = await fetch(`${API_BASE}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_id: selectedBot })
            });
            
            const data = await response.json();
            
            result.innerHTML = `
                <div class="content-topic">📌 ${data.topic}</div>
                <div class="content-text">${data.post_content}</div>
                ${data.note ? `<div style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-dim);">${data.note}</div>` : ''}
            `;
        } catch (err) {
            result.innerHTML = `<div style="color: #ff0064;">Error: ${err.message}</div>`;
        }
    });
}

function initCombat() {
    const runBtn = document.getElementById('run-combat');
    const parentPost = document.getElementById('parent-post');
    const reply = document.getElementById('combat-reply');
    const result = document.getElementById('combat-result');
    
    runBtn.addEventListener('click', async () => {
        const parent = parentPost.value.trim();
        const userReply = reply.value.trim();
        
        if (!userReply) {
            alert('Enter your reply');
            return;
        }
        
        result.classList.add('visible');
        result.innerHTML = '<div class="loading">Bot is responding...</div>';
        
        const history = [
            { role: 'bot', message: "That's statistically false. EV batteries retain 90% capacity after 8 years." },
            { role: 'human', message: "Where are you getting your data from? Corporate propaganda." }
        ];
        
        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    bot_id: 'bot_a',
                    message: userReply,
                    parent_post: parent || 'Electric Vehicles are a complete scam.',
                    comment_history: history
                })
            });
            
            const data = await response.json();
            
            const injectionBadge = data.injection_detected 
                ? '<span class="injection-badge detected">🚨 Injection Detected</span>'
                : '<span class="injection-badge safe">✅ Clean Input</span>';
            
            result.innerHTML = `
                <div class="combat-header">
                    <span>${getBotIcon(data.bot_id)}</span>
                    <div>
                        <div style="font-weight: 600;">${data.bot_name}</div>
                        ${injectionBadge}
                    </div>
                </div>
                <div class="bot-reply">${data.reply}</div>
            `;
        } catch (err) {
            result.innerHTML = `<div style="color: #ff0064;">Error: ${err.message}</div>`;
        }
    });
}

async function loadPersonas() {
    const container = document.getElementById('persona-list');
    
    try {
        const response = await fetch(`${API_BASE}/bots`);
        const data = await response.json();
        
        container.innerHTML = data.bots.map(bot => `
            <div class="persona-card">
                <div class="persona-header">
                    <span>${getBotIcon(bot.id)}</span>
                    <div class="persona-title">${bot.name}</div>
                </div>
                <div class="persona-desc">${bot.description}</div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<div style="color: var(--text-dim);">Could not load personas</div>';
    }
}

function getBotIcon(botId) {
    const icons = {
        'bot_a': '🚀',
        'bot_b': '💀',
        'bot_c': '💰'
    };
    return icons[botId] || '🤖';
}
