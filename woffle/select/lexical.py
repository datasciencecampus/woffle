"""
Selection of the label for the cluster based on decision metric
"""
# -- Imports --------------------------------------------------------------------
# base
import functools
import itertools

from difflib import SequenceMatcher
from typing import Callable, List, NewType, Set

# third party
import numpy as np
import toml

from textacy.similarity import levenshtein, jaccard, hamming

# project
from woffle.functions.lists import foldl, foldl1


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------
with open('config.ini') as file:
    config = toml.load(file)['select']


# -------------------------------------------------------------------------------
#  ____                                     _    _
# / ___|  _   _  _ __   _ __    ___   _ __ | |_ (_) _ __    __ _
# \___ \ | | | || '_ \ | '_ \  / _ \ | '__|| __|| || '_ \  / _` |
#  ___) || |_| || |_) || |_) || (_) || |   | |_ | || | | || (_| |
# |____/  \__,_|| .__/ | .__/  \___/ |_|    \__||_||_| |_| \__, |
#               |_|    |_|                                 |___/
#
# -------------------------------------------------------------------------------
def editMatrix(xs: List[str]) -> Array:
    return np.array([[levenshtein(x,y) for y in xs] for x in xs])


def getMatch(x: str, y: str) -> str:
    match = SequenceMatcher(None, x, y).find_longest_match(0, len(x), 0, len(y))
    return x[match.a : match.a + match.size]


def wg_fetch(x: str, n: int) -> Set[str]:
    tokens = x.split()
    ngrams = (" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))
    return set(ngrams)


def wg_group(x:str) -> Set[str]:
    return set.union(*(wg_fetch(x, i) for i in range(1, len(x.split())+1)))


# -------------------------------------------------------------------------------
#                         _  _  _    _
#   ___  ___   _ __    __| |(_)| |_ (_)  ___   _ __   ___
#  / __|/ _ \ | '_ \  / _` || || __|| | / _ \ | '_ \ / __|
# | (__| (_) || | | || (_| || || |_ | || (_) || | | |\__ \
#  \___|\___/ |_| |_| \__,_||_| \__||_| \___/ |_| |_||___/
#
# -------------------------------------------------------------------------------
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
    return (
        1.0  #TODO: if there is only one thing then we must return no commonality?
        if len(xs) == 1
        else np.mean([jaccard(x.split(), y.split())
                      for x, y in itertools.combinations(xs, 2)])
    )


# charactergram measurement
def ngCond(xs: List[str]) -> float:
    "longest common ngram"
    return (
        1.0 #TODO: if there is only one item then its vacuously 0?
        if len(xs) == 1
        else np.mean([jaccard(*ys) for ys in itertools.combinations(xs, 2)])
    )


# +TODO: decide if there is a better than wordnet approach with spacy
# semantic similarity
def hnCond(xs: List[str]) -> float:
    "implement hypernym lookup"
    return 0


# -------------------------------------------------------------------------------
#             _              _    _
#  ___   ___ | |  ___   ___ | |_ (_)  ___   _ __
# / __| / _ \| | / _ \ / __|| __|| | / _ \ | '_ \
# \__ \|  __/| ||  __/| (__ | |_ | || (_) || | | |
# |___/ \___||_| \___| \___| \__||_| \___/ |_| |_|
#
# -------------------------------------------------------------------------------
def edit(xs: List[str]) -> str:
    return xs[np.sum(editMatrix(xs), axis=1).argmax()]
# selecting the word which has most similarity with all other words


def wordgram(xs: List[str]) -> str:
    common = (wg_group(x) for x in xs)
    return "".join(set.intersection(*common))
# TODO: fix this more: this currently gives the entire intersection even if  the
# words are not consecutive, this is not the correct behaviour


def chargram(xs: List[str]) -> str:
    return foldl1(getMatch, xs)


def hypernyms(xs: List[str]) -> str:
    return "Yep, I need to implement hypernym selector"


def fallback(xs: List[str]) -> str:
    return "Yep, I need to implement the fallback selector"


# -------------------------------------------------------------------------------
#                                                    _
#   __ _  _ __  __ _  _   _  _ __ ___    ___  _ __  | |_  ___
#  / _` || '__|/ _` || | | || '_ ` _ \  / _ \| '_ \ | __|/ __|
# | (_| || |  | (_| || |_| || | | | | ||  __/| | | || |_ \__ \
#  \__,_||_|   \__, | \__,_||_| |_| |_| \___||_| |_| \__||___/
#              |___/
#
# -------------------------------------------------------------------------------
# given conditions on the cluster and a function to run in each condition then
# do the following in a more abstract way
decisions = (
    lambda xs: edCond(xs) > config['edit'],  # high lexical similarity
    lambda xs: wgCond(xs) > config['word'],  # medium lexical similarity
    lambda xs: ngCond(xs) > config['char'],   # low lexical similarity
    lambda xs: hnCond(xs) > config['hype'],  # semantic similarity
    lambda xs: True  # default always true fallback
)


functions = (
    lambda xs: edit(xs),  # high lexical similarity
    lambda xs: wordgram(xs),  # medium lexical similarity
    lambda xs: chargram(xs),  # low lexical similarity
    lambda xs: hypernyms(xs),  # semantic similarity
    lambda xs: fallback(xs)  # default fallback
)


# -------------------------------------------------------------------------------
#  _         _                __
# (_) _ __  | |_  ___  _ __  / _|  __ _   ___  ___
# | || '_ \ | __|/ _ \| '__|| |_  / _` | / __|/ _ \
# | || | | || |_|  __/| |   |  _|| (_| || (__|  __/
# |_||_| |_| \__|\___||_|   |_|   \__,_| \___|\___|
#
# -------------------------------------------------------------------------------
# exposed default interfaces
def represent(decisions, functions, cluster):
    for d, f in zip(decisions, functions):
        if d(cluster):
            return f(cluster)  # stops the first time that d(cluster) is true

select_ = functools.partial(represent, decisions, functions)
select = functools.partial(map, select_)
