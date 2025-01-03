from collections import Counter
import re

def generate_stylometric_info(text):
    words = re.findall(r"\b\w+\b", text)
    num_words = len(words)
    num_chars = len(text)
    word_frequencies = Counter(words)
    return {
        "Number of words": num_words,
        "Number of characters": num_chars,
        "Word frequencies": word_frequencies
    }