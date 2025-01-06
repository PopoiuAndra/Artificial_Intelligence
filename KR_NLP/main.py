# main.py
from text_processing import read_text
from language_detection import detect_language
from stylometry import generate_stylometric_info
from text_transformation import generate_alternative_texts, reconstruct_original_sentence_spacy_v2
from keyword_extraction import extract_keywords_and_generate_sentences

def main():
    # Citește textul de la linia de comandă sau dintr-un fișier
    text = read_text("input.txt")
    print ("\nOriginal Text: ", text, "\n")
    
    # Identifică limba textului
    language = detect_language(text)
    print(f"Language detected: {language}", "\n")

    # Analiza stilometrică
    stylometry_info = generate_stylometric_info(text)
    print("Stylometric Information:", stylometry_info, "\n")

    # Generare texte alternative
    alternative_texts = generate_alternative_texts(text)
    print("Alternative Texts:\n")
    ct = 1
    for alternative_text in alternative_texts:
        print("Version ", ct, " ", reconstruct_original_sentence_spacy_v2(alternative_text, text), "\n")
        keyword_sentences = extract_keywords_and_generate_sentences(alternative_text)
        print("\nGenerated Sentences:")
        for sentence_info in keyword_sentences:
            print(f"\nKeyword: {sentence_info['keyword']}")
            print(f"Original context: {sentence_info['original_context']}")
            print(f"Generated sentence: {sentence_info['generated_sentence']}\n\n")
        ct += 1

if __name__ == "__main__":
    main()