#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-07-05 23:21:49
LastEditTime: 2023-07-06 00:25:22
LastEditors: harry lu
Description: 爬取promptgenius的主程序
FilePath: /Spider/promptgenius/main.py
'''

import json
import random
import time
import requests


def spider_for_promptgenius():
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Cookie": "_ga=GA1.1.1945440313.1688570420; _ga_TY2Y50CCNH=GS1.1.1688570419.1.1.1688570776.0.0.0",
        "Host": "www.promptgenius.site",
        "Referer": "http://www.promptgenius.site/",
    }

    popular_url = "http://www.promptgenius.site/fetch_prompt/special-popular/chn"

    req = requests.get(popular_url, headers=header)
    popular_data = req.json()
    json.dump(popular_data, open("prompt/popular.json", "w", encoding="utf-8"), ensure_ascii=False)

    menu_url = "http://www.promptgenius.site/fetch_classes/chn"
    req = requests.get(menu_url, headers=header)
    menu_data = req.json()
    json.dump(menu_data, open("prompt/menu.json", "w", encoding="utf-8"), ensure_ascii=False)

    for m in menu_data:
        menu_id = m["ID"]
        menu_name = m["name"]
        children_menu = m["childrens"]

        menu_url = f"http://www.promptgenius.site/fetch_prompt/{menu_id}/chn"

        req = requests.get(menu_url, headers=header)
        prompt_data = req.json()
        json.dump(prompt_data, open(f"prompt/{menu_name}.json", 'w', encoding="utf-8"), ensure_ascii=False)

        for child in children_menu:
            child_id = child["ID"]
            child_name = child["name"]
            child_name = child_name.replace("/", "-")
            child_url = f"http://www.promptgenius.site/fetch_prompt/{child_id}/chn"
            req = requests.get(child_url, headers=header)
            prompt_data = req.json()
            json.dump(prompt_data, open(f"prompt/{child_name}.json", 'w', encoding="utf-8"), ensure_ascii=False)

            print(f"爬取{child_name}成功！")

            time.sleep(random.randint(1, 3))

        print(f"爬取{menu_name}成功！")

if __name__ == "__main__":
    spider_for_promptgenius()
