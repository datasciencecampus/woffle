---
currentMenu: themedesc
layout: default
---

# Introduction

`woffle` is built to allow users to perform their NLP based tasks through a
common interface regardless of their choice of back end processing. The
directory hierarchy of the program is task based and because there are so many
different tasks, which can be split further into probabilistic and deterministic
tasks and so `the.import.namespaces.look.rather.messy.and.long`. To circumvent
having to import these things for all tasks there are pre-packaged import blocks
which we refer to as **themes**.

A theme is a way of masking the import block for specific tasks giving the
functions to use with less hassle. The following themes are included in the
current version of the repository

- [**hierarchical clustering**](hcluster.html)
- [**sentiment analysis**](sentiment.html)


Each theme comes with default parsing, embedding (sentiment can be
considered as a mapping from a string into a numeric representation space so the
interface is still referred to as an embedding), clustering and representative
label selection for the cluster options. Please see the links above (or in the
sidebar) for instructions on how to use each of these themes and what their
default builds look like.

If a theme does not meet your needs then I hope that this project makes it easy
enough for you to compose your own processing means. Each step is supposed to be
composable with the previous so long as the correct data type is presented at
each return statement. For more information on how to build a custom processing
procedure then please see the [advanced use](advanced.html) page.


# The breakdown of a theme

Each theme consists of at most four parts

1. Parsing
2. Embedding
3. Grouping
4. Labelling

where these parts are purposefully left quite loosely defined. This allows us to
consider sentiment scores as a mean of embedding by thinking it as mapping text
onto the numeric value corresponding to its sentiment. The internal workings of
each of these things can differ based on projects but we offer some opinionated
defaults for each theme. 

## 1. Parsing

An endomorphism of strings, the default properties of this function across all
projects are deterministic replacements of some items based on matching regular
expressions. The list of all expressions to match is defined in `./etc/regex`
in the form `pattern = replacement`. It is also possible to encode specific
patterns into a replacement and this is split out into `./etc/encoding` but the
functionality is the same. 

### Default functionality

```python
with open('etc/regex') as f:
    replace = toml.load(f)

with open('etc/encoding') as f:
    encode = toml.load(f)

def regexes(r : dict, x : str) -> str:
    return compose(*[zfunctools.partial(re.sub, i, j, flags=re.IGNORECASE)
                for i,j in r.items()])(x)

replacements = functools.partial(regexes, replace)
encoding     = functools.partial(regexes, encode)

parse_ = compose( encoding
                , replacements
                , str.strip
                )

parse = functools.partial(map, parse_)
```

There are, however, probabilistic techniques included in `woffle.parse.prob` in
the form of [spaCy](https://spacy.io) functions. For example, the spacy `parse()` function
converts your text into a spacy `doc` data type before extracting the root of
the phrase, lemmatising it and checking that it is part of the spacy vocabulary
for your chosen language. 

If you wish to use this then you can simply compose them using our provided function
```python
from woffle.parse.deter import parse as dp
from woffle.parse.prob.spacy import parse as pp

from woffle.functions.generics import compose

parse = compose(pp, dp)
```


## 2. Embedding

Any function which maps strings into a numeric space is suitable here. For
hierarchical clustering this takes the form of functions which map strings onto
real valued vectors or perhaps strings to integer valued vectors if you wish to
use term frequency for this. For the included themes the sentiment theme
includes a mapping from string onto `{-1,0,1}` to represent sentiment polarity. 

The interface to this should be provided as `embed()` regardless of which mechanism you
use. 


## 3. Grouping

A similarly abstract concept, this can vary from grouping values based on like
sentiment polarity score to Ward linkage which is provided through the
`hcluster` theme as its default operation. 

## 4. Labelling

This step is very important for the hierarchical clustering theme (see
`./examples/optimus.py` for what it means to perform this in an unsupervised
classification task) where labels are generated through a multi-faceted decision
tree but this task is also available in sentiment where we simply map `{-1,0,1}`
onto the representative `{negative, neutral, positive}` for each piece of text.


## Pre-packaged themes

We provide, as of this version of the woffle template, themes for hierarchical
clustering tasks and sentiment polarity classification tasks. These are
augmented by examples of building both of these using woffle in `./examples` and
the examples are expected to inform you on how to go about these things. 

If you want to perform a task which is not already available or find a bug,
please fork the repo or raise an issue using the appropriate ticket template. 
