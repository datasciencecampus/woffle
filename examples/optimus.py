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
    with open('data/845.csv') as handle:
        text = handle.read().splitlines()
        # list because I'm using it later, also works as a generator expression
        # we also use this instead of .readlines() because it doesn't give \n

    target = list(parse(text))
    numclusters = len(target)
    depth = 1
    labels = {}

    while numclusters > 1:
        print(f"** Depth {depth}")
        print("    -- embedding")
        embedding = list(embed(target))  ## TODO: clusters cannot currently take a map

        print(f"    -- clustering")
        clusters = cluster(embedding, target, depth)

        if len(set(clusters)) == numclusters:
            print("    >> No new clusters generated")
            labels[f"tier_{depth}"] = labels[f"tier_{depth-1}"]
            depth += 1
        else:
            numclusters = len(set(clusters))

            print("    -- generating labels")
            labels[f"tier_{depth}"] = list(select(target, clusters))

            target = [ labels[f"tier_{depth}"][i]
                      if labels[f"tier_{depth}"][i]
                      else text[i]
                      for i in range(len(text))
                     ]
            depth += 1


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
