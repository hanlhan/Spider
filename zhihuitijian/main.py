#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
Author: harry lu
Date: 2023-04-28 14:17:50
LastEditTime: 2023-05-12 22:41:44
LastEditors: harry lu
Description: 爬取智慧体检
FilePath: /Spider/zhihuitijian/main.py
"""

import requests
import json
import time
import random
import os
import re
import json
from pathlib import Path

# from bs4 import BeautifulSoup




# http://81.71.41.57:8800/manager/api/dictunion/examdept_list_get 科室列表
# http://81.71.41.57:8800/manager/api/dictunion/union_list_get?exam_dept_id=80&start=0&page_size=15 组合列表
# http://81.71.41.57:8800/manager/api/dictunion/item_list_get?union_id=2932 组合详情

# http://81.71.41.57:8800/manager/api/package/package_category 套餐分类
# http://81.71.41.57:8800/manager/api/package/dict_package_list?pagesize=999&pkg_class_item_id=15769 套餐列表
# http://81.71.41.57:8800/manager/api/package/dict_package_detail?pkg_id=1571 套餐详细内容







#


headers = {
    "Host": "1.71.41.57:8800",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "ci_session=a3st5g2bgfjdnub5gc1mhc64pb92unn3",
    "Referer": "http://81.71.41.57:8800/dist/",
}

base_menu_url = "http://81.71.41.57:8800/manager/api/dictdiag/diag_menu_get"
base_item_url = "http://81.71.41.57:8800/manager/api/dictdiag/diag_list_get?diag_class_id={}&start={}&page_size=15&keywords="

base_item_menu_url = "http://81.71.41.57:8800/manager/api/dictitem/item_menu_get"
base_item_list_url = "http://81.71.41.57:8800/manager/api/dictitem/item_list_get?item_class_id=&item_branch_id={}&keywords=&start={}&page_size=15"
base_item_info = "http://81.71.41.57:8800/manager/api/dictitem/item_info_get?item_id={}"

base_dept_list = "http://81.71.41.57:8800/manager/api/dictunion/examdept_list_get"
base_union_list = "http://81.71.41.57:8800/manager/api/dictunion/union_list_get?exam_dept_id={}&start={}&page_size=15"
base_union_detail = "http://81.71.41.57:8800/manager/api/dictunion/item_list_get?union_id={}"

base_package_cate = "http://81.71.41.57:8800/manager/api/package/package_category"
base_package_list = "http://81.71.41.57:8800/manager/api/package/dict_package_list?pagesize=999&pkg_class_item_id={}&start={}"
base_package_detail = "http://81.71.41.57:8800/manager/api/package/dict_package_detail?pkg_id={}"

def get_menu_and_list():
    response_menu = requests.get(base_menu_url, headers=headers)
    # print(response_menu.text)
    menudata_json = json.loads(response_menu.text)

    json.dump(
        menudata_json,
        open("data/menudata.json", "w", encoding="utf-8"),
        ensure_ascii=False,
    )

    for menu in menudata_json["data"]:
        diag_class_id = menu["diag_class_id"]
        diag_class_name = menu["diag_class_name"]
        response_item = requests.get(
            base_item_url.format(diag_class_id, 0), headers=headers
        )
        itemdata_json = json.loads(response_item.text)
        total = itemdata_json["data"]["total"]
        pages = total // 15 + 1
        for i in range(pages):
            print("正在爬取{}的第{}页".format(diag_class_name, i))
            if Path("data/{}_{}.json".format(diag_class_name, i)).exists():
                continue
            response_item = requests.get(
                base_item_url.format(diag_class_id, i * 15), headers=headers
            )
            itemdata_json = json.loads(response_item.text)
            json.dump(
                itemdata_json,
                open(
                    "data/{}_{}.json".format(diag_class_name, i), "w", encoding="utf-8"
                ),
                ensure_ascii=False,
            )
            time.sleep(random.randint(6, 15))


def get_detail():
    for file in os.listdir("data"):
        if file.endswith(".json"):
            name = Path(file).stem
            data = json.load(open("data/{}".format(file), "r", encoding="utf-8"))
            if name == "menudata":
                continue
            for item in data["data"]["list"]:
                print("正在爬取{}-{}".format(file, item["diag_id"]))
                diag_id = item["diag_id"]
                diag_name = item["diag_name"]
                diag_name = diag_name.replace("/", " ")
                if Path(
                    "detail/{}_{}_{}.json".format(name, diag_name, diag_id)
                ).exists():
                    continue
                response_detail = requests.get(
                    "http://81.71.41.57:8800/manager/api/dictdiag/diag_detail_get?diag_id="
                    + str(diag_id),
                    headers=headers,
                )
                if response_detail.text == "":
                    print("正在爬取{}-{}失败".format(file, item["diag_id"]))
                    continue
                detaildata_json = json.loads(response_detail.text)
                json.dump(
                    detaildata_json,
                    open(
                        "detail/{}_{}_{}.json".format(name, diag_name, diag_id),
                        "w",
                        encoding="utf-8",
                    ),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(4, 9))


def delete_no_success():
    for file in os.listdir("detail"):
        if file.endswith(".json"):
            data = json.load(open("detail/{}".format(file), "r", encoding="utf-8"))
            if data["status"] == "401":
                print("正在删除{}".format(file))
                os.remove("detail/{}".format(file))


def get_item_menu_and_list():
    if not Path("item_data/item_menudata.json").exists():
        response_menu = requests.get(base_item_menu_url, headers=headers)
        # print(response_menu.text)
        menudata_json = json.loads(response_menu.text)
        json.dump(
            menudata_json,
            open("item_data/item_menudata.json", "w", encoding="utf-8"),
            ensure_ascii=False,
        )

    menudata_json = json.load(
        open("item_data/item_menudata.json", "r", encoding="utf-8")
    )
    for data in menudata_json["data"]:
        item_class_name = data["item_class_name"]
        for item in data["child"]:
            item_branch_id = item["item_branch_id"]
            item_branch_name = item["item_branch_name"]
            item_lists = requests.get(
                base_item_list_url.format(item_branch_id, 0), headers=headers
            )
            item_lists_json = json.loads(item_lists.text)
            total = item_lists_json["data"]["total"]
            for i in range(total // 15 + 1):
                print("正在爬取{}的第{}页".format(item_branch_name, i))
                if Path(
                    "item_data/{}_{}_{}_{}.json".format(
                        item_class_name, item_branch_name, item_branch_id, i
                    )
                ).exists():
                    continue
                item_lists = requests.get(
                    base_item_list_url.format(item_branch_id, i * 15), headers=headers
                )
                item_lists_json = json.loads(item_lists.text)
                json.dump(
                    item_lists_json,
                    open(
                        "item_data/{}_{}_{}_{}.json".format(
                            item_class_name, item_branch_name, item_branch_id, i
                        ),
                        "w",
                        encoding="utf-8",
                    ),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(6, 15))


def get_item_info():
    for file in os.listdir("item_data"):
        if file.endswith(".json"):
            if file == "item_menudata.json":
                continue
            data = json.load(open("item_data/{}".format(file), "r", encoding="utf-8"))
            if data["status"] == "401":
                print("正在删除{}".format(file))
                os.remove("item_data/{}".format(file))
                continue
            for item in data["data"]["list"]:
                item_id = item["id"]
                item_name = item["item_name"]
                item_name = item_name.replace("/", " ")
                path_file = Path("item_detail/{}_{}.json".format(item_name, item_id))
                if path_file.exists():
                    t = json.load(path_file.open("r", encoding="utf-8"))
                    if t["status"] == "401":
                        print("正在删除{}".format(path_file))
                        os.remove(path_file)
                    else:
                        continue
                response_detail = requests.get(
                    base_item_info.format(item_id), headers=headers
                )
                item_detail_json = json.loads(response_detail.text)
                json.dump(
                    item_detail_json,
                    path_file.open("w", encoding="utf-8"),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(4, 9))


def get_dept_list():
    if not Path("union/dept_detail.json").exists():
        response_text = requests.get(base_dept_list, headers=headers)
        dept_list_json = json.loads(response_text.text)
        json.dump(
            dept_list_json,
            open("union/dept_detail.json", "w", encoding="utf-8"),
            ensure_ascii=False,
        )

    dept_list_json = json.load(open("union/dept_detail.json", "r", encoding="utf-8"))
    for data in dept_list_json["data"]:
        dept_id = data["exam_dept_id"]
        dept_name = data["exam_dept_name"]
        union_list_res = requests.get(
            base_union_list.format(dept_id, 0), headers=headers
        )
        union_list_json = json.loads(union_list_res.text)
        total = union_list_json["data"]["total"]
        total = int(total)
        for i in range(total // 15 + 1):
            print("正在爬取{}的第{}页".format(dept_name, i))
            if Path("union/data/{}_{}.json".format(dept_name, i)).exists():
                continue
            item_lists = requests.get(
                base_union_list.format(dept_id, i * 15), headers=headers
            )
            item_lists_json = json.loads(item_lists.text)
            json.dump(
                item_lists_json,
                open(
                    "union/data/{}_{}.json".format(dept_name, i),
                    "w",
                    encoding="utf-8",
                ),
                ensure_ascii=False,
            )
            time.sleep(random.randint(6, 15))

def get_union_detail():
    for file in os.listdir("union/data"):
        if file.endswith(".json"):
            data = json.load(open("union/data/{}".format(file), "r", encoding="utf-8"))
            if data["status"] == "401":
                print("正在删除{}".format(file))
                os.remove("item_data/{}".format(file))
            for item in data["data"]["list"]:
                union_id = item["union_id"]
                union_name = item["union_name"]
                exam_dept_name = item['exam_dept_name']
                union_name = union_name.replace("/", " ")
                path_file = Path("union/detail/{}_{}_{}.json".format(exam_dept_name, union_name, union_id))
                print('正在爬取{} {}'.format(exam_dept_name, union_name))
                if path_file.exists():
                    t = json.load(path_file.open("r", encoding="utf-8"))
                    if t["status"] == "401":
                        print("正在删除{}".format(path_file))
                        os.remove(path_file)
                    else:
                        continue
                response_detail = requests.get(
                    base_union_detail.format(union_id), headers=headers
                )
                item_detail_json = json.loads(response_detail.text)
                json.dump(
                    item_detail_json,
                    path_file.open("w", encoding="utf-8"),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(4, 9))


def get_package_list():
    if not Path("package/package_cate.json").exists():
        response_text = requests.get(base_package_cate, headers=headers)
        package_cate_json = json.loads(response_text.text)
        json.dump(
            package_cate_json,
            open("package/package_cate.json", "w", encoding="utf-8"),
            ensure_ascii=False,
        )

    package_cate_json = json.load(open("package/package_cate.json", "r", encoding="utf-8"))
    for data in package_cate_json["data"]:
        package_name = data['name']
        childs = data['child']
        for child in childs:
            child_name = child['name']
            child_id = child['pkg_class_item_id']
            package_list_res = requests.get(
                base_package_list.format(child_id, 0), headers=headers
            )
            package_list_json = json.loads(package_list_res.text)
            if ('total' not in package_list_json["data"]):
                json.dump(
                    item_lists_json,
                    open(
                        "package/data/{}_{}_{}.json".format(package_name, child_name, 0),
                        "w",
                        encoding="utf-8",
                    ),
                    ensure_ascii=False,
                )
                continue
            total = package_list_json["data"]["total"]
            for i in range(total // 99 + 1):
                print("正在爬取{} {}的第{}页".format(package_name, child_name, i))
                if Path("package/data/{}_{}_{}.json".format(package_name, child_name, i)).exists():
                    continue
                item_lists = requests.get(
                    base_package_list.format(child_id, i * 15), headers=headers
                )
                item_lists_json = json.loads(item_lists.text)
                json.dump(
                    item_lists_json,
                    open(
                        "package/data/{}_{}_{}.json".format(package_name, child_name, i),
                        "w",
                        encoding="utf-8",
                    ),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(6, 15))

def get_package_detail():
    for file in os.listdir("package/data"):
        if file.endswith(".json"):
            data = json.load(open("package/data/{}".format(file), "r", encoding="utf-8"))
            if data["status"] == "401":
                print("正在删除{}".format(file))
                os.remove("item_data/{}".format(file))
            for item in data["data"]["list"]:
                item_id = item["id"]
                pkg_class_name = item["pkg_class_name"]
                pkg_class_item_name = item['pkg_class_item_name']
                pkg_class_name = pkg_class_name.replace("/", " ")
                path_file = Path("package/detail/{}_{}_{}.json".format(pkg_class_item_name, pkg_class_name, item_id))
                print('正在爬取{} {}'.format(pkg_class_item_name, pkg_class_name))
                if path_file.exists():
                    t = json.load(path_file.open("r", encoding="utf-8"))
                    if t["status"] == "401":
                        print("正在删除{}".format(path_file))
                        os.remove(path_file)
                    else:
                        continue
                response_detail = requests.get(
                    base_package_detail.format(item_id), headers=headers
                )
                item_detail_json = json.loads(response_detail.text)
                json.dump(
                    item_detail_json,
                    path_file.open("w", encoding="utf-8"),
                    ensure_ascii=False,
                )
                time.sleep(random.randint(4, 9))


if __name__ == "__main__":
    # get_menu_and_list()
    # get_detail()
    # delete_no_success()

    # get_item_menu_and_list()
    # get_item_info()

    # get_dept_list()
    # get_union_detail()

    # get_package_list()
    get_package_detail()
