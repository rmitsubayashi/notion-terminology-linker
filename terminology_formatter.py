from collections import OrderedDict
import re

def format(terminology):
    filtered_dict = _filter_terms(terminology)
    sorted_dict = _sort_terms(filtered_dict)
    return sorted_dict

def _filter_terms(terminology):
    result = []
    for term in terminology:
        if not _is_alnum(term.term):
            result.append(term)
    return result

# python alnum considers Japanese characters as alphabet
def _is_alnum(string: str) -> bool:
    return re.match('^[a-zA-Z0-9]+$', string)

def _sort_terms(terminology):
    return sorted(terminology, key=lambda x: len(x.term), reverse=True)