# ---------------------- Imports ------------------------------------------------
# third party
import toml
import spacy
import pytest
import hypothesis.strategies as st

from hypothesis import given, example, settings

# selection
import woffle.select.lexical.edits as edit
import woffle.select.lexical.wordgrams as wordgrams
import woffle.select.lexical.chargrams as chargrams
import woffle.select.lexical.hypernyms as hypernyms

# ---------------------- Functions: Edit Distance -------------------------------

@given(st.lists(st.text()))
@example([''])
def test_edit_condition(xs):
    result = edit.condition(xs)
    if xs == ['']:
        assert 0.0 == edit.condition(xs)
    
@given(st.lists(st.text()))
def test_edit_editMatrix(xs):
    # Does it run?
    result = edit.editMatrix(xs)

@given(st.lists(st.text(min_size=1), min_size=1))
def test_edit_selection(xs):
    # Does it run?
    result = edit.selection(xs)

# ---------------------- Functions: Wordgrams -----------------------------------

@given(st.from_regex("[a-zA-Z]+"),
       st.integers(min_value=1, max_value=2))
def test_wordgrams_fetch(x, n):
    # Does it run?
    result = wordgrams.fetch(x, n)

@given(st.from_regex("[a-zA-Z]+"))
def test_wordgrams_group(x):
    # Does it run?
    result = wordgrams.group(x)
    
@given(st.lists(st.from_regex("[a-zA-Z]+"), min_size=1))
def test_wordgrams_selection(xs):
    # Does it run?
    result = wordgrams.selection(xs)
    
@given(st.lists(st.from_regex("[a-zA-Z]+"),min_size=1))
def test_wordgrams_condition(xs):
    # Does it run?
    result = wordgrams.condition(xs)

@given(st.lists(st.from_regex("[a-zA-Z]+"), min_size=1))
def test_wordgrams_scorer(xs):
    # Does it run?
    result = wordgrams.scorer(xs)
    
    assert result >= 0 

# ---------------------- Functions: Chargrams -----------------------------------


@given(st.lists(st.from_regex("[A-z]{3,10}", fullmatch=True), min_size = 1)) 
def test_chargrams_selection(xs):
    # Does it run?
    result = chargrams.selection(xs)
    
@given(st.lists(st.from_regex("[A-z]{3,10}", fullmatch=True), min_size = 0)) 
def test_chargrams_condition(xs):
    # Does it run?
    result = chargrams.condition(xs)

@given(st.lists(st.from_regex("[A-z]{3,10}", fullmatch=True), min_size = 1)) 
def test_chargrams_scorer(xs):
    # Does it run?
    result = chargrams.scorer(xs)
    
    assert result >= 0 

# ---------------------- Functions: Hypernyms -----------------------------------


@given(st.lists(st.from_regex("[A-z]{3,10}", fullmatch=True), min_size = 0)) 
@settings(deadline=None)
def test_hypernyms_selection(xs):
    # Does it run?
    result = hypernyms.selection(xs)
    
@given(st.lists(st.from_regex("[A-z]{3,10}", fullmatch=True), min_size = 0)) 
def test_hypernyms_condition(xs):
    # Does it run?
    result = hypernyms.condition(xs)
