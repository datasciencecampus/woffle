"""
sentiment score embedding

The import function here is 'embed' which has signature
embed :: String -> [Float]. There is also a non-mapped version 
name embed_
"""
# base
import functools

# third party
from textblob import TextBlob

embed_ = lambda string: TextBlob(string).polarity
embed  = functools.partial(map, embed_)
