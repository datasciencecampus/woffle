"""
Useful functions for later
"""

#-- Imports ---------------------------------------------------------------------
import functools


#-- Definitions -----------------------------------------------------------------
#+NOTE: application order is last argument through to first
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# polymorphic
id = lambda x: x
