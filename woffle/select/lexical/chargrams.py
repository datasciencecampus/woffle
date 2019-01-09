"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from typing import List, NewType

# third party
import numpy as np

from textacy.similarity import jaccard

# project
from woffle.functions.lists import strip, foldl1


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Interfaces -----------------------------------------------------------------
# charactergram measurement
def condition(xs: List[str]) -> float:
    "longest common ngram"
    xs_ = strip(xs)
    return (
        0.0 #TODO: if there is only one item then its vacuously 0?
        if len(xs) <= 1
        else np.mean([jaccard(*ys) for ys in itertools.combinations(xs_, 2)])
    )


def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return foldl1(getMatch, xs_)


# -- Supporting functions -------------------------------------------------------
def getMatch(x: str, y: str) -> str:
    match = SequenceMatcher(None, x, y).find_longest_match(0, len(x), 0, len(y))
    return x[match.a : match.a + match.size]
