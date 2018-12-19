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
    embedding = [i for i in embed(target)]  ## TODO: clusters cannot currently take a map
    clusters = [i for i in cluster(embedding, text, 4)]
    labels = select(clusters)

    ## TODO: I think clusters should be numeric representation of the cluster that the
    ## position in the original text belongs to rather than the list of clusters
    ## themselves as this makes it very hard to reverse to apply the label to the
    ## original input

    target = parse(text)  ## target has been consumed at this point
                          ## in a real use case I'd make it a list but for this
                          ## demo I want to make it clear that it isn't a list

    for c, l in zip(clusters, labels):
        print(f"{l:>30s}: {c}")


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
