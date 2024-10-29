

import os

class DataSaver:
    def __init__(self, data, file_path='data/imdb_movie_data.csv'):
        self.data = data
        self.file_path = file_path

    def save_to_csv(self):
        """Saves data to CSV."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.data.to_csv(self.file_path, index=False)
        print(f"Data saved to {self.file_path}")
