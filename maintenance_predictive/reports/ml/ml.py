# reports/ml/ml.py

import os
import re
import string
import joblib
import spacy
from django.conf import settings

# Chargement du modèle spaCy (français)
nlp = spacy.load("fr_core_news_lg")
stop_words = nlp.Defaults.stop_words

# Chemins vers les fichiers
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'logistic_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'tfidf_vectorizer.pkl')

# Chargement unique du modèle et du vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def nettoyer_texte(text):
    """
    Nettoyage, lemmatisation, suppression de ponctuation et stopwords.
    """
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if token.lemma_ not in stop_words and not token.is_space and token.is_alpha
    ]
    return " ".join(tokens)

def predict_score(text):
    """
    Prédit la criticité (score) d’un texte après nettoyage et vectorisation.
    """
    cleaned_text = nettoyer_texte(text)
    X = vectorizer.transform([cleaned_text])
    return model.predict_proba(X)[0][1]
