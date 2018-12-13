"""
flair embedding functionality

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List, NewType

# third party
import flair
import toml

# project
from woffle.functions.compose import compose
from woffle.functions.id      import id

#-- Type synonyms ---------------------------------------------------------------
# TODO: Pyre doesn't really pick up or enforce this type signiture unfortunately. The type for the model is spacy.lang.en.English (for en_core_web_md)
Model = NewType('Model', int)

#-- Definitions -----------------------------------------------------------------

# variables
config = toml.load('config.ini')
model = flair.embeddings.WordEmbeddings(config['flair']['model']).precomputed_word_embeddings


# functions
def embedding(m: Model, x : str) -> List[float]:
    return (x in m.vocab and m.get_vector(x).tolist()) or []


embed_ = functools.partial(embedding, model)
embed = functools.partial(map, embed_)
