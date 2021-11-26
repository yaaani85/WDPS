from my_trident import MyTrident
# import gensim.downloader as api
# # from gensim.models import KeyedVectors
# # try:
# #     word_vectors = KeyedVectors.load("myvectormodel")
# # except:    
# #     word_vectors = api.load('glove-wiki-gigaword-300')
# #     word_vectors.save("myvectormodel")
my_trident = MyTrident()

TYPENAME = "WARC-Type"
KEYNAME = "WARC-TREC-ID"


is_entity_spacy = {"PERSON": my_trident.is_person,
                "GPE": my_trident.is_gpe,
                "NORP": my_trident.is_norp,
                "FAC":my_trident.is_fac,
                "ORG":my_trident.is_org,
                "PRODUCT":my_trident.is_product,
                "EVENT":my_trident.is_event,
                "WORK_OF_ART":my_trident.is_work_of_art,
                "LAW":my_trident.is_law,
                "LANGUAGE":my_trident.is_language}


is_entity = {"PERSON": my_trident.is_person,
                    "ORG":my_trident.is_org,
                    "FAC":my_trident.is_fac,
                    "GPE":my_trident.is_gpe,
                    "WORK_OF_ART":my_trident.is_work_of_art,
                    "PRODUCT":my_trident.is_product,
                    "EVENT":my_trident.is_event,
                    "LOC":my_trident.is_location,
                    "LAW":my_trident.is_law, 
                    "LANGUAGE":my_trident.is_language,
                    "NORP": my_trident.is_norp}


entity_type_to_words = {"PERSON": ["person"],
                        "ORG":["organization", "company", "business"],
                        "GPE":["city", "state", "country"],
                        "WORK_OF_ART":["painting", "art", "book"],
                        "EVENT":["event"],
                        "LOC":["location"],
                        "LAW":["law"],
                        "LANGUAGE":["language"],
                        "NORP":["religious", "political", "organization"],
                        "PRODUCT":["product"],
                        "FAC":["building", "architectural"]                           
                            
                            }

def get_entity_score(entity_type, wikidata_id):
    
    score = is_entity[entity_type](wikidata_id)
    return score

# def get_description_similarity(description,label, entity, entity_type):
    
#     entity_type_in_words = entity_type_to_words[entity_type]
#     entities = entity.split()
    
#     sentence1 = entity_type_in_words + entities
#     clean1 = [word.lower() for word in sentence1 if word in word_vectors.index_to_key]
#     sentence2 = next(iter(description)).split() + next(iter(label)).split() 
#     clean2 = [word.lower() for word in sentence2 if word in word_vectors.index_to_key]
#     return word_vectors.n_similarity(clean1, clean2)

    






def get_key_and_type(payload):
    key = None
    for line in payload.splitlines():       
        if line.startswith(TYPENAME):
            doc_type =  line.split(': ')[1]
            valid_doc_type = True if doc_type == 'response' else False              
            
        
        elif line.startswith(KEYNAME):
            key = line.split(': ')[1]
            
            return key, valid_doc_type

    return key, valid_doc_type


