function voteForSong(songId, songName, artistName, songImage, songVoted) {
  $.ajax({
      url: '/vote',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ song_id: songId, song_name: songName, artist_name: artistName, song_image: songImage }),
      success: function(response) {
          if(response.success) {
              // The song has been successfully voted for, update the button state
              const voteButton = document.querySelector(`button[data-songid="${songId}"]`);
              if (response.success) {
                  // voteButton.disabled = true;
                  voteButton.classList.add('vote-limited');
                  voteButton.innerHTML = '<i class="icon-limited-votes"></i> Vote effectué';
              } else {
                  // Update the button to reflect that a vote has been cast
                  voteButton.dataset.songvoted = 'False';
              }
          } else {
              // There was an error processing your vote
              console.log(response)
              alert('There was an error processing your vote.');
          }
      },
      error: function() {
          alert('Error voting for song.');
      }
  });
}