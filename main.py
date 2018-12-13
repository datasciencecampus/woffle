"""
classification of free text descriptions
"""

# -- Imports ---------------------------------------------------------------------

# Project
## parse
import woffle.parse.deter.parse as dp
import woffle.parse.prob.spacy as pp

## embed
import woffle.embed.numeric.fasttext as ft

## cluster
import woffle.cluster.deter as dc


## support
from woffle.functions.compose import compose_
# this version of compose runs the operations in the order they appear in the list


# -- Definitions ----------------------------------------------------------------
def main():
    """
    This function is where you build your own pipeline from the parts that are
    available in this module. Please see the example below for how to do this
    or RTFM
    """

    # load your data
    fp = "data/test.txt"
    text = [i for i in open(fp, "r").read().splitlines()]

    # compose your cleaning functions
    parse = compose_(dp.parse, data.parse)

    target = parse(text)
    embed = [i for i in ft.embed(target)]  ## TODO: clusters cannot currently take a map
    clusters = dc.cluster(embed, text, 1)

    ## TODO: I think clusters should be numeric representation of the cluster that the
    ## position in the original text belongs to rather than the list of clusters
    ## themselves as this makes it very hard to reverse to apply the label to the
    ## original input
    for cluster in clusters:
        print(cluster.tolist())

    target = clean(text)  ## target has been consumed at this point so just resetting it
                          ## for the purpose of this dummy example
    pairs = ((i, j) for i, j in zip(text, target))
    for o, t in pairs:
        print(f"{o:>30s}: {t}")


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
