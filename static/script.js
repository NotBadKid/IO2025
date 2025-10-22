document.getElementById('mic-button').addEventListener('click', startMicrophone);
 async function startMicrophone() {
            try {
                // Request microphone access
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                // Grab the audio element
                const audioElement = document.getElementById('audioElement');

                // Set the audio element's source to the stream
                audioElement.srcObject = stream;

                // Optional: Automatically play the audio once the stream is ready
                audioElement.play();
            } catch (error) {
                console.error('Error accessing microphone: ', error);
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

