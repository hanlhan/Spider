# coding:utf-8

# 获取 zaller 桌面文化文章

import requests

import re
import os
import html
import json
import time

import pdfkit
from bs4 import BeautifulSoup
import wechatsogou
import datetime
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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
    URL：https://share.zaaap.cn/article/


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
    def printPDF(self, content, title, article_id):

        share_url = "https://share.zaaap.cn/article/" + article_id

        target_path = os.getcwd() + os.path.sep + "ZEALER_4"
        if not os.path.exists(target_path):
                os.makedirs(target_path)

        target_path = target_path + os.path.sep + f'{title}.pdf'

        # content = content.replace('<div', "<img width='800' height='400'")
        # content = content.replace('div>', " >")
        # content = content.replace('data-link', 'src')
        # content = content.replace('data-src', 'src')
        # content = content.replace('data-width', 'width')
        # content = content.replace('data-height', 'height')

        re = '<div class="contain contain-image".*?</div>'

        # bf = BeautifulSoup(content) 

        print(title)

        # if cover_img:
        #     string = "<img width='800' height='400' src='"+ cover_img + "'>"
        #     content = string + content

        html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{title}</title>
                </head>
                <body>
                <h2 style="text-align: center;font-weight: 400;">{title}</h2>
                {content}
                </body>
                </html>
                '''
        # content = str(content)
        # print(content)

        try:
            pdfkit.from_url(share_url, target_path, configuration=self.config)
        except:
            # 部分文章标题含特殊字符，不能作为文件名
            filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
            pdfkit.from_url(share_url, os.path.dirname(target_path) + os.path.sep + filename, configuration=self.config)

        # try:
        #     pdfkit.from_string(content, target_path, configuration=self.config)
        # except:
        #     # 部分文章标题含特殊字符，不能作为文件名
        #     filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        #     pdfkit.from_string(content, os.path.dirname(target_path) + os.path.sep + filename, configuration=self.config)

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
            return title, content, cover_img

    def get_share_content(self, article_id):
        share_url = "https://share.zaaap.cn/article/" + article_id
        driver = webdriver.Chrome(r'E:\\安装软件\\chromedriver_win32\\chromedriver.exe')
        driver.get(share_url)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="share-layout share-top"]'))
        )

        title = driver.title
        content = driver.page_source

        driver.close()

        # print(title)

        # response = requests.get(share_url)
        # result = response.text

        return content, title


    # 运行
    def run(self):

        group_url = "https://appv22.zaaap.cn/group/groupdetailcontent"

        for i in range(300):
            time.sleep(random.random())

            data = {"group_id": 7, "pageNum": int(i) + 1 , "pageSize": 10, "type": 0}
            response = requests.post(group_url, data, timeout = 500)
            # print(response.text)
            result = response.json()

            if result['status'] == 200 and result['msg'] == 'success':
                data = result.get("data").get("content")
                try:
                    for article in data:
                        print("pages: " + str(i+1))
                        article_id = article['id']
                        print(article_id)
                        article_title, article_content, conver_img = self.get_content(article_id)
                        time.sleep(random.random())
                        # article_content, title = self.get_share_content(article_id)
                        self.printPDF(article_content, article_title, article_id)
                        time.sleep(0.5)
                except Exception as ex:
                    print("except: ")
                    print(ex)
                    print("pages: " + str(i+1))
                    print(article_id)
                    continue

                # for article in data:
                #     print("pages: " + str(i+1))
                #     article_id = article['id']
                #     print(article_id)
                #     article_title, article_content, cover_img = self.get_content(article_id)
                #     self.printPDF(article_title, article_content, cover_img)
                #     time.sleep(0.5)

 
if __name__ == "__main__":

    wx = WxCrawler()
    wx.run()

