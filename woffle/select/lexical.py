"""
Selection of the label for the cluster based on decision metric
"""
# -- Imports --------------------------------------------------------------------
# base
import functools
import itertools

from difflib import SequenceMatcher
from typing import Callable, List, NewType, Set, Any, Generator

# third party
import numpy as np
import spacy
import toml

from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from textacy.similarity import levenshtein, jaccard, hamming

# project
from woffle.functions.lists import foldl, foldl1, unpack, unpackG, mapmap


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------
with open('config.ini') as file:
    config = toml.load(file)['select']


model = spacy.load('en_core_web_md')
model.add_pipe(WordnetAnnotator(model.lang), after='tagger')


# -------------------------------------------------------------------------------
#  ____                                     _    _
# / ___|  _   _  _ __   _ __    ___   _ __ | |_ (_) _ __    __ _
# \___ \ | | | || '_ \ | '_ \  / _ \ | '__|| __|| || '_ \  / _` |
#  ___) || |_| || |_) || |_) || (_) || |   | |_ | || | | || (_| |
# |____/  \__,_|| .__/ | .__/  \___/ |_|    \__||_||_| |_| \__, |
#               |_|    |_|                                 |___/
#
# -------------------------------------------------------------------------------
def strip(xs:List[Any]) -> List[Any]:
    return list(x for x in xs if x)


def build(xs: List[str], clusters: List[int]) -> List[Array]:
    return (np.extract(clusters == i, xs) for i in np.unique(clusters))


def editMatrix(xs: List[str]) -> Array:
    return np.array([[levenshtein(x,y) for y in xs] for x in strip(xs)])


def getMatch(x: str, y: str) -> str:
    match = SequenceMatcher(None, x, y).find_longest_match(0, len(x), 0, len(y))
    return x[match.a : match.a + match.size]


# -- wordgram -- #
def wordgram_fetch(x: str, n: int) -> Set[str]:
    tokens = x.split()
    ngrams = (" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))
    return set(ngrams)


def wordgram_group(x:str) -> Set[str]:
    return set.union(*(wordgram_fetch(x, i) for i in range(1, len(x.split())+1)))


# -- wordnet -- #
def gencorpus_(model, xs : List[str]):
    return map(model, xs)
gencorpus = functools.partial(gencorpus_, model)


def synsets(doc):
    return (span._.wordnet.synsets() for span in doc)


def hypernyms(xs):
    return ([x.hypernym_distances() for x in xs])


# currently:
#   corpus = gencorpus(text)
#   hnyms = mapmap(hypernyms, map(synsets, c))
#   working = itertools.chain.from_iterable(hnyms)
#



# -------------------------------------------------------------------------------
#                         _  _  _    _
#   ___  ___   _ __    __| |(_)| |_ (_)  ___   _ __   ___
#  / __|/ _ \ | '_ \  / _` || || __|| | / _ \ | '_ \ / __|
# | (__| (_) || | | || (_| || || |_ | || (_) || | | |\__ \
#  \___|\___/ |_| |_| \__,_||_| \__||_| \___/ |_| |_||___/
#
# -------------------------------------------------------------------------------
# maps levenshtein distance into the closed interval [0,1]
def editCond(xs: List[str]) -> float:
    "average edit distance on cluster"
    xs_ = strip(xs)
    return (
        0.0  # levenshtein returns 1 if they are identical
        if len(xs_) <= 1
        else np.mean([levenshtein(*ys) for ys in itertools.combinations(xs_, 2)])
    )


# wordgram measurement
def wordCond(xs: List[str]) -> float:
    "average number of common words across the cluster"
    xs_ = strip(xs)
    return (
        0.0  #TODO: if there is only one thing then we must return no commonality?
        if len(xs_) <= 1
        else np.mean([jaccard(x.split(), y.split())
                      for x, y in itertools.combinations(xs_, 2)])
    )


# charactergram measurement
def charCond(xs: List[str]) -> float:
    "longest common ngram"
    xs_ = strip(xs)
    return (
        0.0 #TODO: if there is only one item then its vacuously 0?
        if len(xs) <= 1
        else np.mean([jaccard(*ys) for ys in itertools.combinations(xs_, 2)])
    )


# TODO: decide if there is a better than wordnet approach with spacy
# semantic similarity
def hypeCond(xs: List[str]) -> float:
    "implement hypernym lookup"
    xs_ = strip(xs)
    return (
        0.0
        if len(xs_) <= 1
        else 0.0
    )
# TODO: currently always run it, should perhaps check to see if there are enough
# word in vocabulary in order to try to look them up?


# -------------------------------------------------------------------------------
#             _              _    _
#  ___   ___ | |  ___   ___ | |_ (_)  ___   _ __
# / __| / _ \| | / _ \ / __|| __|| | / _ \ | '_ \
# \__ \|  __/| ||  __/| (__ | |_ | || (_) || | | |
# |___/ \___||_| \___| \___| \__||_| \___/ |_| |_|
#
# -------------------------------------------------------------------------------
def edit(xs: List[str]) -> str:
    xs_ = strip(xs)
    return xs_[np.sum(editMatrix(xs_), axis=1).argmax()]
# selecting the word which has most similarity with all other words


def wordgram(xs: List[str]) -> str:
    xs_ = strip(xs)
    common = (wordgram_group(x) for x in xs_)
    return "".join(set.intersection(*common)).strip()


def chargram(xs: List[str]) -> str:
    xs_ = strip(xs)
    return foldl1(getMatch, xs_)


def hypernyms(xs: List[str]) -> str:

    return "HYPE"


def fallback(xs: List[str]) -> str:
    return ""


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
    lambda xs: editCond(xs) > config['edit'],  # high lexical similarity
    lambda xs: wordCond(xs) > config['word'],  # medium lexical similarity
    lambda xs: charCond(xs) > config['char'],   # low lexical similarity
    lambda xs: hypeCond(xs) > config['hype'],  # semantic similarity
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
def represent_(decisions, functions, group):
    for d, f in zip(decisions, functions):
        if d(group):
            return f(group)  # stops the first time that d(group) is true

represent = functools.partial(represent_, decisions, functions)


def select_(xs: List[str], clusters: List[str], cluster: int) -> List[str]:
    groups = build(xs, clusters)
    labels = [represent(group) for group in groups]
    return labels[cluster-1]


def select(xs: List[str], clusters: List[str]) -> List[str]:
    groups = build(xs, clusters)
    labels = [represent(group) for group in groups]
    return (labels[cluster-1] for cluster in clusters)
