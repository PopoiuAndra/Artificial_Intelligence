from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize


def extract_keywords_and_generate_sentences(text):
    sentences = sent_tokenize(text)
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(sentences)
    keywords = vectorizer.get_feature_names_out()

    keyword_sentences = []
    for keyword in keywords:
        for sentence in sentences:
            if keyword in sentence:
                keyword_sentences.append(f"{keyword.capitalize()} - {sentence}")
                break

    return keyword_sentences
