# Setting the scene for doing heirarchical clustering as a task
# this obfuscates all of the much uglier name space stuff and gives you
# the bits you need for the task


import woffle.parse.deter.parse as dp
import woffle.parse.prob.spacy as pp

from woffle.embed.numeric.fasttext import embed, embed_
from woffle.cluster.deter import cluster

from woffle.functions.generics import compose, compose_

from woffle.select.lexical import select, select_

# parse  = compose(pp.parse,  dp.parse)
# parse_ = compose(pp.parse_, dp.parse_)
parse  = dp.parse
parse_ = dp.parse_
