import spotify
import security
from urllib.parse import urlencode
import requests
import base64


from flask import Flask, render_template, render_template_string, request, redirect, session





app = Flask(__name__)
app.secret_key = 'your_secret_key'




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/current_track')
def current_track():
    # access_token = session['access_token'] 
    track_id = spotify.get_current_playing_track("BQBVVjuHilMo2cTUx-km1eRXlwwYreZNJsx2x_H5HToivINDTZE5-SFY5rBALvBVC1M7IIoT_wK_9O9b8MVXCocK1hLyYeUO_xM_1LGIxKlah1dNkfkRITguPKaW6roQfKBHbhezLNGy3enfqPY6qH4M11GVwVXlPHRxpRjGVVQksc5YWA1MY_KRAM9ux9sIgAoYXLWwYIm0dv-yZ3OBs0tOKfDG")  
    print(track_id)
    return track_id



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

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    songs = spotify.search_song("BQCtDZW11VSCSLnz_I-t-znI7QL-he9_-OHIJvfc6ZwOEbwjOvuNh1eXPeZkwaKH4eacqA4IPdTxGN2QvxO4QCK4yy_hw31k4mqq_UCTRaIY43e7EFQ", query)
    
    search_results_template = """
    <style>
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        h2 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 20px;
        }
        h3 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        p {
            margin: 0;
        }
        .vote-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 5px 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 12px;
            margin-top: 5px;
            cursor: pointer;
            border-radius: 3px;
        }
    </style>
    <div class="container">
        <h2>Search Results</h2>
        <ul>
            {% for song in songs %}
            <li>
                <h3>{{ song['name'] }}</h3>
                <p>Artist: {{ song['album']['artists'][0]['name'] }}</p>

                <button class="vote-button">Vote</button>
            </li>
            {% endfor %}
        </ul>
    </div>
    """
    
    rendered_results = render_template_string(search_results_template, songs=songs)

    return rendered_results

if __name__ == '__main__':
    app.run(debug=True)

