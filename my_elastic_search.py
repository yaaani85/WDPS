import requests
import json
from elasticsearch import Elasticsearch

class MyElasticsearch():
    """ This class is a wrapper around Elasticsearch, the functions make querying elasticsearch more intuative"""

    def get_descriptions(self, query, entity_type):        
        QUERY = str(query)

        size = 100 if entity_type == ("GPE" or "LOC")  else 10
            
        e = Elasticsearch()
        p = { "query" : { "query_string" : { "query" : query }}}
        response = e.search(index="wikidata_en", body=json.dumps(p),  size=size)
        id_labels = {}
        if response:
            
            for hit in response['hits']['hits']:
                try:
                    label = hit['_source']['schema_description']
                    id = hit['_id']
                    id_labels.setdefault(id, set()).add(label)
                except:
                    continue
                    
        return id_labels

    def get_titles(self, query, entity_type):
        QUERY = str(query)

        size = 100 if entity_type == ("GPE" or "LOC")  else 10
            
        e = Elasticsearch()
        p = { "query" : { "query_string" : { "query" : query }}}
        response = e.search(index="wikidata_en", body=json.dumps(p),  size=size)
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
