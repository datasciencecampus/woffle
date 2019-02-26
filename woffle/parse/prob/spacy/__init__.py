# list operations
from .parse import parse

# element operations
from .parse import parse_

# needed by other parts
from .parse import roots

# spacy settings
import spacy
activated = spacy.prefer_gpu()
