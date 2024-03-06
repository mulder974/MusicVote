

var socket = io.connect('http://' + document.domain + ':' + location.port);

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
    const tableBody = document.getElementById('songTableBody');
    tableBody.innerHTML = ''; // Clear current rows

    let songs = data.song_voted;

    // Sort the songs (assuming this part remains the same)
    let sortedSongs = Object.entries(songs).sort((a, b) => {
        return b[1].votes_total - a[1].votes_total;
    });

    // Create and append table rows
    sortedSongs.forEach(([songId, song]) => {
        let songRow = document.createElement('tr');
        
        songRow.innerHTML = `
        <td class="text-center"><img src="${song.song_image}" alt="Song Image" style="width:50px; height:auto; border-radius: 5px;"></td>
        <td class="text-center">${song.name}</td>
        <td class="text-center">${song.artist_name}</td>
        <td class="text-center">${song.votes_total}</td>
        <td class="text-center">${song.duration}</td>
        <td class="text-center" style="display: flex;  justify-content: center;">
        <a href="songDetail.html?songId=${songId}" class="btn btn-primary">Details</a>
        </td>
    `;
        tableBody.appendChild(songRow);
    });
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

fetchQueueUpdates();

// Call fetchQueueUpdates every few seconds
setInterval(fetchQueueUpdates, 5000); // 0.5 seconds as an example