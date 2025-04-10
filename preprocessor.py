import spacy
import re

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    doc = nlp(text)
    clean_tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(clean_tokens)
