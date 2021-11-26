# Entity Linker (WDPS, 2021)
This repo comprises an Entity Linker application written in Python. It uses several external libraries such as Stanza, Spacy and Trafilatura. 
The codebases consists of a main.py and three classes: my_elastic_search.py, my_trident.py and parser.py. Furthermore the application uses utils.py for helper functions. 

## Code Instructions 
Please clone this git repo to the local machine. (assets and data are in the .gitignore, so please add those folders)


## To build a new image (on top of karmaresearch/wdps_assignment, with additional requirements installed)

Go to the git repo on local machine and run the following: 

```bash
docker build . --tag=submission --load
```
```bash
docker run -ti -v <path-to-git-submission-and-data>:/app/assignment -p 9200:9200 submission
```


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


# Project Description. 

The task is splitted in the following parts: (1) Parsing HTML to plain text. (2) Named Entity-Recognition (3) Elastic-Search (4) Ranking Search Results
Below the findings/descisions of every part will be discussed shortly.

## Parsing HTML to plain text
This step appears trivial, however this one is as crucial as the other steps. Namely, when too little text is parsed, the NER models are missing potential entities.
On the other hand if too much text is parsed the NER models will create wrong entities. One can observe this is in the annotations.tsv file where entities as "Adobe Flash Player" and "WordPress" 
are parsed. Naturally, if the page is about Adobe Flash player it is an enitity. However in the first 5 files the text is about totally different topics, however in a small div probably some text was present like "Adobe Flash Player required".

The following parsers have been considere in this study: BeautifulSoup, Trafilatura, Justext.
BeautifoulSoup is the first option to explore and it parses base on a set of rules. However, during visual inspection it proved to be hard to only keep the useful text. 
Too much useless text was parsed, leading to wrong entities.  

Trafilatura and Justext are python packages which probably parse with the same packages as with beautifulSoup is built-up on, however they were leading to way better results. 
This is no surpise as for example Justext is the result of an entire PHD thesis. Naturally, they have optimized the set of rules to keep the relevant text. 

Based on visual inspection trafilatura gave the best results and is therefore used in this study. Furthermore, one could consider a model based approach like DragNet. 

## Named Entity-Recognition
Another crucial step in the pipeline, missing or misclassifyng the entitiy (either by name or type) can lead to severe problems further in the pipeline. 
In this study two NER models are considered. The place to start is Spacy, an open source python library for NER. Although the results proved to be decent, the results were not flawless as a lot of entities were missed. 
Therefore, Stanza (the NER model from stanford) was also considered. And this led to better results. More entities were captured, and it led to a better performance overall. 

## Elastic-Search 
Elastic-search in this study is used to query both the title and description based on the search result.
There is not much to tweak in this part of the pipeline, however there is one important factor the size of the returned results. 
If you make increase it too much the ranking becomes unnessery complex. However, if you're size is too small you might miss the correct result. 
In this study, the search size is increased greatly for GPE (city, state, country) entities as they are easy to filter based on checking if they are an instance of either city, state or country. 

## Ranking Search Results
The following strategy is used in order to create a ranking system from scratch. For every Entity Type a different trident function is called. (e.g. Type = person --> my_trident.is_person)
This function gives 5 points if a match should drastically clarify the results. These 5 points are only given if they are direct instances. For example if an entity is Paris and their is an enity with is an instance of city this wikipedia_id gets 5 points. 
The reasoning behind this is that if the entity is already classifed as a city the most often needed entity is the one of the city paris itself. 
Subsequently, if they are a subclass of in the case of GPE geograpichal area the respective result gets three points, because it could be of interest and be the best bet yet the subclasses category can become so large that it is less obivous. 

Finally, if there is a tie so if there is for example more than one result which has the property isHuman (Q5) a similarity score is calculated between (entity + entityType) and (title + description).
The rationale behind this is that for example if the entity is Prime Minister (a page about a Prime minister) that the result Prime Minister of Austria gets a low score, and thus will not be selected (naturally unless the entity is Prime Minister of Austria).
Although this is more advanced than solely checking if the title matches, in practise this did not improve results much (it did improve tho!) because the gensim word2vec contained only true words (although it was supposed to also capture all WikiData dumps of 2014).
We still think using the description information could greatly imorove rsults as its usually just one perfectly clarying sentence. (better than loading the entire wikipedia page). 
However, it needs some improvement. Also, unfortunately we did not manage to install gensim in docker. So for now the ranking is commented out. (If you manage to install gensim easily on docker than it can be run).

(Spacy was also, not able to be installed on docker because of the same reason (numpy?), yet stanza was superior anyway so that is fine). 


## Analysis results


## Other Things tried 







