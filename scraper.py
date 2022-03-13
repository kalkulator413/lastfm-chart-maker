from urllib.request import Request, urlopen
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_data(username):
    data = []
    url = 'https://www.last.fm/user/' + username + '/library/albums?date_preset=LAST_7_DAYS'

    html = urlopen(Request(url, headers = {'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')

    album_data = re.findall(r'content=[",].+ — .+ \(\d+\),', html)[0][9:]
    album_data = album_data.split('),')[:-1]

    for album in album_data:
        num_plays = album[album.rfind('(')+1:]
        artist = fix_string(max(re.findall(r'.+ — ', album), key=lambda w: len(w))[:-3])
        if artist[0] == ' ':
            artist = artist[1:]
        album = fix_string(max(re.findall(r' — .* \(', album), key = lambda w: len(w))[3:-2])
        data.append((album, artist, num_plays, get_album_img(album, artist)))
    return data[:25]
    
def fix_string(s):
    s = s.replace('&#39;', '\'')
    s = s.replace('&quot;', '"')
    s = s.replace('amp;', '')
    s = s.replace(' ', ' ')
    return s

def get_album_img(album, artist):
    results = sp.search(q="artist:" + artist + " album:" + album, type="album")
    items = results['albums']['items']
    if len(items) > 0:
        album = items[0]
        return album['images'][0]['url']
    return None

