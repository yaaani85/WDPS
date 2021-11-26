import trident
import json


class MyTrident:
    """This class is python-wrapper around the trident package"""
    
    def __init__(self):
        """Path and prefixes, I am a aware that this could be done more nicely and efficiently by having using proper sparql queries"""
        KBPATH = "assets/wikidata-20200203-truthy-uri-tridentdb"
        self._db = trident.Db(KBPATH)
        self._terms = {}
        self.prefix = (
            "PREFIX wde: <http://www.wikidata.org/entity/> "
            "PREFIX wdp: <http://www.wikidata.org/prop/direct/> "
            "PREFIX wdpn: <http://www.wikidata.org/prop/direct-normalized/> "
           
        )
        self.where = "select ?s WHERE {"
        
        self.instance_of =  " wdp:P31 wde:"
        
        self.subclass_of = "wdp:P31 ?s . ?s wdp:P279 wde:"

    def get_match(self, query):
        results = self._db.sparql(query)
        json_results = json.loads(results)
        results = json_results["results"]["bindings"]
        match = True if results else False
        return match

    def is_person(self, entity):
        # Only look for exact matches of human and fictional_persons
        human = self.prefix + self.where + entity + self.instance_of + "Q5 }"  # human
        fictional_person = self.prefix + self.where + entity + self.instance_of + "Q15632617 }"  # fictional person
        high_targets = [human, fictional_person]
        for query in high_targets:
            match = self.get_match(query)
          
            if match:
                return 5
        

        return 0

    def is_gpe(self, entity):
        # First query only city, state,country and continent to see if there are direct instance matches
        city = self.prefix + self.where + entity + self.instance_of + "Q515 }"  # city
        state = self.prefix + self.where + entity + self.instance_of + "Q7275 }"  # State
        country = self.prefix + self.where + entity + self.instance_of + "Q6256 }"  # country
        continent = self.prefix + self.where + entity + self.instance_of + "Q5107 }"  # continent

        high_targets = [city, state, country, continent]
        
        for query in high_targets:
            match = self.get_match(query)
            if match:
                return 5
      
        # if no exact match try subclass of geograpich location (Q2221906), more general, yet more noisy.
        general_query = self.prefix + self.where + entity + self.subclass_of + "Q2221906 }"
        general_result = self.get_match(general_query)
        general_result = 1 if True else 0
        return general_result

    def is_org(self, entity):
        # First look for direct instances of organization
        target = self.prefix + self.where + entity +  self.instance_of + "Q43229 }"
        match = self.get_match(target)
        if match:
            return 5
        # Subsequently, look for instances of organization like companies etc. 
        general_query = self.prefix + self.where + entity + self.subclass_of + "Q43229 }" 
        general_result = self.get_match(general_query)      
        
        return 3 if general_result else 0

    def is_fac(self, entity):
        # First look for direct instances of the following
        airport = self.prefix + self.where + entity + self.instance_of + "Q1248784 }"  # airport
        highway = self.prefix + self.where + entity + self.instance_of + "Q269949 }"  # highway
        bridge = self.prefix + self.where + entity + self.instance_of + "Q12280 }"  # bridge
        building = self.prefix + self.where + entity + self.instance_of + "Q41176 }"  # continent
        # By querying for geographic Regions City, State, Country etc .. will result in True

        high_targets = [airport, highway, bridge, building]

        for query in high_targets:
            match = self.get_match(query)
          
            if match:
                return 5

        # if no exact match try subclass of architectural structure (Q2221906)
        general_query = self.prefix + self.where + entity + self.subclass_of + "Q811979 }"
        general_result = self.get_match(general_query)
        general_result = 1 if True else 0
        return general_result

    def is_work_of_art(self, entity):
        work_of_art = self.prefix + self.where + entity + self.instance_of + "Q838948 }"  # work of art
        
        match = self.get_match(work_of_art)
          
        if match:
            return 5
        

        return 0

    def is_event(self, entity):
        # first try events,

        event = self.prefix + self.where + entity + self.instance_of + "Q1656682 }"  # event
       
        match = self.get_match(event)
          
        if match:
            return 5
        # if no match, then occurences of event
        occurence = self.prefix + self.where + entity + self.instance_of + "Q1190554 }" #occurence
        match = self.get_match(occurence)
          
        if match:
            return 3
        return 0

    def is_language(self, entity):
        language = self.prefix + self.where + entity + self.instance_of + "Q34770 }"  # language
        language2 =  self.prefix + self.where + entity + self.instance_of + "Q315 }" #language2
        
        high_targets = [language, language2]
          
        for query in high_targets:
            match = self.get_match(query)
          
            if match:
                return 5
        return 0

    def is_law(self, entity):
        law = self.prefix + self.where + entity + self.instance_of + "Q7748 }"  # law
       
        match = self.get_match(law)
          
        if match:
            return 5
        

        return 0

    def is_location(self, entity):
        location = self.prefix + self.where + entity + self.instance_of + "Q17334923 }"  
        # first look for exact matches of location
       
        match = self.get_match(location)
          
        if match:
            return 5
        # if no match look for sublcasses of geo_location
        geo_location = self.prefix + self.where + entity + self.instance_of + "Q2221906 }" #occurence
        match = self.get_match(geo_location)
          
        if match:
            return 3
        return 0

    def is_product(self, entity):
        # first look for instances of product
        product = self.prefix + self.where + entity + self.instance_of + "Q2424752 }"  # work of art
       
        match = self.get_match(product)
          
        if match:
            return 5
        # if no match search for sublcasses of goods and services 
        general_query = self.prefix + self.where + entity + self.subclass_of + "Q2897903 }" #goods and services
        general_result = self.get_match(general_query)
        general_result = 1 if True else 0
        return general_result

    def is_norp(self, entity):
        # first look for nationalities, religious, and political party
        nationalities = self.prefix + self.where + entity + self.instance_of + "Q231002 }"  # work of art
        religious = self.prefix + self.where + entity + self.instance_of + "Q2566598 }"  # religious
        political_party = self.prefix + self.where + entity + self.instance_of + "Q7278 }"  # religious
        

        high_targets = [nationalities, religious, political_party]

        for query in high_targets:
            match = self.get_match(query)
          
            if match:
                return 5
        return 0


