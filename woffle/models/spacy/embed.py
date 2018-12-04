"""
spaCy embedding functionality

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# third party
import spacy
import toml

# project
from woffle.functions.compose import compose


#-- Definitions -----------------------------------------------------------------
config = toml.load('config.ini')
# load the spacy model
proc = spacy.load(config['spacy']['model'])



embed = lambda x: x
