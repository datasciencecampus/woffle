"""
classification of free text descriptions
"""

# -- Imports ---------------------------------------------------------------------

# Project
from woffle.hcluster import parse, embed, cluster, select


# -- Definitions ----------------------------------------------------------------
def main():
    """
    This function is where you build your own pipeline from the parts that are
    available in this module. Please see the example below for how to do this
    or RTFM
    """

    # load your data
    with open('data/test.txt') as handle:
        text = handle.read().splitlines()
        # list because I'm using it later, also works as a generator expression
        # we also use this instead of .readlines() because it doesn't give \n

    target = parse(text)
    embedding = list(embed(target))  # linkage cannot use an iterator
    clusters = cluster(embedding, 5)
    labels = select(text, clusters)

    for t, l in zip(text, labels):
        print(f"{t:>30s}: {l}")


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
