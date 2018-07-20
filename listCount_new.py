# -*- coding: utf-8 -*-
import sys
import os
import codecs
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import traceback
from datetime import datetime
from pytz import timezone
#from datetime import datetime

# ***********基本信息请谨慎更改**********
page = 'https://weibo.cn' # 简易版微博首页地址
main_page = 'https://weibo.com' # 正式版微博首页地址
comment_page = 'https://weibo.cn/repost/' #简易版微博评论页面地址
##请登录帐号查找自己的cookie填入此处
cook = {"Cookie":""}


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
    html = requests.get(url, cookies=cook).content
    #print("debug ==========:")
    #print(html)

    soup = BeautifulSoup(html, "html.parser")
    list = []
    form = soup.find("form", attrs={"action": "/repost/" + form_action})
    a = form.find('a').get('href')
    b = a[0:len(a)-1] #页面的第一部分
    c = form.find("div").text.split("/")[1]
    d = len(c) -1
    e = c[0:d]
    return int(e)+1

def getComment(url,file):
    """
     获取单个链接页面中的转发连接
    :param url:评论页面链接
    :param file: 文件对象
    """
    #print("debug Here")
    try:
        html = requests.get(url, cookies=cook).content
        #print(html)
        #print("debug html in getComment: "+html)
        soup = BeautifulSoup(html, "html.parser")
        r = soup.findAll('div', attrs={"class": "c"})
        counter = 0
        for e in r:
            size = 0
            name = ''
            uid = ''
            article = ''
            for item in e.find_all('a',href=re.compile("/u")):
                size = size + 1
                name = item.text
                uid = item.get('href').split("/")[2];
                #print("detail")
                #print(name)
            for item in e.find_all('span',attrs={"class":"cc"}):
                size = size + 1
                str = item.find('a').get("href").split("/")
                article = str[2]
                #print("detail")
                #print(article)
            for item in e.find_all('span',attrs={"class":"ct"}):
                repo_info=item.text
                repo_date=re.findall("\d+月\d+日",repo_info)
                repo_time=re.findall("\d+:\d+",repo_info)
                if len(repo_date) != 0:
                    repo_date=repo_date[0]
                else:
                    repo_date=""

                if len(repo_time) != 0:
                    repo_time=repo_time[0]
                else:
                    repo_time=""
                #print(repo_date+repo_time)
                date_time=repo_date+repo_time

            if size == 2:
                repostText=(e.text)

                repostText=(repostText.replace(',','delimiterTag'))
                #print(repostText)

                #else:
                #    repostText=""
                #print(repostText)
                counter+=1
                try:
                    #file.write(link + '\n')
                    file.write("{},{},{},{},{}\n".format(
                        date_time,
                        article,
                        uid,
                        name,
                        repostText
                        ))

                except IOError:
                    print("存入目标文件有误，请重新选择文件")
                    raise IOError("存入目标文件有误，请重新选择文件")

        print(counter)
    except Exception as e:
        print("**********请求连接失败**********")
        print('Failed to upload to ftp: '+ str(e))
        raise Exception()



def getAllComment(list,filename):
    """
    获取一个根节点的所有评论链接
    :param list: 评论页面集合
    """
    bufsize = 0
    file = codecs.open(filename, mode="w",encoding= "utf-8",buffering=bufsize)
    counter=0
    for link in list:
        counter += 1
        #if counter == 1:
        #    continue

        print("debug2: "+link)
        try:
            getComment(link, file)
        except Exception as e:
            print("**********请重新运行程序**********")
            break
        time.sleep(1)
    file.close()

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

def getTreeComment(input_file_name,output_file_name):
    """
    获取文件中所有连接的转发链接
    :param input_file_name:读取文件
    :param output_file_name:输入文件
    """
    start = time.time()
    #print("-----------计时开始-----------")
    #output_file_name = path_change(output_file_name)
    i = 0
    tree_list = readFile(input_file_name)

    bufsize = 0
    file = codecs.open(output_file_name, mode="a",encoding= "utf-8",buffering=bufsize)
    for link in tree_list:
        #print(link)
        i = i + 1
        #print("**********************写入第" + str(i) + "个文件，请耐心等待***************************")
        #getAllComment(getUrlList(link, start_pos),output_file_name +'_file_'+ str(i) +'_startpos_'+str(start_pos) +'_batchNum_'+str(batchNum)+'.txt')
        repostCount = getUrlListCount(link)*10
        file.write("{},{}\n".format(timeTag, repostCount))
        #print("**********************第" + str(i) + "个文件，写入完毕*********************************")
    total_time = time.time() - start
    #print(u"-----------总共耗时：%f 秒-----------" % total_time)
    file.close()
def path_change(filename):
    str = filename[0:len(filename)-4]
    return str
def use_reading():
    print("******************************************************************************")
    print("*                                使用必读                                    *")
    print("*                                一般来说每写入100个链接大约耗时18s            *")
    print("*                                如果转发链接大于1w条，请耐心等待            *")
    print("*                                使用前请耐心阅读使用文档                    *")
    print("*****************************************************************************")



if __name__ == '__main__':
    #use_reading()
    input_file_name = r"./input.txt"
    output_file_name = r"./output.txt"
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    #start_pos = int(sys.argv[3])
    #batchNum=int(sys.argv[4])
    #print(start_pos)
    #print(str(datetime.now()))
    shanghai= timezone('Asia/Shanghai')
    sh_time=datetime.now(shanghai)
    timeTag=(sh_time.strftime('%m/%d/%Y %H:%M:%S'))
    getTreeComment(input_file_name,output_file_name)
