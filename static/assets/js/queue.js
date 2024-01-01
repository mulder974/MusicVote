var socket = io.connect('http://' + document.location.hostname + ':' + location.port);

socket.on('connect', function() {
    console.log('Connected to WebSocket');
});

socket.on('queue_update', function(data) {
    console.log('Track update received:', data);
    updateQueueDisplay(data.name, data.artist, data.album_image_src, data.track_length, data.track_progress);
});


function updateQueueDisplay(response) {
               
            const queueContainer = document.querySelector('.queue');
           
                queueContainer.innerHTML = ''; // Clear current queue
                songs = response.song_voted
                user = response.user
            

                for (let songId in songs) {
                    let song = songs[songId];
                
                    let songVotedLimitReached = song["votes"][user]["max_vote_reached"];                    
                    let songElement = document.createElement('div');
                 

                    let vote = song["votes_total"];
                   
                    

                    songElement.className = 'song-card';
                    songElement.innerHTML = `
                        <img class="album-cover" src="${song.song_image}" alt="Album Cover">
                        <div class="song-info">
                            <h3 class="song-name">${song.name}</h3>
                            <p class="song-artist">${song.artist_name}</p>
                            <p>Votes: ${vote}</p>
                            <button class="vote-button" 
                            data-songId="{{ song['id'] }}"
                            onclick="voteForSong('${songId}')"
                            ${songVotedLimitReached ? 'disabled' : true}>
                            ${songVotedLimitReached 
                            ? '<i class="icon-limited-votes"></i> Max vote atteint' 
                            : '<i class="icon-vote"></i> Vote'}                      
                            </button>
                        </div>
                    `;
                    queueContainer.appendChild(songElement);
                }
            
        }
       




function fetchQueueUpdates() {
    $.ajax({
        url: '/get_songs',
        type: 'GET',
        success: function(response) {
            console.log( "AJAX success, response:", response)
            // Update the queue display with the response
            updateQueueDisplay(response);
        }
    });
}

// Call fetchQueueUpdates every few seconds
setInterval(fetchQueueUpdates, 5000); // 0.5 seconds as an example