import random
from DataModel import DataModel


class PredictionModel:
    
    def __init__(self):
        pass

    def predict(self, text):
        arr = [random.randint(0, 3) for _ in range(len(text.split()))]
        return {
                "response": arr,
                "original_input": text
            }

    def make_predictions(self, data: DataModel):
        result = self.predict(data.text)
        return result
