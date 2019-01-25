"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools

from math import log
from typing import List, NewType, Tuple
from difflib import SequenceMatcher
from collections import Counter
# third party
import numpy as np

from textacy.similarity import jaccard, levenshtein

# project
from woffle.functions.lists import strip, foldl1, unpack


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)

# -- Supporting functions -------------------------------------------------------
def edits(s1: str,s2: str) -> float:
    normalised = levenshtein(s1, s2)
    maximum    = max(map(len,(s1,s2)))
    return maximum*(1 - normalised)


def characters(wl: List[str], start: int = 3, finish: int = 20):
    for word in wl:
        for n in range(start,finish):
            yield [word[i:i+n] for i in range(len(word) - n + 1)]

def scorer(xs: List[str]) -> Tuple[str,float]:
   counts   = Counter(unpack(characters(xs)))
   scores   = {i:(counts[i]**2 * (1+log(len(i)))) for i in counts}
   r        = max(scores, key=scores.get)
   return r, scores[r]

# -- Interfaces -----------------------------------------------------------------
# charactergram measurement
def condition(xs: List[str]) -> float:
    "longest common ngram"
    xs_ = strip(xs)
    # +TODO: will require rethinking the sizes of thresholds
    denom = np.mean([edits(*ys) for ys in itertools.combinations(xs_, 2)])
    return (
        0.0 if len(xs) <= 1 #TODO: if there is only one item then its vacuously 0? 

        else scorer(xs_)[1]/(1+denom*log(len(xs)))
    )

def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return scorer(xs_)[0]

