
## 利用微信cookie获取微信文章

import requests

import time
import json
import os
import pdfkit


class mp_spider(object):

    def __init__(self):
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.offset = 0
        self.count = 0
        self.base_url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzAxMjMwODMyMQ==&uin=NjIxMjM1NjYw&key=a03ebc6fe31ca973995035784c257b2a22161a49c2b743ce472741b796fafebc9b409f6de30aeaecea08025374637072e8051e29a161164cf115b58a3635ef9e5e4367b726846fd5da6564d2875f1186&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&ascene=7&pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD%2BKY0D9GGAHuj7bRTdrshphU5vB%2FeTjNVTzmT0S9J'
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxMjMwODMyMQ==&scene=124&uin=NjIxMjM1NjYw&key=da99e50216a5f345f936af077fd05222cf23ea9b8c7e707910ab588c3ad24ebf49d20411765214150e013bf756c715953337667b7147f9aa6bc3f1fcf7f8f596c97a2cc16a96832d82d78d2290eede59&devicetype=Windows+10+x64&version=62090070&lang=zh_CN&a8scene=7&pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyD%2BKY0D9GGAHuj7bRTdrshphU5vB%2FeTjNVTzmT0S9J&winzoom=1.125',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': 'wxuin=621235660; devicetype=iPhoneiOS13.4.1; version=17000c30; lang=zh_CN; pass_ticket=YiGvgUD5dUvzIuFhGJcVNAyDKY0D9GGAHuj7bRTdrshphU5vB/eTjNVTzmT0S9J; wap_sid2=CMybnagCElxRRjlibVZMa3A4d3VBV2pFRjc5UnNvZVVTQmtDM3BPS1ZJOEZtTXFwcE11VnlLd2N5LXkzWTVpT0lJRlNaUFFOVVg3OHlRWGtueURkc19lMVZBaHk2aWNFQUFBfjCH08T2BTgNQJVO'
        }

    def request_data(self):
        response = requests.get(self.base_url.format(self.offset), headers=self.headers)
        if 200 == response.status_code:
            print(response.text)
            self.parse_data(response.text)

    def parse_data(self, response_data):

        all_datas = json.loads(response_data)

        if 0 == all_datas['ret']:
            if 1 == all_datas['can_msg_continue']:
                summy_datas = all_datas['general_msg_list']
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        title_child = data['app_msg_ext_info']['digest']
                        article_url = data['app_msg_ext_info']['content_url']
                        cover = data['app_msg_ext_info']['cover']
                        copyright = data['app_msg_ext_info']['copyright_stat']
                        copyright = '原创文章_' if copyright == 11 else '非原创文章_'
                        self.count = self.count + 1
                        print('第【{}】篇文章'.format(self.count), copyright, title, title_child, article_url, cover)
                        self.creat_pdf_file(article_url, '{}_{}'.format(copyright, title))
                    except:
                        continue

                time.sleep(3)
                self.offset = all_datas['next_offset']  # 下一页的偏移量
                self.request_data()
            else:
                exit('数据抓取完毕！')
        else:
            exit('数据抓取出错:' + all_datas['errmsg'])

    def creat_pdf_file(self, url, title):
        try:
            file = 'D:/store/file2/{}.pdf'.format(title)
            if not os.path.exists(file):  # 过滤掉重复文件
                pdfkit.from_url(url, file)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    d = mp_spider()
    d.request_data()