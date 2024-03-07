import spotipy
import spotipy.util as util
import datetime
from collections import Counter
from tabulate import tabulate as tab

# Function to authenticate user with Spotify API
def authenticate_user(client_id, client_secret, username):
    redirect_uri = "http://localhost:8888/callback/"
    scope = 'user-read-recently-played'

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    if token:
        return token
    else:
        print("Authentication failed.")
        return None

# Function to get user's listening history from Spotify API for the year 2023
def get_listening_history(token):
    sp = spotipy.Spotify(auth=token)
    
    # Calculate start date for 2023
    start_date = datetime.datetime(2023, 1, 1)

    # Convert date to ISO format required by Spotify API
    start_date_iso = start_date.isoformat() + 'Z'

    # Retrieve user's listening history for 2023
    results = sp.current_user_recently_played(after=start_date_iso)

    return results['items'] if results else []

# Function to analyze listening behavior over 2023
def analyze_listening_behavior(listening_history):
    genres_counter = Counter()
    for item in listening_history:
        track = item['track']
        if 'album' in track:
            for artist in track['artists']:
                if 'genres' in artist:  # Check if 'genres' key exists
                    genres = artist['genres']
                    genres_counter.update(genres)

    return genres_counter

# Function to visualize results in a tabular format
def visualize_results(listening_behavior_changes):
    # Convert the Counter object to a list of tuples for tabulate
    data = [(genre, count) for genre, count in listening_behavior_changes.items()]

    # Sort the data by count in descending order
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

    # Print the table header
    print("Listening behavior changes over 2023:")
    
    # Print the table using tabulate
    print(tab(sorted_data, headers=['Genre', 'Count'], tablefmt='pretty'))

def main():
    # Spotify API credentials
    client_id = ""
    client_secret = ""
    username = ""

    # Step 1: Authenticate User
    token = authenticate_user(client_id, client_secret, username)
    if not token:
        return

    # Step 2: Get User's Listening History for 2023
    listening_history = get_listening_history(token)

    # Step 3: Analyze Listening Behavior over 2023
    listening_behavior_changes = analyze_listening_behavior(listening_history)

    # Step 4: Visualize Results
    #visualize_results(listening_behavior_changes)
    visualize_results(listening_behavior_changes)

if __name__ == "__main__":
    main()
