#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-04-28 14:17:50
LastEditTime: 2023-05-04 16:25:58
LastEditors: harry lu
Description: 爬取智慧体检
FilePath: /Spider/zhihuitijian/main.py
'''

import requests
import json
import time
import random
import os
import re
import json
from pathlib import Path

# from bs4 import BeautifulSoup

# http://81.71.41.57:8800/manager/api/dictdiag/diag_menu_get 目录
# http://81.71.41.57:8800/manager/api/dictdiag/diag_list_get?diag_class_id=934&start=0&page_size=15&keywords= 列表
# http://81.71.41.57:8800/manager/api/dictdiag/diag_detail_get?diag_id=8462 详情

# diag_id id
# diag_name 诊断名称
# diag_code 诊断编码
# diag_gender 性别 0-暂无 1-男 2-女
# diag_type_name 诊断类型
# diag_branch_name 所属分支
# status 状态 0-有效 1-停用

# diag_advise 诊断建议
# diag_ail_explain 诊断解释
# diag_ail_group_explain 团体解释
# diag_group_advise 团体建议
# diag_keywords 诊断关键字



headers = {
    'Host': '1.71.41.57:8800',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ci_session=a3st5g2bgfjdnub5gc1mhc64pb92unn3',
    'Referer': 'http://81.71.41.57:8800/dist/',
}

base_menu_url = 'http://81.71.41.57:8800/manager/api/dictdiag/diag_menu_get'
base_item_url = 'http://81.71.41.57:8800/manager/api/dictdiag/diag_list_get?diag_class_id={}&start={}&page_size=15&keywords='

def get_menu_and_list():

    response_menu = requests.get(base_menu_url, headers=headers)
    # print(response_menu.text)
    menudata_json = json.loads(response_menu.text)

    json.dump(menudata_json, open('data/menudata.json', 'w', encoding='utf-8'), ensure_ascii=False)

    for menu in menudata_json['data']:
        diag_class_id = menu['diag_class_id']
        diag_class_name = menu['diag_class_name']
        response_item = requests.get(base_item_url.format(diag_class_id, 0), headers=headers)
        itemdata_json = json.loads(response_item.text)
        total = itemdata_json['data']['total']
        pages = total // 15 + 1
        for i in range(pages):
            print('正在爬取{}的第{}页'.format(diag_class_name, i))
            if Path('data/{}_{}.json'.format(diag_class_name, i)).exists():
                continue
            response_item = requests.get(base_item_url.format(diag_class_id, i * 15), headers=headers)
            itemdata_json = json.loads(response_item.text)
            json.dump(itemdata_json, open('data/{}_{}.json'.format(diag_class_name, i), 'w', encoding='utf-8'), ensure_ascii=False)
            time.sleep(random.randint(6, 15))

def get_detail():
    for file in os.listdir('data'):
        if file.endswith('.json'):
            print('正在爬取{}'.format(file))
            data = json.load(open('data/{}'.format(file), 'r', encoding='utf-8'))
            for item in data['data']['items']:
                diag_id = item['diag_id']
                if Path('detail/{}.json'.format(diag_id)).exists():
                    continue
                response_detail = requests.get('http://81.71.41.57:8800/manager/api/dictdiag/diag_detail_get?diag_id='+str(diag_id), headers=headers)
                detaildata_json = json.loads(response_detail.text)
                json.dump(detaildata_json, open('detail/{}.json'.format(diag_id), 'w', encoding='utf-8'), ensure_ascii=False)
                time.sleep(random.randint(6, 15))

if __name__ == "__main__":
    # get_menu_and_list()
    get_detail()
