"""
Supporting functions for working with lists and tuples
"""

# -- Imports --------------------------------------------------------------------
import functools
import operator

from typing import List, Generator, Any


# -- Definitions ----------------------------------------------------------------

# -------------------------------------------------------------------------------
#  _ __ ___   __ _ _ __  ___
# | '_ ` _ \ / _` | '_ \/ __|
# | | | | | | (_| | |_) \__ \
# |_| |_| |_|\__,_| .__/|___/
#                 |_|
#
# -------------------------------------------------------------------------------
mapmap = lambda f, s: map(functools.partial(map, f), s)



# -------------------------------------------------------------------------------
#            _                                   _     _
#   ___ __ _| |_ __ _ _ __ ___   ___  _ __ _ __ | |__ (_)___ _ __ ___  ___
#  / __/ _` | __/ _` | '_ ` _ \ / _ \| '__| '_ \| '_ \| / __| '_ ` _ \/ __|
# | (_| (_| | || (_| | | | | | | (_) | |  | |_) | | | | \__ \ | | | | \__ \
#  \___\__,_|\__\__,_|_| |_| |_|\___/|_|  | .__/|_| |_|_|___/_| |_| |_|___/
#                                         |_|
#
# -------------------------------------------------------------------------------
foldl  = lambda f, acc, xs: functools.reduce(f, xs, acc)
foldl1 = lambda f, xs: functools.reduce(f, xs)

def unpack(xxs: List[List[Any]]) -> List[Any]:
    return [x for xs in xxs for x in xs]

def unpackG(xxs) -> Generator[Any, List[List[Any]], List[Any]]:
    return (x for xs in xxs for x in xs)

def strip(xs : List[Any]) -> List[Any]:
    # WARNING: alters lengths of list, use carefully
    return [x for x in xs if x]
