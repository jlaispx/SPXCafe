# pip install spacy
# python -m spacy download en_core_web_sm
# http://github.com/explosion/spacy-models/releases

from datetime import datetime

import spacy

class NLP():

    def __init__(self):
        # print(f"Please Wait...loading model...<{datetime.now()}>")
        self.nlp = spacy.load("en_core_web_sm")
        # print(f"... Finished loading.<{datetime.now()}>")

    def getNameByPartsOfSpeech(self, speech):
        ''' Parse Speech looking for Proper Nouns and stitching them together '''
        names = []
        doc = self.nlp(speech)
        # Parts of Speech (POS) Tagging
        print(f"{'token.text':10s}, {'token.lemma_':12s}, {'token.pos_':10s}, {'token.tag_':10s}, {'token.dep_':10s}, {'token.shape_':12s} token.is_alpha, token.is_stop")
        for token in doc:
            print(f"{token.text:10s}, {token.lemma_:12s}, {token.pos_:10s}, {token.tag_:10s}, {token.dep_:10s}, {token.shape_:12s}, {token.is_alpha},     {token.is_stop}")

            if token.pos_ in ["PROPN"]:
                names.append(token.text)

        name = " ".join(names)
        return name

    def getNounsByPartsOfSpeech(self, speech):
        ''' Parse Speech looking for Nouns and stitching them together '''
        names = []
        doc = self.nlp(speech)
        # Parts of Speech (POS) Tagging
        print(f"{'token.text':10s}, {'token.lemma_':12s}, {'token.pos_':10s}, {'token.tag_':10s}, {'token.dep_':10s}, {'token.shape_':12s} token.is_alpha, token.is_stop")
        for token in doc:
            print(f"{token.text:10s}, {token.lemma_:12s}, {token.pos_:10s}, {token.tag_:10s}, {token.dep_:10s}, {token.shape_:12s}, {token.is_alpha},     {token.is_stop}")

            if token.pos_ in ["NOUN","PROPN"]:
                names.append(token.text)

        name = " ".join(names)
        return name

    def getNameByEntityType(self, speech):
        names = []
        doc = self.nlp(speech)
        # print("Entities found: ")
        for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)

            if ent.label_ == 'PERSON':
                names.append(ent.text)

        name = " ".join(names)
        return name

    def getNounChunks(self, speech):
        names = []
        doc = self.nlp(speech)
        # print("Entities found: ")
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

            names.append(chunk.text)

        name = " ".join(names)
        return name


def main():
    nlpDemo = NLP()

    sentence = 'Hello! Introducing the infamous John Michael and Anthony Elias Smith-Jones. I am swimming, jumping, diving and eating? Do you like soup or pizza?'
    print(f">>> Process: {sentence}")

    name = nlpDemo.getNameByPartsOfSpeech(sentence)
    print(f">>> Name By Speech found: {name}")

    name = nlpDemo.getNameByEntityType(sentence)
    print(f">>> Name By Entity: {name}")

    name = nlpDemo.getNounsByPartsOfSpeech(sentence)
    print(f">>> Name By Nouns: {name}")

    name = nlpDemo.getNounChunks(sentence)
    print(f">>> Name By Noun Chunks: {name}")

if __name__=="__main__":
    main()