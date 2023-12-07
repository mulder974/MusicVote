import requests
import pprint


def set_next_song(musics_votes, access_token, song_in_queue):
   

    sorted_songs = sorted(musics_votes.items(), key=lambda x: x[1]['votes_total'], reverse=True)
    if sorted_songs:

        next_song_id = sorted_songs[0][0]
        song_in_queue = next_song_id

        if sorted_songs[0][1]['votes_total'] != 0:
            print(f"Puting next song in queu: {sorted_songs[0]}")
            print(musics_votes[next_song_id])
            uri = musics_votes[next_song_id]['uri'].replace(":", "%3A")
            url = f'https://api.spotify.com/v1/me/player/queue?uri={uri}'
            print(url)

            # Set the authorization header with the access token
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.post(url, headers=headers)
            # Code to play the song using Spotify API
            if response.status_code == 204:
                return song_in_queue
            else:
                
                print("Failed to set song in queue :" + str(response))
            

        # Update musics_votes to reflect the song has been played
        


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
    print(tracks[0])
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
        track_id = data['item']['id']
        track_name = data['item']['name']
        artist_name = data['item']['album']['artists'][0]['name']
        album_img_src = data['item']['album']['images'][0]['url']
        track_lenght = data['item']['duration_ms']
        track_proress = data['progress_ms']
        
        return track_id, track_name, artist_name, album_img_src, track_lenght, track_proress
    else:
        # Handle errors or no current playing track
        return response

    

pprint.pprint(get_current_playing_track("BQDJkZe9TuD81ngAYnKvd3inVehSCAqKBaGajGtBAcPXAlgdmfHpfM_bcA5pLJUTRUHNZyJC1cSyoCTpi1XYqkhlXw21imJSgz5Na6gg1mL6hkKfi7reR50N7_Nfkuzm06t3Ktv9MbJVG3oFFP_gGzzpYtpq-rN1uPJVivMGWYDC9pCbS9z3gMm4tDGeRKnJ_HxS6juUK7d0jx2szmq9XJ1Ilh3R"))
# print(get_access_token("a47c281636bd4a8b907c14495533e837","c86c9093985040b5a6253f3b66d1850a"))
# print(search_song("BQD9x6uHPDMs6QolRfpRqZR_NKgr7RySjg-b8byVFIpjH-6a_qDX5YVb9KzFIPDMvvjkEMSLZtJFiCr-uTecdnHdV-wZLEuUteQzScZTISSEms4OEGM", "with or without u"))

