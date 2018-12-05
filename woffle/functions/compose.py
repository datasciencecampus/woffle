"""
composing functions
"""

#-- Imports ---------------------------------------------------------------------
import functools


#-- Definitions -----------------------------------------------------------------
#+NOTE: application order is last argument through to first
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


# allows people to use compose but in a 'run in this order' way instead of a
# replace commas with function composition way
def compose_(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)
