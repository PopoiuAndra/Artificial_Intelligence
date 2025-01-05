import requests
import json
import random

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
    print("\nsynset_ids ", synset_ids)
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
            print("Alternatives for ", word, " ", alternatives)
            if alternatives.count(word) > 0:
                alternatives.remove(word)
            if alternatives:
                alternative_sentence[i] = random.choice(alternatives)
    
    return " ".join(alternative_sentence)



# URL-ul WordNet
wordnet_url = "https://www.racai.ro/p/llod/resources/rown-3.0.json"
wordnet_file = "rown-3.0.json"

# Descărcare și încărcare WordNet
#try:
#    download_wordnet(wordnet_url, wordnet_file)
#except Exception as e:
#    print(f"Eroare la descărcare: {e}")

wordnet_data = load_wordnet(wordnet_file)

# Testăm lista de cuvinte
print("Toate cuvintele disponibile în WordNet:")
all_words = list_all_words(wordnet_data)
print("viata este in all_words:", "viață" in all_words)
print("polariza este in all_words:", "polariza" in all_words)
print("cuvinte alternative ", get_relations("viață", wordnet_data))
print("cuvinte alternative ", get_relations("polariza", wordnet_data))

# Testăm propozițiile alternative
text = "viață este frumoasă."
alternative_text = generate_alternative_sentences(text, wordnet_data)
print("Original:", text)
print("Alternativă:", alternative_text)
import spacy

# Load the Romanian model
nlp = spacy.load("ro_core_news_sm")

# Test sentence
doc = nlp("Viața este frumoasă.")
print("Lemmatized words:", [token.lemma_ for token in doc])
text = ""
for token in doc:
    text += token.lemma_ + " "
print("Text lematizat:", text)
print("Text lematizat alternativ:", generate_alternative_sentences(text, wordnet_data))