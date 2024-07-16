class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    def create_features(self):
        self.data['TotalCharges'] = self.data['tenure'] * self.data['MonthlyCharges']
        return self.data
