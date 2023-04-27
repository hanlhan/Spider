#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-04-27 09:18:50
LastEditTime: 2023-04-27 09:19:01
LastEditors: harry lu
Description:
FilePath: \Spider\wx_gzh_article\requestWXArticle.py
'''
import requests
import json
import time
from pymongo import MongoClient

import MySQLdb

url = 'http://mp.weixin.qq.com/mp/profile_ext'

#（公众号不让添加主页链接，xxx表示profile_ext)

# Mongo配置
conn = MongoClient('127.0.0.1', 27017)
db = conn.wx  #连接wx数据库，没有则自动创建
mongo_wx = db.article  #使用article集合，没有则自动创建

# mysql 配置
# mysqldb = MySQLdb.connect("localhost", "root", "1234", "wx", charset='utf8' )
# mysqlcursor = mysqldb.cursor()

def get_wx_article(biz, uin, key, index=0, count=10):
    offset = (index + 1) * count
    params = {
        '__biz': biz,
        'uin': uin,
        'key': key,
        'offset': offset,
        'count': count,
        'action': 'getmsg',
        'f': 'json'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    response = requests.get(url=url, params=params, headers=headers)
    resp_json = response.json()
    if resp_json.get('errmsg') == 'ok':
        resp_json = response.json()
        # 是否还有分页数据， 用于判断return的值
        can_msg_continue = resp_json['can_msg_continue']
        # 当前分页文章数
        msg_count = resp_json['msg_count']
        general_msg_list = json.loads(resp_json['general_msg_list'])
        list = general_msg_list.get('list')
        print(list, "**************")
        for i in list:
            app_msg_ext_info = i['app_msg_ext_info']
            # 标题
            title = app_msg_ext_info['title']
            # 文章地址
            content_url = app_msg_ext_info['content_url']
            # 封面图
            cover = app_msg_ext_info['cover']

            # 发布时间
            datetime = i['comm_msg_info']['datetime']
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))

            print(title)

            # mongo_wx.insert({
            #     'title': title,
            #     'content_url': content_url,
            #     'cover': cover,
            #     'datetime': datetime
            # })

            # sql = "INSERT INTO `wx`.`article`(`title`,`content_url`,`cover`,`datetime`) VALUES ( " + title +", "+content_url+", "+cover+", "+datetime+" );"
        if can_msg_continue == 1:
            return True
        return False
    else:
        print('获取文章异常...')
        print(resp_json)
        return False


if __name__ == '__main__':
    biz = 'MzAxMjMwODMyMQ=='
    uin = 'NjIxMjM1NjYw'
    key = '10772accce8b4669a2e3320019f901d0eae329ee10d6053268825f070ace514b48157047a119699bee420d1284c7bfc5a6cbbc96eda13bfe04c6aec0e1d9a86fb9bc3ee4f863a911019271be3fe5c6b3'
    index = 0
    while 1:
        print(f'开始抓取公众号第{index + 1} 页文章.')
        flag = get_wx_article(biz, uin, key, index=index)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index += 1
        if not flag:
            print('公众号文章已全部抓取完毕，退出程序.')
            break

        print(f'..........准备抓取公众号第{index + 1} 页文章.')