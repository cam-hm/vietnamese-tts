/**
 * Vietnamese TTS - Frontend JavaScript
 * Sử dụng Cartesia API
 */

// DOM Elements
const textInput = document.getElementById('text-input');
const charCount = document.getElementById('char-count');
const voiceSelect = document.getElementById('voice-select');
const speedRange = document.getElementById('speed-range');
const speedValue = document.getElementById('speed-value');
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
generateBtn.addEventListener('click', generateNarration);
downloadBtn.addEventListener('click', downloadAudio);

// Initialize
async function init() {
    updateCharCount();
    await loadVoices();

    // Set default sample text in Vietnamese
    if (!textInput.value) {
        textInput.value = "Xin chào, đây là bản demo chuyển văn bản thành giọng nói tiếng Việt sử dụng Cartesia AI.";
        updateCharCount();
    }
}

// Load voices from API
async function loadVoices() {
    try {
        const response = await fetch('/api/voices');
        if (!response.ok) {
            throw new Error('Failed to load voices');
        }
        const data = await response.json();
        const voices = data.voices || [];

        voiceSelect.innerHTML = '';

        if (voices.length === 0) {
            voiceSelect.innerHTML = '<option value="" disabled>Không có voice tiếng Việt</option>';
            generateBtn.disabled = true;
            return;
        }

        voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = voice.id;
            option.textContent = voice.name || `Voice ${index + 1}`;
            if (voice.description) {
                option.title = voice.description;
            }
            if (index === 0) {
                option.selected = true;
            }
            voiceSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error loading voices:', error);
        voiceSelect.innerHTML = '<option value="" disabled>Lỗi tải voices</option>';
        showError('Không thể tải danh sách voices. Vui lòng thử lại sau.');
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
        showError('Vui lòng nhập văn bản để tạo giọng nói.');
        return;
    }

    if (!voiceSelect.value) {
        showError('Vui lòng chọn một giọng đọc.');
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
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Lỗi: ${response.status}`);
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
        showError(error.message || 'Không thể tạo giọng nói. Vui lòng thử lại.');
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
