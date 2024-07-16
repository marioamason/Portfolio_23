from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ModelEvaluator:
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)

        self.print_interpretations(accuracy, precision, recall, f1)
        return accuracy, precision, recall, f1

    def print_interpretations(self, accuracy, precision, recall, f1):
        print(f"Model Evaluation Metrics:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Interpretation: Approximately {accuracy * 100:.2f}% of the predictions made by your model are correct.")

        print(f"\nPrecision: {precision:.4f}")
        print(f"Interpretation: When your model predicts a customer will churn, it is correct about {precision * 100:.2f}% of the time.")

        print(f"\nRecall: {recall:.4f}")
        print(f"Interpretation: Your model correctly identifies {recall * 100:.2f}% of all actual churns.")

        print(f"\nF1 Score: {f1:.4f}")
        print(f"Interpretation: The F1 score indicates a balance between precision and recall, which is about {f1 * 100:.2f}%.")

