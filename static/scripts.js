/*
const historyContainer = document.getElementById('history-container');
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.getElementById('new-chat-button');
const modeToggle = document.getElementById('mode-toggle');
const modelSelect = document.getElementById('model-select');

let conversationHistory = [];
let currentConversation = [];
let onlineMode = true;
let selectedModel = 'model1';
let isNewChat = true; // Flag to track if it's a new chat

modeToggle.addEventListener('change', () => {
    onlineMode = modeToggle.checked;
});

modelSelect.addEventListener('change', () => {
    selectedModel = modelSelect.value;
});

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    currentConversation.push({ sender, message });
}

function getBotResponse(userMessage) {
    if (onlineMode) {
        console.log(`Online mode, model: ${selectedModel}`);
        const responses = {
            'hello': 'Hello from online mode!',
            'how are you': 'I am doing well in the cloud!',
            'what is your name': `I am online model ${selectedModel}.`,
            'default': 'Online mode: I do not understand.'
        };
        const lowerUserMessage = userMessage.toLowerCase();
        return responses[lowerUserMessage] || responses['default'];
    } else {
        console.log("Offline mode");
        const responses = {
            'hello': 'Hello from offline mode!',
            'how are you': 'I am doing well locally!',
            'what is your name': 'I am an offline chatbot.',
            'default': 'Offline mode: I do not understand.'
        };
        const lowerUserMessage = userMessage.toLowerCase();
        return responses[lowerUserMessage] || responses['default'];
    }
}

function saveConversation() {
    if (currentConversation.length > 0 && isNewChat) { // Only save if it's a new chat
        conversationHistory.push(currentConversation);
        updateHistoryDisplay();
        isNewChat = false; // Reset the flag
    }
}

function updateHistoryDisplay() {
    historyContainer.innerHTML = '<h2>History</h2><button id="new-chat-button">New Chat</button>';
    document.getElementById('new-chat-button').addEventListener('click', newChat);
    conversationHistory.forEach((conversation, index) => {
        const historyItem = document.createElement('div');
        historyItem.classList.add('history-item');
        historyItem.innerHTML = `<span>Conversation ${index + 1}</span><button class="delete-button" data-index="${index}">X</button>`;
        historyItem.addEventListener('click', (event) => {
            if (event.target.classList.contains('delete-button')) {
                return;
            }
            loadConversation(index);
        });
        historyContainer.appendChild(historyItem);
        const deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                const indexToDelete = parseInt(event.target.dataset.index);
                deleteConversation(indexToDelete);
            });
        });
    });
}

function loadConversation(index) {
    chatContainer.innerHTML = ''; // Clear the chat
    currentConversation = conversationHistory[index].slice(); // Copy the conversation
    conversationHistory[index].forEach(messageObj => {
        addMessage(messageObj.message, messageObj.sender);
    });
    isNewChat = false; // It's not a new chat when loading a conversation
}

function deleteConversation(index) {
    conversationHistory.splice(index, 1);
    updateHistoryDisplay();
    chatContainer.innerHTML = '';
    currentConversation = [];
    isNewChat = true; // Start a new chat after deleting
}

function newChat() {
    chatContainer.innerHTML = '';
    currentConversation = [];
    addMessage("Hello! How can I help you?", "bot");
    isNewChat = true; // It's a new chat
}

sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        messageInput.value = '';

        setTimeout(() => {
            const botResponse = getBotResponse(message);
            addMessage(botResponse, 'bot');
            saveConversation();
        }, 500);
    }
});

messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});

setTimeout(() => {
    addMessage("Hello! How can I help you?", "bot");
}, 200);

newChatButton.addEventListener('click', newChat);
*/// scripts.js
// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const modeToggle = document.getElementById('mode-toggle');
    const modelSelect = document.getElementById('model-select');
    const newChatButton = document.getElementById('new-chat-button');

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${sender}: ${message}`;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function loadModels() {
        try {
            const response = await fetch('/models');
            if (response.ok) {
                const data = await response.json();
                const onlineModels = data.online_models;
                const offlineModels = data.offline_models;

                const models = modeToggle.checked ? onlineModels : offlineModels;

                modelSelect.innerHTML = '';
                for (const modelId in models) {
                    const option = document.createElement('option');
                    option.value = modelId;
                    option.textContent = models[modelId];
                    modelSelect.appendChild(option);
                }
            } else {
                console.error('Failed to load models:', response.status);
            }
        } catch (error) {
            console.error('Error loading models:', error);
        }
    }

    loadModels();
    modeToggle.addEventListener('change', loadModels);

    sendButton.addEventListener('click', async () => {
        const message = messageInput.value;
        if (message) {
            appendMessage('You', message);
            messageInput.value = '';

            const mode = modeToggle.checked ? 'online' : 'offline';
            const model = modelSelect.value;

            try {
                const response = await fetch('/ask/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: message, mode: mode, model: model }),
                });

                if (response.ok) {
                    const data = await response.json();
                    appendMessage('Robot', data.response);
                } else {
                    appendMessage('Robot', 'Error: Could not get response.');
                }
            } catch (error) {
                appendMessage('Robot', 'Error: ' + error.message);
            }
        }
    });

    newChatButton.addEventListener('click', () => {
        chatContainer.innerHTML = '';
    });
});