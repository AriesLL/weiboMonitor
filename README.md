weiboMonitor

reference: https://blog.csdn.net/acsyl/article/details/78189042

prerequisite:

pip install requests

pip install bs4 

python 3

example usage:

python ./listUrl_new.py test_input.txt test_output.txt 2 5


input file, specify the monitored weibo id, for example, https://weibo.cn/repost/GmUmH32r2 is the one for test_input.txt

output file, specify the output .txt file name (has to be .txt extension, need to be changed）

start_postition, start page number of the repost, 

batch_number, specify how many pages to crawl

so this command is to 
extract https://weibo.cn/repost/GmUmH32r2?page=2 to https://weibo.cn/repost/GmUmH32r2?page=6

(or 
https://weibo.cn/repost/GmUmH32r2?page=3 to https://weibo.cn/repost/GmUmH32r2?page=7

)
记不清楚了...


output has 4 fields, 
date_time, UID, nickname, repost_text

To add:

scripts to monitor current repost (done, not uploaded yet)
