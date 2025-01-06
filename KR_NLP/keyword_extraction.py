import yake
from nltk.tokenize import sent_tokenize
import wn
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy

wn.download('omw-ro')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def get_word_definition(word, sentence):
    synsets = wn.Wordnet('omw-ro').synsets(word)
    if synsets:
        return synsets[0].definition()
    return None

nlp = spacy.load("ro_core_news_sm")

def generate_contextual_sentence(keyword, original_sentence, definition):
    doc = nlp(original_sentence)
    
    # Find the keyword in the sentence
    keyword_token = None
    for token in doc:
        if token.text.lower() == keyword.lower():
            keyword_token = token
            break
    
    if not keyword_token:
        return f"În contextul dat, cuvântul {keyword} este utilizat astfel: '{original_sentence}'"

    if keyword_token:
        # Handle different parts of speech
        if keyword_token.pos_ in ['NOUN', 'PROPN']:
            if definition:
                # Create a clean sentence focusing on the definition
                return f"{keyword.capitalize()}, în contextul dat, reprezintă {definition}"
            else:
                # Get only relevant modifiers
                modifiers = [t.text for t in keyword_token.children 
                           if t.dep_ in ['amod', 'nummod', 'det']]
                if modifiers:
                    return f"{keyword.capitalize()} este {' '.join(modifiers)} în acest context."
                return f"{keyword.capitalize()} apare ca element principal în acest context."
        
        elif keyword_token.pos_ == 'VERB':
            subject = next((t for t in doc if t.dep_ == 'nsubj' and t.head == keyword_token), None)
            objects = [t for t in doc if t.dep_ in ['dobj', 'iobj'] and t.head == keyword_token]
            
            if definition:
                # Create a clean sentence with the verb definition
                return f"Verbul {keyword} are sensul de {definition} în acest context."
            else:
                if subject and objects:
                    # Create a clean sentence with subject and objects
                    object_text = ' '.join(obj.text for obj in objects)
                    return f"{subject.text.capitalize()} {keyword} {object_text}."
                return f"Acțiunea {keyword} este realizată în acest context."
        
        elif keyword_token.pos_ == 'ADJ':
            noun = keyword_token.head
            if definition:
                return f"Adjectivul {keyword}, care înseamnă {definition}, descrie {noun.text}."
            else:
                return f"În acest context, {noun.text} este caracterizat ca fiind {keyword}."
        
        elif keyword_token.pos_ == 'ADV':
            modified_verb = keyword_token.head
            if definition:
                return f"Adverbul {keyword}, cu sensul de {definition}, modifică acțiunea {modified_verb.text}."
            else:
                return f"În acest context, acțiunea {modified_verb.text} este modificată de adverbul {keyword}."
    
    # Fallback that ensures a clean ending
    if definition:
        return f"În acest context, {keyword} are sensul de {definition}."
    return f"Cuvântul {keyword} este utilizat în contextul: '{original_sentence}'."


def extract_keywords_and_generate_sentences(text):
    # Configure YAKE for keyword extraction
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
    generated_sentences = []
    
    for keyword, _ in keywords:
        # Find a sentence containing the keyword
        relevant_sentence = next(
            (sentence for sentence in sentences if keyword.lower() in sentence.lower()), 
            None
        )

        if relevant_sentence:
            # Get the definition (keeping your existing functionality)
            definition = get_word_definition(keyword, relevant_sentence)
            
            # Generate a new contextual sentence
            new_sentence = generate_contextual_sentence(keyword, relevant_sentence, definition)
            generated_sentences.append({
                'keyword': keyword,
                'original_context': relevant_sentence,
                'generated_sentence': new_sentence
            })
    
    return generated_sentences 