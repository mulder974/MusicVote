function updateQueueDisplay(response) {
    const dashboardContainer = document.querySelector('.dashboard'); // Make sure you have a container with class 'dashboard'
    dashboardContainer.innerHTML = ''; // Clear current dashboard contents

    // Example dashboard sections
    const topSongsSection = document.createElement('div');
    topSongsSection.className = 'top-songs-section';

    const recentActivitySection = document.createElement('div');
    recentActivitySection.className = 'recent-activity-section';

    let songs = response.songs; // Adjust according to your response structure
    let topSongs = getTopSongs(songs); // Implement this function to sort and get top songs
    let recentActivities = getRecentActivities(); // Implement to fetch recent activities

    // Populate Top Songs Section
    topSongs.forEach(song => {
        let songElement = createSongElement(song); // Implement this to create song elements
        topSongsSection.appendChild(songElement);
    });

    // Populate Recent Activities Section
    recentActivities.forEach(activity => {
        let activityElement = createActivityElement(activity); // Implement this function
        recentActivitySection.appendChild(activityElement);
    });

    // Append sections to dashboard container
    dashboardContainer.appendChild(topSongsSection);
    dashboardContainer.appendChild(recentActivitySection);
}

// Utility functions
function getTopSongs(songs) {
    // Logic to determine top songs based on votes or other criteria
}

function getRecentActivities() {
    // Fetch or calculate recent activities
}

function createSongElement(song) {
    // Create and return a DOM element for a song
}

function createActivityElement(activity) {
    // Create and return a DOM element for an activity
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