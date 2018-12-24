"""
Identity functions for different types (for use with typing)
"""

#-- Imports ---------------------------------------------------------------------
import functools

from typing import Any


#-- Definitions -----------------------------------------------------------------
# polymorphic
def id(x : Any) -> Any:
    return x


#+NOTE: application order is last argument through to first
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


# allows people to use compose but in a 'run in this order' way instead of a
# replace commas with function composition way
def compose_(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)
