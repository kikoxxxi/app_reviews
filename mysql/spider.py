# -*- coding:utf-8 -*-

import urllib.request
import re
import json
import sys
import DAL
from DAL import AppDAL, ReviewsContentDAL


def scrapy_item():
    page = 1
    # appid = input("请输入应用id号:");
    # 414478124 #1053012308  #1056015676 #1012298403 #895670960 #972319818 #1201642309 #1236463633 #1238778050 #367003839
    # 427916203 # 1089497855
    app_id = 1089497855
    myurl = "https://itunes.apple.com/rss/customerreviews/page=1/id={}/sortby=mostrecent/json?l=en&&cc=cn".format(
        str(app_id))
    response = urllib.request.urlopen(myurl)
    myjson = json.loads(response.read())
    first_node = myjson["feed"]["entry"][0]
    app_category = first_node["category"]["attributes"]["label"]
    app_name = first_node["im:name"]["label"]
    app_data = {
        "app_id": app_id,
        "app_name": app_name,
        "app_category": app_category,
        "have_data": "0",
    }
    app_dal = AppDAL()
    review_dal = ReviewsContentDAL()
    if app_dal.query_one_set_by_id(app_id):
        pass
    else:
        app_dal.insert_one_set(**app_data)
    index_id = app_dal.query_one_set_by_id(app_id)[0]

    while page < 11:  # 默认循环10次
        myurl = "https://itunes.apple.com/rss/customerreviews/page={}/id={}/sortby=mostrecent/json?l=en&&cc=cn".format(
            str(page), str(app_id))
        response = urllib.request.urlopen(myurl)
        myjson = json.loads(response.read())
        try:
            del(myjson["feed"]["entry"][0])
        except KeyError:
            print("No more data!!!")
            sys.exit(0)
        for node in myjson["feed"]["entry"]:
            review_content = node["content"]["label"]
            review_content = re.sub(r'["\n]', "", review_content)
            if review_dal.query_content_by_id(index_id, review_content):
                print("duplicate review content!!")
            else:
                review_title = node["title"]["label"]
                review_version = node["im:version"]["label"]
                review_rating = node["im:rating"]["label"]
                review_data = {
                    "review_content": review_content,
                    "review_rating": review_rating,
                    "review_version": review_version,
                    "review_split": "0",
                    "review_title": review_title,
                    "review_app_id_id": index_id,
                }
                review_dal.insert_one_set(**review_data)
        print("save {} page's content!!!".format(page))
        page += 1


scrapy_item()
