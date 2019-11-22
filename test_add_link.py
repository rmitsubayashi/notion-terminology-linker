import unittest

from add_link import add_links
from add_link import TermToAdd

class AddLinkTest(unittest.TestCase):
    def test_basic(self):
        result = add_links(
            "単語",
            [TermToAdd("link", "単語")]
        )
        self.assertEqual("[単語](link)", result)
    
    def test_multiple_terms(self):
        result = add_links(
            "単語1 単語2",
            [TermToAdd('link1', '単語1'),
            TermToAdd('link2', '単語2')]
        )
        self.assertEqual("[単語1](link1) [単語2](link2)", result)
    
    def test_multiple_matches(self):
        result = add_links(
            "単語 単語",
            [TermToAdd("link", "単語")]
        )
        self.assertEqual("[単語](link) [単語](link)", result)

    def test_overlapping_terminology(self):
        result = add_links(
            "単語帳 単語",
            [TermToAdd("link1", "単語"),
            TermToAdd("link2", "単語帳")]
        )
        self.assertEqual("[単語帳](link2) [単語](link1)", result)

    def test_link_in_text(self):
        result = add_links(
            "[a 単語 in](link)",
            [TermToAdd("link", "単語")]
        )
        self.assertEqual("[a 単語 in](link)", result)

    # []()の()のところをマッチするRegex書けなかった。
    # なので英語の用語は省く。じゃないとリンクの中にリンクが埋め込まれる。
    # やりたかったけどできなかったこと：']('と')'の間にあるマッチ
    # '('と')'の間のマッチは取れるが、それだと普通の文章中のカッコと被る 
    def test_english(self):
        result = add_links(
            "[english](english url)",
            [TermToAdd("link", "english")]
        )
        self.assertEqual("[english](english url)", result)

if __name__ == '__main__':
    unittest.main()