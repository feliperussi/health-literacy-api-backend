import readability
import spacy
import json
import pandas as pd
from collections import Counter
from DataModel import DataModel

nlp = spacy.load('en_core_web_sm')

class DataProcessing:

    def __init__(self):
        print("Loaded!")
        
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

        total_words = len([token.text for token in doc if token.pos_ != 'PUNCT'])
        total_sentences = len([token.text for token in doc.sents])
        total_characters = len(text)
        passive_voice = len([token.text for token in doc if token.tag_ == 'VBN'])
        active_voice = len([token.text for token in doc if token.tag_ == 'VB'])
        passive_toks = len([token.text for token in doc if (token.dep_ == "nsubjpass") ])
        active_toks = len([token.text for token in doc if (token.dep_ == "nsubj") ])
        adjectives = [token.text for token in doc if token.pos_ == 'ADJ']
        prepositions = [token.text for token in doc if token.pos_ == 'ADP']
        adverbs = [token.text for token in doc if token.pos_ == 'ADV']
        auxiliaries = [token.text for token in doc if token.pos_ == 'AUX']
        conjunctions = [token.text for token in doc if token.pos_ == 'CONJ']
        coord_conjunctions = [token.text for token in doc if token.pos_ == 'CCONJ']
        determiners = [token.text for token in doc if token.pos_ == 'DET']
        interjections = [token.text for token in doc if token.pos_ == 'INTJ']
        nouns = [token.text for token in doc if token.pos_ == 'NOUN']
        numbers = [token.text for token in doc if token.pos_ == 'NUM']
        particles = [token.text for token in doc if token.pos_ == 'PART']
        pronouns = [token.text for token in doc if token.pos_ == 'PRON']
        proper_nouns = [token.text for token in doc if token.pos_ == 'PROPN']
        punctuations = [token.text for token in doc if token.pos_ == 'PUNCT']
        subordinating_conjunctions = [token.text for token in doc if token.pos_ == 'SCONJ']
        symbols = [token.text for token in doc if token.pos_ == 'SYM']
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        other = [token.text for token in doc if token.pos_ == 'X']

        ners = ['PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL']

        persons = [token.text for token in doc if token.ent_type_ == 'PERSON']
        norp = [token.text for token in doc if token.ent_type_ == 'NORP']
        facilities = [token.text for token in doc if token.ent_type_ == 'FAC']
        organizations = [token.text for token in doc if token.ent_type_ == 'ORG']
        gpe = [token.text for token in doc if token.ent_type_ == 'GPE']
        locations = [token.text for token in doc if token.ent_type_ == 'LOC']
        products = [token.text for token in doc if token.ent_type_ == 'PRODUCT']
        events = [token.text for token in doc if token.ent_type_ == 'EVENT']
        works = [token.text for token in doc if token.ent_type_ == 'WORK_OF_ART']
        laws = [token.text for token in doc if token.ent_type_ == 'LAW']
        languages = [token.text for token in doc if token.ent_type_ == 'LANGUAGE']
        dates = [token.text for token in doc if token.ent_type_ == 'DATE']
        times = [token.text for token in doc if token.ent_type_ == 'TIME']
        percentages = [token.text for token in doc if token.ent_type_ == 'PERCENT']
        money = [token.text for token in doc if token.ent_type_ == 'MONEY']
        quantities = [token.text for token in doc if token.ent_type_ == 'QUANTITY']
        ordinals = [token.text for token in doc if token.ent_type_ == 'ORDINAL']
        cardinals = [token.text for token in doc if token.ent_type_ == 'CARDINAL']

        # Stop words and punctuations
        stopwords = [token.text for token in doc if token.is_stop]
        punctuations = [token.text for token in doc if token.pos_ == 'PUNCT']

        # Lowercase all words 
        adjectives = [word.lower() for word in adjectives]
        prepositions = [word.lower() for word in prepositions]
        adverbs = [word.lower() for word in adverbs]
        auxiliaries = [word.lower() for word in auxiliaries]
        conjunctions = [word.lower() for word in conjunctions]
        coord_conjunctions = [word.lower() for word in coord_conjunctions]
        determiners = [word.lower() for word in determiners]
        interjections = [word.lower() for word in interjections]
        nouns = [word.lower() for word in nouns]
        numbers = [word.lower() for word in numbers]
        particles = [word.lower() for word in particles]
        pronouns = [word.lower() for word in pronouns]
        proper_nouns = [word.lower() for word in proper_nouns]
        punctuations = [word.lower() for word in punctuations]
        subordinating_conjunctions = [word.lower() for word in subordinating_conjunctions]
        symbols = [word.lower() for word in symbols]
        verbs = [word.lower() for word in verbs]
        other = [word.lower() for word in other]

        money = [word.lower() for word in money]
        persons = [word.lower() for word in persons]
        norp = [word.lower() for word in norp]
        facilities = [word.lower() for word in facilities]
        organizations = [word.lower() for word in organizations]
        gpe = [word.lower() for word in gpe]
        products = [word.lower() for word in products]
        events = [word.lower() for word in events]
        works = [word.lower() for word in works]
        languages = [word.lower() for word in languages]
        dates = [word.lower() for word in dates]
        times = [word.lower() for word in times]
        quantities = [word.lower() for word in quantities]
        ordinals = [word.lower() for word in ordinals]
        cardinals = [word.lower() for word in cardinals]
        percentages = [word.lower() for word in percentages]
        locations = [word.lower() for word in locations]
        laws = [word.lower() for word in laws]
        

        adjectives_count = Counter(adjectives)
        prepositions_count = Counter(prepositions)
        adverbs_count = Counter(adverbs)
        auxiliaries_count = Counter(auxiliaries)
        conjunctions_count = Counter(conjunctions)
        coord_conjunctions_count = Counter(coord_conjunctions)
        determiners_count = Counter(determiners)
        interjections_count = Counter(interjections)
        nouns_count = Counter(nouns)
        numbers_count = Counter(numbers)
        particles_count = Counter(particles)
        pronouns_count = Counter(pronouns)
        proper_nouns_count = Counter(proper_nouns)
        punctuations_count = Counter(punctuations)
        subordinating_conjunctions_count = Counter(subordinating_conjunctions)
        symbols_count = Counter(symbols)
        verbs_count = Counter(verbs)
        other_count = Counter(other)
        money_count = Counter(money)
        persons_count = Counter(persons)
        norp_count = Counter(norp)
        facilities_count = Counter(facilities)
        organizations_count = Counter(organizations)
        gpe_count = Counter(gpe)
        products_count = Counter(products)
        events_count = Counter(events)
        works_count = Counter(works)
        languages_count = Counter(languages)
        dates_count = Counter(dates)
        times_count = Counter(times)
        quantities_count = Counter(quantities)
        ordinals_count = Counter(ordinals)
        cardinals_count = Counter(cardinals)
        percentages_count = Counter(percentages)
        locations_count = Counter(locations)
        laws_count = Counter(laws)

        stopwords_count = Counter(stopwords)

        # Get the total amount of each type of word
        adjectives_count = sum(adjectives_count.values())
        prepositions_count = sum(prepositions_count.values())
        adverbs_count = sum(adverbs_count.values())
        auxiliaries_count = sum(auxiliaries_count.values())
        conjunctions_count = sum(conjunctions_count.values())
        coord_conjunctions_count = sum(coord_conjunctions_count.values())
        determiners_count = sum(determiners_count.values())
        interjections_count = sum(interjections_count.values())
        nouns_count = sum(nouns_count.values())
        numbers_count = sum(numbers_count.values())
        particles_count = sum(particles_count.values())
        pronouns_count = sum(pronouns_count.values())
        proper_nouns_count = sum(proper_nouns_count.values())
        punctuations_count = sum(punctuations_count.values())
        subordinating_conjunctions_count = sum(subordinating_conjunctions_count.values())
        symbols_count = sum(symbols_count.values())
        verbs_count = sum(verbs_count.values())
        other_count = sum(other_count.values())
        
        money_count = sum(money_count.values())
        persons_count = sum(persons_count.values())
        norp_count = sum(norp_count.values())
        facilities_count = sum(facilities_count.values())
        organizations_count = sum(organizations_count.values())
        gpe_count = sum(gpe_count.values())
        products_count = sum(products_count.values())
        events_count = sum(events_count.values())
        works_count = sum(works_count.values())
        languages_count = sum(languages_count.values())
        dates_count = sum(dates_count.values())
        times_count = sum(times_count.values())
        quantities_count = sum(quantities_count.values())
        ordinals_count = sum(ordinals_count.values())
        cardinals_count = sum(cardinals_count.values())
        percentages_count = sum(percentages_count.values())
        locations_count = sum(locations_count.values())
        laws_count = sum(laws_count.values())

        stopwords_count = sum(stopwords_count.values())

        return {
            "total_words": total_words,
            "total_sentences": total_sentences,
            "total_characters": total_characters,
            "passive_voice": passive_voice,
            "active_voice": active_voice,
            "passive_toks": passive_toks,
            "active_toks": active_toks,
            "verbs": verbs_count,
            "nouns": nouns_count,
            "adjectives": adjectives_count,
            "adverbs": adverbs_count,
            "prepositions": prepositions_count,
            "auxiliaries": auxiliaries_count,
            "conjunctions": conjunctions_count,
            "coord_conjunctions": coord_conjunctions_count,
            "determiners": determiners_count,
            "interjections": interjections_count,
            "numbers": numbers_count,
            "particles": particles_count,
            "pronouns": pronouns_count,
            "proper_nouns": proper_nouns_count,
            "punctuations": punctuations_count,
            "subordinating_conjunctions": subordinating_conjunctions_count,
            "symbols": symbols_count,
            "other": other_count,
            "money": money_count,
            "persons": persons_count,
            "norp": norp_count,
            "facilities": facilities_count,
            "organizations": organizations_count,
            "gpe": gpe_count,
            "products": products_count,
            "events": events_count,
            "works": works_count,
            "languages": languages_count,
            "dates": dates_count,
            "times": times_count,
            "quantities": quantities_count,
            "ordinals": ordinals_count,
            "cardinals": cardinals_count,
            "percentages": percentages_count,
            "stopwords": stopwords_count,
            "locations": locations_count,
            "laws": laws_count,
        }
    
    def readability(self, text):
        scores = readability.getmeasures(text, lang='en')
        scores_dict = dict(scores['readability grades'])
        sentence_dict = dict(scores['sentence info'])
        word_dict = dict(scores['word usage'])
        distribution_dict = self.distributions(text)

        sentence_dict = {k: sentence_dict[k] for k in ("characters_per_word", "syll_per_word", "words_per_sentence", "sentences_per_paragraph", "type_token_ratio", "characters", "syllables", "words", "wordtypes", "sentences", "paragraphs", "long_words", "complex_words", "complex_words_dc")}

        word_dict = {k: word_dict[k] for k in ("tobeverb", "auxverb", "conjunction", "nominalization")}

        distribution_dict.update(sentence_dict)
        distribution_dict.update(word_dict)
        # Concatenate the two dictionaries
        scores_dict.update(distribution_dict)

        return {
            "readability": scores_dict
        }
   
    def get_scores(self, data: DataModel):
        result = self.scores(data.text)
        return result

    def get_distributions(self, data: DataModel):
        result = self.distributions(data.text)
        return result

    def get_readability(self, data: DataModel):
        result = self.readability(data.text)
        return result
