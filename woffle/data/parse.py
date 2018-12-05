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
#      not need to be tested and they can be composed in any order
def letters(x : str) -> str:
    return re.sub(r"[^a-zA-Z]", "", x)

def spaces(x : str) -> str:
    return re.sub(r"\s{2,}", " ", x)

def singles(x : str) -> str:
    return re.sub(r"\s*\b[a-zA-Z].?\b\s*", "", x)

def domainbias(x : str) -> str:
    return re.sub(r"\s?\b(product[s].*|good[s].*\s?)\b", "", x)

def unlines(x : str) -> str:
    return x.replace('\n', '')


# Composition -----------------------------------------------------------------
parse = compose( domainbias
               , letters
               , spaces
               , singles
               , unlines
               , str.strip
               )

