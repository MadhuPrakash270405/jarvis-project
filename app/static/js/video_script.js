document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 240;

    const registerFaceBtn = document.getElementById('register-face-btn');
    const faceCaptureSection = document.getElementById('face-capture-card');
    const voiceCaptureSection = document.getElementById('voice-capture-card');
    const registrationForm = document.getElementById('registration-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const pinInput = document.getElementById('pin');

    let videoStream;
    // Initialize event listeners
    initEventListeners();
    // Get initial video stream for face capture
    getVideoStream();

    // Event listeners initialization
    function initEventListeners() {
        nameInput.addEventListener('input', toggleButtonState);
        emailInput.addEventListener('input', toggleButtonState);
        pinInput.addEventListener('input', function(event) {
            // Allow only digits to be entered
            this.value = this.value.replace(/[^0-9]/g, '');
            toggleButtonState();
        });

        registrationForm.addEventListener('submit', handleFormSubmit);
    }

    function toggleButtonState() {
        registerFaceBtn.disabled = !(nameInput.value.trim() && emailInput.value.trim() && pinInput.value.length === 4);
    }

    async function getVideoStream() {
        try {
            videoStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
            video.srcObject = videoStream;
        } catch (error) {
            console.error("Error accessing video media devices", error);
        }
    }

    function handleFormSubmit(event) {
        event.preventDefault();
        captureFace();
    }



    function captureFace() {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const faceDataURL = canvas.toDataURL('image/png');
        sendFaceData(faceDataURL);
    }

    function sendFaceData(faceDataURL) {
        fetch('/register/face', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: faceDataURL })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Face captured successfully!');
            faceCaptureSection.style.display = 'none';
            voiceCaptureSection.style.display = 'block';
            // Stop the video stream as it's no longer needed
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
                video.srcObject = null;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});
