import os
import shutil
from pathlib import Path

from htmlnode import markdown_to_block
from htmlnode import block_list_to_html
from htmlnode import list_to_textnodes
from htmlnode import get_title_from_blocks
from htmlnode import ParentNode

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
content_root = os.path.join(project_root,"content")
template = os.path.join(project_root,"templates","template.html")
public_root = os.path.join(project_root,"public")
static_root = os.path.join(project_root,"static")
    

def main():    
    # list_files(project_root)  
    delete_files(public_root)
    copy_files(public_root,static_root,"")
    generate_site(content_root,template,public_root)


def generate_site(content_dir,template_path,dest_path):
    items = os.listdir(content_dir)
    dst = dest_path
    
    for item in items:
        full_path = os.path.join(content_dir, item)        
        if os.path.isfile(full_path):
            generate_page(full_path,template_path,dest_path)    
        
        if os.path.isdir(full_path):            
            new_path = os.path.join(dst,item)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            generate_site(full_path,template_path,dest_path)                
            



def generate_page(content_path,template_path,dest_path):
    # template should be a single html template
    # content should be a folder to look through
    # dest_path should be a folder to copy the content to.
    relative_path = os.path.relpath(content_path,content_root)
    dst_file_path = os.path.join(dest_path,relative_path)    
    
    if not os.path.exists(dst_file_path):
        os.makedirs(os.path.dirname(dst_file_path),exist_ok=True)
    
    #template should always be html
    if get_file_extension(template_path) != ".html":
        raise Exception(f"{template_path} isn't .html; The template must be html.")

    if get_file_extension(content_path) != ".md":
        raise Exception(f"{content_path} isn't .md; The content file must be md.")
    
    with open(template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    with open(content_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    node_blocks = markdown_to_block(markdown_content)

    title = get_title_from_blocks(node_blocks)

    content = ParentNode("div",block_list_to_html(list_to_textnodes(node_blocks))).to_html()

    new_html = html_content.replace("{{ Title }}",title).replace("{{ Content }}",content)

    with open(dst_file_path.replace(".md",".html"),'w') as file:
        file.write(new_html)


def get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

def list_files(directory,path="/"):
    items = os.listdir(directory)    
    for i,item in enumerate(items):
        full_path = os.path.join(directory, item)        
        if os.path.isfile(item):
            subtype = "file"        
        print(f"{i}:{path}{item}")
        print(f"{i}:{full_path}")
        if os.path.isdir(full_path):                      
            list_files(full_path,f"{path}{item}/")

def delete_files(directory,path="/"):
    items = os.listdir(directory)

    for i,item in enumerate(items):
        full_path = os.path.join(directory, item)        
        
        if os.path.isfile(full_path):
            os.remove(full_path)   

        if os.path.isdir(full_path):                     
            delete_files(full_path,f"{path}{item}/")
            os.rmdir(full_path)

def copy_files(to_,from_,newdir=""):
    items = os.listdir(from_)
    dst = to_
    if newdir != "":
        dst = os.path.join(to_,newdir)
        if not os.path.exists(dst):
            os.mkdir(dst)
    for item in items:
        full_path = os.path.join(from_, item)        
        if os.path.isfile(full_path):
            shutil.copy(full_path,dst)     
        
        if os.path.isdir(full_path):            
            new_path = os.path.join(dst,item)
            if not os.path.exists(new_path):
                os.mkdir(new_path)                
            copy_files(new_path,full_path)





main()