


function fetchCurrentTrack() {
    console.log("fetchCurrentTrack called");
    $.ajax({
        url: '/current_track',
        type: 'GET',
        success: function(response) {
            console.log("AJAX success, response:", response);
            var newTrackName = response.name;  // Assuming response contains track_id
            var newTrackArtist = response.artist;
            var newAlbumSource = response.album_image_src;
            
            

            // Update the iframe only if the track ID has changed
            if (newTrackName && newTrackName !== lastTrackName) {
                updateCurrentlyPlaying(newTrackName,newTrackArtist,newAlbumSource);
                lastTrackName = newTrackName;  // Update the last track ID
            }
        },
        error: function() {
            console.log("Error fetching current track.");
        }
    });
}


setInterval(fetchCurrentTrack, 10000);


function updateQueueDisplay() {
    $.ajax({
        url: '/get_songs',
        type: 'GET',
        success: function(response) {            
            const queueContainer = document.querySelector('.queue');
           
                document.getElementById('empty-queue-message').style.display = 'none';
                queueContainer.innerHTML = ''; // Clear current queue

                for (let songId in response) {
                    let song = response[songId];
                    let songElement = document.createElement('div');
                    console.log(song);
                    songElement.className = 'song-card';
                    songElement.innerHTML = `
                    <style>
                    .container {
                   max-width: 600px;
                   margin: 0 auto;
                   padding: 20px;
                   background-color: #f8f8f8;
               }
               
               h2 {
                   font-size: 24px;
                   text-align: center;
                   color: #333;
                   margin-bottom: 20px;
               }
               
               .songs-list {
                   list-style-type: none;
                   padding: 0;
               }
               
               .song-card {
                   display: flex;
                   align-items: center;
                   background-color: #ffffff;
                   box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                   border-radius: 8px;
                   margin-bottom: 20px;
                   padding: 15px;
                   transition: transform 0.3s ease;
               }
               
               .song-card:hover {
                   transform: translateY(-3px);
                   box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
               }
               
               .album-cover {
                   width: 60px; /* Adjust size as needed */
                   height: 60px;
                   border-radius: 30px; /* Makes it circular */
                   object-fit: cover;
                   margin-right: 15px;
               }
               
               .song-info {
                   flex-grow: 1;
               }
               
               .song-name {
                   font-size: 18px;
                   margin: 0;
                   color: #333;
               }
               
               .song-artist {
                   font-size: 14px;
                   color: #666;
               }
               
               .vote-button {
                   background-color: #9a191dcd;
                   color: white;
                   border: none;
                   padding: 10px 20px;
                   border-radius: 20px; /* Pill shape */
                   text-transform: uppercase;
                   font-weight: bold;
                   cursor: pointer;
                   transition: background-color 0.3s ease;
               }
               
               .vote-button:hover {
                   background-color: #831519cd
               }
               
               
                   </style>
                        <img class="album-cover" src="${song.song_image}" alt="Album Cover">
                        <div class="song-info">
                            <h3 class="song-name">${song.name}</h3>
                            <p class="song-artist">${song.artist_name}</p>
                            <p>Votes: ${song.votes}</p>
                        </div>
                    `;
                    queueContainer.appendChild(songElement);
                }
            
        },
        error: function(error) {
            console.error('Error fetching song data:', error);
        }
    });
}

function fetchQueueUpdates() {
    $.ajax({
        url: '/get_songs',
        type: 'GET',
        success: function(response) {
            // Update the queue display with the response
            updateQueueDisplay(response);
        }
    });
}

// Call fetchQueueUpdates every few seconds
setInterval(fetchQueueUpdates, 5000); // 5 seconds as an example