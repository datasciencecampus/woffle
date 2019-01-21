"""
edit distance decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from typing import List, NewType

# third party
import numpy as np

from textacy.similarity import levenshtein

# project
from woffle.functions.lists import strip


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------
# maps levenshtein distance into the closed interval [0,1]
def condition(xs: List[str]) -> float:
    "average edit distance on cluster"
    xs_ = strip(xs)
    return (
        0.0  # levenshtein returns 1 if they are identical
        if len(xs_) <= 1
        else np.mean([levenshtein(*ys) for ys in itertools.combinations(xs_, 2)])
    )


def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return xs_[np.sum(editMatrix(xs_), axis=1).argmax()]
# selecting the word which has most similarity with all other words


# -- Supporting functions -------------------------------------------------------
def editMatrix(xs: List[str]) -> Array:
    return np.array([[levenshtein(x,y) for y in xs] for x in strip(xs)])
