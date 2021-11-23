import trident
import json



class MyTrident:
    def __init__(self):
        KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'
        self._db = trident.Db(KBPATH)
        self._terms = {}
  
    def is_person(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
            "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
            "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
            "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q215627 }" %entity                                        
            # By querying for Person both Human (Q5) and Fictional Person (Q15632617) will result in True    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False
            
    def is_gpe(self, entity):
        #City
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE { %s wdp:P31 wde:Q515 }" % entity                                        
        # By querying for geographic Regions City, State, Country etc .. will result in True    
        

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"] 
        return True if results else False

    def is_norp(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q41710 } UNION {wde:%s wdp:P31 ?s . ?s wdp:P279 wde:Q7210356} UNION {wde:%s wdp:P31 ?s . ?s wdp:P279 wde:Q7257}" %entity                                        
        # By querying for Ethnic Groups, Political Organizations and Ideology we strive to capture all NORP 
        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False
        
    def is_fac(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q811979 }" %entity                                        
        # By querying for architectural structure, highways, airports etc .. will result in True    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False


    def is_org(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q17197366 }" %entity                                        
        # By querying for type of organizaion companies agencies and institions will result in True    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False


    def is_product(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q488383 }" %entity                                        
        # By querying for type of organizaion companies agencies and institions will result in True    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False

    def is_event(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q1190554 }" %entity                                        
        # By querying for occurences we hope to capture all events, festival, wars    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False
        

    def is_work_of_art(self,entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 ?s . ?s wdp:P279 wde:Q15621286 }" %entity                                        
        # By querying for intelectual work we hope to capture all creative WOA and songs etc    

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False


    def is_language(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 wde:Q4536530 }" %entity                                        
        # In this case we query specific for language as the sublcasses are less informative

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False


    def is_law(self, entity):
        q="PREFIX wde: <http://www.wikidata.org/entity/> "\
        "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
        "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
        "select ?s WHERE {%s wdp:P31 wde:Q7748 }" %entity                                        
        # In this case we query specific for law as the sublcasses are less informative

        results = self._db.sparql(q)
        json_results = json.loads(results)            
        results = json_results["results"]["bindings"]        
        return True if results else False


    def lookup(self, term):
        if term not in self._terms:
            self._terms[term] = self._db.search_id(term)
        return self._terms[term]
    
    def contents_of_subject(self, term):
        return self.db.po(self.lookup(term))

    def indegree_of_subject(self, term):
        return self.db.indegree(self.lookup(term))



# id_of_test = handler.lookup("test")
# contents_of_subject = handler.contents_of_subject("test")
# indegree_of_subject = handler.indegree_of_subject("test")
