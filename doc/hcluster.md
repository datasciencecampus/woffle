---
currentMenu: hcluster
layout: default
---

# Hierarchical Clustering

Performing unsupervised hierarchical clustering of text. This theme mimics the
functionality found in [optimus](https://github.com/datasciencecampus/optimus)
but in a more functional manner.

## Default options

You are expected to load your text files into a list or generator expression
with each piece of text as a separate entry.


### Parsing

Configuration of the parsing of text can be placed in `./etc/{regex,encoding}`.
The default `parse()` function is an endomorphism of strings and performs the
following operations sequentially

* `str.strip` - remove whitespace from the start and end of the string
* `regex` - perform replacement of regex patterns defined in `./etc/regex` of
  the form `pattern = replacement`
* `encode` - as found in regex but the replacements are usually non-empty, this
  can enable removal of long common words which can influence embeddings negatively


### Embedding

This theme uses [fastText](https://github.com/facebookresearch/fasttext) to
obtain its real valued vector representations of the text it is given. This is
chosen as it is very good at dealing with words which are out of dictionary,
which more traditional embeddings such as word2vec and gloVe cannot handle. 


### Clustering

Ward linkage is chosen as the default mechanism for clustering the numeric
vectors generated in the embedding stage. This creates a dendrogram containing
every single point to be clustered and can be quite computationally costly.
However, it is very good for generating clusters for use in creating a
hierarchy. At a given depth the `cluster()` function will return which points
have been clustered at that point, including all of those which are still
singletons. 


### Label Selection

Following the clustering stage a label is selected using the optimus approach.

1. Firstly a test for all of the cluster's contents being similarly spelt
   happens, if the edit distance is small then one of the spellings is chosen to
   be representative of all of the cluster and is chosen as the label. 
2. If the edit distance is too large then the text in the cluster is tested to
   see if there are common words across them. If this is the case then this
   common word is chosen to be representative of the cluster and assigned as the
   label for all of the items it contains. 
3. Should there be no common word for all of the items in the cluster then we
   look for a common substring. If this is the case and that string is
   sufficiently long then this string is assigned.
4. Following all of the above, if none of them are suitable for labelling the
   cluster then we make use of the WordNet database provided by Princeton
   University and find the lowest common ancestor for all of the terms in the
   cluster. If this fails because the items are too generically related (e.g.
   the lookup comes back as `object` or something similarly abstract) then the
   cluster remains unlabelled.

For more on this theme please see `./examples/optimus.py` which is a working
implementation of the full optimus program in woffle.
