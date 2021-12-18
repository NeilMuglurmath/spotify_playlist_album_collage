import secrets
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from secrets import *

# get username from terminal
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Setting OAuth
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope)

# create Spotify object
sp = spotipy.Spotify(auth_manager=auth_manager)

currPlaylists = sp.current_user_playlists()
saucePlaylist = currPlaylists['items'][0]['id']
saucePlaylist = sp.playlist(saucePlaylist)['tracks']['items']

albumArt = []
albumIDOccur = {}
albumIDsToArtURL = {}

for song in saucePlaylist:
    albumArt.append(song['track']['album']['images'][0]['url'])
    albumID = song['track']['album']['id']
    if albumID in albumIDOccur:
        albumIDOccur[albumID] += 1
    else:
        albumIDOccur[albumID] = 1
        albumIDsToArtURL[albumID] = song['track']['album']['images'][0]['url']

# print(json.dumps(VARIABLE, sort_keys=True,indent=4))
