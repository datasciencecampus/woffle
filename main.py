"""
classification of free text descriptions
"""

#-- Imports ---------------------------------------------------------------------
# third party
import spacy

# Project specific
import src.data as data


#-- Definitions -----------------------------------------------------------------
def main():
    activated  = spacy.prefer_gpu()
    nlp = spacy.load('en')

    fp = 'data/test.txt'
    text = [i for i in open(fp, 'r').readlines()]
    if not text:
        raise ValueError("No descriptions to process")

    cleaned = [data.clean(line) for line in text]
    corpus  = [nlp(line) for line in cleaned]
    target  = [data.parse(doc) for doc in corpus]

    # TODO: rewrite this mess
    with open('output/test.csv', 'w+') as file:
        file.write("original,label\n")
        for i,j in zip(text, target):
            original = i.replace('\n', '')
            label = j + '\n'
            file.write(f"{original},{label}")


#-- Boilerplate -----------------------------------------------------------------
if __name__ == '__main__':
    main()
