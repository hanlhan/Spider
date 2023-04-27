#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-04-27 09:13:35
LastEditTime: 2023-04-27 09:14:38
LastEditors: harry lu
Description: 爬取华校专的文章 并转换为md格式
FilePath: \Spider\huaxiaozhuan\spider_for_hxz.py
'''

import h2md
import requests
import os

from requests_html import HTMLSession

# url = "https://mp.weixin.qq.com/s?__biz=MzAxMjMwODMyMQ==&mid=2456340122&idx=1&sn=ccfff077ffa4b7a2ef888f3757dfb754&chksm=8c2fbc94bb583582e7365d51c1148a51427ae49fe2fd309dd73f7ca245da9f3870d131398b6c&scene=0&xtrack=1&key=10772accce8b4669a2e3320019f901d0eae329ee10d6053268825f070ace514b48157047a119699bee420d1284c7bfc5a6cbbc96eda13bfe04c6aec0e1d9a86fb9bc3ee4f863a911019271be3fe5c6b3&ascene=1&uin=NjIxMjM1NjYw&devicetype=Windows+10&version=62060833&lang=zh_CN&pass_ticket=ELpN%2Fxki%2BqMUDQ%2FjYkORJeOKVFN3c4VnKojdef0A3%2FYYFXgf%2FCvr6X3ObKS15eFx"
url = "http://www.huaxiaozhuan.com/"
root_path = "huaxiaozhuan1"

session = HTMLSession()

r = session.get(url)
r.encoding="utf-8"

# print(r.html.text)
# print(r.html.links)

md = h2md.convert(r.text)

f = open(os.path.join(root_path, "index.md"), "w", encoding="utf-8")
f.write(md)

for link in r.html.links:
    name = os.path.splitext(link)[0]
    filename = os.path.splitext(os.path.basename(link))[0]
    # print(name)
    path = os.path.join(root_path, name)
    if not os.path.exists(path):
        os.makedirs(path)
    urls = url + "/" + link
    print(urls)
    r = session.get(urls)
    r.encoding="utf-8"
    md = h2md.convert(r.text)
    f = open(os.path.join(path, filename+".md"), "a", encoding="utf-8")
    f.write(md)
