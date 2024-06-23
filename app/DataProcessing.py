import readability
import spacy
import pandas as pd
from collections import Counter
from app.DataModel import DataModel

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

class DataProcessing:
    def __init__(self):
        """
        Initialize the DataProcessing class.
        """
        print("Loaded!")
        
    def scores(self, text):
        """
        Calculate readability scores for the given text.

        Args:
            text (str): The input text.

        Returns:
            dict: A dictionary containing readability grades, sentence info, word usage, and sentence beginnings.
        """
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
        """
        Calculate word and entity distributions for the given text.

        Args:
            text (str): The input text.

        Returns:
            dict: A dictionary containing counts of various parts of speech, entities, and other text features.
        """
        doc = nlp(text)
        
        def count_tokens(pos_tag):
            return len([token.text for token in doc if token.pos_ == pos_tag])

        def count_entities(entity_type):
            return len([token.text for token in doc if token.ent_type_ == entity_type])

        counts = {
            "total_words": len([token.text for token in doc if token.pos_ != 'PUNCT']),
            "total_sentences": len(list(doc.sents)),
            "total_characters": len(text),
            "passive_voice": count_tokens('VBN'),
            "active_voice": count_tokens('VB'),
            "passive_toks": len([token.text for token in doc if token.dep_ == "nsubjpass"]),
            "active_toks": len([token.text for token in doc if token.dep_ == "nsubj"]),
            "verbs": count_tokens('VERB'),
            "nouns": count_tokens('NOUN'),
            "adjectives": count_tokens('ADJ'),
            "adverbs": count_tokens('ADV'),
            "prepositions": count_tokens('ADP'),
            "auxiliaries": count_tokens('AUX'),
            "conjunctions": count_tokens('CONJ'),
            "coord_conjunctions": count_tokens('CCONJ'),
            "determiners": count_tokens('DET'),
            "interjections": count_tokens('INTJ'),
            "numbers": count_tokens('NUM'),
            "particles": count_tokens('PART'),
            "pronouns": count_tokens('PRON'),
            "proper_nouns": count_tokens('PROPN'),
            "punctuations": count_tokens('PUNCT'),
            "subordinating_conjunctions": count_tokens('SCONJ'),
            "symbols": count_tokens('SYM'),
            "other": count_tokens('X'),
            "money": count_entities('MONEY'),
            "persons": count_entities('PERSON'),
            "norp": count_entities('NORP'),
            "facilities": count_entities('FAC'),
            "organizations": count_entities('ORG'),
            "gpe": count_entities('GPE'),
            "products": count_entities('PRODUCT'),
            "events": count_entities('EVENT'),
            "works": count_entities('WORK_OF_ART'),
            "languages": count_entities('LANGUAGE'),
            "dates": count_entities('DATE'),
            "times": count_entities('TIME'),
            "quantities": count_entities('QUANTITY'),
            "ordinals": count_entities('ORDINAL'),
            "cardinals": count_entities('CARDINAL'),
            "percentages": count_entities('PERCENT'),
            "locations": count_entities('LOC'),
            "laws": count_entities('LAW'),
            "stopwords": len([token.text for token in doc if token.is_stop]),
        }
        return counts
    
    def readability(self, text):
        """
        Calculate readability scores and distributions for the given text.

        Args:
            text (str): The input text.

        Returns:
            dict: A dictionary containing readability scores and various distributions.
        """
        scores = readability.getmeasures(text, lang='en')
        scores_dict = dict(scores['readability grades'])
        sentence_dict = dict(scores['sentence info'])
        word_dict = dict(scores['word usage'])
        distribution_dict = self.distributions(text)

        # Filter necessary fields from sentence and word dictionaries
        sentence_fields = ["characters_per_word", "syll_per_word", "words_per_sentence", "sentences_per_paragraph", "type_token_ratio", "characters", "syllables", "words", "wordtypes", "sentences", "paragraphs", "long_words", "complex_words", "complex_words_dc"]
        word_fields = ["tobeverb", "auxverb", "conjunction", "nominalization"]

        sentence_dict = {k: sentence_dict[k] for k in sentence_fields}
        word_dict = {k: word_dict[k] for k in word_fields}

        # Update distribution_dict with sentence and word info
        distribution_dict.update(sentence_dict)
        distribution_dict.update(word_dict)
        
        # Update scores_dict with distribution info
        scores_dict.update(distribution_dict)

        return {"readability": scores_dict}
   
    def get_scores(self, data: DataModel):
        """
        Get readability scores for the input data.

        Args:
            data (DataModel): The input data model containing text.

        Returns:
            dict: The readability scores.
        """
        return self.scores(data.text)

    def get_distributions(self, data: DataModel):
        """
        Get word and entity distributions for the input data.

        Args:
            data (DataModel): The input data model containing text.

        Returns:
            dict: The distributions.
        """
        return self.distributions(data.text)

    def get_readability(self, data: DataModel):
        result = self.readability(data.text)
        return result
