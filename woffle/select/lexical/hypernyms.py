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

# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)
Doc = NewType('Doc', spacy.tokens.doc.Doc)

model = spacy.load('en_core_web_md')
model.add_pipe(WordnetAnnotator(model.lang), after='tagger')


# -- Interfaces -----------------------------------------------------------------
# TODO: decide if there is a better than wordnet approach with spacy
# semantic similarity
def condition(xs: List[str]) -> float:
    "implement hypernym lookup"
    return (
        0.0
        if len(xs) <= 1
        else 1.0
    )
# TODO: currently always run it, should perhaps check to see if there are enough
# word in vocabulary in order to try to look them up?

def selection(xs: List[str]) -> str:
    return hypernyms(xs)


#+TODO: this is horrific, but it just needs to work to start with
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
    common = [i for i in common if i not in ( 'entity'
                                    , 'whole'
                                    , 'object'
                                    , 'matter'
                                    , 'physical_entity')]

    return common[0].replace('_', ' ')


# -- wordnet -- #
def gendoc_(model, x: str):
    return model(str(x))
gendoc = functools.partial(gendoc_, model)

def gencorpus(xs: List[str]):
    return map(gendoc, xs)


def lca(syn1, syn2):
    # Find lowest common ancestor
    return syn1.lowest_common_hypernyms(syn2)


#+TODO: replace
# copy of woffle.parse.prob.spacy's roots
def roots(tokens : Doc) -> List[str]:
    return [*filter(lambda x: x.dep_ == 'ROOT', tokens)][0]

#/wip
