"""
spaCy embedding functionality

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

# -- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List, NewType


# third party
import spacy
import toml


# project
from woffle.functions.compose import compose
from woffle.functions.id import id


# -- Type synonyms ---------------------------------------------------------------
# TODO: Pyre doesn't really pick up or enforce this type signiture unfortunately.
# The type for the model is spacy.lang.en.English (for en_core_web_md)
Model = NewType("Model", int)


# -- Definitions -----------------------------------------------------------------

# variables
config = toml.load("config.ini")
model = spacy.load(config["spacy"]["model"])


# functions
def embedding(m: Model, x: str) -> List[float]:
    return m(x).vector.tolist()

  
embed = functools.partial(embedding, model)