"""
spaCy parsing functionality

The important function here is the parse function which has signature
parse :: String -> String, everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# third party
import spacy
import toml

# project
from woffle.functions.compose import compose



#-- Definitions -----------------------------------------------------------------
config = toml.load('config.toml')
# load the spacy model
proc = spacy.load(config['spacy']['model'])


roots = lambda tokens: [i for i in filter (lambda x: x.dep_ == "ROOT", tokens)]
#+TODO: first is here for when you don't want to/cannot do NER, currently there
#       no NER so it is the default target selector
first = lambda list: list[0]
lemma = lambda x: x.lemma_

process = lambda x: proc(x)


# rewrite me
parse = compose(lemma, first, roots, process)
