document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const loginpinInput = document.getElementById('login_pin');
    const emailInput = document.getElementById('login_email');
    const verifyButton = document.querySelector('.btn-verify');
    const canvas = document.createElement('canvas');
    // Function to start the video stream
    function startVideo() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
            .then(stream => {
                video.srcObject = stream;
            })
            .catch(err => console.error("Error accessing media devices:", err));
    }

    // Function to capture the video frame as a data URL
    function captureVideoFrame() {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const faceDataURL = canvas.toDataURL('image/png');
        sendFaceData(faceDataURL);
    }

    // Event listener for the 'Verify Face' button
    verifyButton.addEventListener('click', function () {
        captureVideoFrame();
        
    });

    loginpinInput.addEventListener('input', function(event) {
        this.value = this.value.replace(/[^0-9]/g, '');
        verifyButton.disabled = !(emailInput.value!='' && loginpinInput.value.length === 4);
    });



    // Function to send face data to the server
    function sendFaceData(faceDataURL) {
        let loginpin=loginpinInput.value
        let email=emailInput.value
        console.log("INTO SEND FACE DATAS");
        fetch('/verify/face', {
            method: 'POST',
            headers: {
                 "Authorization": "Bearer " + localStorage.getItem('accessToken'),
                 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: faceDataURL,
                emailInput:email,
                loginpin:loginpin
            })
        })
            .then(response => {
                // Check if the response was successful
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                if( data['message'] === 'Face verified successfully.'){
                    showPopup('Face Verified successfully! You will be redirected to Home Page','success');
                    setTimeout(() =>{
                        window.location.href = '/home'; // Replace '/login' with the actual path to your login page
                    }, 2000);
                }
                else{
                    showPopup('Face not verified! Please try again.','error');
                }
 
            })
            .catch((error) => {
                console.log('Error:', error);
                showPopup('Failed to capture face.');
            });
    }

    // Start the video feed when the page is loaded
    startVideo();
});
