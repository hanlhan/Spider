# encoding:utf-8
import os

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.methods.posts import EditPost, GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from wp_post import wp_post

client = Client('http://tf86.com/xmlrpc.ph', 'fendouai', 'wo2010WO,./')
categories = client.call(taxonomies.GetTerms('category', {"search": "python"}))

# folder_base_path="../sklearn/docs"
folder_base_path = "./docs"

folder_list = os.listdir(folder_base_path)
for folder in folder_list:
    file_list = os.listdir(os.path.join(folder_base_path, folder))
    print(file_list)
    for file_name in file_list:
        file_path = os.path.join(folder_base_path, folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content = f.read()
                content = content + "\n 原文GitHub： https://github.com/jackzhenguo/python-small-examples"
                with open(file_path, "r") as f:
                    title = f.readlines()[0]
                    title = title.replace("#", "")
                    title = "Python有趣的小例子一网打尽："+title
                    print(title)
                result = wp_post(client, title, content, categories)
                print(result)

            except Exception as e:
                print(e)
