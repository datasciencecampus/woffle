"""
text cleaning and processing
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools
import re

# third party
# -- unused, in preparation for later, use case: identifying the best replacement
#    for typos
# import hunspell
# import textacy


#-- Definitions -----------------------------------------------------------------
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# -- cleaning
letters    = functools.partial(re.sub, r"[^a-z ]", "")
spaces     = functools.partial(re.sub, r"\s{2,}", " ")
singletons = functools.partial(re.sub, r" [a-z]? ", "")
unlines    = lambda x: x.replace('\n', '')
domainbias = functools.partial(re.sub, r"\b(product[s].*|good[s].*)\b", "")

clean = compose( domainbias
               , letters
               , spaces
               , singletons
               , unlines
               , str.strip
               , str.lower  # --TODO: breaks NER
               )


# -- parsing
roots = lambda tokens: [i for i in filter (lambda x: x.dep_ == "ROOT", tokens)]
first = lambda list: list[0]
lemma = lambda x: x.lemma_

parse = compose( lemma
               , first
               , roots
               )

