import sys
import os
import codecs
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import traceback


# ***********基本信息请谨慎更改**********
page = 'https://weibo.cn'  # 简易版微博首页地址
main_page = 'https://weibo.com'  # 正式版微博首页地址
comment_page = 'https://weibo.cn/repost/'  # 简易版微博评论页面地址
# 请登录帐号查找自己的cookie填入此处
cook = {"Cookie": "SCF=AsdcgVF2NbIsbWvmWhPdBQiAYJrHzSznn-Yd7Ropjdul1VirhlewfJl-Pb1NL17YKJ6c6JuOC7S5GGzbSPlKYR8.; _T_WM=7e7fb5d90f9d9dad26c9d01980b03345; MLOGIN=1; SUB=_2A252OkLTDeRhGeBL7FAX8yfPwzyIHXVVxW6brDV6PUJbkdBeLRPAkW1NRvRfX3E1cKMspwfYMi89mk6SA7PcYZmU; SUHB=0FQ7u54fxnl6K_; M_WEIBOCN_PARAMS=luicode^%^3D10000011^%^26lfid^%^3D231219_2793_newartificial_1001"}


def getUrlList(url, start_pos):
    """
    获取一个根的所有的转发页面链接
    :param url: 主页面链接
    :return: 所有评论链接
    """
    # print("debug Url: "+url)
    form_action = url
    url = comment_page + url
    # print("debug url: "+url)
    html = requests.get(url, cookies=cook).content
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    list = []
    form = soup.find("form", attrs={"action": "/repost/" + form_action})
    a = form.find('a').get('href')
    b = a[0:len(a) - 1]  # 页面的第一部分
    c = form.find("div").text.split("/")[1]
    d = len(c) - 1
    e = c[0:d]  # Maximum page
    if (int(e) + 1 <= start_pos + (batchNum * 1000)):
        totalbatch = int((int(e) - start_pos) / 1000)
    else:
        totalbatch = batchNum
    for i in range(0, totalbatch):
        num = start_pos + i * 1000
        list.append(page + b + str(num))
    return list


def getComment(url, file):
    """
     获取单个链接页面中的转发连接
    :param url:评论页面链接
    :param file: 文件对象
    """
    try:
        html = requests.get(url, cookies=cook).content
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        r = soup.findAll('div', attrs={"class": "c"})
        counter = 0
        for e in r:
            for item in e.find_all('span', attrs={"class": "ct"}):
                counter += 1
                repo_info = item.text
                repo_date = re.findall("\d+月\d+日", repo_info)
                repo_time = re.findall("\d+:\d+", repo_info)
                if len(repo_date) != 0:
                    repo_date = repo_date[0]
                else:
                    repo_date = ""

                if len(repo_time) != 0:
                    repo_time = repo_time[0]
                else:
                    repo_time = ""
                # print(repo_date + repo_time)
                date_time = repo_date + repo_time

                try:
                    # file.write(link + '\n')
                    file.write("{}\n".format(
                        date_time
                    ))

                except IOError:
                    print("存入目标文件有误，请重新选择文件")
                    raise IOError("存入目标文件有误，请重新选择文件")
        print("==== Total Lines: {}".format(counter))
    except Exception as err:
        print("**********Connection Request Failed**********")
        print('Failed to upload to ftp: {}'.format(err))
        raise Exception()


def getFirstCommentTime(url, file, pageNum):
    """
     获取单个链接页面中的首条时间
    """
    try:
        html = requests.get(url, cookies=cook).content
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        r = soup.findAll('div', attrs={"class": "c"})
        counter = 0
        for e in r:
            for item in e.find_all('span', attrs={"class": "ct"}):
                counter += 1
                repo_info = item.text
                repo_date = re.findall("\d+月\d+日", repo_info)
                repo_time = re.findall("\d+:\d+", repo_info)
                if len(repo_date) != 0:
                    repo_date = repo_date[0]
                else:
                    repo_date = ""

                if len(repo_time) != 0:
                    repo_time = repo_time[0]
                else:
                    repo_time = ""
                # print(repo_date + repo_time)
                date_time = repo_date + repo_time

                try:
                    # file.write(link + '\n')
                    file.write("[{}] {}\n".format(
                        date_time,
                        pageNum
                    ))

                except IOError:
                    print("存入目标文件有误，请重新选择文件")
                    raise IOError("存入目标文件有误，请重新选择文件")
            if counter == 1:
                break
        print("==== Time: {}".format(date_time))
    except Exception as err:
        print("**********Connection Request Failed**********")
        print('Failed to upload to ftp: {}'.format(err))
        raise Exception()


def getAllComment(list, filename):
    """
    获取一个根节点的所有评论链接
    :param list: 评论页面集合
    """
    bufsize = 0
    file = codecs.open(filename, mode="w", encoding="utf-8", buffering=bufsize)
    counter = 0
    for link in list:
        counter += 1
        # if counter == 1:
        #    continue
        print("debug2: " + link)
        pageNum = link.split('=')[-1]
        try:
            getFirstCommentTime(link, file, pageNum)
        except Exception as e:
            print("**********Please Restart the Program**********")
            break
        time.sleep(1)
    print("Total Page: {}".format(counter))
    file.close()


def readFile(filename):
    """
    获取根节点
    :param filename:根节点所在的文件
    :return: 根节点集合
    """
    list = []
    if not os.path.isfile(filename):
        print("*******************File doesn't exist*******************")
        raise Exception("*******************File doesn't exist*******************")
        return
    file = open(filename)
    lines = file.readlines()  # 调用文件的 readline()方法
    for line in lines:
        if len(line) != 0:
            a = line.strip()
            list.append(a)
    return list


def getTreeComment(input_file_name, output_file_name):
    """
    获取文件中所有连接的转发链接
    :param input_file_name:读取文件
    :param output_file_name:输入文件
    """
    start = time.time()
    print("-----------Time Countdown Starts-----------")
    output_file_name = path_change(output_file_name)
    i = 0
    tree_list = readFile(input_file_name)

    for link in tree_list:
        print(link)
        i = i + 1
        print("**********************Writing the " + str(i) + "th file, Please Wait***************************")
        getAllComment(getUrlList(link, start_pos), output_file_name + '_file_' + str(i) + '_startpos_' + str(start_pos) + '.txt')
        print("**********************The " + str(i) + "th file, Write Complete*********************************")
    total_time = time.time() - start
    print(u"-----------Total time spent: %f seconds-----------" % total_time)


def path_change(filename):
    str = filename[0:len(filename) - 4]
    return str


def use_reading():
    print("******************************************************************************")


if __name__ == '__main__':
    use_reading()
    input_file_name = r"./input.txt"
    output_file_name = r"./output.txt"
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    start_pos = int(sys.argv[3])
    batchNum = int(sys.argv[4])
    print(start_pos)
    getTreeComment(input_file_name, output_file_name)
