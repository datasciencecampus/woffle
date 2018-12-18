"""
Selection of the label for the cluster based on decision metric
"""
# -- Imports --------------------------------------------------------------------
# base
import functools
import itertools

from typing import List, NewType

# third party
import numpy as np

from textacy.similarity import levenshtein

# project
from woffle.functions.id import id


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.ndarray)

# -- Definitions ----------------------------------------------------------------

# -- Supporting functions
def editMatrix(xs: List[str]) -> Array:
    return np.array([[levenshtein(x,y) for y in xs] for x in xs])



# -- Decision functions

# maps levenshtein distance into the closed interval [0,1]
def edCond(xs: List[str]) -> float:
    "average edit distance on cluster"
    return (
        1.0  # levenshtein returns 1 if they are identical
        if len(xs) == 1
        else np.mean([levenshtein(*ys) for ys in itertools.combinations(xs, 2)])
    )


# wordgram measurement
def wgCond(xs: List[str]) -> float:
    "average number of common words across the cluster"
    return 0


# charactergram measurement
def ngCond(xs: List[str]) -> float:
    "longest common ngram"
    return 0


# +TODO: decide if there is a better than wordnet approach with spacy
# semantic similarity
def hnCond(xs: List[str]) -> float:
    "implement hypernym lookup"
    return 0


# -- Text replacement functions
# +TODO: write these functions


def edit(xs: List[str]) -> str:
    return xs[np.sum(editMatrix(xs), axis=1).argmax()]


def wordgram(xs: List[str]) -> str:
    return "Yep, I need to implement wordgram selector"


def chargram(xs: List[str]) -> str:
    return "Yep, I need to implement character-gram selector"


def hypernyms(xs: List[str]) -> str:
    return "Yep, I need to implement hypernym selector"


def fallback(xs: List[str]) -> str:
    return "Yep, I need to implement the fallback selector"


# -- Exports --------------------------------------------------------------------
# +TODO: replace all these 0.75s with proper thresholds

# given conditions on the cluster and a function to run in each condition then
# do the following in a more abstract way
decisions = (
    lambda xs: edCond(xs) > 0.75,  # high lexical similarity
    lambda xs: wgCond(xs) > 0.75,  # medium lexical similarity
    lambda xs: ngCond(xs) > 0.75,  # low lexical similarity
    lambda xs: hnCond(xs) > 0.75,  # semantic similarity
    lambda xs: id(xs) == xs,  # default always true fallback
)


functions = (
    lambda xs: edit(xs),  # high lexical similarity
    lambda xs: wordgram(xs),  # medium lexical similarity
    lambda xs: chargram(xs),  # low lexical similarity
    lambda xs: hypernyms(xs),  # semantic similarity
    lambda xs: fallback(xs),  # default fallback
)


# exposed default interface
def select__(decisions, functions, cluster):
    for d, f in zip(decisions, functions):
        if d(cluster):
            return f(cluster)  # stops the first time that d(cluster) is true

select_ = functools.partial(select__, decisions, functions)
select = functools.partial(map, select_)
