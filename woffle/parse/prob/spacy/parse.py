"""
spaCy parsing functionality

The important function here is the parse function which has signature
parse :: String -> String, everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List, NewType


# third party
import spacy
import toml


# project
from woffle.functions.generics import compose


#-- Type synonyms ---------------------------------------------------------------
Doc = NewType('Doc', spacy.tokens.doc.Doc)


#-- Definitions -----------------------------------------------------------------
config = toml.load('config.ini')
# load the spacy model
proc = spacy.load(config['spacy']['model'])


def roots(tokens : Doc) -> List[str]:
    return [i for i in filter (lambda x: x.dep_ == 'ROOT', tokens)][0]

#+TODO: first is here for when you don't want to/cannot do NER, currently there
#       no NER so it is the default target selector
def fst(xs : List[str]) -> str:
    return xs[0]

def lemma(x : Doc) -> str:
    return x.lemma_

def process(x : str) -> Doc:
    return proc(x)

#+TODO: fix this - sadly you can't create a type synonym until after you load a
# language model so it just breaks the tidiness of the code but that's pretty
# minimal in the grand scheme of things
def vocab(m : spacy.lang.en.English, x : str) -> str:
    return x if x in m.vocab else ''
vocab = functools.partial(vocab, proc)


# rewrite me
parse_ = compose(vocab, lemma, fst, roots, process)
parse  = functools.partial(map, parse_)
