
#-- Imports ---------------------------------------------------------------------
import pytest
from woffle.functions.compose import *


#-- Tests -----------------------------------------------------------------------
def test_id():
    assert id(1) is 1

