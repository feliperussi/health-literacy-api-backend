import json
import pandas as pd
from utils.cleaning import clean_by_df
from models.model_gb import GradientBoostingModel
from models.model_rf import RandomForestModel
from models.model_emd import EMDistanceModel
# from DataProcessing import DataProcessing3

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
            prediction_emd, score_plain, score_no_plain =  self.emd_model.predict(sample)
            score_plain = score_plain.to_dict(orient='records')
            score_no_plain = score_no_plain.to_dict(orient='records')
            response = {"prediction": prediction_emd[0], "score_plain": score_plain[0], "score_no_plain": score_no_plain[0]}

        except Exception:
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
        try:
            sample = pd.DataFrame(sample, index=[0])
        except Exception:
            return None
        
        return clean_by_df(sample)
        