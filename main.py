"""
classification of free text descriptions
"""

#-- Imports ---------------------------------------------------------------------

# Project specific
from woffle        import data
from woffle.models import spacy as model


#-- Definitions -----------------------------------------------------------------
def main():

    fp = 'data/test.txt'
    text = [i.replace('\n','') for i in open(fp, 'r').readlines()]
    if not text:
        raise ValueError("No descriptions to process")

    cleaned = [data.clean(line) for line in text]
    corpus  = [model.nlp(line) for line in cleaned]
    parsed  = [data.parse(doc) for doc in corpus]

    target = [word if word in nlp.vocab else None for word in parsed]



    # TODO: rewrite this mess
    with open('output/test.csv', 'w+') as file:
        file.write("original,label\n")
        for i,j in zip(text, target):
            file.write(f"{i},{j}" + '\n')


#-- Boilerplate -----------------------------------------------------------------
if __name__ == '__main__':
    main()
