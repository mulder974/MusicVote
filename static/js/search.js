
let debounceTimeout;
let lastTrackName = null;  // Declare this variable outside of your function



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
            var newTrackName = response.name;  // Ensure this matches your Flask route's response
            var newTrackArtist = response.artist;  // Ensure this matches your Flask route's response
            var newAlbumSource = response.album_image_src;  // Ensure this matches your Flask route's response

            if (newTrackName && newTrackName !== lastTrackName) {
                updateCurrentlyPlaying(newTrackName, newTrackArtist, newAlbumSource);
                lastTrackName = newTrackName;  // Update the last track name
            }
        },
        error: function() {
            console.log("Error fetching current track.");
        }
    });
}

function updateCurrentlyPlaying(trackName, artistName, albumImageSrc) {
    var albumCover = document.getElementById('album-cover');
    var trackTitle = document.getElementById('track-title');
    var trackArtist = document.getElementById('track-artist');

    albumCover.src = albumImageSrc;
    trackTitle.textContent = trackName;
    trackArtist.textContent = artistName;
}

setInterval(fetchCurrentTrack, 100000);

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
            console.log('Vote button clicked for song ID:', songId);
            voteForSong(songId, songName, artistName, songImage);
        }
    });
});
    

  

$(document).ready(function() {
    // Initial function calls
});
