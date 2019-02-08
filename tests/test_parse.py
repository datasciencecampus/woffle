# ---------------------- Imports ------------------------------------------------
# third party
import toml
import functools
import re
import pytest
import hypothesis.strategies as st

from hypothesis import given, assume, example, settings

# generic
import woffle.functions.generics as gen

# parsing
import woffle.parse.deter.parse as dparse


# ---------------------- Functions: Deter Parse ---------------------------------

def configs_fixture():
    with open('etc/regex') as f:
        replace = toml.load(f)
    with open('etc/encoding') as f:
        encode = toml.load(f)
    return replace, encode
replace, encode = configs_fixture()

@given(st.one_of([st.just(replace),
                  st.just(encode)]),
       st.text())
def test_dregexes_basic(r, x):
    r1 = gen.compose(*[functools.partial(re.sub, i, j, flags=re.IGNORECASE)
                       for i, j in r.items()])(x)
    r2 = dparse.regexes(r, x)
    
    assert type(r2) == str
    assert r1 == r2

@given(st.text())
def test_dparse_(s):
    result = dparse.parse_(s)
    
    assert type(result) == str
   
@given(st.lists(st.text()))
def test_dparse(xs):
    r1 = list(map(dparse.parse_,xs))
    r2 = list(dparse.parse(xs))

    assert r1 == r2

