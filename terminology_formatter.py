from collections import OrderedDict
import re

def format(terminology):
    sorted_dict = _sort_terms(terminology)
    return sorted_dict

def _sort_terms(terminology):
    return sorted(terminology, key=lambda x: len(x.term), reverse=True)