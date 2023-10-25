import numpy as np
import json
import pickle
from sklearn.ensemble import RandomForestClassifier

class RandomForestModel:
    def __init__(self, model_path, weights_path, columns_path):
        """
        Initializes the RandomForestModel class.

        Parameters:
        -----------
        model_path : str
            The path to the pre-trained model file.
        weights_path : str
            The path to the weights file.
        columns_path : str
            The path to the columns file.
        """
        self.clf = RandomForestClassifier()
        self.load_model(model_path, weights_path, columns_path)

    def load_model(self, model_path, weights_path, columns_path):
        """
        Loads the pre-trained model, weights and columns.

        Parameters:
        -----------
        model_path : str
            The path to the pre-trained model file.
        weights_path : str
            The path to the weights file.
        columns_path : str
            The path to the columns file.
        """
        with open(model_path, 'rb') as model_file:
            self.clf = pickle.load(model_file)

        with open(weights_path, 'r') as weights_file:
            self.weights = json.load(weights_file)

        with open(columns_path, 'r') as columns_file:
            self.columns = json.load(columns_file)['columns']

    def predict(self, X_test):
        """
        Predicts the target variable for the given input data.

        Parameters:
        -----------
        X_test : numpy.ndarray
            The input data to predict the target variable for.

        Returns:
        --------
        numpy.ndarray
            The predicted target variable for the given input data.
        """
        size = X_test.shape[0]
        default = np.array([-1] * size)
        
        try:
            X_test = X_test[self.columns]
           
        except Exception:
            return default
            
        return np.array(self.clf.predict(X_test))
