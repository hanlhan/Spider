# coding:utf-8

## 利用微信cookie获取微信文章

import requests

import re
import os
import html
import json

import demjson
import pdfkit
from bs4 import BeautifulSoup
import wechatsogou
import datetime
 
 
class WxCrawler(object):
    # 复制出来的 Headers，注意这个 x-wechat-key，有时间限制，会过期。当返回的内容出现 验证 的情况，就需要换 x-wechat-key 了
    headers = """
        Connection: keep-alive
        x-wechat-uin: MTY4MTI3NDIxNg%3D%3D
        x-wechat-key: 5ab2dd82e79bc5343ac5fb7fd20d72509db0ee1772b1043c894b24d441af288ae942feb4cfb4d234f00a4a5ab88c5b625d415b83df4b536d99befc096448d80cfd5a7fcd33380341aa592d070b1399a1
        Upgrade-Insecure-Requests: 1
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/apng,*/*;q=0.8
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,en-US;q=0.9
        Cookie: wxuin=621235660; devicetype=iPhoneiOS13.4.1; version=62090070; lang=zh_CN; pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD+KY0D9GGAHuj7bRTdrshphU5vB/eTjNVTzmT0S9J; wap_sid2=CMybnagCElxsODZPdG9pZVlPS0djeFlIWlhXeXA4b2NENG9rUUpZajJDSWtEUFMwVGp3cEpvMklLQ0FTaENSYk5LbEt4Y0EzWnQ2NFpJQWFjUFpRS3VlUTMtS3NCQ2NFQUFBfjDYiMX2BTgMQJRO
        X-Requested-With: com.tencent.mm
    """
 
    url = "https://mp.weixin.qq.com/mp/homepage?__biz=MzAxMjMwODMyMQ==&hid=13&sn=8c9ad87ebdd2b7ad426100a63e27cb2d&scene=18&uin=NjIxMjM1NjYw&key=c0a498ef66f72aa1dbaa15d63dd42c635f0b40025990d1143bb4473b2fb20b904295672b1fb49703d58b1827aaf2ec084225425e9976b26736eec021fbf551a1dbb5b7f05865b4a0651aec77f9bd1c50&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&ascene=7&pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD%2BKY0D9GGAHuj7bRTdrshphU5vB%2FeTjNVTzmT0S9J&winzoom=1.125"

    # 获取单个文章的URL
    content_url_array = []

    # 将 Headers 转换为 字典
    def header_to_dict(self):
        headers = self.headers.split("\n")
        headers_dict = dict()
        for h in headers:
            k,v = h.split(":")
            headers_dict[k.strip()] = v.strip()
        return headers_dict
 


    #解析文章列表
    def article_list(self, context):
        rex = "msgList = '({.*?})'"
        pattern = re.compile(pattern=rex, flags=re.S)
        match = pattern.search(context)
        if match:
            data = match.group(1)
            data = html.unescape(data)
            data = json.loads(data)
            articles = data.get("list")
            return articles

    # 获取文章URL
    def get_content_url(self, articles):
        content_url_array = []
        for a in articles:
            article_info=[]
            a = str(a).replace("\/", "/")
            a = demjson.decode(a)
            article_info.append(a['app_msg_ext_info']["title"])
            article_info.append(a['app_msg_ext_info']["content_url"])
            # 取更多的
            for multi in a['app_msg_ext_info']["multi_app_msg_item_list"]:
                article_info.append(multi['title'])
                article_info.append(multi['content_url'])
            content_url_array.append(article_info)
        return content_url_array

    
    # 解析单个文章
    def parse_article(self, headers, content_url):
        for i in content_url:
            content_response = requests.get(i, headers=headers, verify=False)
            with open("wx.html", "wb") as f:
                f.write(content_response.content)
            html = open("wx.html", encoding="utf-8").read()
            soup_body = BeautifulSoup(html, "html.parser")
            context = soup_body.find('div', id = 'js_content').text.strip()
            print(context)

    # 翻页
    def page(self, headers):
        response = requests.get(self.page_url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            msg_list = demjson.decode(msg_list)
            self.content_url(msg_list["list"])
            #递归
            self.page(headers)
        else:
            print("无法获取内容")

    # 解析单个文章
    def parse_article(self, headers, url):
        # for i in content_url:
        #     content_response = requests.get(i, headers=headers, verify=False)
        #     with open("wx.html", "wb") as f:
        #         f.write(content_response.content)
        #     html = open("wx.html", encoding="utf-8").read()
        #     soup_body = BeautifulSoup(html, "html.parser")
        #     context = soup_body.find('div', id = 'js_content').text.strip()
        #     print(context)

        content_response = requests.get(url, headers=headers, verify=False)
        with open("wx.html", "wb") as f:
            f.write(content_response.content)
        html = open("wx.html", encoding="utf-8").read()
        soup_body = BeautifulSoup(html, "html.parser")
        context = soup_body.find('div', id = 'js_content').text.strip()
        print(context)

    def parse_art(self, header, url):
        content_response = requests.get(url, headers=headers, verify=False)
        with open("wx.html", "wb") as f:
            f.write(content_response.content)
        html = open("wx.html", encoding="utf-8").read()
        soup_body = BeautifulSoup(html, "html.parser")
        context = soup_body.find('div', id = 'js_content').text.strip()
        print(context)


    # 运行
    def run(self):
        headers = self.header_to_dict()
        response = requests.get(self.url, headers=headers, verify=False)

        article_lists = self.article_list(response.text)
        
        content_urls = self.get_content_url(article_lists)

        ws_api = wechatsogou.WechatSogouAPI()

        gzh_name = "磐创AI"
        targetPath = os.getcwd() + os.path.sep + gzh_name
        # 如果不存在目标文件夹就进行创建
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

        for article_info in content_urls:
            # self.parse_article(headers, url)
            content_info = ws_api.get_article_content(article_info[1])
            
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{article_info[0]}</title>
                </head>
                <body>
                <h2 style="text-align: center;font-weight: 400;">{article_info[0]}</h2>
                {content_info['content_html']}
                </body>
                </html>
                '''
            try:
                pdfkit.from_string(html, targetPath + os.path.sep + f'{article_info[0]}.pdf', configuration=self.config)
            except:
                # 部分文章标题含特殊字符，不能作为文件名
                filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
                pdfkit.from_string(html, targetPath + os.path.sep + filename, configuration=self.config)

            break

 
if __name__ == "__main__":
    wx = WxCrawler()
    wx.run()