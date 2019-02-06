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
from woffle.functions.generics import compose


# -- Type synonyms --------------------------------------------------------------
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------

def z(embedding : Array) -> Array:
    "Cluster hierarchy array"
    return clus.linkage(embedding, "ward")


# returns the cluster number for each row of the original data
def fetch(depth: float, links: Array) -> Array:
    return clus.fcluster(links, depth, criterion="distance")

#+TODO: The xs parameter is redundant
#+TODO: figure out how this works and make it nicer
#+TODO: Typing is not correct on the result. It outputs an np.ndarray
def cluster(embedding: Array, xs: [str], depth: float) -> List[Array]:
    return fetch(depth, z(embedding))
