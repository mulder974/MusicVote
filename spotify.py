import requests

def get_access_token(id,user_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': user_secret
    }
    response = requests.post(url, headers=headers, data=data)
    access_token = response.json()['access_token']

    return response.json()





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
    tracks = data['tracks']['items']

    return tracks

#    # Print the information of each track
#     for track in tracks:
#         print(f"Track: {track['name']}")
#         print(f"Artist: {track['artists'][0]['name']}")
#         print(f"Album: {track['album']['name']}")
#         print(f"Preview URL: {track['preview_url']}")
#         print("-----")

 
#print(get_access_token("a47c281636bd4a8b907c14495533e837","c86c9093985040b5a6253f3b66d1850a"))
# print(search_song("BQD9x6uHPDMs6QolRfpRqZR_NKgr7RySjg-b8byVFIpjH-6a_qDX5YVb9KzFIPDMvvjkEMSLZtJFiCr-uTecdnHdV-wZLEuUteQzScZTISSEms4OEGM", "with or without u"))