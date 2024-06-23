import json
import numpy as np

class EMDistanceModel:
    def __init__(self, path_weights, path_means_label_0, path_means_label_1, columns=None):
        """
        Initialize the EMDistanceModel with paths to the model weights and means.

        Args:
            path_weights (str): Path to the JSON file containing model weights.
            path_means_label_0 (str): Path to the JSON file containing means for label 0.
            path_means_label_1 (str): Path to the JSON file containing means for label 1.
            columns (list, optional): List of columns to consider. Defaults to None.
        """
        self.load_model(path_weights, path_means_label_0, path_means_label_1, columns)
        
    def load_model(self, path_weights, path_means_label_0, path_means_label_1, columns=None):
        """
        Load the model weights and means from JSON files.

        Args:
            path_weights (str): Path to the JSON file containing model weights.
            path_means_label_0 (str): Path to the JSON file containing means for label 0.
            path_means_label_1 (str): Path to the JSON file containing means for label 1.
            columns (list, optional): List of columns to consider. Defaults to None.
        """
        with open(path_weights, 'r', encoding='utf-8') as file:
            self.weights = json.load(file)
        self.columns = self.weights.keys() if columns is None else columns
        with open(path_means_label_0, 'r', encoding='utf-8') as file:
            self.means_label_0 = json.load(file)
        with open(path_means_label_1, 'r', encoding='utf-8') as file:
            self.means_label_1 = json.load(file)

    def predict(self, data_test):
        """
        Predict the label for the given test data using Earth Mover's Distance.

        Args:
            data_test (pd.DataFrame): The test data.

        Returns:
            np.ndarray: Predicted labels.
            pd.DataFrame: Adjusted test data for label 0.
            pd.DataFrame: Adjusted test data for label 1.
        """
        size = data_test.shape[0]
        default = np.array([-1] * size)
        
        try:
            X_test_top_abs = data_test[self.columns].copy()
            X_test_top_pls = data_test[self.columns].copy()
        except KeyError as e:
            print(f"KeyError: {e}")
            return default, None, None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return default, None, None
        
        for col in self.columns:
            try:
                X_test_top_abs[col] = abs(X_test_top_abs[col] - self.means_label_0[col]) * self.weights[col]
                X_test_top_pls[col] = abs(X_test_top_pls[col] - self.means_label_1[col]) * self.weights[col]
            except KeyError as e:
                print(f"KeyError in column '{col}': {e}")
                return default, None, None
            except Exception as e:
                print(f"Unexpected error in column '{col}': {e}")
                return default, None, None

        y_pred = []
        for i in range(len(X_test_top_abs)):
            try:
                if sum(X_test_top_abs.iloc[i]) < sum(X_test_top_pls.iloc[i]):
                    y_pred.append(0)
                else:
                    y_pred.append(1)
            except Exception as e:
                print(f"Error in prediction loop at index {i}: {e}")
                y_pred.append(-1)
                
        return np.array(y_pred), X_test_top_abs, X_test_top_pls
