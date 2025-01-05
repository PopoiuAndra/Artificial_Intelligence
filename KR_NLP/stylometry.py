from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import nltk

# Asigură-te că resursele NLTK sunt descărcate
nltk.download('punkt')

def generate_stylometric_info(text):
    # Tokenizarea cu NLTK
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    
    # Numărul total de cuvinte și caractere
    num_words = len(words)
    num_chars = len(text)
    num_sentences = len(sentences)
    
    # Frecvența cuvintelor
    word_frequencies = FreqDist(words)
    
    # Lungimea medie a cuvintelor și propozițiilor
    avg_word_length = sum(len(word) for word in words) / num_words if num_words > 0 else 0
    avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
    
    return {
        "Number of words": num_words,
        "Number of characters": num_chars,
        "Number of sentences": num_sentences,
        "Average word length": avg_word_length,
        "Average sentence length": avg_sentence_length,
        "Word frequencies": word_frequencies
    }