import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import spotipy.util as util
import random
import time
import pickle

#Authentication - without user
client_credentials_manage = SpotifyClientCredentials(client_id=cid, client_secret=secret, requests_session=True,requests_timeout=10)
#cache_token = client_credentials_manage.get_access_token(cid)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manage)

#file of approx 6000 playlists from spotify, gotten off of kaggle
# pl_file = pd.read_csv('final_playlists.csv')

# print(pl_file) #file prints correctly
# #print(pl_file['uri'].tolist())
# uri_list = []
# #getting a list of all playlist uris from the file
# for uri in pl_file['uri'].tolist():
#     playlist_URI = uri.split(':')[-1]
#     uri_list.append(playlist_URI)
# print(uri_list[0])    

#playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
#playlist_URI = playlist_link.split("/")[-1].split("?")[0]
#print(playlist_URI)

# track_list = []
# #for all playlist uris, go through and get all track uris 
# for link in uri_list:
#     #try to get track uri in each playlist, 
#     #adding a try catch to skip any errors like track not found
#     #if track uri not collected, skip/continue
#     try: 
#         #print('getting in here')
#         response = sp.playlist_tracks(link)
#         track_items = response['items']
        
#         for k in range(len(track_items)):
#             trackItem = track_items[k]
#             track = trackItem['track']
#             print(track['uri'])
#             track_list.append(track['uri'])
#         #response = sp.playlist_items(link, fields = 'items.track.id,total', limit=100)["items"]
#         #track_uris = [x["track"]["uri"] for x in response]
#         # if len(response['items']) == 0:
#         #     break
#         # print(track_uris)
#         # track_list.append(track_uris)
#     except:
#         continue
# print(track_list)

#df_tracks = pd.DataFrame(track_list)
# df_tracks.to_csv('track_uris.csv')

#FIXME: Uncomment this each time before running the track info part after blocking
#getting backup from pickle file and adding to a csv
# with open('fileDump.pickle', 'rb') as handle:
#     b = pickle.load(handle)
# print(b)    
# df_bu2 = pd.DataFrame(b)
# df_backup = pd.read_csv('backup.csv')
# joined = pd.concat([df_bu2, df_backup], ignore_index = True)
# print(joined)
# joined.to_csv('backup.csv')

track_list = pd.read_csv('track_uris.csv')

#FIXME: Update with last URI gotten
#splitting up track list to start at last track gotten in backup file
list = track_list['0'].tolist()
copy_list = list[:list.index('spotify:track:69xUkf647IyVn8cJtQ4zRk')]
copy_list2 = list[list.index('spotify:track:69xUkf647IyVn8cJtQ4zRk')+1:]
print(copy_list2[0])
print(copy_list[0])

# create lists with data 
track_uri_list = []
track_uri_list2 = []
track_name_list = []
artist_uri_list = []
artist_info_list = []
artist_name_list = []
artist_pop_list = []
artist_genres_list = []
album_list = []
track_pop_list = []
#sp.playlist_tracks(playlist_URI)["items"]
for track_uncut in copy_list2:
    trackURI = track_uncut.split(':')[-1]
    track_uri_list.append(trackURI)

print(track_uri_list[0])
count = 0
print(sp.requests_timeout)
print(sp.retries)
print(sp.status_retries)
for track in track_uri_list:
    #URI
    # print('Sleeping 30 sec')
    # time.sleep(30)  
    track_uri = track
    # df = pd.DataFrame(output)
    # print(df)
    # df.to_csv('complete_tracks.csv')
    track_uri_list2.append(track_uri)
    print(track_uri)

    try:
        print('making 1 API call/getting track info')
        #Track name track["track"]["name"]
        track_info = sp.track(track)
        track_name = track_info["name"]
    except spotipy.client.SpotifyException as e:
        print('Spotify Error(%s): %s', e.http_status, e.msg)
   
    print(track_name)
    track_name_list.append(track_name)
    # print('Sleeping 30 sec')
    # time.sleep(30)  
    
    #Main Artist
    try:
        print('getting artist URI from track info')
        artist_uri = track_info["artists"][0]["uri"]
        # print('Sleeping 30 sec')
        # time.sleep(30)  
        print('making 1 API call for artist info')
        artist_info = sp.artist(artist_uri)
    except spotipy.client.SpotifyException as e:
        print('Spotify Error(%s): %s', e.http_status, e.msg)   

    print(artist_uri)
    print(artist_info)
    artist_uri_list.append(artist_uri)
    artist_info_list.append(artist_info)

    #Name, popularity, genre
    print('getting artist name/pop/genres')
    artist_name = artist_info["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    artist_name_list.append(artist_name)
    artist_genres_list.append(artist_genres)
    artist_pop_list.append(artist_pop)
    print(artist_name)
    print(artist_pop)
    print(artist_genres)

    #Album
    print('getting album name from track info')
    album = track_info["album"]["name"]
    album_list.append(album)

    #Popularity of the track
    print('getting pop from track info')
    track_pop = track_info["popularity"]
    track_pop_list.append(track_pop)
    print(track_pop)

    output = {'Track URI':track_uri_list2, 'Track Name':track_name_list, 'Artist URI':artist_uri_list, 
              'Artist Info':artist_info_list, 'Artist Name':artist_name_list, 'Artist Popularity':artist_pop_list,
             'Artist Genres':artist_genres_list, 'Album':album_list, 'Track Popularity':track_pop_list}
    
    with open('fileDump.pickle', 'wb') as handle:
        pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)

    count = count + 1 
    print(count)
    
#print(sp.audio_features(track_uri)[0])

#show output 
#print(output)

#putting output in a DataFrame
df = pd.DataFrame(output)
print(df)
df.to_csv('complete_tracks.csv')
print("done")
