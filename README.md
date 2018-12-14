# woffle

[![Project Status: WIP – Initial development is in progress, but there has not
yet been a stable, usable release suitable for the
public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


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
your own processing. Below is the minimum code required in order to:

- perform regex based cleaning of the text
- clean text using spacy to identify root nouns
- select the first noun as the target noun
- embed the strings using fasttext
- perform a hierarchical clustering of the vectors
- perform a cutoff at depth 3 to generate clusters
- print all of the generated information

This accepts the default actions and structure of the 'hcluster' (hierarchical
clustering) theme. Should you want to 'roll your own' processing please see the
manual on the website.


```python
# import the required parts of the toolkit
from woffle.hcluster import parse, embed, cluster

with open('data/test.txt') as handle:
  text = handle.read().splitlines()

target = parse(text)  # note, generator, not yet evaluated
embed = [i for i in embed(target)] # clusters cannot yet use generators
clusters = [i for i in cluster(embed, text, 3)]

target = parse(text) # generator has been consumed at this point in the above!
pairs  = ((i,j) for i,j in zip(text, target))
for o, t in pairs:
    entrant = [cluster.tolist() for cluster in clusters if o in cluster]
    print(f"{o:>30s}: {t:15s} -> {entrant[0]}")

```

For a more complex example which also incorporates text embedding, clustering
and relabelling clusters see `main.py`.

If you wish to build your own back end then please see the instructions on the [website](https://karetsu.github.io/woffle).
