import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from htmlnode import text_node_to_html_node
from htmlnode import TextNode
from htmlnode import TypeDict
from htmlnode import split_nodes_delimiter
from htmlnode import extract_markdown


class TestHTMLNode(unittest.TestCase):    
    
    def test(self):        
        node    = HTMLNode("p", "This is a paragraph",None,{"text":"arial", "color":"red","size":"md"})        
        self.assertEqual('<p text="arial" color="red" size="md">This is a paragraph</p>',node.to_html())        
        
    def test1(self):
        leafnode    = LeafNode("p", "This is a paragraph",{"text":"arial"})
        self.assertEqual('<p text="arial">This is a paragraph</p>',leafnode.to_html())
    
    def test2(self):
        errornode    = LeafNode("p", None,{"text":"arial"})
        with self.assertRaises(ValueError):
            errornode.to_html()
    
    def test_parent_nodes1(self):
        parent_node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",parent_node.to_html())

    def test_parent_nodes2(self):
        parent_node = ParentNode("p",[ParentNode("p",[ParentNode("p",[LeafNode(None,"Test Text")])]),LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual("<p><p><p>Test Text</p></p>Normal text<i>italic text</i>Normal text</p>",parent_node.to_html())

    def test_node_to_html_node1(self):        
        text_node = TextNode("This is a text node", "text_type_bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<b>This is a text node</b>',html_node.to_html())
    
    def test_node_to_html_node2(self):
        text_node = TextNode("This is a text node", "text_type_italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<i>This is a text node</i>',html_node.to_html())
    
    def test_node_to_html_node3(self):
        text_node = TextNode("This is a text node", "text_type_underline")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<u>This is a text node</u>',html_node.to_html())
    
    def test_node_to_html_node4(self):
        text_node = TextNode("This is a text node", "text_type_link","www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<a href="www.google.com">This is a text node</a>',html_node.to_html())
    
    def test_node_to_html_node5(self):
        text_node = TextNode("This is a text node", "text_type_code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<code>This is a text node</code>',html_node.to_html())
    
    def test_node_to_html_node6(self):
        text_node = TextNode("This is a text node", "text_type_image","www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual('<img src="www.google.com" alt="This is a text node">This is a text node</img>',html_node.to_html())
    
    def setUp(self):
        self.type_dict_obj = TypeDict()
    
    def test_find_key_value(self):
        # Test finding a key-value pair
        result = self.type_dict_obj.find(key="type", value="text_type_bold")
        self.assertEqual(result, "bold")
    
    def test_find_key_only(self):
        # Test finding a key without specifying a value
        result = self.type_dict_obj.find(key="bold")
        self.assertEqual(result, {"type": "text_type_bold", "html": "b", "md": "**"})
    
    def test_find_nested_key1(self):
        # Test finding a key within nested dictionaries
        result = self.type_dict_obj.find(key="type", value="text_type_link")
        self.assertEqual(result, "link")
    
    def test_find_nested_key2(self):
        # Test finding a key within nested dictionaries
        first_ = self.type_dict_obj.find(key="bold")
        result = self.type_dict_obj.find(key="type",parent=first_)
        self.assertEqual(result, "text_type_bold")
    
    def test_find_nonexistent_key(self):
        # Test finding a key that doesn't exist
        result = self.type_dict_obj.find(key="nonexistent")
        self.assertIsNone(result)
    
    def test_split_nodes_delimiter_start_with(self):
        old_nodes = ["**bold**Text"]
        expected_result = [TextNode("bold", "text_type_bold"), TextNode("Text", "text_type_text")]
        result = split_nodes_delimiter(old_nodes, "text_type_bold")
        self.assertEqual(result, expected_result)
    
    def test_split_nodes_delimiter_complex_multiple(self):
        old_nodes = [TextNode("This is a text node with a `code block in it`, how will it format?","text_type_text"),TextNode("This is a *italic* and **BOLD** test node.","text_type_text")]
        expected_result = [TextNode("This is a text node with a ", "text_type_text"), TextNode("code block in it", "text_type_code"),TextNode(", how will it format?", "text_type_text"),TextNode("This is a ", "text_type_text"),TextNode("italic", "text_type_italic"),TextNode(" and ", "text_type_text"),TextNode("BOLD", "text_type_bold"),TextNode(" test node.", "text_type_text")]
        result = split_nodes_delimiter(old_nodes, "text_type_code")        
        new_result = split_nodes_delimiter(result, "text_type_italic")        
        newest_result = split_nodes_delimiter(new_result, "text_type_bold")        
        self.assertEqual(newest_result, expected_result)

    def test_split_nodes_delimiter_end_with(self):
        old_nodes = ["Text**bold**"]
        expected_result = [TextNode("Text", "text_type_text"), TextNode("bold", "text_type_bold")]
        result = split_nodes_delimiter(old_nodes, "text_type_bold")
        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_alternating(self):
        old_nodes = ["Text**bold**Text**bold**"]
        expected_result = [TextNode("Text", "text_type_text"), TextNode("bold", "text_type_bold"), TextNode("Text", "text_type_text"), TextNode("bold", "text_type_bold")]
        result = split_nodes_delimiter(old_nodes, "text_type_bold")
        self.assertEqual(result, expected_result)

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = ["No delimiter here"]
        expected_result = [TextNode("No delimiter here", "text_type_text")]
        result = split_nodes_delimiter(old_nodes, "text_type_bold")
        self.assertEqual(result, expected_result)
    
    def test_error_split_nodes(self):
        old_nodes = ["No delimiter ** here"]
        with self.assertRaises(Exception):
            result = split_nodes_delimiter(old_nodes, "text_type_bold")
    
    def test_extract_markdown_images(self):
        text = "This is a ![sample image](https://example.com/image.png) and ![another image](https://example.com/another.png)"
        expected_result = [("sample image", "https://example.com/image.png"), ("another image", "https://example.com/another.png")]
        result = extract_markdown(text, type="image")
        self.assertEqual(result, expected_result)

    def test_extract_markdown_links(self):
        text = "This is a [sample link](https://example.com/sample) and [another link](https://example.com/another)"
        expected_result = [("sample link", "https://example.com/sample"), ("another link", "https://example.com/another")]
        result = extract_markdown(text, type="link")
        self.assertEqual(result, expected_result)

    def test_extract_markdown_no_matches(self):
        text = "This is some plain text without any markdown."
        expected_result = []
        result = extract_markdown(text, type="image")
        self.assertEqual(result, expected_result)
    
if __name__ == "__main__":
    unittest.main()