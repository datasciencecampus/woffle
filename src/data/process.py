"""
text cleaning and processing
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools
import re

#-- Definitions -----------------------------------------------------------------
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

letters = functools.partial(re.sub, r"[^a-z ]", "")
spaces  = functools.partial(re.sub, r"s{2,}", " ")
clean = compose(letters, spaces, str.lower)

# rewrite me
def select(descs : [str], model : spacy.lang) -> str:
    """select the primary (here: first) target of the description"""

    for desc in descs:
        for token in model(desc):
            if (token.pos_ == 'NOUN')&(token.is_alpha):
                yield token.lemma_
    yield ''
