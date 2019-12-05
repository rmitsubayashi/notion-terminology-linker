import re
from typing import List
from terminology_formatter import format

class TermToAdd:
    def __init__(self, link: str, term: str):
        self.link = link
        # used in formatter
        self.term = term

def add_links(content: str, terminology: List[TermToAdd]) -> str:
    formatted_list = format(terminology)
    for term in formatted_list:
        content = _replace_link(content, term)

    return content

def _replace_link(content: str, term: TermToAdd) -> str:
    regex = term.term + r'(?![^\(]*\)|[^\[]*\]\()'
    link = '[' + term.term + '](' + term.link + ')'
    return re.sub(regex, link, content)