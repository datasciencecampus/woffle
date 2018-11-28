"""
spaCy parsing functionality

The important function here is the parse function which has signature
parse :: String -> String, everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# project
from woffle.functions.compose import compose


#-- Definitions -----------------------------------------------------------------
roots = lambda tokens: [i for i in filter (lambda x: x.dep_ == "ROOT", tokens)]
#+TODO: first is here for when you don't want to/cannot do NER, currently there
#       no NER so it is the default target selector
first = lambda list: list[0]
lemma = lambda x: x.lemma_

process = lambda x: nlp(x)


# rewrite me
parse = process
