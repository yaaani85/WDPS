import trident
import json

entity_dict = {"PERSON": ["Q5"], 
                "GPE":["Q6256", "Q515", "Q7275"], 
                "NORP":["Q231002", "Q25098967", "Q17022266"], 
                "FAC":["Q41176", "Q811979"], 
                "ORG":["Q17197366", "Q43229"], 
                "PRODUCT":["Q488383","Q42889","Q2095"], 
                "EVENT":["Q1656682","Q6823473", "Q1190554"], 
                "WORK_OF_ART":["Q838948"], 
                "LAW":["Q7748"], 
                "LANGUAGE":["Q4536530"]}

class MyTrident:
    def __init__(self):
        KBPATH='assets/wikidata-20200203-truthy-uri-tridentdb'
        self.db = trident.Db(KBPATH)

  
    # Load the KB
    def query(self, entity, entity_type):
        typelist = entity_dict[entity_type]
        entity_set = set(entity)
        resultlist = []
        for type in typelist:
            q="PREFIX wde: <http://www.wikidata.org/entity/> "\
            "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "\
            "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "\
            "select * where { ?s wdp:P31 wde:%s . }" % type

            results = self.db.sparql(q)
            json_results = json.loads(results)            
            results = json_results["results"]
            intermediate_result = [b['s']["value"] for b in results["bindings"]]
            resultlist.extend(intermediate_result)

            

        
        set_data = set(resultlist)
        intersection = set_data.intersection(entity_set)
            
        return intersection
