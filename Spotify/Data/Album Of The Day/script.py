import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter  # Import the Counter class
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Now authenticating")
app_specific_password = ""
# Spotify API credentials
client_id = ""
client_secret = ""
username = ""
redirect_uri = ""

# Initialize the Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read user-read-recently-played"))

def get_listening_history():
    # Get recently played tracks
    recent_tracks = sp.current_user_recently_played(limit=50)  # Adjust the limit as needed

    # Extract album names and timestamps
    albums = []
    for track in recent_tracks["items"]:
        album_name = track["track"]["album"]["name"]
        timestamp = track["played_at"]
        albums.append({"album_name": album_name, "timestamp": timestamp})

    return albums

def tag_favorite_albums(albums, threshold=1):
    album_counts = Counter(album["album_name"] for album in albums)
    favorite_albums = [album for album, count in album_counts.items() if count > threshold]
    return favorite_albums

def filter_recent_albums(albums, months=2):
    now = datetime.now()
    filtered_albums = []
    for album in albums:
        album_timestamp = datetime.strptime(album["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if now - album_timestamp > timedelta(days=30 * months):
            filtered_albums.append(album)  # Include both album name and timestamp
    return filtered_albums

def send_email(output_text):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = ''
    sender_password = app_specific_password

    # Recipient email address
    recipient_email = ''

    # Create the MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Your album of the day is...'

    # Add the output text to the email body
    body = f"Your albums of the day are:\n\n{output_text}"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    user_listening_history = get_listening_history()

    # Set the threshold for frequent listens (adjust as needed)
    listen_threshold = 1

    # Tag favorite albums
    favorite_albums = tag_favorite_albums(user_listening_history, threshold=listen_threshold)

    # Filter out albums listened to within the last 2 months
    filtered_favorite_albums = filter_recent_albums(user_listening_history, months=2)

    print(f"Favorite albums (listened to more than {listen_threshold} times, excluding last 2 months):")
    for album in filtered_favorite_albums:
        print(f"Album: {album['album_name']} | Timestamp: {album['timestamp']}")

    # Randomly select two albums
    random_albums = random.sample(filtered_favorite_albums, 2)

output_text = ""  # Initialize the output_text variable

for album in random_albums:
    album_timestamp = datetime.strptime(album["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_date = album_timestamp.strftime("%b %d, %Y")
    day_of_week = album_timestamp.strftime("%A")  # Get the day of the week
    album_info = f"You last listened to '{album['album_name']}' on {formatted_date} ({day_of_week}). Why not revisit it?"
    
    # Print the album info
    print(album_info)

    # Append the album info to output_text
    output_text += album_info + "\n"

# Now output_text contains all the album information
print("\nComplete output text:")
print(output_text)
send_email(output_text)  # Send the email with the album information

#Next steps
#1. Create a cron job to run the script daily
#2. Add error handling and logging
#3. Customize the email template and sender information
#4. Request user input for email recipient
#5. Add more features, such as recommendations based on favorite albums
#6. Deploy the script to a server for continuous execution
#7. Add more functionality, such as fetching album artwork and additional album details
#8. Explore other APIs and data sources to enhance the album recommendations
# 9. Add a web interface for users to interact with the script and receive recommendations
# 10. Set up environment variables for sensitive information such as API credentials and email passwords
# 11. Update for apple music since I dont even use spotify lol