"""
spaCy selection functionality

The important function here is the select function which has signature
select :: [String] -> String, everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# third party
import spacy
import toml

# project
from woffle.functions.compose import compose


#-- Definitions -----------------------------------------------------------------
config = toml.load('config.toml')
# load the spacy model
proc = spacy.load(config['spacy']['model'])





select = lambda x: x
