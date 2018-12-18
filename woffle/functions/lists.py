import functools
import operator


foldl  = lambda f, acc, xs: functools.reduce(f, xs, acc)
foldl1 = lambda f, xs: functools.reduce(f, xs)
