import requests
import pprint


def play_next_song(musics_votes):
    sorted_songs = sorted(musics_votes.items(), key=lambda x: x[1]['votes_total'], reverse=True)
    print(sorted_songs)
    if sorted_songs:
        next_song_id = sorted_songs[0][0]
        # Code to play the song using Spotify API
        # Update musics_votes to reflect the song has been played
        print(f"Playing next song: {next_song_id}")


def search_song(access_token,query):
  # Set the endpoint URL
    url = f'https://api.spotify.com/v1/search?q={query}&type=track'

    # Set the authorization header with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Get the JSON response
    data = response.json()
    
    # Extract the relevant information from the response
    tracks = data['tracks']['items'][:5]
    return tracks

#    # Print the information of each track
#     for track in tracks:
#         print(f"Track: {track['name']}")  
#         print(f"Artist: {track['artists'][0]['name']}")
#         print(f"Album: {track['album']['name']}")
#         print(f"Preview URL: {track['preview_url']}")
#         print("-----")

def get_current_playing_track(access_token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data['item'])

        track_name = data['item']['name']
        artist_name = data['item']['album']['artists'][0]['name']
        album_img_src = data['item']['album']['images'][0]['url']
        track_lenght = data['item']['duration_ms']
        track_proress = data['progress_ms']

    
      

        
        return track_name, artist_name, album_img_src, track_lenght, track_proress
    else:
        # Handle errors or no current playing track
        return response





pprint.pprint(get_current_playing_track("BQDJkZe9TuD81ngAYnKvd3inVehSCAqKBaGajGtBAcPXAlgdmfHpfM_bcA5pLJUTRUHNZyJC1cSyoCTpi1XYqkhlXw21imJSgz5Na6gg1mL6hkKfi7reR50N7_Nfkuzm06t3Ktv9MbJVG3oFFP_gGzzpYtpq-rN1uPJVivMGWYDC9pCbS9z3gMm4tDGeRKnJ_HxS6juUK7d0jx2szmq9XJ1Ilh3R"))
# print(get_access_token("a47c281636bd4a8b907c14495533e837","c86c9093985040b5a6253f3b66d1850a"))
# print(search_song("BQD9x6uHPDMs6QolRfpRqZR_NKgr7RySjg-b8byVFIpjH-6a_qDX5YVb9KzFIPDMvvjkEMSLZtJFiCr-uTecdnHdV-wZLEuUteQzScZTISSEms4OEGM", "with or without u"))

