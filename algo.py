import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import spotipy.util as util
import pickle

cid = ""
secret = ""
#Authentication - without user
client_credentials_manage = SpotifyClientCredentials(client_id=cid, client_secret=secret, requests_session=True,requests_timeout=10)
#cache_token = client_credentials_manage.get_access_token(cid)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manage)

track_list = pd.read_csv('duringClean.csv')

# remove unnamed columns
#Unnamed: 0.1,Unnamed: 0
#track_list.drop(columns=['artists_song'], inplace=True)

# backup1 = pd.read_csv('newnew.csv')
# backup1.drop(columns=['Track URI', 'Unnamed: 0'],inplace=True)
# print(backup1)
# backup1.to_csv('new_backup.csv', index=False)


#FIXME: Uncomment this each time before running the track info part after
#getting backup from pickle file and adding to a csv
# with open('fileDump.pickle', 'rb') as handle:
#     b = pickle.load(handle)
# print(b)    
# df_bu2 = pd.DataFrame(b)
# df_backup = pd.read_csv('new_backup.csv')
# joined = pd.concat([df_bu2, df_backup], ignore_index = True)
# print(df_bu2)
# joined.to_csv('new_backup.csv', index=False)


#SPLITTING FEATURE LIST
feature_list = pd.read_csv('Final_Features_Copy.csv')
print(feature_list)
print(feature_list.dtypes)

feature_list[["Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", 
                                                            "Acousticness", "Instrumentalness","Liveness", "Valence", "Tempo",
                                                            "Type", "Audio_Features", "URI","Track_Href", "Analysis_URL", "Duration_MS", "Time_Sig"]] = feature_list['0'].str.split(', ', expand=True)
print(feature_list)
print(feature_list.dtypes)
feature_list.to_csv('Final_Features_Copy2.csv', index=False)

#Copying list at last gotten should be next:3gxEZXUjrNbl3TlSrTGbR5 
# 0Y4LVCIZVLEkho5g2SfgfX
#DATA COLLECTION COMPLETE DON'T RUN THIS PART ANYMORE
list = track_list['Track URI'].tolist()
copy_list = list[:list.index('4Pm6d1HchNq8x2Q67OkP8L')]
copy_list2 = list[list.index('4Pm6d1HchNq8x2Q67OkP8L')+1:]
print(copy_list2[0])
print(copy_list[0])

track_features = []
#GETIING TRACK INFO
for track in copy_list2:
    print("Making API call")
    print(track)
    feature = sp.audio_features(track)[0]
    track_features.append(feature)
    output = {'Track URI':feature["id"],'Track Features':track_features}

    with open('fileDump.pickle', 'wb') as handle:
        pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#SAVING DATA     
# df = pd.DataFrame(output)
# print(df)    
# df.to_csv('newBackup.csv', index=False)
# print(track_list)
# track_list.to_csv('duringClean.csv', index=False)
