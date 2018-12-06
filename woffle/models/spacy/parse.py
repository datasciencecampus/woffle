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
from woffle.functions.compose import compose


#-- Type synonyms ---------------------------------------------------------------
Doc = NewType('Doc', spacy.tokens.doc.Doc)


#-- Definitions -----------------------------------------------------------------
config = toml.load('config.ini')
# load the spacy model
proc = spacy.load(config['spacy']['model'])


def roots(token : Doc) -> List[str]:
    return [i for i in filter (lambda x: x.dep_ == 'ROOT', tokens)]

#+TODO: first is here for when you don't want to/cannot do NER, currently there
#       no NER so it is the default target selector
def fst(xs : List[str]) -> str:
    return xs[0]

def lemma(x : Doc) -> str:
    return x.lemma_

def process(x : str) -> Doc:
    return proc(x)

def vocab(m : Doc, x : str) -> str:
    return x if x in m.vocab else ''
vocab = functools.partial(proc, vocab)


# rewrite me
parse = compose(vocab, lemma, first, roots, process)
