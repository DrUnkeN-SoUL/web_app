function liveUpdate() {
    const emotionCountTextArea = document.getElementById('emotionTextArea');

    setInterval(function () {
        fetch('/emotion_counts')
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                var emotionCountStr = "";

                // Check if emotion_count is empty
                if (Object.keys(data.emotion_count).length === 0 && data.emotion_count.constructor === Object) {
                    emotionCountStr = "No faces detected.\n"; // Add a new line
                } else {
                    // Build the emotionCountStr if emotion_count is not empty
                    for (var emotion in data.emotion_count) {
                        emotionCountStr += emotion + ": " + data.emotion_count[emotion] + "\n";
                    }
                }
                // Update the textarea with the emotionCountStr
                emotionCountTextArea.value = emotionCountStr;

                // Update the <p> tags with additional data
                document.getElementById('total_faces_count').innerText = "Total Faces Count: " + data.total_faces_count;
                document.getElementById('total_emotions_identified_count').innerText = "Total Emotions Identified Count: " + data.total_emotions_identified_count;

                // Update the <p> tags with emotion_counts_db data
                document.getElementById('Angry').innerText = "Angry: " + (data.emotion_counts_db['Angry'] || 0);
                document.getElementById('Disgusted').innerText = "Disgusted: " + (data.emotion_counts_db['Disgusted'] || 0);
                document.getElementById('Fearful').innerText = "Fearful: " + (data.emotion_counts_db['Fearful'] || 0);
                document.getElementById('Happy').innerText = "Happy: " + (data.emotion_counts_db['Happy'] || 0);
                document.getElementById('Neutral').innerText = "Neutral: " + (data.emotion_counts_db['Neutral'] || 0);
                document.getElementById('Sad').innerText = "Sad: " + (data.emotion_counts_db['Sad'] || 0);
                document.getElementById('Surprised').innerText = "Surprised: " + (data.emotion_counts_db['Surprised'] || 0);
            })
            .catch(function (error) {
                // Handle errors
                console.error('Fetch error:', error);
            });
    }, 100); // Update every 0.1 second (adjust this interval as needed)
}

// Call the liveUpdate function when the page is loaded
window.onload = function () {
    liveUpdate();
};
