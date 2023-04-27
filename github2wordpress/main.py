#encoding:utf8

import json
import time

import requests
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies

from find_image import *
from image_localization import image_localization
from wp_post import wp_post

with open("languages/lang.json","rb") as f:
    languages=json.load(f)

# g = Github("9a94f25c8bf511b0c94b0ac1e936e56b859a7e56")
g = Github("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")
#client = Client('http://www.tf86.com', 'fendouai', 'wo2010WO')
client = Client('http://www.githubchina.net/xmlrpc.php', 'git', 'wo2010WO')
categories = client.call(taxonomies.GetTerms('category', {"search": "github"}))

print(languages)

base_url="https://gh-trending-api.herokuapp.com/repositories?language="
since="&since=weekly&spoken_language_code=zh"
github_trendings=[]

for language in languages:
    language_urlParam=language['urlParam']
    github_trending=base_url+language_urlParam+since
    github_trendings.append(github_trending)

for github_trending in github_trendings:
    r=requests.get(url=github_trending)
    #print(dir(r))
    # print(r.content)
    # print(r.text)
    projects_json=json.loads(r.text)

    for project_json in projects_json:
        try:
            # print(project_json)
            repo_name=project_json["username"]+"/"+project_json["repositoryName"]
            # print(repo_name)
            repo = g.get_repo(repo_name)
            # print(repo.get_topics())
            contents = repo.get_contents("")
            for content_file in contents:
                # print(content_file.name.lower())
                # print(content_file.name)
                if content_file.name.lower()=="readme.md":
                    readme_file =content_file.name
            contents = repo.get_contents(readme_file)
            # print(type(contents))
            #print(contents.content)
            str_md = base64.b64decode(contents.content).decode("utf-8")
            #print(str_md)
            images_temp="images_temp"
            content=image_localization(str_md,images_temp,client,repo_name)
            title=project_json["repositoryName"]+"/"+project_json["description"]
            result = wp_post(client, title, content, categories)
            time.sleep(5)
        except Exception as e:
            print(str(e))
            repo_name = project_json["username"] + "/" + project_json["repositoryName"]
            print("fail to get " +repo_name)


