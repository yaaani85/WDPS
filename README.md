# Entity Linker (WDPS, 2021)
This repository comprises an Entity Linker application written in Python. It uses several external libraries such as Stanza, Spacy and Trafilatura. 
The codebases consists of a main.py and three classes: my_elastic_search.py, my_trident.py and parser.py. Furthermore the application uses utils.py for helper functions. 

## Setup Instructions 
Please clone this git repo to the local machine. (assets and data are in the .gitignore, so please add those folders)


## To build a new image 
(on top of karmaresearch/wdps_assignment, with additional requirements installed)

Go to the git repo on local machine and run the following: 

```bash
docker build . --tag=submission --load
```
```bash
docker run -ti -v <path-to-git-submission-and-data>:/app/assignment -p 9200:9200 submission
```
I initally planned to create a new docker image, however I could not get in my docker account. Please let me know if you prefer this, then I will fix this asap! (although above option should work fine)

## Things to consider
The following issues are a dependent per host machine, but are nothing new to you so this should not give any issues. 
vm.max_map_count [65530]
sudo chmod -c 0777 -R .
chmod +x ./start_elasticsearch_server.sh

Stanza.download() (line 5 in entity_recognition.py ) is required only the first time. 
However this slows down the program. So if you want to rerun the program please comment this line out. 

Besides that everyting runs in the docker-container (tested) and should give no issues. Please contact us if it does. 

In order to run the program with evaluation, nothing has changed, and is still: 

```bash
./run_example.sh
```


# Project Report 

The task is splitted in the following parts: (1) Parsing HTML to plain text. (2) Named Entity-Recognition (3) Elastic-Search (4) Ranking Search Results
Below the findings/descisions of every part will be discussed shortly.

## Parsing HTML to plain text
This step seems to be trivial, however this step is as crucial as the other steps. Namely, when too little text is parsed, the NER models are missing potential entities.
On the other hand if too much text is parsed the NER models will create wrong entities. One can observe this is in the annotations.tsv file where entities as "Adobe Flash Player" and "WordPress" are parsed. Naturally, if the page is about Adobe Flash player it is an enitity. However, in the first 5 files the text is about totally different topics, this is probabaly due to the fact that in a small div some text was present like "Adobe Flash Player required".

The following parsers have been considere in this study: BeautifulSoup, Trafilatura, Justext.
BeautifoulSoup is the first option to explore and it parses base on a set of rules (e.g. all text in <p> and <div>). However, during visual inspection it proved to be hard to only keep the useful text. Too much useless text was parsed, leading to wrong entities.  

Trafilatura and Justext are python packages which probably parse with the same packages as with beautifulSoup is built-up on, however they were leading to way better results. This is no surpise as for example Justext is the result of an entire PHD thesis. Naturally, they have optimized the set of rules to only keep the relevant text. 

Based on visual inspection trafilatura gave the best results and is therefore used in this study. Furthermore, one could consider a model based approach like DragNet. Or combining multiple parsers. 

## Named Entity-Recognition
NER is Another crucial step in the pipeline, missing or misclassifyng the entitiy (either by name or type) can lead to severe problems further in the pipeline. 
In this study two NER models are considered. The place to start is Spacy, an open source python library for NER. Although the results proved to be decent, the results were not flawless as a lot of entities were missed. 
Therefore, Stanza (the NER model from stanford) was also considered. And this led to better results. More entities were captured, and it led to a better performance overall. 

## Elastic-Search 
Elastic-search in this study is used to query both the title and description based on the search result.
There is not much to tweak in this part of the pipeline, however there is one important factor, namely, the size of the returned results. 
If you increase it too much the ranking becomes unnecessary complex. However, if the size is too small you might miss correct result (e.g. The true page about Berlin shows up at place 20, when querying "Berlin"))
In this study, the search size is increased greatly for GPE (city, state, country) entities as they are easy to disambiguate based on checking if they are an instance of either city, state or country. 

## Ranking Search Results
The following strategy is used in order to create a ranking system from scratch. For every Entity Type a different trident function is called. (e.g. Type = person --> my_trident.is_person)
This function gives 5 points if a match should drastically disambiguate the results. These 5 points are only given if they are direct instances. For example if an entity is Paris and their is a wikipediaID which is an instance of city this wikipedia_id gets 5 points. 
The reasoning behind this is that if the entity is already classifed as a city the most often needed entity is the one of the city paris itself. 
Subsequently, if they are a subclass of (in the case of type is GPE) geograpichal area the respective result gets three points, because a match could be useful however it could aslo be non-informative. 

Finally, if there is a tie, for example if more than one result which has the property isHuman (Q5) a similarity score is calculated between (entity + entityType) and (title + description).
The rationale behind this is that if the entity is for example: Prime Minister (a page about a Prime minister) that the result Prime Minister of Austria gets a low score, and thus will not be selected (naturally unless the entity is Prime Minister of Austria).
Although this is more advanced than solely checking if the title matches the entity, in practise this did not improve results much (it did improve tho!) because the gensim word2vec contained only true words (although it was supposed to also capture all WikiData dumps of 2014).
We still think using the description information could greatly improve results as its usually just one perfectly clarying sentence. (arguably better than loading the entire wikipedia page). 
However, it needs some improvement. Also, unfortunately we did not manage to install gensim in docker. So for now the ranking is commented out. (If you manage to install gensim easily on docker than it can be run).

(Spacy also did not install on docker because of the same reason (numpy?), yet stanza was superior anyway so that is fine). 


## Analysis results
When analysing the pour performance of the entitiy linker the following reasons have been found. 

- The Wikidata in trident is a bit incomplete. For example France does not have the property of being a country, whereas most other countries has. Naturally on Wikidata France is an instance of a country. We're not sure to what extend the dataset is incomplete, however that is incomplete is one of the reasons for incorrectly linking entities. 
- The annotations file incorrectly classifies entities as entities (e.g. Flash Player and WordPress). Missing those hurts performance whereas in fact it is actually correct. 
- The annotations file misses some entities. For example this application correctly links "Morgan Freeman" to the correct Wikipedia_id, yet it is not in the annotations file. 
- Due to the noisy webpage data some entities are misclassified (NER stanza and spacy). This leads to incorrect links, however is a bit out of our control. 
- However, besides the above reasons which are a bit out of our control a large reason for the low performance is that the ranking mechanism is too naive. Attempts have been done to improve the ranking mechanism by more complex queries (sparql is tricky, using it for the first time) or similarity scores, yet unsuccesful. 

## Other Things tried 
Finally, we have tried to parallise the program. Firstly by creating a new tread for every payload, yet this ofcourse did not make the program run faster. 
Then by first calculating the number of payloads and then dividing the work to workers. Howver due to generator functions used in the program it was not so trivial.

Furhermore, we have tried to combine both using multiple parsers as well as multiple NER models. Although this did improve recall by quite some, it decreaesd precision by a lot and is therefore not included in the final submission. 
  
  







