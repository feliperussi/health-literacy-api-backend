import numpy as np
import json
import pickle
from sklearn.ensemble import GradientBoostingClassifier

class GradientBoostingModel:
    def __init__(self, model_path, weights_path, columns_path):
        """
        Initialize the GradientBoostingModel with paths to the model, weights, and columns.

        Args:
            model_path (str): Path to the pickle file containing the trained model.
            weights_path (str): Path to the JSON file containing model weights.
            columns_path (str): Path to the JSON file containing column names.
        """
        self.clf = GradientBoostingClassifier()
        self.load_model(model_path, weights_path, columns_path)

    def load_model(self, model_path, weights_path, columns_path):
        """
        Load the model, weights, and columns from files.

        Args:
            model_path (str): Path to the pickle file containing the trained model.
            weights_path (str): Path to the JSON file containing model weights.
            columns_path (str): Path to the JSON file containing column names.
        """
        with open(model_path, 'rb') as model_file:
            self.clf = pickle.load(model_file)

        with open(weights_path, 'r') as weights_file:
            self.weights = json.load(weights_file)

        with open(columns_path, 'r') as columns_file:
            self.columns = json.load(columns_file)['columns']

    def predict(self, X_test):
        """
        Predict the labels for the given test data.

        Args:
            X_test (pd.DataFrame): The test data.

        Returns:
            np.ndarray: Predicted labels.
        """
        size = X_test.shape[0]
        default = np.array([-1] * size)
        
        try:
            X_test = X_test[self.columns]
        except Exception:
            return default
            
        return np.array(self.clf.predict(X_test))
