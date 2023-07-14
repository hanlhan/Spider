#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
Author: harry lu
Date: 2023-07-14 20:59:24
LastEditTime: 2023-07-14 21:47:58
LastEditors: harry lu
Description: 将爬取的json转换为excel
FilePath: /promptgenius/json2excel.py
'''


import json
import pandas as pd
from pathlib import Path

def json2excel(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'content' in data:
        print(data)
        df = pd.DataFrame(data['content'])
        df.to_excel(json_path.with_suffix('.xls'), index=False)

if __name__ == '__main__':
    root_path = Path(__file__).parent / 'temp/prompt划分'

    for json_path in root_path.rglob('*.json'):
        print(json_path)
        json2excel(json_path)
