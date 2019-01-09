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

# project
from woffle.select.lexical import edits as ed
from woffle.select.lexical import wordgrams as wg
from woffle.select.lexical import chargrams as cg
from woffle.select.lexical import hypernyms as hn


# -- Type synonyms --------------------------------------------------------------
# +TODO: figure out of we need any...
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------
with open('config.ini') as file:
    config = toml.load(file)['select']


def build(xs: List[str], clusters: List[int]) -> List[Array]:
    return (np.extract(clusters == i, xs) for i in np.unique(clusters))

def fallback(xs: List[str]) -> str:
    return ""  #+TODO: fallback is just an empty string to make updating easier


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
    lambda xs: ed.condition(xs) > config['edit'],  # high lexical similarity
    lambda xs: wg.condition(xs) > config['word'],  # medium lexical similarity
    lambda xs: cg.condition(xs) > config['char'],   # low lexical similarity
    lambda xs: hn.condition(xs) > config['hype'],  # semantic similarity
    lambda xs: True  # default always true fallback
)


functions = (
    lambda xs: ed.selection(xs),  # high lexical similarity
    lambda xs: wg.selection(xs),  # medium lexical similarity
    lambda xs: cg.selection(xs),  # low lexical similarity
    lambda xs: hn.selection(xs),  # semantic similarity
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


