import json
import pandas as pd
from app.utils.cleaning import clean_by_df
from app.models.model_gb import GradientBoostingModel
from app.models.model_rf import RandomForestModel
from app.models.model_emd import EMDistanceModel

class PredictionModel:
    def __init__(self, routes_path):
        with open(routes_path, 'r') as file:
            self.routes = json.load(file)

        self.gb_model = GradientBoostingModel(self.routes['gb_model'], self.routes['weights'], self.routes['columns'])
        self.rf_model = RandomForestModel(self.routes['rf_model'], self.routes['weights'], self.routes['columns'])
        self.emd_model = EMDistanceModel(self.routes['weights'], self.routes['means_label_0'], self.routes['means_label_1'])

    def predict(self, sample, model='gb'):
        response = {"prediction": None, "score_plain": None, "score_no_plain": None}
        try:
            sample = self.cleaning(sample)
            if sample is None:
                raise ValueError("Sample is None after cleaning.")
            

            prediction_emd, score_plain, score_no_plain = self.emd_model.predict(sample)
            score_plain = score_plain.to_dict(orient='records')
            score_no_plain = score_no_plain.to_dict(orient='records')
            response = {
                "prediction": prediction_emd[0],
                "score_plain": score_plain[0],
                "score_no_plain": score_no_plain[0]
            }

        except Exception as e:
            return response
        
        if model == 'gb':
            prediction_gb = self.gb_model.predict(sample)
            response['prediction'] = prediction_gb[0]
        elif model == 'rf':
            prediction_rf = self.rf_model.predict(sample)
            response['prediction'] = prediction_rf[0]
        elif model == 'emd':
            response['prediction'] = prediction_emd[0]

        return response

    def cleaning(self, sample):
        """
        Clean and preprocess the input sample.

        Args:
            sample (dict): The input data sample.

        Returns:
            pd.DataFrame: The cleaned and preprocessed sample.
        """
        try:
            # Flatten the nested dictionary structure
            flat_sample = pd.json_normalize(sample)
            sample_df = pd.DataFrame(flat_sample)

            # Remove 'readability.' prefix from column names
            sample_df.columns = [col.replace('readability.', '') for col in sample_df.columns]
        except Exception as e:
            return None
        
        cleaned_sample = clean_by_df(sample_df)
        return cleaned_sample
