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

letters    = functools.partial(re.sub, r"[^a-zA-Z ]", "")
spaces     = functools.partial(re.sub, r"\s{2,}", " ")
singles    = functools.partial(re.sub, r"\s*\b[a-zA-Z].?\b\s*", "")
unlines    = lambda x: x.replace('\n', '')
domainbias = functools.partial(re.sub, r"\s?\b(product[s].*|good[s].*\s?)\b", "")


#-- Composition -----------------------------------------------------------------
parse = compose( domainbias
               , letters
               , spaces
               , singles
               , unlines
               , str.strip
               , str.lower  # --TODO: breaks NER
               )
