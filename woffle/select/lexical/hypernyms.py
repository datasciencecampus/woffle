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

def selection(*args):
    pass

# WIP/

model = spacy.load('en_core_web_md')
model.add_pipe(WordnetAnnotator(model), after='tagger')


def hypernyms(xs: List[str]) -> str:
    corpus = list(gencorpus(xs))

    syns = [i for doc in corpus for i in synsets(doc)]
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
    common = [i for i in common if i not in ('entity', 'whole', 'object')]

    return common


## the optimus version does this
def hypernyms_(xs):

    corpus = list(gencorpus(xs))
    syns = [i[0] for doc in corpus for i in synsets(doc)]

    ancestors = [k for i,j in itertools.combinations(syns, 2) for k in lca(i, j)]

    try:
        return max(ancestors, key=ancestors.count).name().split('.')[0].replace('_', ' ')
    except:
        return ''

# -- wordnet -- #
def gendoc_(model, x: str):
    return model(str(x))
gendoc = functools.partial(gendoc_, model)

def gencorpus(xs: List[str]):
    return map(gendoc, xs)


# TODO: swap out lists for generators where possible
def synsets(doc):
    gd_ = lambda x: x if x.pos_ == 'NOUN' else ""
    gd = lambda x: x if len(x) == 1 else gd_(x)
    return [span._.wordnet.synsets() for span in gd(doc)]


def lca(syn1, syn2):
    # Find lowest common ancestor
    return syn1.lowest_common_hypernyms(syn2)

# /WIP

