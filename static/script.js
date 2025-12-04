// API interaction and UI logic

const API_BASE = '';

// DOM Elements
const messagesInput = document.getElementById('messages-input');
const loadSampleBtn = document.getElementById('load-sample-btn');
const extractMemoryBtn = document.getElementById('extract-memory-btn');
const memoryResults = document.getElementById('memory-results');
const memoryContent = document.getElementById('memory-content');

const userMessage = document.getElementById('user-message');
const comparePersonalitiesBtn = document.getElementById('compare-personalities-btn');
const personalityResults = document.getElementById('personality-results');
const personalityContent = document.getElementById('personality-content');

const personalitySelect = document.getElementById('personality-select');
const chatInput = document.getElementById('chat-input');
const sendChatBtn = document.getElementById('send-chat-btn');
const chatContainer = document.getElementById('chat-container');

let chatHistory = [];

const loadingOverlay = document.getElementById('loading-overlay');

// Utility Functions
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

function showError(message) {
    alert(`Error: ${message}`);
}

// Load Sample Messages
loadSampleBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/sample-messages');
        const data = await response.json();
        messagesInput.value = JSON.stringify(data, null, 2);
    } catch (error) {
        showError('Failed to load sample messages');
    }
});

// Extract Memory
extractMemoryBtn.addEventListener('click', async () => {
    try {
        const messages = JSON.parse(messagesInput.value);

        showLoading();
        const response = await fetch(`${API_BASE}/api/extract-memory`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages })
        });

        if (!response.ok) {
            throw new Error('Memory extraction failed');
        }

        const memory = await response.json();
        displayMemory(memory);
        memoryResults.classList.remove('hidden');
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

function displayMemory(memory) {
    memoryContent.innerHTML = `
        <div class="memory-category">
            <h4>👍 Preferences</h4>
            <p><strong>Likes:</strong></p>
            <ul>${memory.preferences.likes.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Dislikes:</strong></p>
            <ul>${memory.preferences.dislikes.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Habits:</strong></p>
            <ul>${memory.preferences.habits.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Interests:</strong></p>
            <ul>${memory.preferences.interests.map(item => `<li>${item}</li>`).join('')}</ul>
        </div>
        
        <div class="memory-category">
            <h4>💫 Emotional Patterns</h4>
            <p><strong>Dominant Emotions:</strong></p>
            <ul>${memory.emotional_patterns.dominant_emotions.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Communication Style:</strong> ${memory.emotional_patterns.communication_style}</p>
            <p><strong>Emotional Triggers:</strong></p>
            <ul>${memory.emotional_patterns.emotional_triggers.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Stress Indicators:</strong></p>
            <ul>${memory.emotional_patterns.stress_indicators.map(item => `<li>${item}</li>`).join('')}</ul>
        </div>
        
        <div class="memory-category">
            <h4>📝 Important Facts</h4>
            <p><strong>Personal Info:</strong></p>
            <ul>${memory.facts.personal_info.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Relationships:</strong></p>
            <ul>${memory.facts.relationships.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Goals:</strong></p>
            <ul>${memory.facts.goals.map(item => `<li>${item}</li>`).join('')}</ul>
            <p><strong>Events:</strong></p>
            <ul>${memory.facts.events.map(item => `<li>${item}</li>`).join('')}</ul>
        </div>
        
        <div class="memory-category">
            <h4>📊 Summary</h4>
            <p>${memory.summary}</p>
        </div>
    `;
}

// Compare Personalities
comparePersonalitiesBtn.addEventListener('click', async () => {
    const message = userMessage.value.trim();

    if (!message) {
        showError('Please enter a message');
        return;
    }

    try {
        showLoading();
        const response = await fetch(`${API_BASE}/api/compare-personalities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error('Personality comparison failed');
        }

        const data = await response.json();
        displayPersonalities(data.responses);
        personalityResults.classList.remove('hidden');
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

function displayPersonalities(responses) {
    personalityContent.innerHTML = Object.entries(responses)
        .map(([name, response]) => `
            <div class="personality-item">
                <span class="personality-label">${name}</span>
                <p>${response}</p>
            </div>
        `).join('');
}

// Interactive Chat
sendChatBtn.addEventListener('click', async () => {
    const message = chatInput.value.trim();
    const personality = personalitySelect.value;

    if (!message) return;

    // Add user message to UI and history
    addChatMessage(message, 'user');
    chatInput.value = '';

    try {
        // Show typing indicator
        showTypingIndicator();

        // Prepare history for API (exclude the message we just added to avoid duplication if we were to rely solely on history, 
        // but the API takes 'message' and 'history' separately. 
        // The 'history' should contain PREVIOUS messages.)
        // So we pass the current chatHistory EXCLUDING the latest user message we just pushed?
        // Actually, let's push to chatHistory AFTER we send? 
        // No, we want to show it immediately.
        // The API expects 'history' as context. So we should pass the history *before* this new message.

        const historyToSend = chatHistory.slice(0, -1); // Exclude the just-added user message

        const response = await fetch(`${API_BASE}/api/transform-personality`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                personality,
                history: historyToSend
            })
        });

        hideTypingIndicator();

        if (!response.ok) {
            throw new Error('Chat failed');
        }

        const data = await response.json();
        addChatMessage(data.transformed_response, 'ai', data.personality_used);

    } catch (error) {
        showError(error.message);
        // Optionally remove the user message if it failed? Nah.
    }
});

function addChatMessage(content, sender, personality = null) {
    // Add to history
    chatHistory.push({
        content: content,
        sender: sender,
        timestamp: new Date().toISOString()
    });

    // Remove placeholder if it exists
    const placeholder = chatContainer.querySelector('.chat-placeholder');
    if (placeholder) {
        placeholder.remove();
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender);

    if (sender === 'ai' && personality) {
        // Find readable name
        const option = Array.from(personalitySelect.options).find(o => o.value === personality);
        const personalityName = option ? option.text : personality;

        const senderDiv = document.createElement('div');
        senderDiv.classList.add('chat-message-sender');
        senderDiv.textContent = personalityName;
        messageDiv.appendChild(senderDiv);
    }

    const contentDiv = document.createElement('div');
    contentDiv.textContent = content;
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    chatContainer.appendChild(indicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}
