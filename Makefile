##
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
all: py ft ftmodel flair spacy
almost: py ft flair spacy

clean:
	@printf "${START} Cleaning"
	@find . -name '__pycache__' -exec rm -rf {} +
	@sleep 4
	@printf "\r${END} clean  \n"

dist-clean:
	@printf "${START} Cleaning"
	@rm -rf build/ dist/ *.egg-info
	@printf "\r${END} dist-clean   \n"

test: clean
	@printf "${START} Testing"
	@pytest --color=yes $(TEST_PATH)
	@printf "${END} testing\n"

run:
	@printf "${START} Running woffle"
	@python main.py
	@printf "\r${END} run            \n"


#-- Package installation --------------------------------------------------------
py:
	@printf "${START} Installing: python environment"
	@pip install -r requirements.txt 1>$(LOGFILE)
	@printf "\r${END} python environment\n"

ft:
	@printf "${START} Installing: fasttext"
	@rm -rf ./fasttext | /bin/true
	@git clone https://github.com/facebookresearch/fasttext 1>/dev/null 2>&1
	@pip install fasttext 1>$(LOGFILE)
	@cd ../ && rm -rf fasttext 1>$(LOGFILE)
	@printf "\r${END} fasttext\n"

ftmodel:
	@printf "${START} Installing: download fasttext model"
	@cd models
	@curl -o wiki.en.zip https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.en.zip
	@cd ../
	@printf "\r${END} download fasttext model\n"

flair:
	@printf "${START} Installing: flair"
	@pip install flair 1>$(LOGFILE)
	@python -c "import flair;flair.models.SequenceTagger.load('ner')" 1>$(LOGFILE) 2>&1
	@python -c "import flair;flair.models.SequenceTagger.load('pos')" 1>$(LOGFILE) 2>&1
	@python -c "import flair;flair.embeddings.WordEmbeddings('en-news')" 1>$(LOGFILE) 2>&1
	@printf "\r${END} flair\n"

# for those without a GPU
flair-fast:
	@printf "${START} Installing: flair-fast"
	@python -c "import flair;flair.models.SequenceTagger('ner-fast')" 1>$(LOGFILE) 2>&1
	@python -c "import flair;flair.models.SequenceTagger('pos-fast')" 1>$(LOGFILE) 2>&1
	@printf "\r${END} flair-fast\n"

spacy:
	@printf "${START} Installing: spacy"
	@pip install spacy 1>$(LOGFILE)
	@python -m spacy download en_core_web_sm  1>$(LOGFILE)
	@printf "\r${END} spacy\n"

# end
