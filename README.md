# woffle

[![Project Status: WIP – Initial development is in progress, but there has not
yet been a stable, usable release suitable for the
public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


Please note that this is an active project so some of the instructions are
incomplete and may not yet work. If you find one and there is not an issue
already raised for it then please do so. PRs welcome.


As a follow on from [optimus](https://github.com/datasciencecampus/optimus) this
will allow extension of the work to include
arbitrary user defined means of processing their text. The initial aim of this
is to turn optimus from the sprawling tangle of classes that it is into a pure
as possible functional program.

Eventually it will be a way to tie together all your NLP tasks and give you the
option to use whatever back end you like but through a common interface.


## Introduction

`woffle` is a project template which aims to allows you to compose various NLP
tasks via a common interface using each of the most popular currently available
tools. This includes

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
program runs to prevent any late exceptions being raised. This is currently not
yet implemented but is in the immediate tasks to perform.


## Installation

`woffle` is intended for use on modern linux and macOS operating systems. This
is due to the dependency on GNU `make`, `curl` et al. (see the contents of
`Makefile` for more details. If you are comfortable setting up the dependencies
in Windows I don't believe that there is a reason it should not work.


The standard installation, including an installation of fasttext (but without a
model), flair and spacy looks like:

``` sh
git clone https://github.com/datasciencecampus/woffle
cd woffle
make
```

If you also wish to download the `wiki.en.zip` vectors for fasttext then add:

``` sh
make ftmodel
```

and if you do not have a CUDA enabled GPU then you may wish to use the flair
models which are optimised for running on CPUs instead:

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

For more on the included **themes** please see the
[documentation](https://datasciencecampus.github.io/woffle/themes.md). If you wish to
build your own back end then please see the instructions on the
[website](https://datasciencecampus.github.io/woffle).
