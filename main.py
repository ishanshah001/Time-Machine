"""
@author: Ishan Shah

A spotify playlist creastor for given date.
"""

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Enter your client id. This one won't work!
CLIENT_ID = "9b46b674bc7245ddaac61d5dc33f95a9"

# Enter your token. This one won't work!
CLIENT_SECRET = "9ff8bfb8630040cab0e953e797d76340"

# ------------------------URL generator---------------------------------------------

url="https://www.billboard.com/charts/hot-100/"

date = input("Enter date (yyyy-mm-dd) you wish to travel to: ")
# date="2001-01-31"
url += date


# -----------------------Scraping data------------------------------------------------
response = requests.get(url=url)
data = response.text

soup=BeautifulSoup(data,"html.parser")

song_name_list=[]
song_artist_list=[]

for song_name in soup.select(selector=".chart-element__information .chart-element__information__song"):
    song_name_list+=[song_name.getText()]

for song_artist in soup.select(selector=".chart-element__information .chart-element__information__artist"):
    song_artist_list+=[song_artist.getText()]

song_info = []
for i in range(len(song_name_list)):
    song_info += [song_name_list[i] + " by " + song_artist_list[i]]


# -----------------------Using spotify api to generate playlist-------------------------
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:5000/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


song_uris = []
year = date.split("-")[0]
for song in song_name_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

playlist = sp.user_playlist_create(user=user_id, name="Top songs of the day", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(playlist["external_urls"]["spotify"])


