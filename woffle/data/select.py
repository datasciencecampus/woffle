# an idea of how this should work
# +TODO: write these two, they are super simple
# from woffle.functions.lists import head, tail
head = lambda l: l[0]
tail = lambda l: l[1:]


# given conditions on the cluster and a function to run in each condition then
# do the following in a more abstract way
conditions = [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0]
functions = [lambda x: x, lambda x: x, lambda x: x, lambda x: x]

zipped = zip(conditions, functions)


def decide(fs, x):
    return [i(x) and j(x) for i, j in fs]


def select(cluster):
    return head(cluster) or select(tail(cluster))


# this code will not work, but the plan here then is that we can just use a
# combination of decide and select to combine the functions on the values
# in the way we want - its the most obvious way to get what we want
#
# decide is also horrific in terms of computation, we will turn this into a
# generator function so as to only process the decision as far as is needed
