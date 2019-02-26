---
currentMenu: home
layout: default
---

`woffle` aims to be an opinionated (but sensible) project template for the
majority of your language processing tasks.

What this means is that by default it *prefers* some tools over others. However,
we have tried to make it as easy as possible for you to quickly add your own
code in to perform additional functionality whilst still fitting
in and communicating well with all of the other pieces.


Working on projects such as
[pyGrams](https://github.com/datasciencecampus/pygrams),
[pelican cove](https://github.com/datasciencecampus/pelican_cove) and
[optimus](https://github.com/datasciencecampus/optimus) it became clear that our
NLP projects generally consist of up to 4 tasks.

1. **Parsing**
   Data tends to need cleaning before we can really do a lot of NLP stuff with
   it.
2. **Embedding**
    Because computers are really bad at understanding language we come
    pre-packed with various ways of converting all of that text into numbers so
    that your computer can do stuff. This can sometimes seem like a contrivance
    where we consider sentiment scores for text as an 'embedding' but all we
    mean is "generating a numeric representation for text" and this hopefully
    follows.
3. **Clustering**
   Whether grouping sentences with like sentiment, generating hierarchical
   classifications of text or looking at some density based clustering
   mechanisms it often helps to collect things that are similar to understand
   what is going on.
4. **Selection**
   Oftentimes, such as when generating a hierarchical classification of things,
   we want to replace a cluster of text with a single entity in some way.

Now I'll be able to do these faster and with less code using `woffle`. If you
wish to implement your task using woffle then please see [Getting
Started](./getstarted.md).
