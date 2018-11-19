"""
Implementation of flair as the back end for NER and POS functionality
"""

#-- Imports ---------------------------------------------------------------------
import flair


#-- Definitions -----------------------------------------------------------------
pos = lambda x: x
ner = lambda x: x


#+NOTE:
# if spacy is activated then you can use ner-ontonotes, otherwise use the more
# cpu friendly ner-ontonotes-fast

# examples/play
import flair

sentence = flair.data.Sentence("chocolate")

model  = flair.embeddings.WordEmbeddings("en-crawl")
tagger = flair.models.SequenceTagger.load("ner-ontonotes")


tagger.predict(sentence)
model.embed(sentence)

print(sentence.to_tagged_string())
for entity in sentence:
    print(entity.embedding)
