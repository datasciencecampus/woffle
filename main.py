"""
classification of free text descriptions
"""

# -- Imports ---------------------------------------------------------------------

# Project
from woffle.hcluster import parse, embed, cluster


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

    target = parse(text)
    embed = [i for i in embed(target)]  ## TODO: clusters cannot currently take a map
    clusters = [i for i in cluster(embed, text, 4)]

    ## TODO: I think clusters should be numeric representation of the cluster that the
    ## position in the original text belongs to rather than the list of clusters
    ## themselves as this makes it very hard to reverse to apply the label to the
    ## original input

    target = parse(text)  ## target has been consumed at this point
                          ## in a real use case I'd make it a list but for this
                          ## demo I want to make it clear that it isn't a list
    pairs = ((i, j) for i, j in zip(text, target))
    for o, t in pairs:
        entrant = [cluster.tolist() for cluster in clusters if o in cluster]
        print(f"{o:>30s}: {t:15s} -> {entrant[0]}")


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
