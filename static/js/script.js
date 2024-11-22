/**
 * Fetches emotion and song recommendations from the server.
 */
function fetchEmotionAndRecommendations() {
    console.log("Fetching recommendations..."); // Debug log to confirm function call
    fetch("/recommend")
        .then((response) => {
            console.log("HTTP Response:", response); // Log the HTTP response
            if (!response.ok) {
                console.error("Error: HTTP status", response.status); // Log any HTTP errors
                throw new Error("Failed to fetch recommendations.");
            }
            return response.json(); // Parse the response as JSON
        })
        .then((data) => {
            console.log("Fetched Data:", data); // Debug log to confirm received data

            // Update detected emotion display
            const emotionDisplay = document.getElementById("emotion-display");
            if (data.emotion) {
                emotionDisplay.innerText = `Detected Emotion: ${data.emotion}`;
            } else {
                emotionDisplay.innerText = "Waiting for emotion detection...";
            }

            // Update recommendations list
            const recommendationsDiv = document.getElementById("recommendations");
            recommendationsDiv.innerHTML = ""; // Clear existing recommendations

            if (data.recommendations && data.recommendations.length > 0) {
                data.recommendations.forEach((rec) => {
                    const song = document.createElement("div");
                    song.style.display = "flex";
                    song.style.alignItems = "center";
                    song.style.marginBottom = "15px";

                    // Add album cover image
                    const albumCover = document.createElement("img");
                    albumCover.src = rec.album_cover || "/static/images/placeholder.jpg";
                    albumCover.alt = `${rec.name} Album Cover`;
                    albumCover.style.width = "50px";
                    albumCover.style.height = "50px";
                    albumCover.style.marginRight = "15px";
                    albumCover.style.borderRadius = "5px";

                    // Add song details
                    const songDetails = document.createElement("div");
                    songDetails.innerHTML = `
                        <p>
                            <a href="${rec.url}" target="_blank" style="text-decoration: none; color: #007bff;">
                                ${rec.name}
                            </a> by ${rec.artist}
                        </p>
                    `;

                    // Append album cover and details to the song container
                    song.appendChild(albumCover);
                    song.appendChild(songDetails);

                    // Add song container to the recommendations div
                    recommendationsDiv.appendChild(song);
                });
            } else {
                recommendationsDiv.innerHTML += "<p>No recommendations found. Please wait for emotion detection to stabilize.</p>";
            }
        })
        .catch((error) => {
            // Handle any errors during fetch or data parsing
            console.error("Error fetching data:", error);
            const emotionDisplay = document.getElementById("emotion-display");
            emotionDisplay.innerText = "Error detecting emotion. Please wait...";
        });
}

// Regularly update recommendations and detected emotion every 2 seconds
setInterval(fetchEmotionAndRecommendations, 2000);

// Trigger the initial fetch to ensure immediate data load
fetchEmotionAndRecommendations();
