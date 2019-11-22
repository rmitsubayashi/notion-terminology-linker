import unittest

from replace_link import replace_links
from replace_link import TermToReplace

class ReplaceLinkTest(unittest.TestCase):
    def test_basic(self):
        result = replace_links(
            '[単語州](link)',
            [TermToReplace('link', 'new_link','単語集')]
        )
        self.assertEqual('[単語集](new_link)', result)

    def test_multiple_terms(self):
        result = replace_links(
            '[単語州](link1) [全単語州](link2)',
            [TermToReplace('link1', 'new_link1', '単語集'),
            TermToReplace('link2', 'new_link2', '全単語集')]
        )
        self.assertEqual('[単語集](new_link1) [全単語集](new_link2)', result)

    def test_multiple_matches(self):
        result = replace_links(
            '[単語州](link) [単語州](link)',
            [TermToReplace('link', 'new_link','単語集')]
        )
        self.assertEqual('[単語集](new_link) [単語集](new_link)', result)

if __name__ == '__main__':
    unittest.main()