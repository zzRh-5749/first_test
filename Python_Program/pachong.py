import requests
import json
import re
import pandas as pd
import jieba
import csv
#从网页中找到它的url
url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1413&productId=3510413&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
#京东的headers的配置
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Connection':'close',
'Referer':'https://www.jd.com/'
}
#打开一个名为pinglun13的csv文档，把爬到的数据放进去
with open('F:\Python_Programe\pinglun13.csv', 'a', newline='') as f:  #a为可读可写
    row = ('用户名', '类型', '表盘大小', '评论') #设置四列用来存放数据
    writer = csv.writer(f)
    writer.writerow(row)
for i in range(1,50):    #爬取50页的评论
 url1='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1413&productId=3510413&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold='
 url2='i'
 url3='&pageSize=10&isShadowSku=0&fold=1'
 res=requests.get(url,headers=headers)  #用requests.get获得数据
 jd=json.loads(res.text.lstrip('fetchJSON_comment98vv1413(').rstrip(');'))
 com_list=jd['comments']
 for comment in com_list:
    user = comment['nickname']        #获取用户名
    color = comment['productColor']   #获取表带的颜色
    size = comment['productSize']    #手手表的型号
    test = comment['content']      #评论
        # print(infor)
    with open('F:\Python_Programe\pinglun13.csv', 'a', newline='')as csv_file:
        rows = (user,color,size,test)   #将获取的数据加到csv的每一行中
        writer = csv.writer(csv_file)
        writer.writerow(rows)
print(2)


