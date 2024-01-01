var socket = io.connect('http://' + document.location.hostname + ':' + location.port);

socket.on('connect', function() {
    console.log('Connected to WebSocket');
});


socket.on('vote_processed', function(data) {
    console.log(data.message);
    fetchQueueUpdates();
});

socket.on('song_changed', function(data) {
    console.log(data.message);
    fetchQueueUpdates();
});

function updateQueueDisplay(data) {
    const queueContainer = document.querySelector('.queue');
    queueContainer.innerHTML = ''; // Clear current queue

    let songs = data.song_voted;
    let user = data.user;

    // Convert songs to an array and sort by votes_total
    let sortedSongs = Object.entries(songs).sort((a, b) => {
        return b[1].votes_total - a[1].votes_total;
    });

    sortedSongs.forEach(([songId, song]) => {
        let songVotedLimitReached = song["votes"][user]["max_vote_reached"];
        let songElement = document.createElement('div');
        songElement.className = 'song-card';
        songElement.innerHTML = `
            <img class="album-cover" src="${song.song_image}" alt="Album Cover">
            <div class="song-info">
                <h3 class="song-name">${song.name}</h3>
                <p class="song-artist">${song.artist_name}</p>
                <p>Votes: ${song.votes_total}</p>
                <button class="vote-button" 
                data-songId="${songId}"
                onclick="voteForSong('${songId}')"
                ${songVotedLimitReached ? 'disabled' : ''}>
                ${songVotedLimitReached 
                ? '<i class="icon-limited-votes"></i> Max vote atteint' 
                : '<i class="icon-vote"></i> Vote'}                      
                </button>
            </div>
        `;
        queueContainer.appendChild(songElement);
    });
}
       




function fetchQueueUpdates() {
    console.log( "trying to fetch queue updates...");

    $.ajax({
        url: '/get_songs',
        type: 'GET',
        success: function(response) {
            console.log( "AJAX success, response:", response);
            // Update the queue display with the response
            updateQueueDisplay(response);
        }
    });
}

fetchQueueUpdates();
// Call fetchQueueUpdates every few seconds
