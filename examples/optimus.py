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

    # thresholds
    thresholds = (3, 15, 3)
    # (start, end, step) in N^3
    # start >= 1, end > start, step > 0

    print("** Preparing data")
    # load your data
    with open('data/test.txt') as handle:
        text = handle.read().splitlines()
        # list because I'm using it later, also works as a generator expression
        # we also use this instead of .readlines() because it doesn't give \n

    print("    -- parsing")
    target = list(parse(text))
    print("    -- clustering")
    numclusters = len(target)
    depth = thresholds[0]
    labels = {}

    targetM = target.copy()  # mutable target

    while depth <= thresholds[1]:
        print(f"** Depth {depth}")
        print("    -- embedding")
        embedding = list(embed(targetM))

        print(f"    -- clustering")
        clusters = cluster(embedding, depth)

        if len(set(clusters)) == numclusters:
            print("    >> No new clusters generated")
            labels[f"tier_{depth}"] = labels[f"tier_{depth-thresholds[2]}"]
        else:
            numclusters = len(set(clusters))

            print("    -- generating labels")
            labels[f"tier_{depth}"] = list(select(targetM, clusters))
            targetM = [i if i else j for i,j in zip(labels[f"tier_{depth}"], targetM)]

        depth += thresholds[2]

    print("** Writing output")

    # make the output match optimus
    dty = labels
    dty['original'] = text
    dty['current_labels'] = dty[f'tier_{thresholds[1]}']

    df = pd.DataFrame.from_dict(dty, orient='index').transpose()

    # reordering to match optimus
    df_ = df[[df.columns[-2], *list(df.columns[:-3]), df.columns[-1]]]

    df_.to_csv('output/test.csv', index=False)


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
