# ---------------------- Test setup imports -------------------------------------
import pytest
import hypothesis.strategies as st

from hypothesis import given, assume, example, settings
from hypothesis.extra import numpy as stnp
# auxilary modules for test cases
import functools 
import toml
import re 
import numpy as np
import spacy
import flair
import fastText

# ---------------------- Imports to test ----------------------------------------

# generic
import woffle.functions.lists as lst
import woffle.functions.generics as gen

# parsing
import woffle.parse.deter.parse as dparse
import woffle.parse.prob.spacy.parse as spacy_pparse

# clustering
import woffle.cluster.deter.cluster as dcluster

# embedding
# import woffle.embed.numeric.spacy.embed as sp
# import woffle.embed.numeric.flair.embed as fl
# import woffle.embed.numeric.fasttext.embed as ft

# selection
import woffle.select.lexical.edits as edit
import woffle.select.lexical.wordgrams as wordgrams
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

# ---------------------- Functions: Proba Parse ---------------------------------



# ---------------------- Functions: Deter Cluster -------------------------------

@given(stnp.arrays(dtype=np.float, elements=st.floats(-1,1), shape=(200,100)),
       st.integers(min_value=1)
)
def test_dcluster(arr, d):
    result = dcluster(arr, [], d)
    
    assert hasattr(result,"__iter__") 

# ---------------------- Functions: Spacy ---------------------------------------
   
# def spacy_fixture():
#     config = toml.load("config.ini")
#     model  = spacy.load(config["spacy"]["model"])
#     return model
# spacy_model = spacy_fixture()

# @given(st.just(spacy_model),
#        st.text())
# @settings(deadline=None)
# def test_spacy_embedding(m, s):
#     singular_embedding = sp.embedding(m,s)

#     assert type(singular_embedding) == list

# @given(st.text())
# @settings(deadline=None)
# def test_spacy_embed_(s):
#     result = sp.embed_(s)
    
#     assert type(result) == list
    

# @given(st.lists(st.text()))
# @settings(deadline=None)
# def test_spacy_embed(xs):
#     result = sp.embed(xs)
    
#     assert len(list(result)) == len(xs)

# ---------------------- Functions: Flair ---------------------------------------
# def flair_fixture():
#     config = toml.load("config.ini")
#     model = flair.embeddings.WordEmbeddings(config['flair']['model']).precomputed_word_embeddings
#     return model
# flair_model = flair_fixture()

# @given(st.just(flair_model),
#        st.text())
# def test_flair_embedding(m, s):
#     singular_embedding = fl.embedding(m,s)

#     assert type(singular_embedding) == list

# @given(st.text())
# def test_flair_embed_(s):
#     result = fl.embed_(s)
    
#     assert type(result) == list
    
# @given(st.lists(st.text()))
# def test_flair_embed(xs):
#     result = fl.embed(xs)
    
#     assert len(list(result)) == len(xs)

# ---------------------- Functions: FastText ------------------------------------

# def fasttext_fixture():
#     config = toml.load("config.ini")
#     model = fastText.load_model(config['fasttext']['model'])
#     return model
    
# @given(st.just(flair_fixture()),
#        st.text())
# def test_flair_embedding(m, s):
#     singular_embedding = ft.embedding(m,s)

#     assert type(singular_embedding) == list

# @given(st.text())
# def test_flair_embed_(s):
#     result = ft.embed_(s)
    
#     assert type(result) == list
    
# @given(st.lists(st.text()))
# def test_flair_embed(xs):
#     result = ft.embed(xs)
    
#     assert len(list(result)) == len(xs)


# ---------------------- Functions: Edit Distance -------------------------------

@given(st.lists(st.text()))
@example([''])
def test_edit_condition(xs):
    result = edit.condition(xs)
    if xs == ['']:
        assert 0.0 == edit.condition(xs)
    
@given(st.lists(st.text()))
def test_edit_editMatrix(xs):
    result = edit.editMatrix(xs)

@given(st.lists(st.text(min_size=1), min_size=1))
def test_edit_selection(xs):
    result = edit.selection(xs)

# ---------------------- Functions: Wordgrams -----------------------------------

@given(st.text(), st.integers(min_value=1, max_value=2))
def test_wordgrams_fetch(x, n):
    result = wordgrams.fetch(x, n)

@given(st.text())
def test_wordgrams_group(x):
    result = wordgrams.group(x)

@given(st.text())
def test_wordgrams_group(x):
    result = wordgrams.group(x)
