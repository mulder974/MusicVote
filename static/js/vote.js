function voteForSong(songId, songName, artistName, songImage) {
    $.ajax({
      url: '/vote',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ song_id: songId, song_name: songName, artist_name: artistName, song_image: songImage }),
      success: function(response) {
        if(response.success) {
          // The song has been successfully voted for, now update the queue page
           // Implement this function to update the queue
        } else {
          alert('There was an error processing your vote.');
        }
      },
      error: function() {
        alert('Error voting for song.');
      }
    });
  }