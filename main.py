"""
classification of free text descriptions
"""

#-- Imports ---------------------------------------------------------------------
# third party
import spacy

# Project specific
import src.data as data

#--
# Definitions -----------------------------------------------------------------


def main():
    activated  = spacy.prefer_gpu()
    nlp = spacy.load('en')

    fp = 'data/test.txt'
    text = [i.replace("\n", "") for i in open(fp, 'r').readlines()]
    if not text:
        raise ValueError("No descriptions to process")

    cleaned = [data.clean(desc) for desc in text]
    target = [word for word in data.select(text, nlp)]

    with open('output/test.csv', 'w') as file:
        file.write("original,label")
        for i,j in zip(descs, target):
            file.write(f"{i},{j}")


#-- Boilerplate -----------------------------------------------------------------
if __name__ == '__main__':
    main()

