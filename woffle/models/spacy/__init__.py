"""
spaCy back end

includes the common functions for NLP in the spaCy way
"""

#-- Imports ---------------------------------------------------------------------
import spacy


#-- Definitions -----------------------------------------------------------------
activated  = spacy.prefer_gpu()
nlp = spacy.load('en_core_web_md')
