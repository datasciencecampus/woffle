# woffle

![](https://travis-ci.com/karetsu/woffle.svg?branch=develop)

Please note that this is an active project so some of the instructions are
incomplete and may not yet work. If you find one and there is not an issue
already raised for it then please do so. PRs welcome.

## Introduction

As a follow on from [optimus](https://github.com/datasciencecampus/optimus) this will allow extension of the work to include
arbitrary user defined means of processing their text. The initial aim of this
is to turn optimus from the sprawling tangle of classes that it is into a pure
as possible functional program.

Eventually it will be a way to tie together all your NLP tasks and give you the
option to use whatever back end you like but through a common interface.


## Installation

This program is intended for use on modern linux and macOS operating systems. If
you wish to install it then perform the following actions to get a working
environment including an installation of fasttext, flair and spacy.

``` sh
git clone https://github.com/karetsu/woffle
cd woffle
make
```

If you also wish to download the `wiki.en.zip` vectors for fasttext then also do

``` sh
make ftmodel
```

and if you do not have a CUDA enabled GPU then you may wish to use the flair
models which are optimised for running on CPUs instead

``` sh
make flair-fast
```



## Usage

The intention of this repo is to provide a working example from which to base
your own processing. The minimum example in order to clean text using spacy to
identify nouns and performing simple regex is

``` python

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

For a more complex example which also incorporates text embedding, clustering
and relabelling clusters see `main.py`.

If you wish to build your own back end then please see the instructions on the [website](https://karetsu.github.io/woffle).
