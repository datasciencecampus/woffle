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
Array = NewType('Array', np.array)


# -- Definitions ----------------------------------------------------------------

def z(embedding : Array) -> Array:
    "Cluster hierarchy array"
    return clus.linkage(embedding, "ward")


# returns the cluster number for each row of the original data
def fetch(depth: float, links: Array) -> Array:
    return clus.fcluster(links, depth, criterion="distance")


#+TODO: figure out how this works and make it nicer
def cluster(embedding: Array, xs: [str], depth: float) -> List[Array]:
    return fetch(depth, z(embedding))
