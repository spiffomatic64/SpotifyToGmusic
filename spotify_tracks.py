#! python3 

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import sys

f = open("out.txt", "w", encoding="utf-8")

def write_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        f.write("%d\t%s\t%s\n" % (i, track['artists'][0]['name'], track['name']))
        
def get_tracks(uri):
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    return results['tracks']

# https://spotipy.readthedocs.io/en/latest/#authorization-code-flow
# I used environment variables to setup auth, but you can also use: util.prompt_for_user_token
# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
# export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

theSoundOfEverything = "spotify:user:thesoundsofspotify:playlist:69fEt9DN5r4JQATi52sRtq"
tracks = get_tracks(theSoundOfEverything)
write_tracks(tracks)

while tracks['next']:
    print('.', end='', flush=True)
    tracks = sp.next(tracks)
    write_tracks(tracks)
