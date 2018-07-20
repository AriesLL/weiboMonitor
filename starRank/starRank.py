#https://pyformat.info/
from __future__ import unicode_literals, division, print_function
#from __future__ import , print_function

#import diff_match_patch
import csv
import argparse
import sys
import os
import codecs

maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str



import json
import csv
import sys
import re
from datetime import date
from time import mktime
from urllib.request import urlopen

from bs4 import BeautifulSoup



fileName=sys.argv[1]  #input
output_file=sys.argv[2]  #output
#mode=sys.argv[3]  # mode = 0 is before clean, 1 is clean

#output_handle_0 = codecs.open(output_file_mode_0,encoding="utf-16",mode='w')
#output_handle_1 = codecs.open(output_file_mode_1,encoding="utf-16",mode='w')

output_file_mode_0 = output_file+"_mode_0_utf8.csv"
output_file_mode_1 = output_file+"_mode_1_utf8.csv"
output_handle_0 = codecs.open(output_file_mode_0,encoding="utf-8",mode='w')
output_handle_1 = codecs.open(output_file_mode_1,encoding="utf-8",mode='w')






def getNum(entryStr):
    #print(entryStr)
    if len(re.findall("\d+\.\d+",entryStr)) != 0 :
        admire_num = float(re.findall("\d+\.\d+",entryStr)[0])
    else:
        admire_num = int((re.findall("\d+",entryStr)[0]))
    
    if len(re.findall("万", entryStr)) != 0:
        admire_num = int(admire_num * 10000)
    if len(re.findall("亿", entryStr)) != 0:
        admire_num = int(admire_num * 100000000)

    return admire_num

def getWeiboNum(entryStr):
    #print(entryStr)
    #if len(re.findall("\d+\.\d+",entryStr)) != 0 :
    #print(entryStr)
    weiboCount = int(re.findall("\d+",entryStr)[1])
    #else:
    #    admire_num = int((re.findall("\d+",entryStr)[0]))
    
    if len(re.findall("万", entryStr)) != 0:
        weiboCount = int(weiboCount * 10000)
    if len(re.findall("亿", entryStr)) != 0:
        weiboCount = int(weiboCount * 100000000)

    return weiboCount


def getElement(stNum,d, output_handle, mode):
    stEach=d['rankList']['list'][stNum]
    stPersonData=stEach['stPersonData']
    lUserid=stPersonData['lUserid']
    strNick=stPersonData['strNick']
    strHead=stPersonData['strHead']
    lGiftPoint=stPersonData['lGiftPoint']
    iRank=stEach['iRank']
    stFavoriteStar=stEach['stFavoriteStar']
    strStarName=stFavoriteStar['strStarName']
    strPersonalLink=stEach['strPersonalLink']
    #res=[lUserid, strNick, lGiftPoint, iRank]
    #print(str(lUserid)+','+strNick+','+str(lGiftPoint)+','+str(iRank))
    if mode == "0":
        output_handle.write("{},{},{},{},{},{},{}\n".format(lUserid, strNick, lGiftPoint, iRank, strStarName, strHead, strPersonalLink))
    else:
        output_handle.write("{},{},{},{},{}\n".format(lUserid, strNick, lGiftPoint, iRank, strStarName))
                    

#def extract


with open(fileName) as json_data:
    d = json.load(json_data)
    #print(d)
    #print(d['rankList'])
#print(d['rankList']['list'][0])
    cardlistInfo=d['data']['cardlistInfo']
    title_top=cardlistInfo['title_top']
    #print(title_top)
    #stListLen=len(stList)
    #for i in range(0,stListLen):
    #    getElement(i,d,output_handle, mode)
    #output_handle.write("{}\n".format(title_top))

    cards=d['data']['cards']
    cardsLen=len(cards)
    #print(cardsLen)

    ####### card0 info #######
    card0=cards[0]
    card0user=card0['user']
    follow_count=card0user['follow_count']
    fans=card0user['followers_count']
    screen_name=card0user['screen_name']
    #print(follow_count)
    #print(fans)
    #print(screen_name)

    ####### card1 info #######
    card1=cards[1]
    title=card1['title']
    month=re.findall("\d+",title)[0]
    day=re.findall("\d+",title)[1]

    date=month+"/"+day+"/2018"
    #print(date)
    #print(title)
    card_group=card1['card_group']
    card_group_len=len(card_group)

    #print(card_group_len)
    if card_group_len > 4:
        top3 = False
        total_score = card_group[3]['rank_list'][0]['data']
        total_rank= card_group[3]['rank_list'][0]['rank']
        #print(total_score)
        #print(total_rank)
        
    else:
        top3 = True
        for i in range(0,3):
            if screen_name == card_group[i]['rank_list'][0]['user']['screen_name']:
                total_score = card_group[i]['rank_list'][0]['data']
                total_rank= card_group[i]['rank_list'][0]['rank'] 
                
    ####### card2 info #######
    # card2 is a summary of card 3 4 5 6


    ####### card3 info #######
    ##  阅读数  ### 
    card3=cards[3]['card_group']

    # rank
    read_rank = card3[0]['title_extra_text']
    read_rank =int(re.findall("\d+",read_rank)[0])
    #print(read_rank)

    #阅读数 和阅读数得分
    read_num = card3[1]['group'][0]['item_title']
    read_num = getNum(str(read_num))
    #print(read_num)

    #阅读数得分（满分30分）
    read_score = card3[1]['group'][1]['item_title']
    read_score =float(re.findall("\d+\.\d+",read_score)[0])
    #print(read_score)

    # 发微博数
    weibo_count = card3[2]['group']
    weibo_count_30 = weibo_count[0]['title_sub']
    #print(weibo_count_30)
    #最近30天发微博：15条, not use getNum function, 
    weibo_count_30 = getWeiboNum(str(weibo_count_30))
    #print(weibo_count_30)
    
    weibo_count_7 = weibo_count[1]['title_sub']
    #print(weibo_count_7)
    weibo_count_7 = getWeiboNum(str(weibo_count_7))
    #print(weibo_count_7)
    
    weibo_count_1 = weibo_count[2]['title_sub']
    weibo_count_1 = getNum(str(weibo_count_1))
    #print(weibo_count_1)
    #re.findall("\d+.\d+",


    ####### card4 info #######
    ## 互动数 ###

    card4=cards[4]['card_group']
    # rank
    react_rank = int(re.findall("\d+",card4[0]['title_extra_text'])[0])
    #print(react_rank)
    
    #昨日互动数
    react_num = card4[1]['group'][0]['item_title']
    react_num = getNum(str(react_num))
    #print(react_num)
    #互动数得分（满分30分）
    react_score = card4[1]['group'][1]['item_title']
    #if len(re.findall("\d+.\d+",react_score)) == 0:
    #    react_score =float(re.findall("\d+",react_score)[0])
    #else:
    react_score =float(re.findall("\d+\.\d+",react_score)[0])
    #print(react_score)

    #双卡片 ，互动数详情
    react_count = card4[2]['group']
    react_weibo = react_count[0]['title_sub']
    #print(react_weibo)
    react_weibo = getNum(str(react_weibo))
    
    react_comment = react_count[1]['title_sub']
    react_comment = getNum(str(react_comment))
    
    react_story = react_count[2]['title_sub']
    react_story = getNum(str(react_story))
    #print(react_story)
    
    ####### card5 info #######
    ## 社会影响力 ##
    card5 = cards[5]['card_group']
    # 单项排名 rank
    impact_rank = int(re.findall("\d+",card5[0]['title_extra_text'])[0])
    #print(impact_rank)
    
    #昨日社会影响力 = 昨日提及他的微博阅读数
    impact_num = card5[1]['group'][0]['item_title']
    impact_num = getNum(str(impact_num))
    #print(impact_num)
    
    #社会影响力得分（满分20分）
    impact_score = card5[1]['group'][1]['item_title']
    impact_score = float(re.findall("\d+\.\d+",impact_score)[0])
    #print(impact_score)
    
    #昨日搜索量
    search_num = card5[3]['desc_extr']
    search_num = getNum(str(search_num))
    #print(search_num)
    
    ####### card6 info #######
    #爱慕值
    ## 社会影响力 ##
    card6 = cards[6]['card_group']
    # 单项排名 rank
    admire_rank = int(re.findall("\d+",card6[0]['title_extra_text'])[0])
    #print(admire_rank)
    
    #昨日爱慕值
    admire_num = card6[1]['group'][0]['item_title']
    admire_num = getNum(str(admire_num))
    
    #admire_num =int(admire_num)
    #print(admire_num)
    
    #爱慕值得分（满分20分）
    admire_score = card6[1]['group'][1]['item_title']
    admire_score =float(re.findall("\d+\.\d+",admire_score)[0])
    #print(admire_score)
    
    #昨日搜索量
    flower_count = card6[2]['group']
    #昨日送花人数
    flower_fans = flower_count[0]['title_sub']
    flower_fans = getNum(str(flower_fans))
    #print(flower_fans)
    #昨日送花次数
    flower_num = flower_count[1]['title_sub']
    flower_num = getNum(str(flower_num))
    #print(flower_num)

    #print(total_rank)
    #print(total_score)

            #print(i)
    #print(top3)

    # mode 0

    # mode 1
    # title_top, title, screen_name, follow_count, fans, total_rank, total_score,
    # read_rank, read_score, read_num, weibo_count_30, weibo_count_7, weibo_count_1
    # react_rank, react_score, react_num, react_weibo, react_comment, react_story
    # impact_rank, impact_score, impact_num, search_num
    # admire_rank, admire_score, admire_num, flower_fans, flower_num
    print("{},{},{},{},{},{},{},{}\n".format(
        screen_name,
        fans, 
        total_rank, 
        total_score, 
        read_score, 
        react_score, 
        impact_score, 
        admire_score
        ))
    #output_handle_0.write("粉丝数,总分,排行,阅读数（30分）,互动数（30分）,社会影响力（20分）,爱慕值（20分）\n")
    output_handle_0.write("{},{},{},{},{},{},{},{}\n".format(
        "昵称",
        "粉丝数", 
        "总分", 
        "总排行", 
        "阅读（30分）", 
        "互动（30分）", 
        "社会影响力（20分）", 
        "爱慕值（20分）"
        ))


    output_handle_0.write("{},{},{},{},{},{},{},{}\n".format(
        screen_name,
        fans, 
        total_score, 
        total_rank, 
        read_score, 
        react_score, 
        impact_score, 
        admire_score
        ))

    output_handle_0.close()

    output_handle_1.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
        "昵称",
        "日期",
        "粉丝数", 
        "总分", 
        "总排行", 
        "分（阅读）", 
        "排名（阅读）",
        "阅读数",
        "30天微博数",
        "7天微博数",
        "昨日微博数",
        "分（互动）", 
        "排名（互动）",
        "互动数",
        "微博互动",
        "评论互动",
        "故事互动",
        "分（社会影响力）", 
        "排名（社会影响力）",
        "提及微博阅读数",
        "搜索量",
        "分（爱慕）",
        "排名（爱慕）",
        "爱慕值",
        "送花人数",
        "送花次数"
        ))

    output_handle_1.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
        screen_name,
        date,
        fans, 
        total_score, 
        total_rank, 
        read_score, 
        read_rank,
        read_num,
        weibo_count_30,
        weibo_count_7,
        weibo_count_1,
        react_score, 
        react_rank,
        react_num,
        react_weibo,
        react_comment,
        react_story,
        impact_score, 
        impact_rank,
        impact_num,
        search_num,
        admire_score,
        admire_rank,
        admire_num,
        flower_fans,
        flower_num
        ))


    output_handle_1.close()






