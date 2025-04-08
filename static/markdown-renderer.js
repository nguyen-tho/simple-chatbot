// markdown-renderer.js
function renderMarkdown(elementId, markdownText) {
    // Check if marked is available
    if (typeof marked === 'undefined') {
        console.error("marked.js is not loaded. Please include it in your HTML.");
        return;
    }

    const html = marked.parse(markdownText);
    document.getElementById(elementId).innerHTML = html;
}

// Add the marked.js library dynamically.
function loadMarked() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    document.head.appendChild(script);
}

loadMarked();