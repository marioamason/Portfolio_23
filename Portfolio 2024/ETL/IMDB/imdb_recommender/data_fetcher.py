import subprocess
import sys

# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing IMDbPY, install if not found
try:
    from imdb import IMDb
except ModuleNotFoundError:
    print("IMDbPY not found. Installing IMDbPY...")
    install_package("IMDbPY")
    from imdb import IMDb  # Import again after installation

# Now you can proceed with the rest of your code
ia = IMDb()

from imdb import IMDb

class DataFetcher:
    def __init__(self, top_n=50):
        self.ia = IMDb()
        self.top_n = top_n

    def fetch_top_movies(self):
        """Fetches details of top N movies from IMDb."""
        top_movies = self.ia.get_top50_movies()[:self.top_n]
        movie_data = []

        for movie in top_movies:
            movie_id = movie.movieID
            movie_details = self.ia.get_movie(movie_id)
            movie_data.append({
                'Title': movie_details.get('title'),
                'Genres': movie_details.get('genres'),
                'Rating': movie_details.get('rating'),
                'Plot Summary': movie_details.get('plot outline')
            })

        return movie_data
