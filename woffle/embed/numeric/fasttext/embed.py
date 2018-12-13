"""
fasttext embedding functionality

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List, NewType

# third party
import fastText
import toml

# project
from woffle.functions.compose import compose
from woffle.functions.id      import id


#-- Type synonyms ---------------------------------------------------------------
Model = NewType('Model', fastText.FastText._FastText)


#-- Definitions -----------------------------------------------------------------

# variables
config = toml.load('config.ini')
model = fastText.load_model(config['fasttext']['model'])


def embedding(m: Model, x : str) -> List[float]:
    return m.get_word_vector(x)

embed_ = functools.partial(embedding, model)
embed  = functools.partial(map, embed_)
