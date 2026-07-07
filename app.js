const API_BASE = window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5001/api' 
    : '/api';

let selectedBot = 'bot_a';
let comments = [
    { role: 'human', text: "That's statistically false. Modern EV batteries retain 90% capacity after 8 years." },
    { role: 'bot', text: "Where are you getting your data from? Corporate propaganda." }
];

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initRouter();
    initContent();
    initCombat();
    loadPersonas();
    renderComments();
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
            results.innerHTML = '<div style="text-align: center; color: var(--text-dim);">Enter a message first</div>';
            return;
        }
        
        results.innerHTML = '<div class="loading">Processing...</div>';
        
        try {
            const response = await fetch(`${API_BASE}/route`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ post, threshold: Number.parseFloat(thresholdValue.textContent) })
            });
            
            const data = await response.json();
            
            if (data.routed_bots && data.routed_bots.length > 0) {
                results.innerHTML = data.routed_bots.map(bot => `
                    <div class="result-item">
                        <div class="result-bot">
                            <div class="result-avatar">${getAgentLetter(bot.bot_id)}</div>
                            <div>
                                <div class="result-name">${bot.bot_name}</div>
                            </div>
                        </div>
                        <div class="result-score">${bot.similarity_score.toFixed(2)}</div>
                    </div>
                `).join('');
            } else {
                results.innerHTML = '<div style="text-align: center; color: var(--text-dim);">No agents matched</div>';
            }
        } catch (err) {
            results.innerHTML = `<div style="color: var(--error-color);">Error: ${err.message}</div>`;
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
        result.innerHTML = '<div class="loading">Generating...</div>';
        
        try {
            const response = await fetch(`${API_BASE}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_id: selectedBot })
            });
            
            const data = await response.json();
            
            result.innerHTML = `
                <div class="content-topic">${data.topic}</div>
                <div class="content-text">${data.post_content}</div>
                ${data.note ? `<div style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-dim);">${data.note}</div>` : ''}
            `;
        } catch (err) {
            result.innerHTML = `<div style="color: var(--error-color);">Error: ${err.message}</div>`;
        }
    });
}

function renderComments() {
    const container = document.getElementById('comment-thread');
    container.innerHTML = comments.map((comment, index) => `
        <div class="thread-item">
            <div class="thread-header">
                <span class="thread-badge">${comment.role === 'human' ? 'HUMAN' : 'AGENT'}</span>
                <button class="thread-remove" onclick="removeComment(${index})">×</button>
            </div>
            <div class="thread-text" contenteditable="true" onblur="updateComment(${index}, this.textContent)">${comment.text}</div>
        </div>
    `).join('');
}

function removeComment(index) {
    comments.splice(index, 1);
    renderComments();
}

function updateComment(index, newText) {
    comments[index].text = newText.trim();
}

function initCombat() {
    const runBtn = document.getElementById('run-combat');
    const addCommentBtn = document.getElementById('add-comment');
    const modal = document.getElementById('comment-modal');
    const modalClose = document.getElementById('modal-close');
    const modalCancel = document.getElementById('modal-cancel');
    const modalSubmit = document.getElementById('modal-submit');
    const commentRole = document.getElementById('comment-role');
    const commentText = document.getElementById('comment-text');
    const combatBot = document.getElementById('combat-bot');
    const parentPost = document.getElementById('parent-post');
    const reply = document.getElementById('combat-reply');
    const result = document.getElementById('combat-result');
    const displayPlaceholder = document.querySelector('.display-placeholder');
    
    addCommentBtn.addEventListener('click', () => {
        modal.classList.add('active');
        commentText.value = '';
        commentRole.value = 'human';
    });
    
    modalClose.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    modalCancel.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
    
    modalSubmit.addEventListener('click', () => {
        const role = commentRole.value;
        const text = commentText.value.trim();
        
        if (!text) {
            alert('Please enter comment text');
            return;
        }
        
        comments.push({ role, text });
        renderComments();
        modal.classList.remove('active');
    });
    
    runBtn.addEventListener('click', async () => {
        const parent = parentPost.value.trim();
        const userReply = reply.value.trim();
        const botId = combatBot.value;
        
        if (!userReply) {
            alert('Enter your test input');
            return;
        }
        
        displayPlaceholder.style.display = 'none';
        result.classList.add('visible');
        result.innerHTML = '<div class="loading">Processing...</div>';
        
        const history = comments.map(c => ({
            role: c.role,
            message: c.text
        }));
        
        try {
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    bot_id: botId,
                    message: userReply,
                    parent_post: parent || 'Electric Vehicles are a complete scam.',
                    comment_history: history
                })
            });
            
            const data = await response.json();
            
            const statusIndicator = data.injection_detected 
                ? '<div class="status-indicator detected">INJECTION DETECTED</div>'
                : '<div class="status-indicator safe">CLEAN INPUT</div>';
            
            result.innerHTML = `
                <div class="defense-response">
                    <div class="response-header">
                        <div class="response-bot">
                            <div class="response-bot-avatar">${getAgentLetter(data.bot_id)}</div>
                            <div class="response-bot-name">${data.bot_name}</div>
                        </div>
                    </div>
                    <div class="response-text">${data.reply}</div>
                    <div class="defense-status">
                        ${statusIndicator}
                        <span style="color: var(--text-dim); font-size: 0.85rem;">Defense system active</span>
                    </div>
                </div>
            `;
        } catch (err) {
            result.innerHTML = `<div style="color: var(--error-color);">Error: ${err.message}</div>`;
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
                    <div class="persona-avatar">${getAgentLetter(bot.id)}</div>
                    <div class="persona-title">${bot.name}</div>
                </div>
                <div class="persona-desc">${bot.description}</div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<div style="color: var(--text-dim);">Could not load personas</div>';
    }
}

function getAgentLetter(botId) {
    const letters = {
        'bot_a': 'A',
        'bot_b': 'B',
        'bot_c': 'C'
    };
    return letters[botId] || '?';
}
