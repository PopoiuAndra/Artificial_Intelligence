# main.py
from text_processing import read_text
from language_detection import detect_language
from stylometry import generate_stylometric_info
from text_transformation import generate_alternative_texts
from keyword_extraction import extract_keywords_and_generate_sentences

def main():
    # Citește textul de la linia de comandă sau dintr-un fișier
    text = read_text("input.txt")
    
    # Identifică limba textului
    language = detect_language(text)
    print(f"Language detected: {language}")

    # Analiza stilometrică
    stylometry_info = generate_stylometric_info(text)
    print("Stylometric Information:", stylometry_info)

    # Generare texte alternative
    alternative_texts = generate_alternative_texts(text)
    print("Alternative Texts:")
    for i, alt_text in enumerate(alternative_texts):
        print(f"Version {i+1}: {alt_text}")

    # Extragere cuvinte cheie și generare propoziții
    keyword_sentences = extract_keywords_and_generate_sentences(text)
    print("Keyword Sentences:")
    for sentence in keyword_sentences:
        print(sentence)

if __name__ == "__main__":
    main()