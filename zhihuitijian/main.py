#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-04-28 14:17:50
LastEditTime: 2023-04-28 15:08:53
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

# http://81.71.41.57:8800/manager/api/dictdiag/diag_menu_get
# http://81.71.41.57:8800/manager/api/dictdiag/diag_list_get?diag_class_id=934&start=0&page_size=15&keywords=


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

response_menu = requests.get(base_menu_url, headers=headers)
print(response_menu.text)
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
        response_item = requests.get(base_item_url.format(diag_class_id, i * 15), headers=headers)
        itemdata_json = json.loads(response_item.text)
        if Path('data/{}_{}.json'.format(diag_class_name, i)).exists():
            continue
        json.dump(itemdata_json, open('data/{}_{}.json'.format(diag_class_name, i), 'w', encoding='utf-8'), ensure_ascii=False)
        time.sleep(random.randint(1, 3))
