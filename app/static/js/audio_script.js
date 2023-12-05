window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.interimResults = true;
recognition.lang = 'en-US';

const transcription = document.getElementById('transcription');
const bars = document.querySelectorAll('.bar'); // Select all bars
const toggleBtn = document.getElementById('voice-toggle-btn');
let isListening = false;

recognition.addEventListener('result', e => {
    const transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');

    transcription.textContent = transcript;
    bars.forEach(bar => bar.style.backgroundColor = '#0f0'); // Change to active color
});

recognition.addEventListener('end', () => {
    if (isListening) {
        recognition.start();
        bars.forEach(bar => bar.style.backgroundColor = '#f00'); // Reset to default color
    } else {
        bars.forEach(bar => bar.style.backgroundColor = '#555'); // Dim the bars
    }
});

toggleBtn.addEventListener('click', () => {
    if (isListening) {
        recognition.stop();
        toggleBtn.textContent = 'Start Transcription';
        
        bars.forEach(bar => bar.style.animationPlayState = 'paused'); // Pause the animation
    } else {
        recognition.start();
        toggleBtn.textContent = 'Stop Transcription';
        
        bars.forEach(bar => bar.style.animationPlayState = 'running'); // Resume the animation
    }
    isListening = !isListening;
});
