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
const historyContainer = document.getElementById('history-container');
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.getElementById('new-chat-button');
const modeToggle = document.getElementById('mode-toggle');
const modelSelect = document.getElementById('model-select');

let conversationHistory = [];
let currentConversation = [];
let onlineMode = false;
let selectedModel = modelSelect.value;
let isNewChat = true; // Flag to track if it's a new chat

async function checkInternetConnection() {
    try {
        const response = await fetch('https://1.1.1.1/cdn-cgi/trace', {
            method: 'HEAD',
            cache: 'no-store',
        });
        return response.ok;
    } catch (error) {
        return false;
    }
}

modeToggle.addEventListener('change', async () => {
    if (modeToggle.checked) {
        const isConnected = await checkInternetConnection();
        if (isConnected) {
            onlineMode = true;
            console.log('Online mode enabled.');
        } else {
            modeToggle.checked = false;
            alert('Internet connection is required for online mode.');
        }
    } else {
        onlineMode = false;
        console.log('Offline mode enabled.');
    }
});

modelSelect.addEventListener('change', () => {
    selectedModel = modelSelect.value;
    console.log('Selected model:', selectedModel);
});

checkInternetConnection().then((isConnected) => {
    if (!isConnected && modeToggle.checked) {
        modeToggle.checked = false;
        alert('Internet connection lost. Online mode disabled.');
    }
});

window.addEventListener('online', (event) => {
    console.log('You are now online.');
    //If the toggle is already on, or if the toggle is off, but the user is trying to turn it on, do not alert.
    if (!modeToggle.checked) {
        alert('Internet connection restored. Online mode available.');
    }
});

window.addEventListener('offline', (event) => {
    console.log('You are now offline.');
    if (modeToggle.checked) {
        modeToggle.checked = false;
        alert('Internet connection lost. Online mode disabled.');
    }
});

/*
function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    currentConversation.push({ sender, message });
}
*/

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const modeToggle = document.getElementById('mode-toggle');
    const modelSelect = document.getElementById('model-select');
    const newChatButton = document.getElementById('new-chat-button');
    /*
    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${sender}: ${message}`;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    */
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
            addMessage(message, 'user');
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
                    const answer = data.response;
                    if (answer) {
                        addMessage(answer, 'bot');
                    } else {
                        addMessage('Error: No answer received.', 'bot');
                    }
                } else {
                    addMessage('Error: Could not get response.', 'bot');
                }
                saveConversation(); // Save the conversation when the page loads
            } catch (error) {
                addMessage('Error: ' + error.message, 'bot');
            }
        }

    });
}
);
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
/*
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
*/
messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});

setTimeout(() => {
    addMessage("Hello! How can I help you?", "bot");
}, 200);

newChatButton.addEventListener('click', newChat);

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    // Check if marked is available
    if (typeof marked === 'undefined') {
        console.error("marked.js is not loaded. Please include it in your HTML.");
        messageDiv.textContent = message; // Fallback to plain text
    } else {
        messageDiv.innerHTML = marked.parse(message); // Render Markdown
    }

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    currentConversation.push({ sender, message });
}

// Ensure marked.js is loaded (if not already)
function ensureMarkedLoaded() {
    if (typeof marked === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
        document.head.appendChild(script);
    }
}

// Call ensureMarkedLoaded somewhere before addMessage is used.
ensureMarkedLoaded();