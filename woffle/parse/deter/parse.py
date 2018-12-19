"""
text cleaning
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools
import re

# third party
import toml

# project
from woffle.functions.compose import compose


#-- Definitions -----------------------------------------------------------------
#-- cleaning
#NOTE: all functions are endomorphic String -> String so their composition does
#      not need to be tested and they can be composed in any order

# read the config files for the operations
with open('etc/regex') as f:
    replace = toml.load(f)

with open('etc/encoding') as f:
    encode = toml.load(f)

def regexes(r : dict, x : str) -> str:
    return compose(*[functools.partial(re.sub, i, j, flags=re.IGNORECASE)
                for i,j in r.items()])(x)

replacements = functools.partial(regexes, replace)
encoding     = functools.partial(regexes, encode)


# Composition -----------------------------------------------------------------
parse_ = compose( encoding
                 , replacements
                 , str.strip
                 )

parse = functools.partial(map, parse_)
