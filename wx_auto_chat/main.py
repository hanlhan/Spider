#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-04-27 09:20:30
LastEditTime: 2023-04-27 09:20:15
LastEditors: harry lu
Description: 微信自动聊天机器人
FilePath: \Spider\wx_auto_chat\main.py
'''
import requests
import random
import json

import itchat
import jieba
import MySQLdb


from elasticsearch import Elasticsearch
from itchat.content import *


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        user_text = getUserText(msg)
        # jieba 分词
        # word_list = jieba.cut_for_search(user_text)

        # results = getResultByMysql(word_list)
        results = getResultByBotmind(user_text)
        returnmsg = getReplyMsg(results)
        # print(returnmsg)
        msg.user.send(returnmsg)

# 返回用户消息内容
def getReplyMsg(results):
    r_list = random.sample(range(10), 3)

    returnmsg = ""
    i = 0
    for row in results:
        # if i < 3:
        # if i in r_list:
        link = row['link']
        title = row['title']
        short_url = getShortURL(link)
        returnmsg = returnmsg + row['title'] + short_url + "\n\n"
        # i += 1

    return returnmsg

def getStopWord():
    stop_list = []
    with open("stop_words.txt", encoding='utf-8') as f:
        lines = f.readlines()
    stop_list = [x.strip() for x in lines]
    return stop_list

# 获取用户实际消息
# 因原消息带有@信息，要把它去掉
def getUserText(msg):
    user_text = msg.text

    my_info = itchat.search_friends()
    my_nick_name = my_info['NickName']

    text_index = user_text.find(my_nick_name)
    user_text = user_text[text_index + len(my_nick_name) + 1:]

    return user_text

# 获取短网址
def getShortURL(content_url):
    url_key = "5d1b30e68e676d2bbabccab4@91c1aa1b9a041207ccea6d12d5c6f00e"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    querystring = {"url": content_url, "key": url_key}
    url = "http://suo.im/api.htm"
    short_url = requests.get(url, params=querystring, headers=headers)

    return short_url.text

# 通过ES获取结果
def getResultByES(word_list):
    es = Elasticsearch()

    word_list = " ".join(word_list)
    query = {'query': {"match": {"context": word_list}}}
    results = es.search(index="article", body=query)

    return results

# 通过数据库获取结果
def getResultByMysql(word_list):
    # mysql 配置
    mysqldb = MySQLdb.connect("localhost", "root", "1234", "wx", charset='utf8' )
    mysqlcursor = mysqldb.cursor()

    stop_list = getStopWord()

    word_list = "|".join([word for word in word_list if word not in stop_list])
    sql = "select * from article where title regexp'" + word_list + "' limit 10"
    mysqlcursor.execute(sql)
    results = mysqlcursor.fetchall()

    return results

# 通过 BotMind 获取结果
def getResultByBotmind(word_list):
    url = "http://193.112.6.146:8080/BotMind/api/Dialogue"

    data = {
        "msgType":0,
        "msgContent": {
            "textInfo": {
                "text":"文章推荐：" + word_list
        },
        "imgInfo": {
            "url":"imageUrl"
        },
        "audioInfo": {
            "url":"audioUrl"
        },
        "locInfo": {
            "province": "广东",
            "city": "深圳",
            "county": "南山区",
            "location": "22.5323230000,113.9366400000"
        }
        },
        "devInfo": {
            "userId": "pxm",
            "robotId": "pxm_robot",
            "accessToken": ""
        },
        "userInfo": {
            "userId":"test11"
        }
    }

    result = requests.post(url, json=data)
    result = json.loads(result.text)
    result = json.loads(result["磐小妹"])
    # print(result)
    return result

# 主程序
if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)
    itchat.run(True)
