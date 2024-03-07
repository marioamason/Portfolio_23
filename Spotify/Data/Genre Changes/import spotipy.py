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
        print("User authenticated successfully.")
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

    # Retrieve user's listening history after 2023
    results = sp.current_user_recently_played(after=start_date_iso)

    listening_history = results['items'] if results else []
    print(f"Retrieved {len(listening_history)} items from user's listening history for 2023.")
    return listening_history

# Function to get artist's genres from Spotify API
def get_artist_genres(artist_id, token):
    sp = spotipy.Spotify(auth=token)
    artist = sp.artist(artist_id)
    return artist.get('genres', [])

# Function to analyze listening behavior over 2023
def analyze_listening_behavior(listening_history, token):
    # Initialize a dictionary to store genre counts for each day
    genre_counts_by_day = {}

    for item in listening_history:
        # Extract the full date from the played_at timestamp
        played_at = item['played_at']
        day = played_at[:10]  # Extract year-month-day part

        # If day is not already in the dictionary, initialize it with an empty Counter
        if day not in genre_counts_by_day:
            genre_counts_by_day[day] = Counter()

        track = item['track']
        if 'album' in track:
            for artist in track['artists']:
                if 'id' in artist:  # Check if 'id' key exists
                    artist_id = artist['id']
                    genres = get_artist_genres(artist_id, token)
                    if genres:  # Check if genres list is not empty
                        genre_counts_by_day[day].update(genres)

    print("Listening behavior analyzed successfully.")
    return genre_counts_by_day

# Function to visualize results in a tabular format
def visualize_results(genre_counts_by_day):
    # Print the table header
    print("Listening behavior changes over 2023 by day:")

    # Iterate over the days and print the genre counts for each day
    for day, genre_counts in genre_counts_by_day.items():
        # Convert the Counter object to a list of tuples for tabulate
        data = [(genre, count) for genre, count in genre_counts.items()]

        # Sort the data by count in descending order
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

        # Print the day
        print(f"\nDay: {day}")

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
    genre_counts_by_day = analyze_listening_behavior(listening_history, token)

    # Step 4: Visualize Results
    visualize_results(genre_counts_by_day)

if __name__ == "__main__":
    main()
