import unittest

from htmlnode import markdown_to_block
from htmlnode import BlockNode

class TestMarkdownParser(unittest.TestCase):
    def test_header1_conversion(self):
        markdown = "# This is a header"
        result = markdown_to_block(markdown)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].block_type, "header1")
        self.assertEqual(result[0].textnodes, ["This is a header"])

    def test_unordered_list_conversion(self):
        markdown = "* Item 1\n* Item 2"
        result = markdown_to_block(markdown)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].block_type, "ulist")
        self.assertListEqual(result[0].textnodes, ["Item 1", "Item 2"])

    def test_paragraph_conversion(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_block(markdown)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].block_type, "paragraph")
        self.assertEqual(result[0].textnodes, ["This is a simple paragraph."])

    def test_empty_lines(self):
        markdown = "\n\n"
        result = markdown_to_block(markdown)
        self.assertEqual(len(result), 0)

    def test_mixed_content(self):
        markdown = "# Header\n\nThis is text.\n\n* List Item 1"
        result = markdown_to_block(markdown)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].block_type, "header1")
        self.assertEqual(result[1].block_type, "paragraph")
        self.assertEqual(result[2].block_type, "ulist")

    def test_headers(self):
        markdown = "# Header1\n## Header2\n### Header3\n#### Header4\n##### Header5\n###### Header6"
        expected = [
            BlockNode(["Header1"], "header1"),
            BlockNode(["Header2"], "header2"),
            BlockNode(["Header3"], "header3"),
            BlockNode(["Header4"], "header4"),
            BlockNode(["Header5"], "header5"),
            BlockNode(["Header6"], "header6")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_unordered_lists(self):
        markdown = "* Item 1\n* Item 2\n- Item 3\n- Item 4"
        expected = [
            BlockNode(["Item 1", "Item 2", "Item 3", "Item 4"], "ulist")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\n3. Item 3"
        expected = [
            BlockNode(["Item 1", "Item 2", "Item 3"], "olist")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_quote(self):
        markdown = ">This is a quote"
        expected = [BlockNode(["This is a quote"], "quote")]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_code_block(self):
        markdown = "```\nCode line 1\nCode line 2\n```"
        expected = [
            BlockNode(["Code line 1", "Code line 2"], "code")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_paragraphs(self):
        markdown = "This is a paragraph.\n\nThis is another paragraph."
        expected = [
            BlockNode(["This is a paragraph."], "paragraph"),
            BlockNode(["This is another paragraph."], "paragraph")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        markdown = "# Header\n* List item 1\n* List item 2\n>Quote here\n```\nCode block\n```\nAnother paragraph."
        expected = [
            BlockNode(["Header"], "header1"),
            BlockNode(["List item 1", "List item 2"], "ulist"),
            BlockNode(["Quote here"], "quote"),
            BlockNode(["Code block"], "code"),
            BlockNode(["Another paragraph."], "paragraph")
        ]
        result = markdown_to_block(markdown)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
