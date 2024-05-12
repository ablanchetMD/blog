
from htmlnode import HTMLNode
from htmlnode import TextNode
from htmlnode import split_nodes_special
from htmlnode import markdown_to_block
from htmlnode import list_to_textnodes
from htmlnode import ParentNode
from htmlnode import block_list_to_html

# Import the os module to get the path to the markdown file
import os

# Define the path to your Markdown file
file_path = os.path.join('md', 'test.md')

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    markdown_content = file.read()

# Output the content
block_list = markdown_to_block(markdown_content)
print(block_list)
new_list = list_to_textnodes(block_list)
print("*******")
print(new_list)
print("********")
html_list = ParentNode("div",block_list_to_html(new_list))
print(html_list.to_html())




