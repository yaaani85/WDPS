import gzip
from parser import Parser
from entity_recognition import Named_Entity_Recognition
from my_elastic_search import MyElasticsearch
from utils import (
   
    get_key_and_type,
    get_entity_score,

)
import time
from multiprocessing import Pool
from threading import Thread


start_time = time.time()
parser = Parser()
elastic_search = MyElasticsearch()
named_entity_recognition = Named_Entity_Recognition()

result = {}
HTML_TAG = "<!DOCTYPE html"
ENTITY_BLACKLIST = [
    "DATE",
    "TIME",
    "PERCENT",
    "MONEY",
    "QUANTITY",
    "ORDINAL",
    "CARDINAL",
]
# The goal of this function process the webpage and returns a list of labels -> entity ID
def find_labels(payload):
    if not payload:
        return
    # The variable payload contains the source code of a webpage and some additional meta-data.
    # We firt retrieve the ID of the webpage, which is indicated in a line that starts with KEYNAME.
    # The ID is contained in the variable 'key'
    key = None
    # Only consider docs of type "response"
    key, valid_doc_type = get_key_and_type(payload)

    if not valid_doc_type or not key:
        return

    try:
        # Only keep the HTML response
        html = HTML_TAG + payload.split(HTML_TAG)[1]
        text = parser.trafilatura(html)

        # below combines parsers, higher recall, much lower precision
        # text2 = parser.beautiful_soup(html)
        # text = text + text2

        # keep only unique tuples (entity, entity_type)
        entities = set(named_entity_recognition.stanza(text))

        # below combines NER models, higher recall, much lower precision
        # entities_spacy = set(named_entity_recognition.spacy(text))
        # entities = set.union(entities_spacy, entities_stanza)
    except Exception as e:
        # Return when error in creating HTML or entities
        return

    for entity, entity_type in entities:
        # Entities such as 100.000Euro are not in sample annotations, thus keeping them would only hurt precision.
        if entity_type in ENTITY_BLACKLIST:
            continue

        try:
            # Only Capitalize if all lower. google -> Google. yet USA remains USA.
            entity = entity.capitalize() if entity.islower() else entity

            search_results_titles = elastic_search.get_titles(entity, entity_type)
            search_results_descriptions = elastic_search.get_descriptions(
                entity, entity_type
            )

            top_result = rank_search_results(
                search_results_titles, search_results_descriptions, entity, entity_type
            )

            yield key, entity, top_result

        except Exception as e:
            continue


def rank_search_results(
    search_results_titles, search_results_descriptions, entity, entity_type
):
    ranking = []
    for wikidata_id, label in search_results_titles.items():
        score = 0

        try:
            score = get_entity_score(entity_type, wikidata_id)
        except Exception as e:
            # if no score can be calculated, the assumtption is that the wikidata_id is non-useful, thus score 0
            score = 0

        if label == entity:
            # quite often the name is exactly the same as the entity label, therefore a small bonus if they match
            score += 0.3
        else:
            try:
                score += 0  # solely for docker, runs locally
                # score += get_description_similarity(search_results_descriptions[wikidata_id], label, entity, entity_type)
            except Exception as e:
                # if there is an error it could be due to the fact that entity+entity type both were not found in gensim dict.
                # giving a zero score is considered too much of a punishment.
                score += 0.3

        ranking.append((wikidata_id, score))

    # return highest rank
    sorted_ranking = sorted(ranking, key=lambda x: (-x[1], x[0]))
    wikidata_id, _ = sorted_ranking[0]
    return wikidata_id


def split_records(stream):
    payload = ""
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ""
        else:
            payload += line
    yield payload


if __name__ == "__main__":
    import sys

    try:
        _, INPUT = sys.argv
    except Exception as e:
        print("Usage: python starter-code.py INPUT")
        sys.exit(0)

    with gzip.open(INPUT, "rt", errors="ignore") as fo:
        for record in split_records(fo):
            for key, label, wikidata_id in find_labels(record):
                print(key + "\t" + label + "\t" + wikidata_id)
# TODO allow for different parsers/NER/etc
