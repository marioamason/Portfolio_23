import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

# Scopes required for accessing user's top tracks and audio features
SCOPE = 'user-top-read user-read-recently-played'

# Authenticate and authorize the user
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE))
user = sp.current_user()
print("User: ", user['display_name'])

# Get the user's top 100 tracks
results = sp.current_user_top_tracks(limit=5, time_range='long_term')

# List to store the track IDs of the user's top tracks
top_tracks = []
# Iterate over each track and retrieve its audio features
for item in results['items']:
    track_id = item['id']
    top_tracks.append(track_id)

# Convert the list of track IDs to a comma-separated string
top_tracks_string = ",".join(top_tracks)

# Retrieve audio features for the top tracks
audio_features = sp.audio_features(top_tracks_string)

audio_feature_values = []
for track_features in audio_features:
    if track_features is not None:
        feature_values = [track_features['danceability'], track_features['energy'], track_features['key'],
                          track_features['loudness'], track_features['speechiness'], track_features['acousticness'],
                          track_features['instrumentalness'], track_features['liveness'], track_features['valence'],
                          track_features['tempo']]
        audio_feature_values.append(feature_values)

# Search for recommended tracks using audio features
recommended_tracks = sp.recommendations(seed_tracks=top_tracks, limit=50)

# Print the recommended tracks
print("Recommended Tracks:")
for track in recommended_tracks['tracks']:
    print(track['name'], "-", track['artists'][0]['name'])
