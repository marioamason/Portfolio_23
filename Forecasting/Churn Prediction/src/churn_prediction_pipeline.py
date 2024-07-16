from src.data_loader import DataLoader
from src.data_preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTrainer
from src.model_evaluation import ModelEvaluator

class ChurnPredictionPipeline:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path

    def run_pipeline(self):
        # Load data
        loader = DataLoader(self.data_path)
        data = loader.load_data()

        # Preprocess data
        preprocessor = DataPreprocessor(data)
        data = preprocessor.preprocess()

        # Feature engineering
        engineer = FeatureEngineer(data)
        data = engineer.create_features()

        # Train model
        trainer = ModelTrainer(data)
        model, X_test, y_test = trainer.train_model()
        trainer.save_model(model, self.model_path)

        # Evaluate model
        evaluator = ModelEvaluator(model, X_test, y_test)
        evaluator.evaluate_model()
