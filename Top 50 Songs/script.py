import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Genius credentials
client_id = ''
client_secret = ''
access_token = ''

def get_genius_lyrics(song_title, artist_name):
    """
    Get the lyrics for a given song from the Genius API.
    
    Parameters:
        song_title (str): The title of the song.
        artist_name (str): The name of the artist.
        
    Returns:
        str: The lyrics of the song, or None if lyrics are not found.
    """
    base_url = 'https://api.genius.com'
    search_url = base_url + '/search'
    headers = {'Authorization': 'Bearer ' + access_token}
    data = {'q': song_title + ' ' + artist_name}
    
    response = requests.get(search_url, data=data, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        hits = json_response['response']['hits']
        for hit in hits:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_api_path = hit['result']['api_path']
                song_url = base_url + song_api_path
                response = requests.get(song_url, headers=headers)
                if response.status_code == 200:
                    song_json = response.json()
                    song_lyrics_path = song_json['response']['song']['path']
                    song_lyrics_url = 'https://genius.com' + song_lyrics_path
                    response = requests.get(song_lyrics_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        lyrics_div = soup.find('div', class_='lyrics')
                        if lyrics_div:
                            lyrics_lines = lyrics_div.get_text().split('\n')
                            first_line = lyrics_lines[0].strip()
                            lyrics = '\n'.join(lyrics_lines[1:]).strip()
                            return first_line, lyrics
    return None, None

def get_top_songs(year):
    """
    Get the top 100 songs for a given year from the Billboard Hot 100 chart via Wikipedia.
    
    Parameters:
        year (int): The year for which to retrieve the top songs.
        
    Returns:
        list: A list of dictionaries containing song information (ranking, title, artist, first_line, and lyrics).
    """
    url = f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='wikitable')
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            top_songs = []
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 3:
                    rank = columns[0].text.strip()
                    title = columns[1].text.strip()
                    artist = columns[2].text.strip()
                    first_line, lyrics = get_genius_lyrics(title, artist)
                    top_songs.append({
                        'Rank': rank, 
                        'Title': title, 
                        'Artist': artist, 
                        'First Line': first_line, 
                        'Lyrics': lyrics
                    })
            return top_songs
        else:
            print(f"No table found for {year}")
            return None
    else:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}")
        return None

def get_top_songs_past_n_years(n):
    """
    Get the top 100 songs for each year over the past n years.
    
    Parameters:
        n (int): Number of years to go back.
        
    Returns:
        dict: A dictionary where keys are years and values are DataFrames containing song information.
    """
    current_year = datetime.now().year
    top_songs_data = {}
    
    for year in range(current_year - n, current_year):
        top_songs = get_top_songs(year)
        if top_songs:
            top_songs_data[year] = pd.DataFrame(top_songs)
    
    return top_songs_data

# Example usage:
past_n_years = 5
top_songs_past_n_years = get_top_songs_past_n_years(past_n_years)
for year, top_songs_df in top_songs_past_n_years.items():
    print(f'Top songs of {year}:')
    print(top_songs_df)
    print('\n')