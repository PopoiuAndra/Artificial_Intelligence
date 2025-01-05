# main.py
from text_processing import read_text
from language_detection import detect_language
from stylometry import generate_stylometric_info
from text_transformation import generate_alternative_texts, reconstruct_original_sentence_spacy_v2
#from keyword_extraction import extract_keywords_and_generate_sentences

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
    ct = 1
    for alternative_text in alternative_texts:
        print("Version ", ct, " ", reconstruct_original_sentence_spacy_v2(alternative_text, text))
        ct += 1

    # Extragere cuvinte cheie și generare propoziții
    #keyword_sentences = extract_keywords_and_generate_sentences(text)
    print("Generated Sentences:")
    #for sentence in keyword_sentences:
     #   print(sentence)

if __name__ == "__main__":
    main()