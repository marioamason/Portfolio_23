import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def authenticate_user(client_id, client_secret, username):
    redirect_uri = 'http://localhost/'
    scope = 'user-read-recently-played'

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    if token:
        return token
    else:
        print("Authentication failed.")
        return None

def get_recently_played_artists(token, limit=10):
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_recently_played(limit=limit)
    artists = []

    if results and 'items' in results:
        for item in results['items']:
            artist_name = item['track']['artists'][0]['name']
            artists.append(artist_name)

    return artists

def get_artist_details(token, artist_name):
    sp = spotipy.Spotify(auth=token)
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    
    if results and 'artists' in results and 'items' in results['artists'] and len(results['artists']['items']) > 0:
        artist = results['artists']['items'][0]
        birthday = artist.get('birthdate', 'N/A')
        birth_city = artist.get('birthplace', 'N/A')
        return birthday, birth_city
    else:
        print("Failed to retrieve artist details.")
        return None, None
    
def get_artist_details(artist_name):
    # Search artist on Wikipedia
    url = f"https://en.wikipedia.org/wiki/{artist_name}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract artist details (birthday and birth city)
        birthday = soup.find('span', {'class': 'bday'})
        birth_city = soup.find('div', {'class': 'birthplace'})

        return birthday.text if birthday else None, birth_city.text.strip() if birth_city else None
    else:
        print("Failed to retrieve artist details.")
        return None, None

def get_zodiac_sign(birthday):
    if not birthday:
        return 'N/A'

    birthdate = datetime.strptime(birthday, '%Y-%m-%d')
    if (birthdate.month == 3 and birthdate.day >= 21) or (birthdate.month == 4 and birthdate.day <= 19):
        return 'Aries (Mar 21 - Apr 19)'
    elif (birthdate.month == 4 and birthdate.day >= 20) or (birthdate.month == 5 and birthdate.day <= 20):
        return 'Taurus (Apr 20 - May 20)'
    elif (birthdate.month == 5 and birthdate.day >= 21) or (birthdate.month == 6 and birthdate.day <= 20):
        return 'Gemini (May 21 - Jun 20)'
    elif (birthdate.month == 6 and birthdate.day >= 21) or (birthdate.month == 7 and birthdate.day <= 22):
        return 'Cancer (Jun 21 - Jul 22)'
    elif (birthdate.month == 7 and birthdate.day >= 23) or (birthdate.month == 8 and birthdate.day <= 22):
        return 'Leo (Jul 23 - Aug 22)'
    elif (birthdate.month == 8 and birthdate.day >= 23) or (birthdate.month == 9 and birthdate.day <= 22):
        return 'Virgo (Aug 23 - Sep 22)'
    elif (birthdate.month == 9 and birthdate.day >= 23) or (birthdate.month == 10 and birthdate.day <= 22):
        return 'Libra (Sep 23 - Oct 22)'
    elif (birthdate.month == 10 and birthdate.day >= 23) or (birthdate.month == 11 and birthdate.day <= 21):
        return 'Scorpio (Oct 23 - Nov 21)'
    elif (birthdate.month == 11 and birthdate.day >= 22) or (birthdate.month == 12 and birthdate.day <= 21):
        return 'Sagittarius (Nov 22 - Dec 21)'
    elif (birthdate.month == 12 and birthdate.day >= 22) or (birthdate.month == 1 and birthdate.day <= 19):
        return 'Capricorn (Dec 22 - Jan 19)'
    elif (birthdate.month == 1 and birthdate.day >= 20) or (birthdate.month == 2 and birthdate.day <= 18):
        return 'Aquarius (Jan 20 - Feb 18)'
    else:
        return 'Pisces (Feb 19 - Mar 20)'

def get_chinese_zodiac_animal(birthday):
    if not birthday or birthday == 'N/A':
        return 'N/A'

    birthdate = datetime.strptime(birthday, '%Y-%m-%d')
    start_year = 1900
    animal_list = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
    return animal_list[(birthdate.year - start_year) % 12]


def get_artist_discography(sp, artist_name):
    search_results = sp.search(q=f'artist:{artist_name}', type='artist')
    if search_results and 'artists' in search_results:
        artists = search_results['artists']['items']
        if artists:
            artist_id = artists[0]['id']
            albums = sp.artist_albums(artist_id, album_type='album', limit=50)
            return albums['items']
    return None

def get_highest_selling_album(sp, artist_name):
    albums = get_artist_discography(sp, artist_name)
    if albums:
        highest_selling_album = max(albums, key=lambda x: x.get('popularity', 0))
        return highest_selling_album
    return None


def main():
    # Spotify API credentials
    client_id = ""
    client_secret = ""
    username = ""

    # Step 1: Authenticate User
    token = authenticate_user(client_id, client_secret, username)
    if not token:
        return
    sp = spotipy.Spotify(auth=token)
    # Step 2: Get User's Listening History (10 most listened-to artists)
    artists = get_recently_played_artists(token, limit=10)
    if not artists:
        return

    # Step 3: Get Artist Details and Display Results
    print("Most listened-to artists:")
    for artist_name in artists:
        birthday, birth_city = get_artist_details(artist_name)
        zodiac_sign = get_zodiac_sign(birthday)
        chinese_zodiac_animal = get_chinese_zodiac_animal(birthday)

        print(f"Artist: {artist_name}")
        if birthday:
            print(f"Birthday: {birthday}")
            print(f"Zodiac Sign: {zodiac_sign}")
            print(f"Chinese Zodiac Animal: {chinese_zodiac_animal}")
        else:
            print("Birthday: N/A")
        if birth_city:
            print(f"Birth city: {birth_city}")
        else:
            print("Birth city: N/A")
        print()

    print("Highest Selling Albums:")
    for artist_name in artists:
        highest_selling_album = get_highest_selling_album(sp, artist_name)
        if highest_selling_album:
            print(f"Artist: {artist_name}")
            print(f"Highest Selling Album: {highest_selling_album['name']}")
            print()
        else:
            print(f"No discography found for artist: {artist_name}")

if __name__ == "__main__":
    main()

# Next Steps
