"""
Identity functions for different types (for use with typing)
"""

#-- Imports ---------------------------------------------------------------------
from typing import Any

#-- Definitions -----------------------------------------------------------------
# polymorphic
def id(x : Any) -> Any:
    return x
