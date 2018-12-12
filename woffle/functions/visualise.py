"""
a function to output a sample of the embeddings 

visualise  -> shows the data straight in the browser,
visualise_ -> saves the data into 'embedding_plot.html'

"""

# -- Imports ---------------------------------------------------------------------
# base 
import functools

from typing import List

# third party
import numpy as np
import bokeh 

from bokeh.plotting import figure, save, show, output_file
from sklearn.manifold import TSNE

# project
from woffle.functions.compose import compose

# -- Bokeh Settings ---------------------------------------------------------------

output_file('embedding_plot.html')
fig = figure()

# -- Type synonyms ----------------------------------------------------------------

Array  = NewType('Array' , np.ndarray )
Figure = NewType('Figure', bokeh.plotting.figure.Figure)

# -- Definitions ------------------------------------------------------------------

tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=1000).fit_transform

def scatterplot(data : Array, fig : Figure):
    fig.scatter(data[:,0], data[:,1])
    return fig
scatter = functools.partial(scatterplot, fig=fig)

# -- Compose functions  -----------------------------------------------------------

visualise  = compose(show, scatter, tsne)
visualise_ = compose(save, scatter, tsne)
