
let lastTrackName = null;  

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    console.log('Connected to WebSocket');
});

socket.on('track_update', function(data) {
    console.log('Track update received:', data);
    updateCurrentlyPlaying(data.name, data.artist, data.album_image_src, data.track_length, data.track_progress);
});

function handleSearchInput() {
    var query = $('#search-input').val();
    if (query.length >= 1) {
        // Send an AJAX request to the Flask server to get search results
        $.ajax({
            url: '/search',
            type: 'POST',
            data: { query: query },
            success: function(data) {
                // Update the search results container with the returned HTML
                $('#search-results-container').html(data);
            }
        });
    } else {
        // Clear the search results container if the search query is empty
        $('#search-results-container').empty();
    }
}
function fetchCurrentTrack() {
    console.log("fetchCurrentTrack called");
    $.ajax({
        url: '/current_track',
        type: 'GET',
        success: function(response) {
            console.log("AJAX success, response:", response);            
        },
        error: function() {
            console.log("Error fetching current track.");
        }
    });
}

function updateCurrentlyPlaying(trackName, artistName, albumImageSrc, trackLenght, trackProgress) {
    var albumCover = document.getElementById('album-cover');
    var trackTitle = document.getElementById('track-title');
    var trackArtist = document.getElementById('track-artist'); 

    var progressBar = document.getElementById('song-progress-bar');
    var percentage = (trackProgress / trackLenght) * 100;
    console.log(trackLenght)
    console.log(trackProgress)
    console.log(percentage)

    progressBar.style.width = percentage + '%';
    albumCover.src = albumImageSrc;
    trackTitle.textContent = trackName;
    trackArtist.textContent = artistName;
}


$('#search-form').on('submit', function(e) {
    e.preventDefault();
    handleSearchInput();
});



document.addEventListener('DOMContentLoaded', () => {
    // Attach the event listener to the parent container of the buttons
    // Replace '.container' with the actual selector of your parent container
    const container = document.querySelector('#search-results-container');

    container.addEventListener('click', function(event) {
        // Check if the clicked element is a vote button
        if (event.target.classList.contains('vote-button')) {
            const songId = event.target.dataset.songid;
            const songName = event.target.dataset.songname;
            const artistName = event.target.dataset.artistname;
            const songImage = event.target.dataset.songimage;  
            const songVoted =event.target.dataset.songvoted;          
            console.log('Vote button clicked for song ID:', songId);
            voteForSong(songId, songName, artistName, songImage, songVoted);
        }
    });
});
    

    
$(document).ready(function() {
    // Initial function calls
});


$('#search-form').on('submit', function(e) {
    e.preventDefault();
    handleSearchInput();
});

fetchCurrentTrack();

setInterval(fetchCurrentTrack, 1000);
