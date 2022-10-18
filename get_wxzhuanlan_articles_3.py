# coding:utf-8

# 获取微信公众号专栏文章

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
 
 
class WxCrawler(object):

    def __init__(self, url, headers, mp_name, zl_name, man_urls):
        # 获取单个文章的URL
        self.content_url_array = []
        self.mp_name = mp_name
        self.zl_name = zl_name
        self.man_urls = None
        if len(man_urls) > 0:
            self.man_urls = True
            self.content_url_array=man_urls
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.url = url
        # 复制出来的 Headers，注意这个 x-wechat-key，有时间限制，会过期。当返回的内容出现 验证 的情况，就需要换 x-wechat-key 了
        self.headers = headers

        self.targetPath = os.getcwd() + os.path.sep + self.mp_name + os.path.sep + self.zl_name
        # 如果不存在目标文件夹就进行创建
        if not os.path.exists(self.targetPath):
            os.makedirs(self.targetPath)
        self.ws_api = wechatsogou.WechatSogouAPI()

    # 将 Headers 转换为 字典
    def header_to_dict(self):
        headers = self.headers.split("\n")
        headers_dict = dict()
        for h in headers:
            k,v = h.split(":")
            headers_dict[k.strip()] = v.strip()
        return headers_dict

    #解析初始文章列表
    def article_list(self, context):
        rex = "var data=({.*?});"
        pattern = re.compile(pattern=rex, flags=re.S)
        match = pattern.search(context)
        if match:
            data = match.group(1)
            data = html.unescape(data)
            data = json.loads(data)
            articles = data.get("appmsg_list")
            cate_list = data.get('cate_list')
            return articles, cate_list

    # 获取初始文章URL
    def get_content_url(self, articles):
        for a in articles:
            a = str(a).replace("\/", "/")
            a = demjson.decode(a)
            article_info=ArticleInfo(a["title"], a["link"])
            self.content_url_array.append(article_info)

    # 翻页
    def get_more_articles(self, headers, begin, count):
        headers = self.header_to_dict()
        
        base_url = self.url + '&begin='+str(begin)+'&count='+str(count)+'&action=appmsg_list&f=json&r=0.03157105780673497&appmsg_token=1063_jhL2x7LBiiW%2B5EeqOlcuGdAAaXj9VkanNfTgaw~~'
        
        headers['Referer']=self.url
        response = requests.post(base_url, headers=headers)
        
        result = response.json()
        if result["base_resp"].get('ret') == 0:
            msg_list = result.get("appmsg_list")
            for article in msg_list:
                article_info = ArticleInfo(article['title'], article['link'])
                self.content_url_array.append(article_info)
            #递归
            if result.get('has_more') == 1:
                time.sleep(0.1)
                self.get_more_articles(headers, begin + count, count)
            else:
                print("文章获取完毕")
                return
        else:
            print("无法获取内容")
            return

    # 获取子菜单文章
    def get_child_articles(self, headers, cid, begin, count, cate_list_count):
        headers = self.header_to_dict()
        base_url = self.url + '&cid='+str(cid)+'&begin='+str(begin)+'&count='+str(count)+'&action=appmsg_list&f=json&r=0.03157105780673497&appmsg_token=1063_jhL2x7LBiiW%2B5EeqOlcuGdAAaXj9VkanNfTgaw~~'

        headers['Referer']=self.url
        response = requests.post(base_url, headers=headers)

        print('cid: '+str(cid))
        print('begin: '+str(begin))

        result = response.json()
        if result["base_resp"].get('ret') == 0:
            msg_list = result.get("appmsg_list")
            for article in msg_list:
                article_info = ArticleInfo(article['title'], article['link'])
                self.content_url_array.append(article_info)
            #递归
            if result.get('has_more') == 1:
                time.sleep(0.1)
                self.get_child_articles(headers, cid, begin + count, count, cate_list_count)
            elif cid >= cate_list_count:
                return
            else:
                self.get_child_articles(headers, cid + 1, 0, count, cate_list_count)
                # return

            
        else:
            print("无法获取内容")
            return
    
    def getAllArticles(self, context):
        # 解析第一次文章列表
        first_articles_info, cate_list = self.article_list(context)
        self.get_content_url(first_articles_info)
        # 获取剩余文章
        self.get_more_articles(self.headers, 6, 5)

        if len(cate_list) > 0:
            self.get_child_articles(self.headers, 0, 0, 5, len(cate_list))

    # 输出为PDF
    def printPDF(self, article_info):
        content_info = self.ws_api.get_article_content(article_info.getUrl())

        title = article_info.getTitle()

        print(title)

        title = title.replace(':', '：')
        title = title.replace('|', '｜')

        print(title)

        print()
        # print(content_info['content_html'])

        html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{title}</title>
                </head>
                <body>
                <h2 style="text-align: center;font-weight: 400;">{title}</h2>
                {content_info['content_html']}
                </body>
                </html>
                '''
        # try:
        #     pdfkit.from_string(html, self.targetPath + os.path.sep + f'{title}.pdf', configuration=self.config)
        # except:
        #     # 部分文章标题含特殊字符，不能作为文件名
        #     filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        #     pdfkit.from_string(html, self.targetPath + os.path.sep + filename, configuration=self.config)


    # 运行
    def run(self):
        if not self.man_urls:
            headers = self.header_to_dict()
            response = requests.get(self.url, headers=headers, verify=False)
            self.getAllArticles(response.text)

        print('文章数量：' + str(len(self.content_url_array)))

        for article_info in self.content_url_array:
            # self.printPDF(article_info)
            time.sleep(0.5)




class ArticleInfo(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url
    
    def getTitle(self):
        return self.title
    
    def getUrl(self):
        return self.url

    def __str__(self):
        print(self.title)


 
if __name__ == "__main__":
    mp_name='磐创AI'
    zl_name='ML与DL基础'

    url = "https://mp.weixin.qq.com/mp/homepage?__biz=MzAxMjMwODMyMQ==&hid=15&sn=3251d6c338dfc2b0d5ac6c4fe0bc2326&scene=18&uin=NjIxMjM1NjYw&key=a03ebc6fe31ca97399664e148f95e86e51b7a02154f8d04ff0afe6529df595d01d1d75fa145e8ad005bed3d49c2a430eb725ca1e92798dfafb9adec86746c4825afab6595b6cba674da3caa6a42fe711&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&ascene=7&pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD%2BKY0D9GGAHuj7bRTdrshphU5vB%2FeTjNVTzmT0S9J&winzoom=1.125"

    headers="""
        Connection: keep-alive
        x-wechat-uin: MTY4MTI3NDIxNg%3D%3D
        x-wechat-key: 5ab2dd82e79bc5343ac5fb7fd20d72509db0ee1772b1043c894b24d441af288ae942feb4cfb4d234f00a4a5ab88c5b625d415b83df4b536d99befc096448d80cfd5a7fcd33380341aa592d070b1399a1
        Upgrade-Insecure-Requests: 1
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/apng,*/*;q=0.8
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,en-US;q=0.9
        Cookie: wxuin=621235660; devicetype=Windows10x64; version=62090070; wxtokenkey=777; pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD+KY0D9GGAHuj7bRTdrshphU5vB/eTjNVTzmT0S9J; wap_sid2=CMybnagCElxTQzdkNUhMd0RZMzgxVXgzTktCUWduN1hneGVNY3hkN3JSVWZXQ3dPcDhJcUItYVB0TkZrMGZIaHlsSVB6QTJFQXdkT09iOXNualRaLTZsSk9tZU8taWNFQUFBfjCP0Mj2BTgMQJRO
        X-Requested-With: com.tencent.mm
    """

    man_urls=[]
    # man_urls=[ArticleInfo('TensorFlow系列专题(十二)：CNN最全原理剖析(多图多公式)', 'https://mp.weixin.qq.com/s/vcw_b2jBMiPQLW5gbjyVlg'),
    #           ArticleInfo('TensorFlow系列专题(十四)：手把手带你搭建卷积神经网络实现冰山图像分类', 'https://mp.weixin.qq.com/s/G2eQ_wmIqOgx7gHEi9UJNA')]

    wx = WxCrawler(url, headers, mp_name, zl_name, man_urls)
    wx.run()


'''
参考文章：
    1. https://cloud.tencent.com/developer/article/1356563
    2. https://zhuanlan.zhihu.com/p/72079102
    3. https://blog.csdn.net/ityouknow/article/details/104509404
'''