import requests
import json
from elasticsearch import Elasticsearch

def search(query):
    e = Elasticsearch()
    p = { "query" : { "query_string" : { "query" : query }}}
    response = e.search(index="wikidata_en", body=json.dumps(p),  size=10)
    id_labels = {}
    if response:
        
        for hit in response['hits']['hits']:
            try:
                label = hit['_source']['schema_name']
                id = hit['_id']
                id_labels.setdefault(id, set()).add(label)
            except:
                continue

    return id_labels

if __name__ == '__main__':
    import sys
    try:
        _, QUERY = sys.argv
    except Exception as e:
        QUERY = 'Lady Gaga'

    for entity, labels in search(QUERY).items():
        print(entity, labels)
