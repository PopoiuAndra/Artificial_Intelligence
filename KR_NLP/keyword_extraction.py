import yake
from nltk.tokenize import sent_tokenize
import wn
import nltk
wn.download('omw-ro')
nltk.download('omw-1.4')

def get_word_definition(word, sentence):
    synsets = wn.Wordnet('omw-ro').synsets(word)
    if synsets:
        return synsets[0].definition()
    return None


def extract_keywords_and_generate_sentences(text):
    # Configurare YAKE pentru extragerea cuvintelor cheie
    language = "ro"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    num_keywords = 3

    kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        top=num_keywords
    )
    
    keywords = kw_extractor.extract_keywords(text)

    sentences = sent_tokenize(text)
    keyword_sentences = []

    for keyword, _ in keywords:
        # Găsește o propoziție care conține cuvântul cheie
        relevant_sentence = next(
            (sentence for sentence in sentences if keyword.lower() in sentence.lower()), 
            None
        )

        # Obține definiția și construiește o propoziție nouă
        if relevant_sentence:
            definition = get_word_definition(keyword, relevant_sentence)
            if definition:
                keyword_sentences.append(
                    f"Keyword: '{keyword}'\nContext: '{relevant_sentence}'\nDefinition: '{definition}'"
                )
            else:
                keyword_sentences.append(
                    f"Keyword: '{keyword}'\nContext: '{relevant_sentence}'\nDefinition: Not found"
                )
    return keyword_sentences