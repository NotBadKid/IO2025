let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let audioStream;

document.getElementById('mic-button').addEventListener('click', toggleRecording);
async function toggleRecording() {
    if (isRecording) {
        // Stop recording and save the file
        mediaRecorder.stop();
    } else {
        // Start recording
        await startRecording();
    }
    isRecording = !isRecording;
}

async function startRecording() {
    try {
        // Get user media (microphone)
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // Create a MediaRecorder instance for 'audio/webm' format
        mediaRecorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm' });

        // Collect audio data as chunks
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        // Once recording stops, save the audio file
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // Create a new FormData object to send the Blob to the server
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.webm');

            // Send the audio file to the server
            await saveAudio(formData);

            // Reset audioChunks for next recording
            audioChunks = [];
        };

        // Start recording
        mediaRecorder.start();
    } catch (error) {
        console.error('Error starting microphone: ', error);
    }
}

async function saveAudio(formData) {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Audio processed successfully:', data);
            // Handle the response here (e.g., show the answer or audio URL)
        } else {
            console.error('Failed to process audio:', data.error);
        }
    } catch (error) {
        console.error('Error during fetch:', error);
    }
}



//document.getElementById('mic-button').addEventListener('click', function() {
//    // Get the value from the textarea
////    const userInput = document.getElementById('userInput').value;
//    const userInput = "sampleData"
//    // Define the data to be sent in the POST request
//    const data = {
//        text: userInput
//    };
//
//    // Send the POST request
//    fetch('/submitPrompt', {
//        method: 'POST', // Use the POST method
//        headers: {
//            'Content-Type': 'application/json', // Specify the content type
//        },
//        body: JSON.stringify(data) // Convert the data object to a JSON string
//    })
//    .then(response => response.json())  // Parse the JSON response from the server
//    .then(data => {
//        console.log('Success:', data); // Log the server's response
//    })
//    .catch((error) => {
//        console.error('Error:', error); // Handle any errors
//    });
//});

document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;

    themeToggle.addEventListener('click', function() {
        // Przełączanie klasy na body
        body.classList.toggle('dark-theme');
        body.classList.toggle('light-theme');

        // Aktualizacja wyglądu przełącznika
        updateToggleAppearance();
    });

    function updateToggleAppearance() {
        const iconSun = document.querySelector('.icon-sun');
        const toggleNight = document.querySelector('.toggle-night-selected');

        if (body.classList.contains('dark-theme')) {
            // Tryb ciemny aktywny - księżyc podświetlony
            iconSun.style.filter = 'saturate(0.5)';
            iconSun.style.backgroundColor = 'transparent';
            toggleNight.style.backgroundColor = '#4A90E2';
        } else {
            // Tryb jasny aktywny - słońce podświetlone
            iconSun.style.filter = 'saturate(1)';
            iconSun.style.backgroundColor = '#4A90E2';
            toggleNight.style.backgroundColor = 'transparent';
        }
    }

    // Inicjalizacja wyglądu przełącznika przy ładowaniu strony
    updateToggleAppearance();
});
