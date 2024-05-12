import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node    = TextNode("This is a text node", "bold")
        node2   = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node    = TextNode("This is a text 1 node", "bold")
        node2   = TextNode("This is a text 2 node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_uneq2(self):
        node    = TextNode("This is a text 1 node", "bold")
        node2   = TextNode("This is a text 1 node", "italic")
        self.assertNotEqual(node, node2)
    
    def test_uneq3(self):
        node    = TextNode("This is a text 1 node", "bold","www")
        node2   = TextNode("This is a text 1 node", "bold")
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
