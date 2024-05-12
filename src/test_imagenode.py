import unittest


from htmlnode import TextNode
from htmlnode import split_nodes_special
from htmlnode import split_nodes_delimiter
from htmlnode import text_to_textnodes

class TestHTMLNode(unittest.TestCase):    
    def test_split_nodes_special_images(self):
            # Test case for splitting nodes with images
            old_nodes = ["This is ![image1](https://example.com/image1.png) and ![image2](https://example.com/image2.png)",
                        "Another node with ![image3](https://example.com/image3.png)"]
            expected_result = [
                TextNode("This is ", "text_type_text"),
                TextNode("image1", "text_type_image", "https://example.com/image1.png"),
                TextNode(" and ", "text_type_text"),
                TextNode("image2", "text_type_image", "https://example.com/image2.png"),
                TextNode("Another node with ", "text_type_text"),
                TextNode("image3", "text_type_image", "https://example.com/image3.png")
            ]
            result = split_nodes_special(old_nodes, subtype="image")
            self.assertEqual(result, expected_result)

    def test_split_nodes_special_links(self):
        # Test case for splitting nodes with links
        old_nodes = ["This is [link1](https://example.com/link1) and [link2](https://example.com/link2)",
                    "Another node with [link3](https://example.com/link3)"]
        expected_result = [
            TextNode("This is ", "text_type_text"),
            TextNode("link1", "text_type_link", "https://example.com/link1"),
            TextNode(" and ", "text_type_text"),
            TextNode("link2", "text_type_link", "https://example.com/link2"),
            TextNode("Another node with ", "text_type_text"),
            TextNode("link3", "text_type_link", "https://example.com/link3")
        ]
        result = split_nodes_special(old_nodes, subtype="link")
        self.assertEqual(result, expected_result)

    def test_split_nodes_special_mixed(self):
        # Test case for splitting nodes with both images and links
        old_nodes = ["This is ![image1](https://example.com/image1.png) and [link1](https://example.com/link1)",
                    "Another node with ![image2](https://example.com/image2.png) and [link2](https://example.com/link2)"]
        expected_result = [
            TextNode("This is ", "text_type_text"),
            TextNode("image1", "text_type_image", "https://example.com/image1.png"),
            TextNode(" and ", "text_type_text"),
            TextNode("link1", "text_type_link", "https://example.com/link1"),
            TextNode("Another node with ", "text_type_text"),
            TextNode("image2", "text_type_image", "https://example.com/image2.png"),
            TextNode(" and ", "text_type_text"),
            TextNode("link2", "text_type_link", "https://example.com/link2")
        ]
        result = split_nodes_special(old_nodes, subtype="image")
        new_result = split_nodes_special(result, subtype="link")
        self.assertEqual(new_result, expected_result)

    def test_split_nodes_special_no_special_nodes(self):
        # Test case for no special nodes to split
        old_nodes = ["This is a regular text node", "Another regular text node"]
        expected_result = [
            TextNode("This is a regular text node", "text_type_text"),
            TextNode("Another regular text node", "text_type_text")
        ]
        result = split_nodes_delimiter(old_nodes,"text_type_text")
        new_result = split_nodes_special(result)
        self.assertEqual(new_result, expected_result)
    def test_text_to_textnodes_bold_italic_code(self):
        # Test case with bold, italic, and code markdown
        text = "This is **bold**, *italic*, and `code` text."
        expected_result = [
            TextNode("This is ", "text_type_text"),
            TextNode("bold", "text_type_bold"),
            TextNode(", ", "text_type_text"),
            TextNode("italic", "text_type_italic"),
            TextNode(", and ", "text_type_text"),
            TextNode("code", "text_type_code"),
            TextNode(" text.", "text_type_text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_images_links(self):
        # Test case with images and links markdown
        text = "This is an ![image](https://example.com/image.png) and a [link](https://example.com/link)."
        expected_result = [
            TextNode("This is an ", "text_type_text"),
            TextNode("image", "text_type_image", "https://example.com/image.png"),
            TextNode(" and a ", "text_type_text"),
            TextNode("link", "text_type_link", "https://example.com/link"),
            TextNode(".", "text_type_text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_mixed(self):
        # Test case with mixed markdown
        text = "**Bold** and *italic* text with ![image](https://example.com/image.png) and [link](https://example.com/link)."
        expected_result = [
            TextNode("Bold", "text_type_bold"),
            TextNode(" and ", "text_type_text"),
            TextNode("italic", "text_type_italic"),
            TextNode(" text with ", "text_type_text"),            
            TextNode("image", "text_type_image", "https://example.com/image.png"),
            TextNode(" and ", "text_type_text"),
            TextNode("link", "text_type_link", "https://example.com/link"),
            TextNode(".", "text_type_text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)

    def test_text_to_textnodes_plain_text(self):
        # Test case with plain text (no markdown)
        text = "This is plain text without any markdown."
        expected_result = [
            TextNode("This is plain text without any markdown.", "text_type_text")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()