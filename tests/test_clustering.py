# ---------------------- Imports ------------------------------------------------
# third party
import functools
import pytest
import hypothesis.strategies as st
import hypothesis.extra.numpy as stnp
import numpy as np

from hypothesis import given 


# clustering
import woffle.cluster.deter.cluster as dcluster

# ---------------------- Functions: Deter Cluster -------------------------------

@given(stnp.arrays(dtype=np.float, elements=st.floats(-1,1), shape=(200,100)),
       st.integers(min_value=1)
)
def test_dcluster(arr, d):
    result = dcluster(arr, d)
    
    assert hasattr(result,"__iter__") 
