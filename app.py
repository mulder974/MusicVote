import spotify
import security
from urllib.parse import urlencode
import requests
import base64
from flask import Flask, render_template, render_template_string, request, redirect, session, jsonify, url_for
import security
import time

musics_votes = {}
song_in_queue = ""



app = Flask(__name__)
app.secret_key = 'your_secret_key'

MAX_VOTES_PER_SONG = 1
spotify_token = "BQDS57w4jO44YVBKTz85Bx7hKyJJwTZF7kUWXrae82icOagy6t0rxcpNMRsGc7vXvKE-6RB97kOYV4ApAmAhEw75jwSoNVSfbfq5YiJfqWPx0Kqg7xcNQEVKRirGsfIAMEmvpsd0sAd_jyoclZdWcfoQQgpS9TVh2yfGxMCyn3zKccZmltFJ0pmakJXRpa1CGnTRbTL-8t6ax8eVEh9hkzbjei-VUw"





@app.route('/')
def index():
    return render_template('index.html')



@app.route('/generate_jwt')
def generate_jwt():
    token = request.args.get('token')
    #On check si il y a dejà un jwt dans la session de l'user
    try :
        jwt = session['user_token'] 
        jwt = request.headers.get('Authorization')            
        decoded = security.is_jwt_valid(jwt)
        if not isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            return redirect('queu')      
        
    #Sinon on vérifie le token inclue dans le qr code et on génère un nouveau jwt
        elif security.is_qr_valid(token):
                jwt = security.generate_jwt(token)
                session['user_token'] = jwt                
                return redirect('queu')          
        else:
        # Token is invalid
                return jsonify({'message': decoded}), 401  
                        
    except :
        if security.is_qr_valid(token):
                jwt = security.generate_jwt(token)
                session['user_token'] = jwt
                    # Store token in session
                return redirect('queu')         
        else:
        # Token is invalid
                return jsonify({'message': decoded}), 401      
        
        

@app.route('/get_spotify_token', methods=['GET'])
def get_spotify_token():
    state = security.generate_token(16)
    scope = 'user-read-private user-read-currently-playing user-read-playback-state user-modify-playback-state'
    params = urlencode({
            'response_type': 'code',
            'client_id': 'a47c281636bd4a8b907c14495533e837',
            'scope': scope,
            'redirect_uri': 'http://192.168.1.95:4000/callback',
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
    redirect_uri = 'http://192.168.1.95:4000/callback'

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

        return f"Access token received : {access_token}"
    else:
        return "Error fetching access token."


    
@app.route('/invalid_token')
def invalid_token():
    return "Invalid token. Please scan the QR code to access voting.", 403


@app.route('/get_songs')
def get_songs():
    jwt = session["user_token"]
    song_voted = {}
    for song in musics_votes.keys():
         if musics_votes[song]["votes_total"] > 0:
            song_voted[song] = musics_votes[song]
    print(song_voted)        
    return jsonify({"song_voted": song_voted, "user":jwt})

@app.route('/current_track')
def current_track():
    global song_in_queue
    # access_token = session['access_token'] 
    track_id, track_name, artist_name, album_img_src, track_lenght, track_progress = spotify.get_current_playing_track(spotify_token)
    
    if song_in_queue == track_id:
        song_in_queue = ""

    if track_lenght - track_progress < 5000 and song_in_queue == '':  # 1000 mili seconds before the end
       song_in_queue = spotify.set_next_song(musics_votes, spotify_token, song_in_queue)
       if song_in_queue:
            del musics_votes[song_in_queue]
    
    return jsonify({'name': track_name, 'artist': artist_name, 'album_image_src': album_img_src, 'track_lenght': track_lenght, 'track_progress': track_progress})



@app.route('/vote', methods=['POST'])
def vote():
    try:
        # Extract user ID from JWT token
        jwt = session.get("user_token")
        if not jwt:
            return jsonify({'message': 'Unauthorized access'}), 401

        decoded = security.is_jwt_valid(jwt)
        if not isinstance(decoded, str):
            return jsonify({'message': 'Invalid token'}), 401

        data = request.get_json()
        song_id = data.get('song_id')
        if not song_id:
            return jsonify({'message': 'Missing song ID'}), 400
        
        song_vote_info = musics_votes[song_id]

        song_vote_info["votes_total"] += 1
        # Increment the vote count for the current user
        song_vote_info["votes"][jwt]["nb_votes"] += 1
        if song_vote_info["votes"][jwt]["nb_votes"] >= MAX_VOTES_PER_SONG:
            song_vote_info["votes"][jwt]["max_vote_reached"] = True
             
            
        song_vote_info["name"] = data.get('song_name')
        song_vote_info["artist_name"] = data.get('artist_name')
        song_vote_info["song_image"] = data.get('song_image')
        

        return jsonify(success=True)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in vote route: {e}")
        return jsonify({'message': 'An error occurred processing your vote'}), 500



    
    # # Fetch the song data. You need to replace this with your actual song fetching logic.
    # song = get_song_by_id(song_id)
    # song['votes'] = votes[song_id]

    # return jsonify(success=True, song=song)

@app.route('/searching')
def searching():
    try :
        jwt = session['user_token'] 
        decoded = security.is_jwt_valid(jwt)
        if isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            return render_template('search.html')      
    except Exception as e: 
            return jsonify({'message': 'An error occurred'}), 500
    
    return jsonify({'message': 'Unauthorized access'}), 401



@app.route('/search', methods=['POST'])
def search():
    jwt = session['user_token'] 
    query = request.form.get('query')
    songs = spotify.search_song(spotify_token, query)

    for song in songs: 

        song_id = song['id']
        if song_id not in musics_votes.keys():
            musics_votes[song_id] = {}
            musics_votes[song_id]["votes"] = {jwt : {"nb_votes": 0, "max_vote_reached": False}}
            musics_votes[song_id]["votes"][jwt]["nb_votes"]  = 0
            musics_votes[song_id]["votes_total"] = 0
            musics_votes[song_id]["uri"] = song['uri']
        song['voted'] = has_user_reached_vote_limit(jwt, song_id)

         
    search_results_template = """
    
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
                data-songImage="{{ song['album']['images'][2]['url'] }}"
                data-songVoted="{{ song['voted'] }}"
                {% if song['voted'] %}disabled{% endif %}>
                {% if song['voted'] %}
        <i class="icon-limited-votes"></i> Max vote atteint
    {% else %}
        <i class="icon-vote"></i> Vote
    {% endif %}
                </button>
    </li>
{% endfor %}
    </ul>
</div>
    """
    
    
    rendered_results = render_template_string(search_results_template, songs=songs)

    return rendered_results

@app.route('/queu')
def queu():
    try :
        jwt = session['user_token'] 
        decoded = security.is_jwt_valid(jwt)
        if isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            return render_template('queu.html')      
    except Exception as e: 
            return jsonify({'message': 'An error occurred'}), 500
    
    return jsonify({'message': 'Unauthorized access'}), 401




def has_user_reached_vote_limit(jwt, song_id):
    if musics_votes[song_id]["votes"][jwt]["max_vote_reached"]:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 7000)

