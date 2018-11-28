"""
text cleaning
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools
import re

# project
from woffle.functions.compose import compose


#-- Definitions -----------------------------------------------------------------
#-- cleaning
#NOTE: all functions are endomorphic String -> String so their composition does
#      not need to be tested

letters    = functools.partial(re.sub, r"[^a-z ]", "")
spaces     = functools.partial(re.sub, r"\s{2,}", " ")
singletons = functools.partial(re.sub, r" [a-z]? ", "")
unlines    = lambda x: x.replace('\n', '')
domainbias = functools.partial(re.sub, r"\b(product[s].*|good[s].*)\b", "")


#-- Composition -----------------------------------------------------------------
parse = compose( domainbias
               , letters
               , spaces
               , singletons
               , unlines
               , str.strip
               , str.lower  # --TODO: breaks NER
               )
