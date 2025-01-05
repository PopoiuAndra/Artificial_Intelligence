import requests
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

nlp = spacy.load("ro_core_news_sm")  

# Descărcare fișier WordNet JSON
def download_wordnet(url, save_path="rown-3.0.json"):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Fișierul WordNet a fost descărcat și salvat la {save_path}")
    else:
        print(f"Eroare la descărcarea fișierului: {response.status_code}")

# Încarcă WordNet-ul românesc din fișier JSON
def load_wordnet(json_file):
    with open(json_file, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

# Obține toate cuvintele din WordNet
def list_all_words(wordnet_data):
    words = set()
    entries = wordnet_data.get("@graph", [])
    for entry in entries:
        if "entry" in entry:
            for word_entry in entry["entry"]:
                words.add(word_entry["lemma"]["writtenForm"])
    return words

# Obține gloss-ul pentru un synsetRef
def get_gloss_for_synset(synset_id, wordnet_data):
    for sub_entry in wordnet_data["@graph"]:
        if "synset" in sub_entry:  # Check for the synset in sub-entry
            for entry in sub_entry["synset"]:
                    if entry["@id"] == synset_id:
                        definitions = entry.get("definition", [])
                        return " ".join(d["gloss"] for d in definitions)
    return []

def get_id_for_word(word, wordnet_data):
    entries = wordnet_data.get("@graph", [])
    for entry in entries:
        if "entry" in entry:
            for word_entry in entry["entry"]:
                if "lemma" in word_entry:
                    if "writtenForm" in word_entry["lemma"] and word_entry["lemma"]["writtenForm"] == word:
                        if "sense" in word_entry:
                            for sense in word_entry["sense"]:
                                return sense["synsetRef"]
    return []

# Disambiguate the sense of a word based on context
def disambiguate_sense(word, sentence, wordnet_data):
    entries = wordnet_data.get("@graph", [])
    doc = nlp(sentence)
    context = " ".join([token.lemma_ for token in doc])

    synset_ids = set()
    for entry in entries:
        if "entry" in entry:
            for word_entry in entry["entry"]:
                if word_entry["lemma"]["writtenForm"] == word:
                    for sense in word_entry.get("sense", []):
                        synset_ids.add(sense["synsetRef"])

    if not synset_ids:
        return []

    ##print("\nsynset_ids ", synset_ids)
    vectorizer = TfidfVectorizer()
    glosses = [get_gloss_for_synset(synset_id, wordnet_data) for synset_id in synset_ids]
    glosses = [g for g in glosses if g]
    if not glosses:
        return []

    vectors = vectorizer.fit_transform([context] + glosses)
    #print("vectors ", vectors, "After")
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    best_index = similarities.argmax()

     # != original word synset id 
    ##print("word", word, get_id_for_word(word, wordnet_data))
    if list(synset_ids)[best_index] != get_id_for_word(word, wordnet_data):
        return list(synset_ids)[best_index] 
    else :
        if len(synset_ids) > 1:
            return list(synset_ids)[best_index - 1]
        else:
            return list(synset_ids)[best_index]

# Găsește relațiile pentru un cuvânt dat în formă normală
def get_relations(word, wordnet_data):
    entries = wordnet_data.get("@graph", [])
    relations = []
    synset_ids = set()

    # Găsește synsetRef pentru cuvânt
    for entry in entries:
        if "entry" in entry:
            #print("In entry")
            for word_entry in entry["entry"]:
                if word_entry["lemma"]["writtenForm"] == word:
                    #print("In word_entry ", word_entry["lemma"]["writtenForm"])
                    for sense in word_entry.get("sense", []):
                        #print("In sense ", sense["synsetRef"])
                        synset_ids.add(sense["synsetRef"])

    if synset_ids == []:
        return []
    ##print("\nsynset_ids ", synset_ids)
    # Găsește relațiile pentru fiecare synsetRef
    for synset_id in synset_ids:
        for entry in entries:
            if "synset" in entry:    
                for word_entry in entry["synset"]:
                    if word_entry["@id"] == synset_id:
                       #print("In word_entry2 ", word_entry["@id"])
                       if "relations" in word_entry:
                            for relation in word_entry["relations"]:
                                    #print("In relation ", relation["relType"], " ", relation["target"])
                                    # search for the target word in the entry
                                    if relation["relType"] == "hyponym":
                                        for entry2 in entries:
                                            if "entry" in entry2:
                                                for word_entry2 in entry2["entry"]:
                                                    if "sense" in word_entry2:
                                                        ceva = word_entry2["sense"]
                                                        for i in ceva:
                                                            #print("In word_entry2 sense synsetRef ", i["synsetRef"])
                                                            if i["synsetRef"] == relation["target"]:
                                                                #print("In word_entry2 sense synsetRef target", word_entry2["lemma"]["writtenForm"])
                                                                relations.append( word_entry2["lemma"]["writtenForm"])
    return relations

# Găsește sinonimele pentru un cuvânt
def get_synonyms(word, wordnet_data):
    entries = wordnet_data.get("@graph", [])
    synonyms = []

    # Găsește synsetRef pentru cuvânt
    synset_ids = set()
    for entry in entries:
        if "entry" in entry:
            for word_entry in entry["entry"]:
                if word_entry["lemma"]["writtenForm"] == word:
                    for sense in word_entry.get("sense", []):
                        synset_ids.add(sense["synsetRef"])

    # Găsește sinonimele din același synset
    for synset_id in synset_ids:
        for entry in entries:
            if entry.get("@id") == synset_id:
                for related_entry in entries:
                    if "entry" in related_entry:
                        for word_entry in related_entry["entry"]:
                            for sense in word_entry.get("sense", []):
                                if sense["synsetRef"] == synset_id and word_entry["lemma"]["writtenForm"] != word:
                                    synonyms.append(word_entry["lemma"]["writtenForm"])
    return list(set(synonyms))

def get_written_form_by_synset(synset_ref, wordnet_data):
    for entry in wordnet_data.get("@graph", []):
        if "entry" in entry:  # Focus only on entries with the 'entry' key
            for word_entry in entry["entry"]:
                if "sense" in word_entry:
                    # Check if any sense matches the given synsetRef
                    for sense in word_entry["sense"]:
                        if sense.get("synsetRef") == synset_ref:
                            return (word_entry["lemma"]["writtenForm"])
    return []

# Generează propoziții alternative
def generate_alternative_sentences(sentence, wordnet_data, replacement_ratio=0.2):
    words = sentence.split()
    num_replacements = max(1, int(len(words) * replacement_ratio))  # Cel puțin un cuvânt de înlocuit
    
    # Selectează cuvintele care vor fi înlocuite
    words_to_replace = words.copy()
    alternative_sentence = words.copy()
    
    for i, word in enumerate(words):
        if word in words_to_replace:
            # Caută alternative în WordNet
            alternatives = get_relations(word, wordnet_data)
            ##print("Alternatives for ", word, " ", alternatives)
            alternatives = disambiguate_sense(word, sentence, wordnet_data)
            ##print("Alternatives for ", word, " ", alternatives)
            if alternatives.count(word) > 0:
                alternatives.remove(word)
            if alternatives:
                alternative_sentence[i] =  get_written_form_by_synset(alternatives, wordnet_data)
    
    return " ".join(alternative_sentence)


def reconstruct_original_sentence_spacy(lemmatized_sentence, original_sentence):
    # Process both sentences using SpaCy
    original_doc = nlp(original_sentence)
    lemmatized_doc = nlp(lemmatized_sentence)

    # Create a mapping from lemmatized tokens to their original tokens
    lemma_to_original = {}
    for orig_token in original_doc:
        if orig_token.lemma_ not in lemma_to_original:
            lemma_to_original[orig_token.lemma_] = orig_token.text

    # Reconstruct the sentence by mapping lemmatized tokens back to original tokens
    reconstructed_tokens = [
        lemma_to_original.get(token.lemma_, token.text) for token in lemmatized_doc
    ]
    return " ".join(reconstructed_tokens)

def reconstruct_original_sentence_spacy_v2(lemmatized_sentence, original_sentence):
    # Curățăm propoziția lematizată (eliminăm parantezele [] și _)
    lemmatized_sentence = lemmatized_sentence.replace("[", "").replace("]", "").replace("_", " ")

    # Analizăm propozițiile originale și lematizate
    original_doc = nlp(original_sentence)
    lemmatized_doc = nlp(lemmatized_sentence)
    
    # Creăm o hartă între tokenii originali și lematizați
    lemma_to_original = {}
    for orig_token in original_doc:
        lemma_key = orig_token.lemma_
        
        # Dacă cuvântul este reflexiv (ex. "se află"), combină-l corect
        if orig_token.morph.get("Reflex") == "Yes" and orig_token.dep_ in {"aux", "expl"}:
            lemma_key = f"[se] {lemma_key}"

        # Adăugăm token-ul în hartă
        lemma_to_original[lemma_key] = orig_token.text
    
    # Reconstruim propoziția ținând cont de morfologia cuvintelor
    reconstructed_tokens = []
    for lem_token in lemmatized_doc:
        # Verificăm forma corectă pe baza morfologiei
        lemma_key = lem_token.lemma_
        
        # Dacă cuvântul este reflexiv (ex. "se află"), combină-l corect
        if lem_token.morph.get("Reflex") == "Yes" and lem_token.dep_ in {"aux", "expl"}:
            lemma_key = f"[se] {lemma_key}"
        
        # Verifică morfologia pentru a păstra forma corectă (ex. caz genitiv: "dascălului")
        if lemma_key in lemma_to_original:
            # Verifică dacă există forma morfologică (caz, genitiv, etc.)
            morph_info = lem_token.morph
            original_word = lemma_to_original[lemma_key]
            ##print("Original word: ", original_word)
            ##print("Morph info: ", morph_info)
            
            # Dacă cuvântul original are o formă diferită din cauza cazului, păstrează forma corectă
            if morph_info.get("Case"):
                case = morph_info.get("Case")
                if case == "Gen":
                    # Dacă cuvântul este în genitiv, asigură-te că ai forma corectă
                    reconstructed_tokens.append(original_word + "ului")  # Adăugăm sufixul de genitiv
                else:
                    reconstructed_tokens.append(original_word)
            else:
                reconstructed_tokens.append(original_word)
        else:
            reconstructed_tokens.append(lem_token.text)
    
    # Îmbinăm cuvintele reconstruit
    reconstructed_sentence = " ".join(reconstructed_tokens)
    
    # Returnăm propoziția reconstruită
    return reconstructed_sentence

def generate_alternative_texts(text):
    # Load the Romanian model  

    # URL-ul WordNet
    wordnet_url = "https://www.racai.ro/p/llod/resources/rown-3.0.json"
    wordnet_file = "rown-3.0.json"

    # Descărcare și încărcare WordNet
    #try:
    #    download_wordnet(wordnet_url, wordnet_file)
    #except Exception as e:
    #    print(f"Eroare la descărcare: {e}")

    wordnet_data = load_wordnet(wordnet_file)

    # Testăm propozițiile alternative
    
    #text = "Elevii răspund solicitărilor profesorului, cer lămuriri și participă activ la lecții. Este important să existe un dialog între profesor și elevi pentru a facilita învățarea."
    #alternative_text = generate_alternative_sentences(text, wordnet_data)
    #print("Original:", text)
    #print("Alternativă:", alternative_text)
    # Test sentence
    doc = nlp("Elevii răspund solicitărilor profesorului, cer lămuriri și participă activ la lecții. Este important să existe un dialog între profesor și elevi pentru a facilita învățarea.")
    #make doc lower case
    doc = nlp(text.lower())
    #print("Lemmatized words:", [token.lemma_ for token in doc])
    text = ""
    for token in doc:
        text += token.lemma_ + " "
    #print("Text lematizat:", text)
    new_text = generate_alternative_sentences(text, wordnet_data)
    #print("Text lematizat alternativ:", new_text)
    return new_text

    #print("Propozitie originala: ", base_text)
    #print("Reconstructie propozitie: ", reconstruct_original_sentence_spacy(new_text, base_text))
    #print("Reconstructie propozitie v2: ", reconstruct_original_sentence_spacy_v2(new_text, base_text))
     