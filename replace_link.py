import re
from typing import List
from terminology_formatter import format

class TermToReplace:
    def __init__(self, old_url, new_url, term):
        self.old_url = old_url
        self.new_url = new_url
        #used in formatter
        self.term = term

def replace_links(content: str, terminology: List[TermToReplace]) -> str:
    formatted_list = format(terminology)
    for term in formatted_list:
        content = _replace_link(content, term)
    return content

def _replace_link(content: str, term: TermToReplace) -> str:
    regex = r'(\[)([^\]]*)(\]\()(' + term.old_url + r')(\))'
    to_replace = r'\1' + term.term + r'\3' + term.new_url + r'\5'
    return re.sub(regex, to_replace, content)