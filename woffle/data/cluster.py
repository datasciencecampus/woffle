"""
clustering
"""

#-- Imports ---------------------------------------------------------------------
# third party
import scipy.cluster.hierarchy as H


#-- Definitions
Z = lambda embed: h.linkage(embed, 'ward')
clusters = lambda depth: H.fcluster(Z, depth, criterion='distance')
# or: clusters = H.fcluster(Z, 1,  depth='1') -- not sure which is correct right now



"""
# how to go fetch the clusters for a given depth


import numpy as np

# depth 1
c = clusters(1)
_,counts = np.unique(c, return_counts=True)
# words is a numpy array of the processed strings
targets = [words[np.where(clusters == i)] for i in np.unique(clusters)]
"""
