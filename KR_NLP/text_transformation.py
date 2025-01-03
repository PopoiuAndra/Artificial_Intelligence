from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
import random

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)

def generate_alternative_texts(text):
    words = text.split()
    num_to_replace = max(1, int(0.2 * len(words)))
    alternative_texts = []

    for _ in range(3):  # Generate 3 alternative versions
        new_text = words[:]
        indices = random.sample(range(len(words)), num_to_replace)
        for idx in indices:
            synonyms = list(get_synonyms(words[idx]))
            if synonyms:
                new_text[idx] = random.choice(synonyms)
        alternative_texts.append(" ".join(new_text))

    return alternative_texts
