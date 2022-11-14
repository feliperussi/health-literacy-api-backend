import random
import readability
import spacy
from collections import Counter
from DataModel import DataModel
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')
class PredictionModel:

    def __init__(self):
        pass
    
    def page(self, id):
        '''Return https://www.clinicaltrials.gov/ct2/show/{id} if id is valid make a request to verify if it is valid'''
        if id is None:
            return "Not valid id"
        if id == "":
            return "Not valid id"
        return f'https://www.clinicaltrials.gov/ct2/show/{id}'

    def scores(self, text):
        scores = readability.getmeasures(text, lang='en')
        readability_dict = dict(scores['readability grades'])
        sentence_dict = dict(scores['sentence info'])
        word_dict = dict(scores['word usage'])
        sentence_beg_dict = dict(scores['sentence beginnings'])
        return {
            "readability_grades": readability_dict,
            "sentence_info": sentence_dict,
            "word_usage": word_dict,
            "sentence_beginnings": sentence_beg_dict
        }

    def distributions(self, text):
        doc = nlp(text)
        verbs = [token.text.lower() for token in doc if token.pos_ == 'VERB']
        nouns = [token.text.lower() for token in doc if token.pos_ == 'NOUN']
        adjectives = [token.text.lower() for token in doc if token.pos_ == 'ADJ']

        verbs_count = Counter(verbs)
        nouns_count = Counter(nouns)
        adjectives_count = Counter(adjectives)

        return {
            "verbs": dict(verbs_count),
            "nouns": dict(nouns_count),
            "adjectives": dict(adjectives_count)
        }

    def predict(self, text):
        arr = [random.randint(0, 3) for _ in range(len(text.split()))]
        return {
                "response": arr,
                "original_input": text
            }
    
    def make_predictions(self, data: DataModel):
        result = self.predict(data.text)
        return result

    def get_scores(self, data: DataModel):
        result = self.scores(data.text)
        return result

    def get_distributions(self, data: DataModel):
        result = self.distributions(data.text)
        return result

    def get_page(self, data: DataModel):
        result = self.page(data.text)
        return result

