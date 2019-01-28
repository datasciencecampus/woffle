"""
wordgram decision metrics for lexical similarity of text
"""

# -- Imports --------------------------------------------------------------------
# base
import itertools
import re

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


# -- Interfaces -----------------------------------------------------------------
# charactergram measurement
def condition(xs: List[str]) -> float:
    "longest common ngram"
    xs_ = strip(xs)
    return (
        0.0 if ((len(xs_) <= 1) or (np.min([len(x) for x in xs_]) < 3))
        #TODO: if there is only one item then its vacuously 0?
        else scorer(xs_)
    )


def selection(xs: List[str]) -> str:
    xs_ = strip(xs)
    return label(xs_)


# -- Supporting functions -------------------------------------------------------
def characters(xs: List[str], start: int = 3, finish: int = 20):
    return unpack([get(x, n) for x in xs for n in range(start, finish)])


def get(x: str, n: int) -> List[str]:
    # fetch all charactergrams of length n from x
    regex = f"(?=({'.'*n}))"
    return re.findall(regex, x)

# alternative (bad) version
get_ = lambda n: lambda x: re.findall(f"(?=({'.'*n}))", x)


def scorer(xs: List[str]) -> float:
    cgrams = characters(xs)
    score = (sum(i in j for j in xs)**2 * (1+log(len(i))) for i in cgrams)
    return max(score)


def label(xs: List[str]) -> float:
    cgrams = characters(xs)
    score = [np.sum(i in j for j in xs)**2 * (1+log(len(i))) for i in cgrams]
    candidate = [cgrams[i] for i,j in enumerate(score) if j==np.max(score)]
    return candidate[0]

#+TODO: brain not working, make this betterer
