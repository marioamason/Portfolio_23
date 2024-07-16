import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class ModelTrainer:
    def __init__(self, data):
        self.data = data

    def split_data(self):
        X = self.data.drop('Churn', axis=1)
        y = self.data['Churn']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        X_train, X_test, y_train, y_test = self.split_data()
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model, X_test, y_test

    def save_model(self, model, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
