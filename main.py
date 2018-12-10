"""
classification of free text descriptions
"""

# -- Imports ---------------------------------------------------------------------

# Project
from woffle import data
from woffle.functions.compose import compose
from woffle.models import spacy as model


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
    clean = compose(model.parse, data.parse)
    target = [clean(line) for line in text]
    pairs = [(i, j) for i, j in zip(text, target)]

    for o, t in pairs:
        print(f"{o:>30s}: {t}")


# -- Boilerplate ----------------------------------------------------------------
if __name__ == "__main__":
    main()
