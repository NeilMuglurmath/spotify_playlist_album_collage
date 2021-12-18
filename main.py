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
import requests
import shutil

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
# saucePlaylist = sorted(
# saucePlaylist, key=lambda k: k['added_at'], reverse=True)

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

albumIDOccur = {k: v for k, v in sorted(
    albumIDOccur.items(), key=lambda item: item[1], reverse=True)}
albumIDOccur = list(albumIDOccur.items())

for i in albumIDOccur:
    filename = albumIDsToArtURL[i[0]].split("/")[-1]
    r = requests.get(albumIDsToArtURL[i[0]], stream=True)
    r.raw.decode_content = True
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    # print(json.dumps(VARIABLE, sort_keys=True,indent=4))
