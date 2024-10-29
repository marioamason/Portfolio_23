

import pandas as pd

class DataCleaner:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def clean_data(self):
        """Cleans and transforms raw movie data."""
        df = pd.DataFrame(self.raw_data)
        df['Genres'] = df['Genres'].apply(lambda x: ', '.join(x) if x else 'Unknown')
        df['Rating'] = df['Rating'].fillna(0)  # Fill missing ratings with 0
        df['Rating Weight'] = df['Rating'].apply(lambda x: x if x > 5 else 0.5 * x)
        return df
