// scripts.js
const historyContainer = document.getElementById('history-container');
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.getElementById('new-chat-button');
const modeToggle = document.getElementById('mode-toggle');
const modelSelect = document.getElementById('model-select');
const modeLabel = document.getElementById('mode-label');

let currentConversation = [];
let onlineMode = false;
let selectedModel = modelSelect.value;
let currentChatId = null;

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
            //alert('Online mode enabled.');
            console.log('Online mode enabled.');
        } else {
            modeToggle.checked = false;
            //console.warn('Internet connection is required for online mode.');
            alert('Internet connection is required for online mode.');
        }
    } else {
        onlineMode = false;
        //alert('Offline mode enabled.');
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

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const modeToggle = document.getElementById('mode-toggle');
    const modelSelect = document.getElementById('model-select');
    const newChatButton = document.getElementById('new-chat-button');
    
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
    
    // Add this call to fetch history when the page loads
    fetchHistory();

    sendButton.addEventListener('click', async () => {
        const message = messageInput.value;
        if (message) {
            const userTimestamp = Date.now();
            addMessage(message, 'user', userTimestamp);
            messageInput.value = '';

            const mode = modeToggle.checked ? 'online' : 'offline';
            const model = modelSelect.value;

            try {
                if (!currentChatId) {
                    await newChat();
                }

                const response = await fetch('/ask/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        question: message, 
                        mode: mode, 
                        model: model, 
                        timestamp: userTimestamp,
                        chat_id: currentChatId
                    }),
                });

                if (response.ok) {
                    const data = await response.json();
                    const answer = data.response;
                    if (answer) {
                        const botTimestamp = Date.now();
                        addMessage(answer, 'bot', botTimestamp);
                    } else {
                        addMessage('Error: No answer received.', 'bot', Date.now());
                    }
                } else {
                    addMessage('Error: Could not get response.', 'bot', Date.now());
                }
            } catch (error) {
                addMessage('Error: ' + error.message, 'bot', Date.now());
            }
            sendConversationToServer(currentConversation);
        }
    });
});

function addMessage(message, sender, timestamp) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    if (typeof marked === 'undefined') {
        console.error("marked.js is not loaded. Please include it in your HTML.");
        messageDiv.textContent = message;
    } else {
        messageDiv.innerHTML = marked.parse(message);
    }

    const timeString = new Date(timestamp).toLocaleTimeString();
    const timestampSpan = document.createElement('span');
    timestampSpan.classList.add('timestamp');
    timestampSpan.textContent = ` (${timeString})`;
    messageDiv.appendChild(timestampSpan);

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    currentConversation.push({ sender, message, timestamp });

    updateUI();
}

async function newChat() {
    chatContainer.innerHTML = '';
    currentConversation = [];
    addMessage("Hello! How can I help you?", "bot", Date.now());

    try {
        const response = await fetch('/new_chat');
        if (response.ok) {
            const data = await response.json();
            currentChatId = data.chat_id;
            console.log("New chat created with ID:", currentChatId);
            // Call fetchHistory() after creating a new chat to refresh the list
            fetchHistory();
        } else {
            console.error('Failed to get new chat ID:', response.status);
        }
    } catch (error) {
        console.error('Error getting new chat ID:', error);
    }
    updateUI();
}

// Function to fetch and display the list of saved conversations
async function fetchHistory() {
    try {
        const response = await fetch('/get_history');
        if (response.ok) {
            const data = await response.json();
            // Call the function to update the display with the fetched data
            updateHistoryDisplay(data.history);
        } else {
            console.error('Failed to fetch history:', response.status);
        }
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}


// Updated function to display fetched history
function updateHistoryDisplay(historyFiles) {
    const historyList = document.getElementById('history-list');
    
    // Clear only the history list, not the whole container
    historyList.innerHTML = ''; 

    // Sort files in descending order based on their timestamp
    historyFiles.sort((a, b) => {
        const timestampA = parseInt(a.split('_')[1], 10);
        const timestampB = parseInt(b.split('_')[1], 10);
        return timestampB - timestampA;
    });

    historyFiles.forEach((fileName) => {
        const historyItem = document.createElement('div');
        historyItem.classList.add('history-item');
        
        // Remove file extension for display
        const displayName = fileName.replace('.json', '');
        historyItem.innerHTML = `<span>${displayName}</span><button class="delete-button" data-filename="${fileName}">❌</button>`;
        
        historyItem.querySelector('.delete-button').addEventListener('click', (event) => {
            event.stopPropagation();
            if (confirm(`Are you sure you want to delete this conversation?`)) {
                deleteConversation(fileName.replace('.json', ''));
            }
        });
        
        historyItem.addEventListener('click', (event) => {
            loadConversation(fileName.replace('.json', ''));
        });
        
        // Append the item to the new history-list div
        historyList.appendChild(historyItem);
    });
    // Event listeners for the buttons in the aside tag
    document.getElementById('new-chat-button').addEventListener('click', newChat);
    const toggleButton = document.getElementById('toggle-history-btn');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            document.getElementById('history-container').classList.toggle('collapsed');
        });
    }
}

// New function to handle conversation deletion
async function deleteConversation(chatId) {
    try {
        const response = await fetch(`/delete_conversation/${chatId}`, {
            method: 'DELETE',
        });
        
        if (response.ok) {
            console.log(`Conversation ${chatId} deleted successfully.`);
            // After deletion, re-fetch the history to update the display
            fetchHistory();
        } else {
            const errorData = await response.json();
            console.error('Failed to delete conversation:', errorData.detail);
            alert('Failed to delete conversation.');
        }
    } catch (error) {
        console.error('Error deleting conversation:', error);
        alert('An error occurred while deleting the conversation.');
    }
}

// Updated function to load a specific conversation by ID
async function loadConversation(chatId) {
    chatContainer.innerHTML = '';
    currentConversation = [];
    currentChatId = chatId; // Set the current chat ID to the loaded one

    try {
        const response = await fetch(`/get_conversation/${chatId}`);
        if (response.ok) {
            const data = await response.json();
            const conversation = data.conversation;
            conversation.forEach(messageObj => {
                addMessage(messageObj.message, messageObj.sender, messageObj.timestamp);
            });
        } else {
            console.error('Failed to load conversation:', response.status);
            addMessage('Error: Could not load conversation.', 'bot', Date.now());
        }
    } catch (error) {
        console.error('Error loading conversation:', error);
        addMessage('Error: ' + error.message, 'bot', Date.now());
    }
    updateUI();
}

function sendConversationToServer(conversationData) {
     if (!currentChatId) {
        console.error("Cannot save conversation, no chat ID exists.");
        return;
    }

    fetch('/save_conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        },
        body: JSON.stringify({ chat_id: currentChatId, conversation: conversationData }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Conversation saved successfully on the server.');
        } else {
            console.error('Failed to save conversation on the server:', data.error);
        }
    })
    .catch(error => {
        console.error('Error sending conversation to server:', error);
    });
}

messageInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    if (event.shiftKey) {
      event.preventDefault();
      const start = messageInput.selectionStart;
      const end = messageInput.selectionEnd;
      messageInput.value = messageInput.value.substring(0, start) + '\n' + messageInput.value.substring(end);
      messageInput.selectionStart = messageInput.selectionEnd = start + 1;
    } else {
      sendButton.click();
    }
  }
});

setTimeout(() => {
    newChat();
}, 200);

newChatButton.addEventListener('click', newChat);

function ensureMarkedLoaded() {
    if (typeof marked === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
        document.head.appendChild(script);
    }
}

ensureMarkedLoaded();
/*
async function setupVoiceRecording(recordButtonId, textareaId) {
    const recordButton = document.getElementById(recordButtonId);
    const textarea = document.getElementById(textareaId);

    let mediaRecorder;
    let audioChunks = [];

    recordButton.addEventListener('click', async () => {
        if (recordButton.classList.contains('recording')) {
            mediaRecorder.stop();
            recordButton.textContent = 'Record';
            recordButton.classList.remove('recording');
        } else {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const formData = new FormData();
                    formData.append('file', audioBlob, 'temp/temp_audio.wav');

                    const response = await fetch('/voice_record', {
                        method: 'POST',
                        body: formData
                    });

                    if (response.ok) {
                        const result = await response.json();
                        textarea.value = result.recognized_text || 'Could not recognize speech.';
                    } else {
                        console.error('Error:', response.statusText);
                        textarea.value = 'Error in speech recognition.';
                    }
                };

                mediaRecorder.start();
                recordButton.textContent = 'Stop Recording';
                recordButton.classList.add('recording');

            } catch (error) {
                console.error('Microphone access denied:', error);
                alert('Please allow microphone access.');
            }
        }
    });
}
*/
function clearMessageInput() {
    const messageInput = document.getElementById('message-input');
    const clearBtn = document.getElementById('clear-button');
    clearBtn.addEventListener('click', () => {
        messageInput.value = ''; // Clear the input field
        messageInput.focus(); // Set focus back to the input field
        console.log('Message input cleared and focused.');
    });
}
document.addEventListener('DOMContentLoaded', () => {
    setupVoiceRecording('record-button', 'message-input');
});

document.addEventListener('DOMContentLoaded', () => {
    clearMessageInput();
});


document.addEventListener('DOMContentLoaded', () => {
    const historyContainer = document.getElementById('history-container');
    const toggleButton = document.getElementById('toggle-history-btn');

    toggleButton.addEventListener('click', () => {
        console.log('Toggle history button clicked');
        historyContainer.classList.toggle('collapsed');
    });
});


// Hàm kiểm tra tràn nội dung trong history-list và chat-container
function checkOverflowStatus() {
    const historyList = document.getElementById('history-list');
    const chatContainer = document.getElementById('chat-container');

    // 1. Kiểm tra số lượng cuộc hội thoại trong history-list
    const historyItems = historyList.querySelectorAll('.history-item');
    const isHistoryOverflow = historyItems.length >= 10;

    // 2. Kiểm tra chiều cao nội dung trong chat-container
    const contentHeight = chatContainer.scrollHeight;
    const containerHeight = chatContainer.clientHeight;
    const isChatOverflow = (contentHeight / containerHeight) > 0.5;

    // Trả về một đối tượng chứa trạng thái của cả hai khu vực
    return {
        isHistoryOverflow: isHistoryOverflow,
        isChatOverflow: isChatOverflow
    };
}

// Ví dụ về cách sử dụng hàm này
// Bạn có thể gọi hàm này sau khi thêm một tin nhắn mới hoặc một cuộc hội thoại mới
function updateUI() {
    const status = checkOverflowStatus();
    console.log("Trạng thái History:", status.isHistoryOverflow ? "Đã tràn, cần cuộn" : "Bình thường");
    console.log("Trạng thái Chat:", status.isChatOverflow ? "Đã tràn, cần cuộn" : "Bình thường");

    // Dựa vào trạng thái, bạn có thể thực hiện các hành động khác
    if (status.isChatOverflow) {
        // Cuộn xuống cuối
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

