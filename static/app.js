/**
 * BBC Documentary TTS - Frontend JavaScript
 */

// DOM Elements
const textInput = document.getElementById('text-input');
const charCount = document.getElementById('char-count');
const voiceSelect = document.getElementById('voice-select');
const speedRange = document.getElementById('speed-range');
const speedValue = document.getElementById('speed-value');
const pitchRange = document.getElementById('pitch-range');
const pitchValue = document.getElementById('pitch-value');
const generateBtn = document.getElementById('generate-btn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const audioSection = document.getElementById('audio-section');
const audioPlayer = document.getElementById('audio-player');
const downloadBtn = document.getElementById('download-btn');

// State
let currentAudioBlob = null;

// Event Listeners
textInput.addEventListener('input', updateCharCount);
speedRange.addEventListener('input', () => {
    speedValue.textContent = parseFloat(speedRange.value).toFixed(2);
});
pitchRange.addEventListener('input', () => {
    pitchValue.textContent = parseFloat(pitchRange.value).toFixed(1);
});
generateBtn.addEventListener('click', generateNarration);
downloadBtn.addEventListener('click', downloadAudio);

// Initialize
function init() {
    updateCharCount();

    // Set default sample text
    if (!textInput.value) {
        textInput.value = "In the heart of the African savanna, a remarkable story unfolds. Here, where the sun paints the sky in shades of amber and gold, life persists in ways that defy imagination.";
        updateCharCount();
    }
}

// Update character count
function updateCharCount() {
    const count = textInput.value.length;
    charCount.textContent = count;

    if (count > 4500) {
        charCount.style.color = '#ef4444';
    } else if (count > 4000) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '';
    }
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

// Generate narration
async function generateNarration() {
    const text = textInput.value.trim();

    if (!text) {
        showError('Please enter some text to narrate.');
        return;
    }

    // UI State: Loading
    generateBtn.disabled = true;
    loading.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    audioSection.classList.add('hidden');

    try {
        const response = await fetch('/api/synthesize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                voice: voiceSelect.value,
                speaking_rate: parseFloat(speedRange.value),
                pitch: parseFloat(pitchRange.value)
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error: ${response.status}`);
        }

        // Get audio blob
        currentAudioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(currentAudioBlob);

        // Update audio player
        audioPlayer.src = audioUrl;
        audioSection.classList.remove('hidden');

        // Auto-play
        audioPlayer.play().catch(() => {
            // Autoplay might be blocked, that's okay
        });

    } catch (error) {
        console.error('TTS Error:', error);
        showError(error.message || 'Failed to generate narration. Please try again.');
    } finally {
        generateBtn.disabled = false;
        loading.classList.add('hidden');
    }
}

// Download audio
function downloadAudio() {
    if (!currentAudioBlob) return;

    const url = URL.createObjectURL(currentAudioBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'narration.mp3';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', init);
