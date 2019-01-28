"""
bert embedding functionality

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List, NewType

# third party
import torch
import toml
from pytorch_pretrained_bert import BertTokenizer, BertModel

# project
from woffle.functions.generics import compose
from woffle.functions.generics import id


#-- Type synonyms ---------------------------------------------------------------
Model = NewType('Model', BertModel)
Tokenizer = NewType('Tokenizer', BertModel)

#-- Definitions -----------------------------------------------------------------

# variables
config    = toml.load('config.ini')
model     = BertModel.from_pretrained(config['bert']['model'])
tokenizer = BertTokenizer.from_pretrained(config['bert']['model'])


def embedding(text: str, m: Model, t: Tokenizer):
    tokens = t.tokenize(text)
    ids    = t.convert_tokens_to_ids(tokens)
    _, CLS = m(torch.tensor([ids]))
    return CLS.reshape(CLS.shape[-1]).tolist()

embed_ = functools.partial(embedding, m=model, t=tokenizer)
embed  = functools.partial(map, embed_)
