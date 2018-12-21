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
