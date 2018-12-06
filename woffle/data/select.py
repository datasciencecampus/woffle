# an idea of how this should work
import operator

# given conditions on the cluster and a function to run in each condition then
# do the following in a more abstract way
conditions = [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0]
functions = [lambda x: x, lambda x: x, lambda x: x, lambda x: x]

decide = [(i, j) for i, j in zip(conditions, functions)]


def select(cluster):
    pass


# the actual return is going to be some horrific combination of operator.or_
# and operator.and_ but will mimic the functionality like:
#
# return (
#    ((conditions[0] and functions[0])(cluster))
#    or ((conditions[1] and functions[1])(cluster))
#    or ((conditions[2] and functions[2])(cluster))
#    or ((conditions[3] and functions[3](cluster)))
#    or (''))
#
# we really need to return a functools.reduce with an or over the list of
# (condition[i] and functions[i])(cluster)
#
# this is basically a left fold of the functions of the cluster combined with
# an and - it feels like applicative should be useful here but this is python
# country...
