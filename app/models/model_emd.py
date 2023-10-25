import json
import numpy as np
import scipy.stats as stats

class EMDistanceModel:
    def __init__(self, path_weights, path_means_label_0, path_means_label_1, columns=None):
        self.load_model(path_weights, path_means_label_0, path_means_label_1, columns)
        
    def load_model(self, path_weights, path_means_label_0, path_means_label_1, columns=None):
        with open(path_weights, 'r', encoding='utf-8') as file:
            self.weights = json.load(file)
        self.columns = self.weights.keys() if columns is None else columns
        with open(path_means_label_0, 'r', encoding='utf-8') as file:
            self.means_label_0 = json.load(file)
        with open(path_means_label_1, 'r', encoding='utf-8') as file:
            self.means_label_1 = json.load(file)

    def predict(self, data_test):
        size = data_test.shape[0]
        default = np.array([-1] * size)
        try:
            X_test_top_abs = data_test[self.columns].copy()
            X_test_top_pls = data_test[self.columns].copy()
        except Exception:
            return default
        
        for col in self.columns:
            X_test_top_abs[col] = abs(X_test_top_abs[col] - self.means_label_0[col])*self.weights[col]
            X_test_top_pls[col] = abs(X_test_top_pls[col] - self.means_label_1[col])*self.weights[col]

        y_pred = []
        for i in range(len(X_test_top_abs)):
            if sum(X_test_top_abs.iloc[i]) < sum(X_test_top_pls.iloc[i]):
                y_pred.append(0)
            else:
                y_pred.append(1)
                
        return np.array(y_pred), X_test_top_abs, X_test_top_pls
