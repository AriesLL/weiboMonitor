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
cook = {"Cookie": ""}


def findPage(file, linkWithoutNum, lastfoundPageNum, Hour, Minute):
    curNum = lastfoundPageNum + 500
    pageFound = False
    stack = 20

    try:
        offset = 500
        while pageFound == False and stack > 0:

            reloadstack = 10
            while reloadstack > 0:
                print("Loading page {}...  try {}".format(curNum, (11 - reloadstack)))
                html = requests.get((linkWithoutNum + str(int(curNum))), cookies=cook).content
                soup = BeautifulSoup(html, "html.parser")
                r = soup.findAll('div', attrs={"class": "c"})

                if len(r) > 3:
                    reloadstack = 0
                    for e in r:
                        for item in e.find_all('span', attrs={"class": "ct"}):
                            repo_info = item.text
                            repo_time = re.findall("\d+:\d+", repo_info)
                            if len(repo_time) != 0:
                                repo_time = repo_time[0]
                            else:
                                break
                            curHourMinute = repo_time.split(":")
                            if len(curHourMinute) != 0:
                                curHour = int(repo_time.split(":")[0])
                                curMinute = int(repo_time.split(":")[1])
                            else:
                                break

                            if curHour == Hour and curMinute == Minute:
                                print('!!!!!!!! FOUND !!!!!!!! {}:{} at [{}]\n'.format(Hour, Minute, int(curNum)))
                                pageFound = True
                                try:
                                    # file.write(link + '\n')
                                    file.write("[{}] {} page:{}\n".format(
                                        repo_time,
                                        int((45127 - curNum) * 10),
                                        int(curNum)
                                    ))
                                    return curNum
                                except IOError:
                                    print("存入目标文件有误，请重新选择文件")
                                    raise IOError("存入目标文件有误，请重新选择文件")
                    if pageFound == False:
                        print('Not found')
                        print("## Time: {}:{}".format(curHour, curMinute))
                        print("## Page: {}".format(curNum))
                        if Minute == 0:
                            if curHour > Hour:
                                offset = 500
                            elif curHour == Hour:
                                if offset < 0:
                                    offset *= -0.5
                            elif curHour < Hour:
                                if offset > 0:
                                    offset *= -0.5
                        if Minute == 30:
                            if curHour > Hour:
                                offset = 500
                            elif curHour < Hour:
                                if offset > 0:
                                    offset = -500
                            elif curHour == Hour:
                                if curMinute > 30:
                                    if offset < 0:
                                        offset *= -0.5
                                if curMinute < 30:
                                    if offset > 0:
                                        offset *= -0.5
                else:
                    print('NEED RELOAD!\n')
                    reloadstack -= 1
                    if reloadstack == 0:
                        print("**********Loaded page {} too many times**********".format(curNum))
                        raise Exception()

            print("## offset: {}\n".format(offset))
            curNum = int(curNum + offset)
            stack -= 1
        return curNum
    except Exception as err:
        print("**********Connection Request Failed**********")
        print('Failed to upload to ftp: {}'.format(err))
        raise Exception()


def getAllIncrements(filename, url):
    """
    Find the increment of repost in every hour
    """
    form_action = url
    url = comment_page + url
    html = requests.get(url, cookies=cook).content

    soup = BeautifulSoup(html, "html.parser")
    list = []
    form = soup.find("form", attrs={"action": "/repost/" + form_action})
    a = form.find('a').get('href')
    b = a[0:len(a) - 1]  # 页面的第一部分
    c = form.find("div").text.split("/")[1]
    d = len(c) - 1
    e = c[0:d]  # Maximum page
    linkWithoutNum = page + b

    bufsize = 0
    file = codecs.open(filename, mode="w", encoding="utf-8", buffering=bufsize)

    hour = 22
    minute = 0
    lastfoundPageNum = 1
    while hour >= 0:
        try:
            lastfoundPageNum = int(findPage(file, linkWithoutNum, lastfoundPageNum, hour, minute))
            if(minute == 30):
                minute = 0
            else:
                minute = 30
                hour -= 1
            time.sleep(1)
        except Exception as e:
            print("**********Please Restart the Program**********")
            break
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
        getAllIncrements(output_file_name + '_file_' + str(i) + '_startpos_' + str(start_pos) + '.txt', link)
        # getAllComment(getUrlList(link, start_pos), output_file_name + '_file_' + str(i) + '_startpos_' + str(start_pos) + '.txt')
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
    getTreeComment(input_file_name, output_file_name)
