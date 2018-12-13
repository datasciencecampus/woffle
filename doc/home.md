---
currentMenu: home
layout: default
---

# Welcome

Please note that this is an active project so some of the instructions are
incomplete and may not yet work. If you find one and there is not an issue
already raised for it then please do so.


## Introduction

`woffle` is a meta-API which allows you to compose various NLP tasks via a
common interface using each of the most popular currently available tools. This
includes

- spaCy
- fastText
- flair
- others coming soon


The project was borne out of frustrations in trying to tie together all of the
methods and attributes of each of popular NLP programs. I intend to have the
program broken down into composable tasks where each task takes some 'sensible'
default operations and when you import a specific part of the tool then it only
exposes that one thing and these tasks will be separated by whether they are
deterministic processing or whether the output is probabilistically generated
(it makes it easier to control what models are left hanging around).

Currently the tasks we aim to perform are

- **parsing**
  including replacement of a list of regex strings defined in a configuration file
- **embedding**
  not only generating numeric vectors from your text using
  fasttext, spacy's gloVe implementation and similar but I envision that this
  should also include tasks such as topic modelling and semantic analysis
  purely because they are mappings from your text into some kind of
  representation space
- **clustering**
  deterministic (e.g. Ward linkage) clustering and proabilitistic clustering
  will be included
- **selection**
  the ability to replace the content of a cluster
  with a representative 'label', in optimus this is based on functions of the
  cluster based on decisions on the content of the cluster but this could be as
  simple as replacing the the cluster with its sentiment score


These functions will be called the same thing regardless of which back end you
use and most importantly they will be composable so that you can chain
deterministic and probabilistic functions together, where it makes sense.

A type checking tool ([pyre](https://pyre-check.org)) will be available to
ensure that any custom pipelines have functions of the same type before the
program runs to prevent any late exceptions being raised.


## Installation

This program is intended for use on modern linux and macOS operating systems. If
you wish to install it then perform the following actions to get a working
environment including an installation of fasttext, flair and spacy.

```sh
git clone https://github.com/karetsu/woffle
cd woffle
make

# If you also wish to download the `wiki.en.zip` vectors for fasttext then also do
make ftmodel

# and if you do not have a CUDA enabled GPU then you may wish to use the flair
#models which are optimised for running on CPUs instead
make flair-fast
```


## Usage

This program is intended to give you a common toolkit without needing to know
the model specific commands to perform the tasks. In order to use the program it
is currently recommended to

```sh
git clone https://github.com/karetsu/woffle myProjectName
```

so that it provides a working directory for specific projects. Included is an
example of how you would use the tool to do some simple parsing of an example
dataset and return the cleaned target phrase for the sentence using a
combination of deterministic (i.e. regex replacements )and probabilistic parsing
(using spaCy) to achieve this goal.

The minimum example in order to clean text using spacy to identify nouns,
selecting the first noun it encounters and doing a little cleaning is

```python
from woffle                   import data
from woffle.functions.compose import compose
from woffle.models            import spacy   as model

fp = 'data/test.txt'
text = [i.replace('\n','') for i in open(fp, 'r').readlines()]

clean = compose(model.parse, data.parse)
cleaned = [clean(line) for line in text]

for i, j in zip(text, cleaned):
    print(f"{i} -> {j}")
```

For more detailed and complex examples please see
[`examples`](https://github.com/karetsu/woffle/tree/master/examples).