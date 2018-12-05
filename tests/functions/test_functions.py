
#-- Imports ---------------------------------------------------------------------
import pytest
from woffle.functions.id import *


#-- Tests -----------------------------------------------------------------------
def test_id():
    assert id(1) is 1

