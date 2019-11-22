from typing import List

class TermToRemove:
    def __init__(self, link: str, term: str):
        self.link = link
        self.term = term

def remove_links(content: str, terminology: List[TermToRemove]):
    for term in terminology:
        content = _remove_link(content, term)
    return content

def _remove_link(content, term: TermToRemove):
    return content.replace('['+term.term+']('+term.link+')', term.term)