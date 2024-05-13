import re
import os

class TextNode:
    def __init__(self,text,text_type,url=""):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other_node):
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
    
    def __repr__(self):        
        return f"TextNode({self.text},{self.text_type},{self.url})"




class HTMLNode:
    def __init__(self, tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag == None or self.tag == "":
            return self.value
        else:                            
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"        

    def props_to_html(self):
        returned_string = ""
        if self.props != None:                  
            for key,value in self.props.items():                      
                returned_string += f' {key}="{value}"'        
        return returned_string
    
    def __repr__(self):
        return f'tag={self.tag},value={self.value},children={self.children},props={self.props}'

class LeafNode(HTMLNode):
    def __init__(self,tag=None,value=None,props=None):
        super().__init__(tag,value,children=None,props=props)


class ParentNode(HTMLNode):
    def __init__(self,tag=None,children=None,props=None):
        super().__init__(tag,value=None,children=children,props=props)
    
    def to_html(self):        
        if self.tag == None:
            raise ValueError()
        if len(self.children) < 1:
            raise ValueError()
        else:
            returned_string = f"<{self.tag}{self.props_to_html()}>"            
            for child in self.children:
                returned_string += child.to_html()                    
            return returned_string +f"</{self.tag}>"


class TypeDict:
    def __init__(self):
        self.type_dict = [
            {"bold":{"type":"text_type_bold",
                    "html":"b",
                    "md":"**"}},
            {"italic":{"type":"text_type_italic",
                    "html":"i",
                    "md":"*"}},
            {"image":{"type":"text_type_image",
                    "html":"img",
                    "md":"![]"}},
            {"link":{"type":"text_type_link",
                    "html":"a",
                    "md":"[]"}},
            {"code":{"type":"text_type_code",
                    "html":"code",
                    "md":"`"}},
            {"text":{"type":"text_type_text",
                    "html":"",
                    "md":""}}]
    
    def get_category(self,subtype,category):
        if subtype == None or category == None:
            raise Exception(f"{self}.get_category : Need a type and a category specified")
        for item in self.type_dict:            
            if category in item.keys():                              
                return self.find(key=subtype,parent=item)
        raise Exception(f"{self}.get_category : Couldn't find category : {category}")
    
    # Specify a key to find that key in the parent,wherever it is nested.
    # Specify a key and value to return the parent.
    def find(self,key=None,value=None,parent=None,last_parent=None):        
        if parent == None:
            parent = self.type_dict
        if key == None:
            raise Exception(f"{self}.find({parent}): At least a key must be specified")              
        if isinstance(parent,dict):                               
            for k,v in parent.items():                                  
                if k == key and value == v:
                    # found the items in the parent, so return the parent.                                                                                          
                    return last_parent
                elif k == key and value == None:                    
                    # found the key in the parent, so return the value.                    
                    return v
                else:
                    # If the value is an object, we're going to look into it.
                    if isinstance(v,dict):                                                                     
                        result = self.find(key,value,v,k)
                        if result is not None:
                            return result               
        if isinstance(parent,list):
            for item in parent:
                result = self.find(key,value,item)
                if result is not None:
                    return result
        return None


def text_node_to_html_node(text_node):
    type_dict = {"text_type_bold":"b","text_type_italic":"i","text_type_underline":"u","text_type_link":"a", "text_type_code":"code","text_type_image":"img","text_type_text":""}

    if text_node.text_type == "text_type_link":
        return LeafNode(type_dict[text_node.text_type],text_node.text,{"href":text_node.url})
    elif text_node.text_type == "text_type_image":
        return LeafNode(type_dict[text_node.text_type],text_node.text,{"src":text_node.url, "alt":text_node.text})
    else:
        return LeafNode(type_dict[text_node.text_type],text_node.text)

def split_nodes_delimiter(old_nodes,text_type="text_type_text"):
    new_list = []
    type_dict = TypeDict()
    category = type_dict.find("type",text_type)
    if category == None:
        raise Exception(f"split_nodes_delimiter(): Couldn't find a category for '{text_type}'.")
    delimiter = type_dict.get_category("md",category)    
    for node in old_nodes:        

        if isinstance(node,TextNode):
            if delimiter == "*":
                node.text = node.text.replace("**", "|||")
            split_list = node.text.split(delimiter)
            default_text_type = node.text_type
        else:
            default_text_type = "text_type_text"   
            if delimiter == "*":
                node = node.replace("**", "|||")
            elif delimiter == "":
                new_list.append(TextNode(node,default_text_type))
                continue
            split_list = node.split(delimiter)                  
        
        # If the length is even, something is wrong.
        if len(split_list) % 2 == 0:
            raise Exception(f"split_node_delimiter({old_nodes},{text_type}) Incorrect syntax : No closing delimiter.")
        for i,item in enumerate(split_list):            
            if i % 2 == 0:
                # is even:
                if item != "":
                    if delimiter == "*":
                        item = item.replace("|||","**")
                    new_list.append(TextNode(item, default_text_type))                    
            else:
                # is odd:
                if delimiter == "*":
                    item = item.replace("|||","**")
                new_list.append(TextNode(item,text_type))    
    return new_list

def text_to_textnodes(text):
    return_list = [text]
    return_list = split_nodes_delimiter(return_list,"text_type_bold")
    return_list = split_nodes_delimiter(return_list,"text_type_italic")
    return_list = split_nodes_delimiter(return_list,"text_type_code")
    return_list = split_nodes_special(return_list,"image")
    return_list = split_nodes_special(return_list,"link")
    return return_list

def list_to_textnodes(list_of_blocks):
    return_list = []
    for block in list_of_blocks:
        txt_list = []  
        
        for text in block.textnodes: 
            if block.block_type == "ul" or block.block_type == "ol":
                txt_list = txt_list + [BlockNode(text_to_textnodes(text),"li")]
            elif block.block_type == "pre":
                txt_list = txt_list + [TextNode(text,"text_type_text")]
            else:
                txt_list = txt_list + text_to_textnodes(text)                            
        if block.block_type == "pre":
            return_list.append(BlockNode([BlockNode(txt_list,"code")],block.block_type))
        else:
            return_list.append(BlockNode(txt_list,block.block_type))
    return return_list

def block_list_to_html(block_list):    
    return_list = []
    # First Block is a DIV
    for block in block_list:
        if isinstance(block,TextNode):
            print(f"TextNode : {block}")
            return_list = return_list + [text_node_to_html_node(block)]
        
        if isinstance(block,BlockNode):
            print(f"BlockNode : {block}")
            return_list = return_list + [ParentNode(block.block_type,block_list_to_html(block.textnodes))]
    return return_list




def split_nodes_special(old_nodes,subtype="image"):
    
    new_nodes = []
    for node in old_nodes:
        if isinstance(node,TextNode):
            node_text = node.text
            node_type = node.text_type
        else:
            node_text = node
            node_type = "text_type_text"            
        
        # Are there images in the current node?
        item_list = extract_markdown(node_text,subtype)
        new_list = []
        if len(item_list) > 0:

            if subtype == "image":
                prefix = "!"
                text_type = "text_type_image"
            else:
                prefix = ""
                text_type = "text_type_link"            
            
            split_index = 0            
            for item_info in item_list:
                tag = f"{prefix}[{item_info[0]}]({item_info[1]})"
                item_index = node_text.find(tag)
                if item_index != -1:
                    new_list.append(node_text[split_index:item_index])
                    split_index = item_index + len(tag)
            new_list.append(node_text[split_index:])   
            
            for i in range(0,len(new_list)-1,1):

                if new_list[i] != "":                  
                    new_nodes.append(TextNode(new_list[i],node_type))
                new_nodes.append(TextNode(item_list[i][0],text_type,item_list[i][1]))
                if i == len(new_list)-2:
                    if new_list[i+1] != "":                      
                        new_nodes.append(TextNode(new_list[i+1],node_type))
                    break
        else:
            new_nodes.append(node)    
    return new_nodes

class BlockNode:
    def __init__(self,textnodes,block_type):
        self.textnodes = textnodes
        self.block_type = block_type
    
    def __eq__(self,other_node):
        return self.textnodes == other_node.textnodes and self.block_type == other_node.block_type

    def __repr__(self):
        return f'BlockNode({self.block_type})={self.textnodes}'

class BlockDict:
    def __init__(self):
        self.types = [
            {"# ":"h1"},
            {"## ":"h2"},
            {"### ":"h3"},
            {"#### ":"h4"},
            {"##### ":"h5"},
            {"###### ":"h6"},
            {"* ":"ul"},
            {"- ":"ul"},
            {">":"blockquote"},
            {"```":"pre"},
            {"#. ":"ol"},            

        ]
        
def markdown_to_block(markdown):
    lines = markdown.split("\n")
    block_dict = BlockDict().types
    def create_block(old_list,line_list,block_type):
        # print(f"create_blocknode {line_list,block_type}")
        old_list.append(BlockNode(line_list,block_type))
        return old_list

    line_ls = []
    block_ls = []
    current_block = "p"
    last_block = ""
    bcode = False
    nlist = 1
    for i,line in enumerate(lines):
        bskip = False
        # print(f"{i} : {line} : current_block: {current_block} / last block : {last_block}")
        if line.strip() == "":
            # only save if there is content.
            if len(line_ls) > 0:
                block_ls = create_block(block_ls,line_ls,last_block) 
            # we are on a new line, so we should save the previous to a block.
            # we should do that as well if we are at the end of the document.
            current_block = "p"
            last_block = ""            
            nlist = 1
            line_ls = []      
        for block_type in block_dict:
            k = next(iter(block_type))
            v = block_type[k]
            # print(f"{k},{v}")
            item_index = -1
            if k != "#. ":
                item_index = line.find(k)
            else:
                pattern = r'\b\d+\. '
                match = re.search(pattern,line)
                if match != None:                    
                    item_index = line.find(match.group())                                    
                         
            # we only care if the k is at the start of the line :
            if item_index == 0 and k != "#. " and k != "```" and bcode == False:                              
                current_block = v                
                bskip = True
                if current_block != last_block and len(line_ls) > 0:
                    block_ls = create_block(block_ls,line_ls,last_block) 
                    line_ls = []
                last_block = current_block
                line_ls.append(line[len(k):].strip())
            elif item_index == 0 and k == "#. " and bcode == False:                
                n = int(match.group().replace(". ",""))
                # print(f"{nlist} == {n}, {nlist == n}")
                if nlist == n:                    
                    nlist += 1
                    current_block = v
                    bskip = True
                    if current_block != last_block and len(line_ls) > 0:                    
                        block_ls = create_block(block_ls,line_ls,last_block) 
                        line_ls = []
                    last_block = current_block
                    line_ls.append(line[len(match.group()):].strip())
                else:                    
                    if len(line_ls) > 0:
                        block_ls = create_block(block_ls,line_ls,last_block)                         
                        line_ls = []
                    current_block = "p"
                    last_block = current_block
                    nlist = 1
            elif item_index == 0 and k == "```":
                # print("code logic")
                # start a code block or end a code block
                if bcode == False:
                    bcode = True
                    # Start
                    current_block = "pre"
                    bskip = True                    
                else:
                    bcode = False
                    bskip = True
                    if len(line_ls) > 0:
                        block_ls = create_block(block_ls,line_ls,last_block)  
                    # End
                    line_ls = []
                    current_block ="p"
            
        if line.strip() != "" and bskip==False:
            if bcode == False:
                current_block = "p"
            if current_block != last_block and len(line_ls) > 0:
                block_ls = create_block(block_ls,line_ls,last_block)  
                line_ls = []
            line_ls.append(line.strip())
            last_block = current_block        
      
        if i == len(lines) - 1:
            # only save if there is content.
            if len(line_ls) > 0:
                block_ls = create_block(block_ls,line_ls,current_block)                  
    # print(block_ls)        
    return block_ls

def get_title_from_blocks(list_block):
    title = ""
    for block in list_block:
        if block.block_type == "h1":
            if isinstance(block.textnodes,list):
                for str in block.textnodes:
                    title += str
            elif isinstance(block.textnodes,str):
                title = block.textnodes
    
    if title != "":
        return title
    else:
        raise Exception("No valid title found in markdown file.")


   



def extract_markdown(text,type="image"):
    if type == "image":
        srch_pattern = r"!\[[^\]]*\]\([^\)]*\)"
        nd_pattern = r"!\[[^\]]*\]"
    else:
        srch_pattern = r"\[[^\]]*\]\([^\)]*\)"
        nd_pattern = r"\[[^\]]*\]"

    matches = re.findall(srch_pattern,text)
    list = []
    strip_pattern = r"[\[\]!()]"

    for item in matches:        
        alttext = re.findall(nd_pattern,item)        
        formated_text = re.sub(strip_pattern,"",alttext[0])
        url = re.findall(r"\([^\)]*\)",item)        
        formated_url = re.sub(strip_pattern,"",url[0])        
        list.append((formated_text,formated_url))
    return list

           




                 
            
        


    



