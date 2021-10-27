import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "6a118825a92f4d5891cb9f0c74b50b5b"
CLIENT_SECRET = "23ba76a828aa4dc2818bae20f9ef00e6"

response = requests.get("https://www.top50songs.info/artist.php?artist=Maher%20Zain&v=12110664")
top_musics = response.text

song_names = []
soup = BeautifulSoup(top_musics, "html.parser")
music_names = soup.select("li a")

for music in music_names:
    song_names.append(music.getText().split(' ',1)[1])

print(song_names)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))
user_id = sp.current_user()["id"]
song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# print(song_names)

#Creating a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"Maher Zain Top Musics ever", public=False)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


























