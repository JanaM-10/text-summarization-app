// DOM Elements
const textInput = document.getElementById('text-input');
const summarizeBtn = document.getElementById('summarize-btn');
const summaryContainer = document.getElementById('summary-container');
const summaryOutput = document.getElementById('summary-output');
const copyBtn = document.getElementById('copy-btn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');

// API Configuration
// Update this URL to match your Flask backend endpoint
const API_URL = 'http://localhost:5000/api/summarize';

// Event Listeners
summarizeBtn.addEventListener('click', handleSummarize);
copyBtn.addEventListener('click', handleCopy);

// Handle Summarize Button Click
async function handleSummarize() {
    const text = textInput.value.trim();
    
    // Validation
    if (!text) {
        alert('Please enter some text to summarize.');
        return;
    }
    
    if (text.length < 50) {
        alert('Please enter at least 50 characters for better summarization.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    summaryContainer.style.display = 'none';
    
    try {
        // Make API request to Flask backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display summary
        if (data.summary) {
            summaryOutput.textContent = data.summary;
            summaryContainer.style.display = 'block';
        } else {
            throw new Error('No summary received from server');
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while summarizing the text. Please make sure the backend server is running and try again.');
        summaryContainer.style.display = 'none';
    } finally {
        setLoadingState(false);
    }
}

// Set Loading State
function setLoadingState(isLoading) {
    if (isLoading) {
        summarizeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        summarizeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Handle Copy Button Click
function handleCopy() {
    const summaryText = summaryOutput.textContent;
    
    if (!summaryText) {
        return;
    }
    
    // Copy to clipboard
    navigator.clipboard.writeText(summaryText).then(() => {
        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = 'rgba(16, 185, 129, 0.3)';
        copyBtn.style.borderColor = '#10b981';
        copyBtn.style.color = '#10b981';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = 'rgba(167, 139, 250, 0.2)';
            copyBtn.style.borderColor = 'rgba(167, 139, 250, 0.4)';
            copyBtn.style.color = '#a78bfa';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy text to clipboard');
    });
}

// Allow Enter key to trigger summarize (Ctrl+Enter or Cmd+Enter)
textInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        handleSummarize();
    }
});

