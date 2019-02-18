# ---------------------- Imports ------------------------------------------------
# third party
import functools
import pytest
import hypothesis.strategies as st

from hypothesis import given 

# generic
import woffle.functions.lists as lst
import woffle.functions.generics as gen

# ---------------------- Functions: Lists ---------------------------------------

@given(st.lists(st.lists(st.floats())))
def test_unpack(xxs):
    assert lst.unpack(xxs) == [x for xs in xxs for x in xs]

@given(st.lists(st.text()))
def test_strip(xs):
    assert lst.strip(xs) == [x for x in xs if x]

# ---------------------- Functions: Generics ------------------------------------

@given(st.one_of([st.integers(), st.text()]))
def test_id(i):
    assert gen.id(i) == i

@given(st.lists(st.integers()))
def test_composition_basic(integers):
    comp = gen.compose(str, sum, functools.partial(map, int))
    assert callable(comp)  
    assert comp(integers) == str(sum(map(int,integers)))

@given(st.just(len),
       st.just(range),
       st.lists(st.floats())
)
def test_composition_alternative(f1,f2, value):
    r1 = gen.compose_(f1,f2)(value) 
    r2 = f2(f1(value))
    assert r1 == r2
