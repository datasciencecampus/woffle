"""
woffle implementation of https://github.com/datasciencecampus/optimus
"""

print("** Importing woffle")
# -- Imports ---------------------------------------------------------------------
# third party
import pandas as pd

# Project
from woffle.hcluster import parse, embed, cluster, select


# -- Definitions ----------------------------------------------------------------
def main():
    """
    This function is where you build your own pipeline from the parts that are
    available in this module. Please see the example below for how to do this
    or RTFM
    """

    print("** Preparing data")
    # load your data
    with open('data/845.csv') as handle:
        text = handle.read().splitlines()
        # list because I'm using it later, also works as a generator expression
        # we also use this instead of .readlines() because it doesn't give \n

    print("    -- parsing")
    target = list(parse(text))
    print("    -- clustering")
    numclusters = len(target)
    depth = 5
    labels = {}

    #+TODO: consider immutable version of this but its perhaps not really needed
    # mutable list to update the target words at each depth
    targetM = target  # mutable target

    while depth < 60:
        print(f"** Depth {depth}")
        print("    -- embedding")
        embedding = list(embed(targetM))  ## TODO: clusters cannot currently take a map

        print(f"    -- clustering")
        clusters = cluster(embedding, targetM, depth)

        if len(set(clusters)) == numclusters:
            print("    >> No new clusters generated")
            labels[f"tier_{depth}"] = labels[f"tier_{depth-5}"]
        else:
            numclusters = len(set(clusters))

            print("    -- generating labels")
            labels[f"tier_{depth}"] = list(select(targetM, clusters))
            #+TODO: make this better
            targetM = [i if i else j for i,j in zip(labels[f"tier_{depth}"], targetM)]

        depth += 5

    print("** Writing output")

    # make the output match optimus
    dty = labels
    dty['original'] = text
    dty['current_labels'] = dty['tier_55']

    df = pd.DataFrame.from_dict(dty, orient='index').transpose()

    # reordering to match optimus
    #TODO: sloppy, fix up, look sharp
    df_ = df[[df.columns[-2], *list(df.columns[:-3]), df.columns[-1]]]

    df_.to_csv('output/test.csv', index=False)


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
