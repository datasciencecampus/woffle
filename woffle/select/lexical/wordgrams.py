"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from typing import List, NewType, Set

# third party
import numpy as np

from textacy.similarity import jaccard

# project
from woffle.functions.lists import strip


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
    return set.union(*(fetch(x, i) for i in range(1, len(x.split())+1)))
