---
currentMenu: sentiment
---

# Sentiment Analysis

The current implementation uses the rudamentary functionality
available in the `TextBlob` python package.The `embed` function 
uses polarity to assign scores to strings which then can be used in
conjunction with clustering or other techniques. 

# Sentiment module in woffle

The sentiment part of woffle currently contains deterministic
clustering, sentiment embed based on `TextBlob` and deterministic
parsing.

All of the following can be imported in python as:

```python
from woffle.sentiment import cluster, embed, parse
``` 

For an example pipeline please refer to the `sentiment.py` in
the `examples` directory.

## Structure of the example file:

Firstly it imports the relevant parts of the pipeline as 
described in the previous section.

It then loads in the `example_comments.txt` from the `data` folder
then `parses` them and `embeds` them. 

These scores are then clustered and a rudamentary plot of the
outcome of the clustering is presented. 

