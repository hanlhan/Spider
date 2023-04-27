# coding:utf-8

# 获取 zaller 桌面文化文章

import requests

import re
import os
import html
import json
import time

import demjson
import pdfkit
from bs4 import BeautifulSoup
import wechatsogou
import datetime
import random
import logging


logging.basicConfig(filename='logger2.log', level=logging.INFO)

'''

1. 分组：桌面文化
    URL：https://appv22.zaaap.cn/group/groupdetailcontent
    Method：Post
    Content：group_id = 7
            pageNum	1
            pageSize	10
            type	0

2. 文章内容：
    URL：https://appv22.zaaap.cn/content/content/detail
    Method：Post
    Content：cid	1037544
            device_uuid	

   评论：
    URL：https://appv22.zaaap.cn/content/commentdetail
    Method：Post
    Content：id	1037544
            pageNum	1
            pageSize	20


    分享链接：
    URL：https://share.zaaap.cn/article


'''
 
 
class WxCrawler(object):

    def __init__(self):
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.ws_api = wechatsogou.WechatSogouAPI()

    # 将 Headers 转换为 字典
    def header_to_dict(self):
        headers = self.headers.split("\n")
        headers_dict = dict()
        for h in headers:
            k,v = h.split(":")
            headers_dict[k.strip()] = v.strip()
        return headers_dict

    # 输出为PDF
    def printPDF(self, title, content, cover_img):
        print(title)

        bf = BeautifulSoup(content, features="lxml")

        pics = bf.find_all("div", 'contain contain-image')

        img_tags = []

        i=0
        for pic in pics:
            if pic.has_attr('data-src'):
                pic_src = pic['data-src']
            else:
                pic_src = pic['data-link']
            pic_title = pic['data-title']
            pic_width = '750'
            pic_height = str(int(pic['data-height'])/int(pic['data-width'])*750)

            img_tag = bf.new_tag('img', src=pic_src, width=pic_width, height=pic_height, title=pic_title)
            pic_title_tag = bf.new_tag('span', style='text-align: center; font-size: 16px; line-height: 22px; overflow: hidden; display: block;')
            pic_title_tag.string=pic_title
            # img_tag.insert_after(pic_title_tag)
            # pics.append(img_tag)
            img_tags.append(img_tag)
            bf.find_all("div", 'contain contain-image')[0].insert_after(pic_title_tag)
            bf.find_all("div", 'contain contain-image')[0].replace_with(img_tag)

            i=i+1

        content = bf.body.prettify()


        if cover_img:
            string = "<img width='800' height='600' src='"+ cover_img + "'>"
            content = string + content

        target_path = os.getcwd() + os.path.sep + "ZEALER_5"           
        if not os.path.exists(target_path):
                os.makedirs(target_path)

        target_path = target_path + os.path.sep + f'{title}.pdf'

        html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{title}</title>
                    <style>p{{font-size:18px;}}</style>
                </head>
                <body>
                <h1 style="text-align: center;font-weight: 400; font-size:20px">{title}</h1>
                {content}
                </body>
                </html>
                '''

        try:
            pdfkit.from_string(html, target_path, configuration=self.config)
        except:
            # 部分文章标题含特殊字符，不能作为文件名
            filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
            pdfkit.from_string(html, os.path.dirname(target_path) + os.path.sep + filename, configuration=self.config)

    def get_content(self, id):
        article_url = "https://appv22.zaaap.cn/content/content/detail"
        data = {"cid": id, "device_uuid": ""}
        response = requests.post(article_url, data)
        result = response.json()

        if result['status'] == 200 and result['msg'] == 'success':
            data = result.get("data")
            title = data['title']
            content = data['content']
            cover_img = data['cover']
            title = title.replace(':', '：')
            title = title.replace('|', '｜')
            title = title.replace('?', '')
            title = title.replace('"', '')
            return title, content, cover_img


    # 运行
    def run(self):

        group_url = "https://appv22.zaaap.cn/group/groupdetailcontent"

        for i in range(300):
            time.sleep(random.random())

            data = {"group_id": 7, "pageNum": int(i) + 1, "pageSize": 10, "type": 0}
            response = requests.post(group_url, data, timeout = 500)
            # print(response.text)
            result = response.json()

            if result['status'] == 200 and result['msg'] == 'success':
                data = result.get("data").get("content")
                if len(data) <= 0:
                    break
                try:
                    for article in data:
                        print("pages: " + str(i + 1))
                        article_id = article['id']
                        # print(article_id)
                        article_title, article_content, conver_img = self.get_content(article_id)
                        # logging.info(article_id + "    " + article_title)
                        self.printPDF(article_title, article_content, conver_img)
                        time.sleep(0.5)
                        print('---------------')
                        print()
                except Exception as ex:
                    print("except:")
                    print(ex)
                    print("pages: " + str(i+1))
                    print(article_id)
                    continue

    def run_single(self, article_id):
        group_url = "https://appv22.zaaap.cn/group/groupdetailcontent"

        # print(article_id)
        article_title, article_content, conver_img = self.get_content(article_id)
        # logging.info(article_id + "    " + article_title)
        self.printPDF(article_title, article_content, conver_img)
        time.sleep(0.5)
        print('---------------')
        print()
        

 
if __name__ == "__main__":

    wx = WxCrawler()
    wx.run()
    # wx.run_single(1030742)

