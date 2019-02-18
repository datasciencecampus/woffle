"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import functools
import itertools

from typing import List, Any, NewType

# third party
import spacy
import numpy as np

from textacy.similarity import jaccard
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

# project
from woffle.functions.lists import strip
from woffle.parse.prob.spacy import roots

# -- Type synonyms --------------------------------------------------------------
Array = NewType('Array', np.array)
Doc = NewType('Doc', spacy.tokens.doc.Doc)

model = spacy.load('en_core_web_md')
model.add_pipe(WordnetAnnotator(model.lang), after='tagger')


# -- Interfaces -----------------------------------------------------------------
# semantic similarity
def condition(xs: List[str]) -> float:
    "implement hypernym lookup"
    xs_ = strip(xs)
    return (
        0.0
        if len(xs_) <= 1
        else 1.0
    )

def selection(xs: List[str]) -> str:
    return hypernyms(xs)


def hypernyms(xs: List[str]) -> str:
    corpus = map(roots, gencorpus(xs))

    syns = [token._.wordnet.synsets() for token in corpus]
    lengths = [len(s) for s in syns]
    flat = [j for i in syns for j in i]

    flatM = flat  # mutable flat, in case we need the original

    common = []

    for length in lengths:
        left  = flatM[:length]
        right = flatM[length:]

        for i, j in itertools.product(left, right):
            common.append(lca(i,j))
        flatM = right

    # remove things which are too abstract
    common = [j.name().split('.')[0] for i in common for j in i]
    # TODO - replace this with a config file list of these things
    common = [i for i in common if i not in ( 'entity'
                                    , 'whole'
                                    , 'object'
                                    , 'matter'
                                    , 'physical_entity')]

    return (len(common) and common[0].replace('_', ' ')) or ''
    # if it cannot find a common hypernym returns empty string


# -- wordnet -- #
def gendoc_(model, x: str):
    return model(str(x))
gendoc = functools.partial(gendoc_, model)

def gencorpus(xs: List[str]):
    return map(gendoc, xs)


def lca(syn1, syn2):
    # Find lowest common ancestor
    return syn1.lowest_common_hypernyms(syn2)
