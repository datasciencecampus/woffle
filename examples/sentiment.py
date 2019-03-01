"""
woffle implementation of sentiment scoring and clustering by sentiment
"""
# -- Imports ---------------------------------------------------------------------
# Third Party
import numpy as np
import matplotlib.pyplot as plt

# Project
from woffle.functions.generics import compose

from woffle.sentiment import parse, embed, cluster

# -- Definitions ----------------------------------------------------------------
def plot(array):
    plt.scatter(array[:,1], array[:,0])
    plt.show()


def main():
    """
    This function is where we build our pipeline to create the embeddings from an
    example set of comments.
    """

    with open('data/example_comments.txt') as comments:
        comments = comments.read().splitlines()

    # Create the sentiment scores
    scores = compose(list, embed, parse)(comments)

    # Use some form of clustering (in this case inbuilt hclustering) to get groups
    clusters = cluster(np.array(scores).reshape(-1,1), 0.5)

    # Return scores and cluster labels
    return np.array(list(zip(scores, clusters)))


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    plot(main())

