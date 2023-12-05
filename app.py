import spotify
import security
from urllib.parse import urlencode
import requests
import base64
from flask import Flask, render_template, render_template_string, request, redirect, session, jsonify


voted_songs = {}



app = Flask(__name__)
app.secret_key = 'your_secret_key'


# In-memory storage for demonstration purposes



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/current_track')
def current_track():
    # access_token = session['access_token'] 
    track_name, artist_name, album_img_src = spotify.get_current_playing_track("BQCv4QPPlv-80jQI-LYnYjA7RCfZ6gHKQPQnZvRxBCsGgGHz6-3Hyavu-mkpc44MPCZvGe7U5j4mCL22Sody9X3kSet3PcF8e9tCbPfsEu7KCrS-9yRZKRmIMfOBzTAbgmPolKwwkcXvbmUM8ovhntDKNx275ulM8U_imDAwJs_Oa3q5J4sYp76xPc3Ogmd0MKxJ9J8Ji_B0VmNvBZK2xzLLBubc")  
    
    return jsonify({'name': track_name, 'artist': artist_name, 'album_image_src': album_img_src})




@app.route('/login', methods=['GET'])
def login():
    state = security.get_random_string(16)
    scope = 'user-read-private user-read-currently-playing user-read-playback-state'
    params = urlencode({
            'response_type': 'code',
            'client_id': 'a47c281636bd4a8b907c14495533e837',
            'scope': scope,
            'redirect_uri': 'http://127.0.0.1:5000/callback',
            'state': state
        })
    
    redirect_url = 'https://accounts.spotify.com/authorize?' + params        
    
    return redirect(redirect_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if state is None:
        # Handle the state mismatch error
        return redirect('/#' + urlencode({'error': 'state_mismatch'}))

    # Your Spotify API credentials
    client_id = 'a47c281636bd4a8b907c14495533e837'
    client_secret = 'c86c9093985040b5a6253f3b66d1850a'
    redirect_uri = 'http://127.0.0.1:5000/callback'

    # Encode Client ID and Secret in Base64
    client_credentials = f"{client_id}:{client_secret}"
    client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

    # Headers
    headers = {
        'Authorization': f"Basic {client_credentials_b64}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # POST data
    post_data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    # Make the POST request
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=post_data)

    if response.status_code == 200:
        # Extract and use the access token
        access_token = response.json().get('access_token')
        print("Access token : " + access_token)
        session['access_token'] = access_token

        return "Access token received."
    else:
        return "Error fetching access token."


@app.route('/voting')
def voting():
    return render_template('voting.html')

@app.route('/get_songs')
def get_songs():
    return jsonify(voted_songs)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    
    song_id = data.get('song_id')
    
    if song_id in voted_songs:
        voted_songs[song_id]["votes"] += 1

    else:
        voted_songs[song_id] = {}
        voted_songs[song_id]["votes"] = 1
        voted_songs[song_id]["name"] = data.get('song_name')
        voted_songs[song_id]["artist_name"] = data.get('artist_name')
        voted_songs[song_id]["song_image"] = data.get('song_image')
    return jsonify(success=True)
    
    # # Fetch the song data. You need to replace this with your actual song fetching logic.
    # song = get_song_by_id(song_id)
    # song['votes'] = votes[song_id]

    # return jsonify(success=True, song=song)

@app.route('/searching')
def searching():
    return render_template('search.html')


@app.route('/queu')
def queu():
    return render_template('queu.html')



@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    songs = spotify.search_song("BQCv4QPPlv-80jQI-LYnYjA7RCfZ6gHKQPQnZvRxBCsGgGHz6-3Hyavu-mkpc44MPCZvGe7U5j4mCL22Sody9X3kSet3PcF8e9tCbPfsEu7KCrS-9yRZKRmIMfOBzTAbgmPolKwwkcXvbmUM8ovhntDKNx275ulM8U_imDAwJs_Oa3q5J4sYp76xPc3Ogmd0MKxJ9J8Ji_B0VmNvBZK2xzLLBubc", query)
    
    search_results_template = """
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
    <div class="container">
    <h2>Search Results</h2>
    <ul class="songs-list">
        {% for song in songs %}
        <li class="song-card">
            <img class="album-cover" src="{{ song['album']['images'][2]['url'] }}" alt="Album Cover">
            <div class="song-info">
                <h3 class="song-name">{{ song['name'] }}</h3>
                <p class="song-artist">{{ song['album']['artists'][0]['name'] }}</p>
            </div>
            <button class="vote-button" 
                    data-songId="{{ song['id'] }}" 
                    data-songName="{{ song['name'] }}" 
                    data-artistName="{{ song['album']['artists'][0]['name'] }}"
                    data-songImage = "{{ song['album']['images'][2]['url'] }}" 
                    >Voter !</button>
        </li>
        {% endfor %}
    </ul>
</div>
    """
    
    rendered_results = render_template_string(search_results_template, songs=songs)

    return rendered_results

if __name__ == '__main__':
    app.run(debug=True)

