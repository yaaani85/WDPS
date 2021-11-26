# from nltk.tag import StanfordNERTagger
# from nltk.tokenize import word_tokenize
# import spacy
import stanza
stanza.download('en', processors='tokenize,ner', verbose=False)


class Named_Entity_Recognition:
    """This class combines several NER models
    Arguably it is more a namespace than a true class
    """
    def __init__(self):
        # self._st = StanfordNERTagger(  "/home/yannick/WDPS/assignment-code/assignment/assets/stanford-ner-2020-11-17/classifiers/english.muc.7class.distsim.crf.ser.gz",
		# 			   "/home/yannick/WDPS/assignment-code/assignment/assets/stanford-ner-2020-11-17/stanford-ner.jar",
		# 			   encoding='utf-8')
        # self._nlp = spacy.load("en_core_web_lg")

        self._nlp_stanza = stanza.Pipeline(lang='en', processors='tokenize,ner', verbose=False)

    # def spacy(self, text):
    #     document = self._nlp(text)
    #     entities_and_type = [(token.text.replace("\n", " "), token.label_) for token in document.ents if len(token.text) < 15]  
    #     return entities_and_type

    # def stanford(self, text):
    #     tokenized_text = word_tokenize(text)
    #     classified_text = self._st.tag(tokenized_text)
    #     entities_and_type = [(x, y) for (x,y) in classified_text if y != "O"]  
    #     return entities_and_type

    def stanza(self, text):
        document = self._nlp_stanza(text)        
        entities_and_type = [(token.text.replace("\n", " "), token.type) for token in document.ents if len(token.text) < 15]  
        return entities_and_type