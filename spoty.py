import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import spotipy.util as util
import random

#Authentication - without user
client_credentials_manage = SpotifyClientCredentials(client_id=cid, client_secret=secret, requests_session=True)
#cache_token = client_credentials_manage.get_access_token(cid)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manage)

#file of approx 6000 playlists from spotify, gotten off of kaggle
pl_file = pd.read_csv('final_playlists.csv')

print(pl_file) #file prints correctly
#print(pl_file['uri'].tolist())
uri_list = []
#getting a list of all playlist uris from the file
for uri in pl_file['uri'].tolist():
    playlist_URI = uri.split(':')[-1]
    uri_list.append(playlist_URI)
print(uri_list[0])    

#playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
#playlist_URI = playlist_link.split("/")[-1].split("?")[0]
#print(playlist_URI)

track_list = []
#for all playlist uris, go through and get all track uris 
for link in uri_list:
    #try to get track uri in each playlist, 
    #adding a try catch to skip any errors like track not found
    #if track uri not collected, skip/continue
    try: 
        print('getting in here')
        response = sp.playlist_tracks(link)
        track_items = response['items']

        for k in range(len(track_items)):
            trackItem = track_items[k]
            track = trackItem['track']
            track_list.append(track['uri'])
        #response = sp.playlist_items(link, fields = 'items.track.id,total', limit=100)["items"]
        #track_uris = [x["track"]["uri"] for x in response]
        # if len(response['items']) == 0:
        #     break
        # print(track_uris)
        # track_list.append(track_uris)
    except:
        continue
print(track_list)

df_tracks = pd.DataFrame(track_list)
df_tracks.to_csv('track_uris.csv')

# create lists with data 
track_uri_list = []
track_name_list = []
artist_uri_list = []
artist_info_list = []
artist_name_list = []
artist_pop_list = []
artist_genres_list = []
album_list = []
track_pop_list = []

#sp.playlist_tracks(playlist_URI)["items"]

for track in track_list:
    #URI
    track_uri = track
    track_uri_list.append(track_uri)
    #print(track_uri)

    #Track name track["track"]["name"]
    track_name = sp.track(track)["track"]["name"]
    track_name_list.append(track_name)
    #print(track_name)

    #Main Artist
    artist_uri = sp.track(track)["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    artist_uri_list.append(artist_uri)
    artist_info_list.append(artist_info)
    #print(artist_info)


    #Name, popularity, genre
    artist_name = sp.track(track)["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    artist_name_list.append(artist_name)
    artist_genres_list.append(artist_genres)
    artist_pop_list.append(artist_pop)
    #print(artist_name)
    #print(artist_pop)
    #print(artist_genres)

    #Album
    album = sp.track(track)["track"]["album"]["name"]
    album_list.append(album)
    
    #Popularity of the track
    track_pop = sp.track(track)["track"]["popularity"]
    track_pop_list.append(track_pop)
    #print(track_pop)

    output = {'Track URI':track_uri_list, 'Track Name':track_name_list, 'Artist URI':artist_uri_list, 
              'Artist Info':artist_info_list, 'Artist Name':artist_name_list, 'Artist Popularity':artist_pop_list,
             'Artist Genres':artist_genres_list, 'Album':album_list, 'Track Popularity':track_pop_list}
    
print(sp.audio_features(track_uri)[0])

#show output 
#print(output)

#putting output in a DataFrame
df = pd.DataFrame(output)
print(df)