__author__ = 'POW'

import sys
import os
import codecs
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import traceback
import math
import json
import pymongo
from datetime import datetime
from pytz import timezone

# Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

dbUri = 'mongodb://ywu:pow19940914@ds018508.mlab.com:18508/weibo_test_db'

page = 'https://weibo.cn'  # 简易版微博首页地址
main_page = 'https://weibo.com'  # 正式版微博首页地址
comment_page = 'https://weibo.cn/repost/'  # 简易版微博评论页面地址
superTopic_page = "https://www.weibo.com/p/100808bbda4f3a28c15e70cec89c0ba08455b0/super_index"
# 请登录帐号查找自己的cookie填入此处
cook = {"Cookie": ""}

###############################################################################
# main
###############################################################################


def getUrlListCount(url):
    """
    获取一个根的所有的转发页面链接
    :param url: 主页面链接
    :return: 所有评论链接
    """
    #print("debug Url: "+url)
    form_action = url
    url = comment_page + url
    #print("debug url: "+url)
    superTopic_url = "https://www.weibo.com/p/100808bbda4f3a28c15e70cec89c0ba08455b0/super_index"
    html = requests.get(superTopic_page, cookies=cook).content
    #print("debug ==========:")
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    span = soup.find("meta", attrs={"name": "description"})['content']
    print("debug ==========:")
    print(span)
    print("debug ==========:")
    s = span.text.split("[")[1]
    result = s[s.find("[") + 1:s.find("]")]
    return int(result)


def getTreeComment(input_file_name):
    """
    获取文件中所有连接的转发链接
    :param input_file_name:读取文件
    """
    start = time.time()
    # print("-----------计时开始-----------")
    client = pymongo.MongoClient(dbUri)
    db = client.get_database()
    zn = db['my_zn_reposts']
    lmy = db['my_lmy_reposts']
    ycy = db['my_ycy_reposts']

    i = 0
    tree_list = readFile(input_file_name)

    repostCount = getUrlListCount(superTopic_page)

    last_count = zn.find().sort('_id', -1).limit(1)[0]['repostCount']
    increment = repostCount - last_count
    data = {
        'Time': sh_time,
        'repostCount': repostCount,
        'repostIncrement': increment
    }
    zn.insert_one(data)
    print("----------- ZN [{}] {} {} -----------".format(timeTag, repostCount, increment))
    time.sleep(1)
        #print("**********************第" + str(i) + "个文件，写入完毕*********************************")
    total_time = time.time() - start
    #print(u"-----------总共耗时：%f 秒-----------" % total_time)
    client.close()
    print("\n************************************* Finished *************************************\n")


def readFile(filename):
    """
    获取根节点
    :param filename:根节点所在的文件
    :return: 根节点集合
    """
    list = []
    if not os.path.isfile(filename):
        print("*******************文件不存在请检查文件是否存在*******************")
        raise Exception("*******************文件不存在请检查文件是否存在*******************")
        return
    #bufsize = 0
    file = open(filename)
    lines = file.readlines()  # 调用文件的 readline()方法
    for line in lines:
        if len(line) != 0:
            a = line.strip()
            list.append(a)
    return list


def prep():
    print("\n************************************* Starts *************************************\n")


if __name__ == '__main__':
    prep()
    input_file_name = sys.argv[1]

    shanghai = timezone('Asia/Shanghai')
    sh_time = datetime.now(shanghai)
    timeTag = (sh_time.strftime('%m/%d/%Y %H:%M:%S'))
    getTreeComment(input_file_name)


# if __name__ == '__main__':
#     main(sys.argv[1:])
