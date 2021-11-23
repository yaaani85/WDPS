import gzip
from bs4 import BeautifulSoup, Comment
import re
import spacy
from my_elastic_search import search
import justext
import html2text
import trafilatura
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from my_trident import MyTrident
myTrident = MyTrident()

is_entity = {"PERSON": myTrident.is_person,
                "GPE": myTrident.is_gpe,
                "NORP": myTrident.is_norp,
                "FAC":myTrident.is_fac,
                "ORG":myTrident.is_org,
                "PRODUCT":myTrident.is_product,
                "EVENT":myTrident.is_event,
                "WORK_OF_ART":myTrident.is_work_of_art,
                "LAW":myTrident.is_law,
                "LANGUAGE":myTrident.is_language}

st = StanfordNERTagger(  "/home/yannick/WDPS/assignment-code/assignment/assets/stanford-ner-2020-11-17/classifiers/english.muc.7class.distsim.crf.ser.gz",
					   "/home/yannick/WDPS/assignment-code/assignment/assets/stanford-ner-2020-11-17/stanford-ner.jar",
					   encoding='utf-8')
nlp = spacy.load("en_core_web_lg")
result = {}
KEYNAME = "WARC-TREC-ID"
TYPENAME = "WARC-Type"
HTML_TAG = "<!DOCTYPE html"
ENTITY_BLACKLIST = ["DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL", "PERSON"]
# The goal of this function process the webpage and returns a list of labels -> entity ID


def find_labels(payload):
    if payload == '':
        return
    # The variable payload contains the source code of a webpage and some additional meta-data.
    # We firt retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
    # The ID is contained in the variable 'key'
    key = None
    
    key, valid_doc_type = get_key_and_type(payload)

    if not valid_doc_type:
        return
    
    # To match length sample_annotations.tsv
    if key == "clueweb12-0000tw-00-00093":
        quit()

    try:
        html = HTML_TAG + payload.split(HTML_TAG)[1] 
        text = parse_html_to_text(html)
        #keep only unique tuples (entity, entity_type) 
        entities = set(text_to_entities(text))   
    except Exception as e:   
        # Return when error in creating HTML or entities
        return  


    for entity, entity_type in entities:        
   
        if entity_type in ENTITY_BLACKLIST:
            continue
        try:
            entity = entity.capitalize() if entity.islower() else entity
            search_results = elastic_search(entity)  
            wikidata_id = rank_search_results(search_results, entity, entity_type)
            yield key, entity, wikidata_id
            
                
                # if match return the match
               
        
        except Exception as e:
            continue
       
    # Problem 1: The webpage is typically encoded in HTML format.
    # We should get rid of the HTML tags and retrieve the text. How can we do it?

    # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
    # entities in the text?

    # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
    # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?

    # To tackle this problem, you have access to two tools that can be useful. The first is a SPARQL engine (Trident)
    # with a local copy of Wikidata. The file "test_sparql.py" shows how you can execute SPARQL queries to retrieve
    # valuable knowledge. Please be aware that a SPARQL engine is not the best tool in case you want to lookup for
    # some strings. For this task, you can use elasticsearch, which is also installed in the docker image.
    # The file start_elasticsearch_server.sh will start the elasticsearch server while the file
    # test_elasticsearch_server.py shows how you can query the engine.

    # A simple implementation would be to first query elasticsearch to retrieve all the entities with a label
    # that is similar to the text found in the web page. Then, you can access the SPARQL engine to retrieve valuable
    # knowledge that can help you to disambiguate the entity. For instance, if you know that the webpage refers to persons
    # then you can query the knowledge base to filter out all the entities that are not persons...

    # Obviously, more sophisticated implementations that the one suggested above are more than welcome :-)
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



def parse_html_to_text(html):
    # text = dragnet.extract(html)

    text = trafilatura.extract(html)
    return text

    # other options considered less optimal:    
    #return parse_justtext(html)
    #return parse_beautiful_soup(html)

  
       


def parse_justtext(html):  
    text = ""
    paragraphs = justext.justext(html, justext.get_stoplist("English"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            text += paragraph.text
            
     
    if not text:
        # print("no text found")
        Exception("No text")

    return text

def parse_beautiful_soup(html):
    
    soup = BeautifulSoup(html, 'html.parser')

    # Try more advanced techniques here.   
    for data in soup(['style', 'script','aside', 'footer']):
        # Remove tags
        data.extract()
  
    # return data by retrieving the tag content
    text =  " ".join(re.split(r'[\n\t]+', soup.get_text())).replace(".", "")


    return text

def text_to_entities(text):
    # Both methods work, spacy seems better. Foramlly test both taggers. 
    # spacy
    document = nlp(text)
    entities_and_type = [(token.text.replace("\n", " "), token.label_) for token in document.ents]  

    # try:
    #     capitlized = [(x.capitalize(), y)  if x.islower() else x for x,y in entities_and_type]
    #     return capitlized

    # except:
    # Stanford
    # tokenized_text = word_tokenize(text)
    # classified_text = st.tag(tokenized_text)
    # entities_and_type = [(x, y) for (x,y) in classified_text if y != "O"]  
    return entities_and_type



def elastic_search(entity):
    QUERY = str(entity)
    search_results =  search(QUERY).items()
    return search_results

def rank_search_results(search_results, entity, entity_type):
    ranking = []
    for wikidata_id, label in search_results:
        # is person/loc/ etc
        score = 0

        try:
            if is_entity[entity_type](wikidata_id):
                score += 1
        except:
            score += 0
        
        if label == entity:
            score += 0.5
        
        ranking.append((wikidata_id, score))
    
    # return first one
    sorted_ranking = sorted(ranking,key=lambda x:(-x[1],x[0]))
    wikidata_id, _ = sorted_ranking[0]
    return wikidata_id


def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)

    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):
            for key, label, wikidata_id in find_labels(record):
                print(key + '\t' + label + '\t' + wikidata_id)
                

