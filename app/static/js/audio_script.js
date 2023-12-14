window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.interimResults = true;
recognition.lang = 'en-IN';

const transcription = document.getElementById('transcription');
const outputTranscription=document.getElementById('output_transcription');
const bars = document.querySelectorAll('.bar'); // Select all bars
const toggleBtn = document.getElementById('voice-toggle-btn');
let isListening = false;
let shouldRestartRecognition = false;

// Example usage
speak("Good evening, Boss. What can I do for you?");


recognition.addEventListener('result', e => {
    const transcript = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')

    transcription.textContent = transcript;

    bars.forEach(bar => bar.style.backgroundColor = '#0f0'); // Change to active color
    // Check if the result is final
    if (e.results[0].isFinal) {
        stopTranscription(); // Stop listening
        send_the_transcript(transcript); // Send the transcript
    }
});


function startTranscription() {
    if (!isListening) {
        recognition.start();
        toggleBtn.textContent = 'Stop Transcription';
        bars.forEach(bar => bar.style.animationPlayState = 'running');
        isListening = true;
        shouldRestartRecognition = true; // Set flag when starting
    }
}

function stopTranscription() {
    if (isListening) {
        recognition.stop();
        toggleBtn.textContent = 'Start Transcription';
        bars.forEach(bar => bar.style.animationPlayState = 'paused');
        isListening = false;
        shouldRestartRecognition = false; // Clear flag when stopping
    }
}


recognition.addEventListener('end', () => {
    isListening = false;
    if (shouldRestartRecognition) {
        startTranscription();
        bars.forEach(bar => bar.style.backgroundColor = '#f00');
    } else {
        bars.forEach(bar => bar.style.backgroundColor = '#555');
    }
});


toggleBtn.addEventListener('click', () => {
    if (isListening) {
        stopTranscription();
    } else {
        startTranscription();
    }
});



function send_the_transcript(transcript) {
    outputTranscription.textContent = 'Processing...';
    fetch('/process_transcript', {
        method: 'POST',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('accessToken'),
             'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: transcript })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        outputTranscription.textContent = data['message'];
        showPopup('Transcript processed successfully!', 'success');
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
        showPopup('Error processing transcript.', 'error');
    });
}


function speak(text) {
    console.log('TRANSCRIPT: ' + text);
    if ('speechSynthesis' in window) {
        var utterance = new SpeechSynthesisUtterance(text);

        // List available voices and select one that sounds more like JARVIS
        window.speechSynthesis.onvoiceschanged = function () {
            var voices = window.speechSynthesis.getVoices();
            utterance.voice = voices.find(voice => voice.name === "Google UK English Male");

            utterance.rate = 1; // You can adjust the rate
            utterance.pitch = 1.2; // You can adjust the pitch

            window.speechSynthesis.speak(utterance);
        };
    } else {
        alert("Sorry, your browser does not support text to speech!");
    }
}


