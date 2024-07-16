from src.churn_prediction_pipeline import ChurnPredictionPipeline

if __name__ == "__main__":
    data_path = "data/raw_data.csv"
    model_path = "models/churn_model.pkl"

    pipeline = ChurnPredictionPipeline(data_path, model_path)
    pipeline.run_pipeline()
