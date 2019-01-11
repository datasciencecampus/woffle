"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from collections import Counter
from typing import List, NewType, Set
from math import log
from operator import add

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
        0.0  #TODO: if there is only one thing then we must return no commonality?
        if len(xs_) <= 1
        else np.mean([jaccard(x.split(), y.split())
                      for x, y in itertools.combinations(xs_, 2)])
    )

def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    common = (group(x) for x in xs_)
    return "".join(set.intersection(*common)).strip()


# -- Supporting functions -------------------------------------------------------
def fetch(x: str, n: int) -> Set[str]:
    tokens = x.split()
    ngrams = (" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))
    return set(ngrams)


def group(x:str) -> Set[str]:
    return (x and set.union(*(fetch(x, i) for i in range(1, len(x.split())+1)))) or set()


def max_len(xs: List[str]) -> int:
    tokens = map(str.split, xs)
    return max([len(w) for t in tokens for w in t])


def scorer(xs: List[str]) -> float:
   count    = [Counter(group(s)) for s in xs]
   counts   = foldl(add, Counter(), count)
   score    = lambda d: {i:(d[i]**2 * (1+log(len(i.split())))) for i in d}
   scores   = score(counts)
   r        = max(scores, key=lambda key: scores[key])
   return r, scores[r]

#+TODO: this is an over-complicated mechanism when a list of scores would work

# -- Interfaces -----------------------------------------------------------------
# wordgram measurement
def condition(xs: List[str]) -> float:
    "average number of common words across the cluster"
    xs_ = strip(xs)
    return (
        0.0 if (len(xs_) <= 1) or (max_len(xs_) < 3) else
        scorer(xs_)[1]
    )


def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return scorer(xs_)[0]
