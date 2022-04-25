#!/usr/bin/env python
# coding: utf-8

# In[3]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd

client_id = "04f95818e6204d0c859618683e385c82"
client_secret = "4b8b6aa9c8c34c3099eb55bfa8454482"
    
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# In[4]:


def make_df(playlist_uri, genre):
    uri = playlist_uri    # the URI is split by ':' to get the username and playlist ID
    username = uri.split(':')[1]
    playlist_id = uri.split(':')[0]

    results = sp.user_playlist(username, playlist_id, 'tracks')
    
    playlist_tracks_data = results['tracks']
    #playlist_tracks_id = []
    playlist_tracks_titles = []
    #playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_genre = []
    
    for i in range(50):
        playlist_genre.append(genre)

    for track in playlist_tracks_data['items']:
        #playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])
        # adds a list of all artists involved in the song to the list of artists for the playlist
        artist_list = []
        for artist in track['track']['artists']:
             artist_list.append(artist['name'])
    #     playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])
    
    features_df = pd.DataFrame()
    #Merge Playlist template
    features_df['title'] = playlist_tracks_titles[:50]
    features_df['first_artist'] = playlist_tracks_first_artists[:50]
    features_df['genre'] = playlist_genre
    # features_df['all_artists'] = playlist_tracks_artists
    #features_df = features_df.set_index('id')
    # features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
    #                            'danceability', 'energy', 'key', 'loudness',
    #                            'mode', 'acousticness', 'instrumentalness',
    #                            'liveness', 'valence', 'tempo',
    #                            'duration_ms', 'time_signature']]

    
    
    features_df = features_df[['first_artist','title', 'genre']]
    features_df.to_csv(f'DH_{genre}.csv', index=False)
    #display(features_df.head(50))


# In[5]:


playlist_links = {"pop": "37i9dQZF1DX4mWCZw6qYIw:5b47b6ac5d3341e0",
                 "rock": "37i9dQZF1DX3oM43CtKnRV:74abf2c14bce47f5",
                 "folk": "37i9dQZF1DXaUDcU6KDCj4:e1845fff16494e23",
                 "pop2": "37i9dQZF1DWUZMtnnlvJ9p:e2895698f60940bc",
                 "rap":"37i9dQZF1DX9oh43oAzkyx:73e3512f20324180"}


# In[6]:


playlist_uri = playlist_links["pop2"]
print(playlist_uri)
make_df(playlist_uri, "ult_pop")


# In[7]:


playlist_uri = playlist_links["pop"]
print(playlist_uri)
make_df(playlist_uri, "pop")


# In[11]:


playlist_uri = playlist_links["rock"]
print(playlist_uri)
make_df(playlist_uri, "rock")


# In[12]:


playlist_uri = playlist_links["folk"]
print(playlist_uri, "folk")
make_df(playlist_uri, "folk")


# In[8]:


playlist_uri = playlist_links["rap"]
print(playlist_uri)
make_df(playlist_uri, "rap")


# In[ ]:




