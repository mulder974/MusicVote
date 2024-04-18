import spotify
import security
from urllib.parse import urlencode
import requests
import base64
from flask import Flask, render_template, render_template_string, request, redirect, session, jsonify, url_for
import security
import time
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pprint
import os
import logging


secret_key = os.getenv('SECRET_KEY')

logging.basicConfig(filename='error.log', level=logging.WARNING)


#Variables
musics_votes = {}
active_tables = {}
nb_tables = 0
next_song = ""
MAX_VOTES_PER_USER = 1
spotify_token = "BQALtRXNb6UpvvhucSEzZ4GtHxfTEbuv_NFJagSl0aOGPyYHuDa4__ZVLpRwJ5ViU-a5yaVVLV0Qq6mDp7a24U-4vZyDPF3ESB-7wQwyOrV1bhoNhMbSi3OEkQG6wIiQBOJgsHZTzPLgzvCNt6tzWGO4Vx8MK-MQ3tidMA2rSiukOpPKoJTL7xLD8GYwfc5epOJQHzOL8g-Pg0kxzaHZtfi6kgjGAg"

host = 'http://0.0.0.0'
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
# app.secret_key = 'your_secret_key'

#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# User loader
@login_manager.user_loader
def load_user(id):
    return User(id)







#==================HTML ROUTE=========================#


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searching')
def searching():
    try :
        jwt = session['user_token'] 
        decoded = security.is_jwt_valid(jwt)
        if isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            return render_template('search.html')      
    except Exception as e: 
            print(e)
            return jsonify({'message': 'An error occurred'}), 500
    
    return jsonify({'message': 'Unauthorized access'}), 401


@app.route('/queue')
def queue():
    try :
        jwt = session['user_token'] 
        decoded = security.is_jwt_valid(jwt)
        if isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            return render_template('queue.html')      
    except Exception as e: 
            return jsonify({'message': 'An error occurred'}), 500
    
    return jsonify({'message': 'Unauthorized access'}), 401

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
    redirect_uri = host + ':4000/callback'


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


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@app.route('/parametres')
@login_required
def parametres():
    return render_template('layouts/parametres.html')

@app.route('/musiques')
@login_required
def musiques():
    return render_template('layouts/musiques.html')

@app.route('/tables')
@login_required
def tables():
    return render_template('layouts/tables.html')

#================== Log routes =========================#

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        security.good_credentials(username,password)
        
        if security.good_credentials(username,password):
            login_user(User(username))
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'

    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully.'

#================== TOKENS =========================#


@app.route('/generate_jwt')
def generate_jwt():
    global nb_tables

    token = request.args.get('token')
    #On check si il y a dejà un jwt dans la session de l'user
    try :
        jwt = session['user_token'] 
        jwt = request.headers.get('Authorization')            
        decoded = security.is_jwt_valid(jwt)
        if not isinstance(decoded, str):
            # Token is valid, proceed with the route logic
            nb_tables += 1
            active_tables[jwt] = {"table_number" : nb_tables ,"max_vote" : MAX_VOTES_PER_USER}
            return redirect('queue')      
        
    #Sinon on vérifie le token inclue dans le qr code et on génère un nouveau jwt
        elif security.is_qr_valid(token):
                jwt = security.generate_jwt(token)
                session['user_token'] = jwt 
                nb_tables += 1
                active_tables[jwt] = {"table_number" : nb_tables ,"max_vote" : MAX_VOTES_PER_USER}
               
                return redirect('queue')          
        else:
        # Token is invalid
                return jsonify({'message': decoded}), 401  
                        
    except :
        if security.is_qr_valid(token):
                jwt = security.generate_jwt(token)
                session['user_token'] = jwt
                    # Store token in session
                nb_tables += 1
                active_tables[jwt] = {"table_number" : nb_tables ,"max_vote" : MAX_VOTES_PER_USER}

                return redirect('queue')         
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
            'redirect_uri': host + ':4000/callback',
            'state': state
        })
    
    redirect_url = 'https://accounts.spotify.com/authorize?' + params   
            
    return redirect(redirect_url)


@app.route('/invalid_token')
def invalid_token():
    return "Invalid token. Please scan the QR code to access voting.", 403


#==================LOGIC ROUTE=========================#

@app.route('/get_songs')
def get_songs():
    jwt = session["user_token"]
    song_voted = {} 
    for song in musics_votes.keys():
         if musics_votes[song]["votes_total"] > 0:
            song_voted[song] = musics_votes[song]


    return jsonify({"song_voted": song_voted, "user":jwt}) # On a besoin de l'user pour ensuite vérifier 
                                                           # siil peut cliquer ou non sur le bouton de vote lorsque la queue est affichée
@app.route('/current_track')
def current_track():
    try: 
        global next_song
        # access_token = session['access_token'] 
        track_id, track_name, artist_name, album_img_src, track_lenght, track_progress = spotify.get_current_playing_track(spotify_token)
        print("next_song : " + next_song)
        
        if next_song == track_id:
            next_song = ""

        if track_lenght - track_progress < 15000 and next_song == '':  # 1.1 seconds before the end
            next_song = spotify.set_next_song(musics_votes, spotify_token)
            print("next_song : " + next_song)

            if next_song != "":
                del musics_votes[next_song]
                socketio.emit('song_changed', next_song)
                

        
        track_info = {
            'name': track_name,
            'artist': artist_name,
            'album_image_src': album_img_src,
            'track_length': track_lenght,
            'track_progress': track_progress
        }

        socketio.emit('track_update', track_info)
        return jsonify(track_info)
    except:
        print("Erreur avec le son en cours de lecture")
        return jsonify({"Exception" :'Erreur avec le son en cours de lecture'})



@app.route('/vote', methods=['POST'])
def vote():

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
    if song_vote_info["votes"][jwt]["nb_votes"] >= active_tables[jwt]["max_vote"]:
        song_vote_info["votes"][jwt]["max_vote_reached"] = True
            
        
    song_vote_info["name"] = data.get('song_name')
    song_vote_info["artist_name"] = data.get('artist_name')
    song_vote_info["song_image"] = data.get('song_image')
    song_vote_info["song_duration"] = data.get('song_duration')

    socketio.emit('vote_processed', {'message': 'A vote has been processed'})
    
    pprint.pprint(active_tables)

    return jsonify(success=True)


@app.route('/changeVoteLimit', methods=['POST'])
def change_vote_limit():
    data = request.json  # Assuming the limit is sent as JSON
    limit = data.get('limit')
    table_id = data.get('tableId')  # Assuming you're also sending the table ID

    # Example: Update the active_tables structure or database with the new limit
    # This is a placeholder. Adjust according to your actual data structure.
    if table_id in active_tables:
        active_tables[table_id]["max_vote"] = limit
        print(active_tables)
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Table ID not found"), 404





    
    # # Fetch the song data. You need to replace this with your actual song fetching logic.
    # song = get_song_by_id(song_id)
    # song['votes'] = votes[song_id]

    # return jsonify(success=True, song=song)


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
            song_duration_sec = round(song['duration_ms'] / 1000 )
            mins = song_duration_sec // 60 
            seconds = song_duration_sec % 60
            musics_votes[song_id]["duration"] = f"{mins}:{seconds:02d}"   


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
                data-duration="{{ song['duration'] }}"
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

@app.route('/fetchTablesAndVotes', methods=['GET'])
def fetchTablesAndVotes():
    tables_data = {}
    
    for table_id in active_tables.keys():
        tables_data[table_id] = {"table_number:" : active_tables[table_id]["table_number"],  
            "votes": [],
            "voteLimit": MAX_VOTES_PER_USER,  # Assuming a global variable for max votes
        }

        # Iterate through each song in the voting data
        for music in musics_votes.keys(): 
            if musics_votes[music]["votes_total"] > 0:
                if table_id in musics_votes[music]["votes"]:
                    vote_info = musics_votes[music]["votes"][table_id]
                    tables_data[table_id]["votes"].append({
                        "music_id": music,
                        "nb_votes": vote_info["nb_votes"],
                        "max_vote_reached": vote_info["max_vote_reached"],
                        "name": musics_votes[music]["name"],
                        "artist_name": musics_votes[music]["artist_name"],
                    })

    pprint.pprint(tables_data)

    return jsonify(tables_data)


def has_user_reached_vote_limit(jwt, song_id):
    if musics_votes[song_id]["votes"][jwt]["max_vote_reached"]:
        return True
    else:
        return False
    
#==================WEB SOCKETS=========================#
    
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(debug=False, host=host, port = 4000)