"""
Term Frequency - Inverse Document Frequency embedding

The important function here is 'embed' which has signature
embed :: String -> [Float], everything else should just be part of it
"""

#-- Imports ---------------------------------------------------------------------
# base
import functools

from typing import List

# third party
import textacy
import numpy as np

#-- Functions -------------------------------------------------------------------

def embed(xs : List[str]) -> List[float]:
    v = textacy.vsm.Vectorizer(apply_idf=True)
    xs_ = [x.split() for x in xs]
    intermediary = v.fit_transform(xs_).todense()
    return [np.array(i) for i in intermediary]
