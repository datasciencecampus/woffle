---
currentMenu: start
---
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
combination of deterministic (i.e. regex replacements) and probabilistic parsing
(using spaCy) to achieve this goal.


Below is the minimum code required in order to:

- perform regex based cleaning of the text
- clean text using spacy to identify root nouns
- select the first noun as the target noun
- embed the strings using fasttext
- perform a hierarchical clustering of the vectors
- perform a cutoff at depth 3 to generate clusters
- print all of the generated information


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

For more detailed and complex examples please see
[`examples`](https://github.com/karetsu/woffle/tree/master/examples).
