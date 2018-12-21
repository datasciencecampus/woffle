"""
woffle implementation of https://github.com/datasciencecampus/optimus
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

    target = list(parse(text))
    numclusters = len(target)
    depth = 1
    labels = {}

    while numclusters > 1:
        embedding = list(embed(target))  ## TODO: clusters cannot currently take a map
        clusters = cluster(embedding, target, depth)

        if len(clusters) == numclusters:
            depth += 1
        else:
            print(f"Processing: depth {depth}, clusters {len(clusters)}")
            numclusters = len(clusters)
            labels[depth] = select(target, clusters)

            target = labels[depth]

    return labels

# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
