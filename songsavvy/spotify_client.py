from songsavvy import db
from songsavvy.models import OAuthToken
from dotenv import load_dotenv
from requests import post, get
import json
import os
from datetime import datetime
import base64

load_dotenv()

def get_id_from_url(song_url):
    print(song_url)
    song_id = song_url.split('/')[4]
    song_id = song_id.split('?')[0]
    return song_url.split('/')[4].split('?')[0]

class SpotifyClient():

    CLIENT_ID=os.getenv('CLIENT_ID')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')

    def __init__(self) -> None:
        if not self.is_token_valid:
            self.access_token = self.authorize()
        else:
            self.access_token = self.get_existing_access_token()

        
    @property
    def auth_header(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    @property
    def is_token_valid(self):
        token = self.token_object
        if token:
            formatted_time_accessed = token.time_accessed
            time_since_last_auth = datetime.utcnow() - formatted_time_accessed

            if time_since_last_auth.seconds < 3600:
                return True
        return False

    @property
    def token_object(self):
        return OAuthToken.query.first()
    
    def get_existing_access_token(self):
        return self.token_object.access_token
    

    def authorize(self):
        print('Requesting new OAuthToken from the Spotify API')
        auth_string = SpotifyClient.CLIENT_ID + ':' + SpotifyClient.CLIENT_SECRET
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        print(json_result)
        token = json_result['access_token']
        old_token_obj = self.token_object
        if old_token_obj:
            db.session.delete(old_token_obj)
        new_token_obj = OAuthToken(access_token=json_result['access_token'])
        db.session.add(new_token_obj)
        db.session.commit()
        return token
    
    def get_tracks(self, song_id):
        url = f'https://api.spotify.com/v1/tracks/{song_id}'
        
        response = get(
            url, 
            headers=self.auth_header
        )

        print(f'Access Token: {self.access_token}')

        response_json = response.json()

        if 'error' in response_json.keys():
            pass
        # response_json = json.loads(response)

        return response_json
    
    pass


if __name__ == "__main__":
    # client = SpotifyClient()
    # print(client.get_tracks('7LSpFCvRZZot2AlmkUzy9k'))
    print(get_id_from_url('https://open.spotify.com/track/7LSpFCvRZZot2AlmkUzy9k?si=f0c95884c8f94e27'))
    