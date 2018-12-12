# woffle
#
# @file
# @version 0.1

TEST_PATH=./
LOGFILE=setup.log

.DEFAULT_GOAL := almost

# Making common strings a bit more pretty
RED=\e[31m
GREEN=\e[35m
NONE=\e[0m
BOLD=\e[1m

START=${RED}ᐅ${NONE}
END=⌁ \${BOLD}${GREEN}COMPLETE:${NONE}

#-- General ---------------------------------------------------------------------
.PHONY: all almost py test ft flair spacy
all: clean py ft ftmodel flair spacy
almost: clean py ft flair spacy

clean:
	@printf "${START} Cleaning"
	@find . -name '__pycache__' -or -name '*.log' -exec rm -rf {} +
	@printf "\r${END} clean  \n"

dist-clean:
	@printf "${START} Cleaning"
	@rm -rf build/ dist/ *.egg-info
	@printf "\r${END} dist-clean   \n"

run:
	@printf "${START} Running woffle"
	@python main.py
	@printf "\r${END} run            \n"

check: 
	@printf "${START} Performing type checks"
	@pyre init 
	@pyre --search-path . check
	@printf "${END} Completed type checks\n"


#-- Package installation --------------------------------------------------------
py:
	@printf "${START} Installing: python environment"
	@pip install -r requirements.txt 1>>$(LOGFILE)
	@printf "\r${END} python environment    \n"

ft:
	@printf "${START} Installing: fasttext"
	@pip install git+git://github.com/facebookresearch/fasttext.git 1>>$(LOGFILE)
	@printf "\r${END} fasttext     \n"

ftmodel:
	@printf "${START} Installing: download fasttext model"
	@curl -o models/wiki.en.zip https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip
	@printf "\r${END} download fasttext model    \n"

flair:
	@printf "${START} Installing: flair"
	@pip install flair 1>>$(LOGFILE)
	@python -c "import flair;flair.models.SequenceTagger.load('ner')" 1>>$(LOGFILE) 2>&1
	@python -c "import flair;flair.models.SequenceTagger.load('pos')" 1>>$(LOGFILE) 2>&1
	@python -c "import flair;flair.embeddings.WordEmbeddings('en-news')" 1>>$(LOGFILE) 2>&1
	@printf "\r${END} flair    \n"

# for those without a GPU
flair-fast:
	@printf "${START} Installing: flair-fast"
	@python -c "import flair;flair.models.SequenceTagger.load('ner-fast')" 1>>$(LOGFILE) 2>&1
	@python -c "import flair;flair.models.SequenceTagger.load('pos-fast')" 1>>$(LOGFILE) 2>&1
	@printf "\r${END} flair-fast    \n"

spacy:
	@printf "${START} Installing: spacy"
	@pip install spacy 1>>$(LOGFILE)
	@python -m spacy download en_core_web_sm  1>>$(LOGFILE)
	@printf "\r${END} spacy    \n"

# end
