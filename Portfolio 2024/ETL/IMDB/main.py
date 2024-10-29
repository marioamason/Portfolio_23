

from imdb_recommender.data_fetcher import DataFetcher
from imdb_recommender.data_cleaner import DataCleaner
from imdb_recommender.data_saver import DataSaver

def main():
    # Step 1: Fetch Data
    fetcher = DataFetcher(top_n=50)
    raw_data = fetcher.fetch_top_movies()

    # Step 2: Clean Data
    cleaner = DataCleaner(raw_data)
    clean_data = cleaner.clean_data()

    # Step 3: Save Data
    saver = DataSaver(clean_data)
    saver.save_to_csv()

if __name__ == "__main__":
    main()
