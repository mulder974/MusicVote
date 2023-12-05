import requests
import pprint





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
    pprint.pprint(tracks[0])
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
        track_name = data['item']['name']
        artist_name = data['item']['album']['artists'][0]['name']
        album_id = data['item']['album']['id']
        album_img_src = data['item']['album']['images'][0]['url']

    
      

        
        return track_name, artist_name, album_img_src
    else:
        # Handle errors or no current playing track
        return response





# print(get_current_song("BQCwKHRKbolk8l74UE5o6fXTpbCifFZHiFbwOx18aOx-mp2bmiXVvM5rzkoXOXABSiUTPT_5LrHYtV2_F7PbCM-rERVDzfOjThWclkH7D3Md8RXOyVo"))
# print(get_access_token("a47c281636bd4a8b907c14495533e837","c86c9093985040b5a6253f3b66d1850a"))
# print(search_song("BQD9x6uHPDMs6QolRfpRqZR_NKgr7RySjg-b8byVFIpjH-6a_qDX5YVb9KzFIPDMvvjkEMSLZtJFiCr-uTecdnHdV-wZLEuUteQzScZTISSEms4OEGM", "with or without u"))

