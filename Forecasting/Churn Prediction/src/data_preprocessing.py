import pandas as pd
from sklearn.preprocessing import LabelEncoder

class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def handle_missing_values(self):
        self.data.fillna(method='ffill', inplace=True)

    def encode_categorical_features(self):
        le = LabelEncoder()
        for column in self.data.select_dtypes(include=['object']).columns:
            self.data[column] = le.fit_transform(self.data[column])

    def preprocess(self):
        self.handle_missing_values()
        self.encode_categorical_features()
        return self.data
