"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from typing import List, NewType, Set
from math import log

# third party
import numpy as np

from textacy.similarity import jaccard

# project
from woffle.functions.lists import strip, foldl

# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Interfaces -----------------------------------------------------------------
# wordgram measurement
def condition(xs: List[str]) -> float:
    "average number of common words across the cluster"
    xs_ = strip(xs)
    return (
        0.0 if (len(xs_) <= 1) or (wordLen(xs_) < 3) else
        scorer(xs_)
    )


def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return label(xs_)


# -- Supporting functions -------------------------------------------------------
def fetch(x: str, n: int) -> Set[str]:
    tokens = x.split()
    ngrams = (" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))
    return set(ngrams)


def group(x:str) -> Set[str]:
    return (x and set.union(*(fetch(x, i) for i in range(1, len(x.split())+1)))) or set()


def wordLen(xs: List[str]) -> int:
    tokens = map(str.split, xs)
    return np.min([len(w) for t in tokens for w in t])


def scorer(xs: List[str]) -> float:
    score = (sum(i in j for j in xs)**2 * (1+log(len(i.split()))) for i in xs)
    return max(score)


def label(xs: List[str]) -> float:
    ys = [j for i in xs for j in group(i)]
    # score = (sum(i in j for j in ys)**2 * (1+log(len(i.split()))) for i in ys)
    score = (sum(i == j for j in ys)**2 * (1+log(len(i.split()))) for i in ys)
    nScore = (i / len(ys) for i in score)
    return ys[nScore == max(nScore)]
#TODO: this requires going over the list a couple of times, its pretty fast but
#      could be better - if it becomes a resource hog then fix it
#TODO: need to change score so that it stops counting against itself and the
#      string it came from as this weighs words from long descriptions more
