"""
clustering
"""

# -- Imports --------------------------------------------------------------------
# base
from typing import List, NewType

# third party
import numpy as np
import scipy.cluster.hierarchy as clus


# project
from woffle.functions.compose import compose


# -- Type synonyms --------------------------------------------------------------
Array = NewType('Array', np.ndarray)


# -- Definitions ----------------------------------------------------------------

def z(embedding : Array) -> Array:
    "Cluster hierarchy array"
    return clus.linkage(embedding, "ward")


# returns the cluster number for each row of the original data
def fetch(depth: float, links: Array) -> Array:
    return clus.fcluster(links, depth, criterion="distance")
#+WARNING: will need a partial somewhere probably, this should be for the depth?


def build(xs: List[str], numbers: Array) -> List[Array]:
    return (np.extract(numbers == i, xs) for i in np.unique(numbers))


#+TODO: figure out how this works and make it nicer
def cluster(embedding: Array, xs: List[str], depth: float) -> List[Array]:
    return build(xs, fetch(depth, z(embedding)))

