'''
Created on 2020年3月1日

@author: xiaojihua

监控腾讯乐问社区，当有新的帖子或者新的乐问时，系统声音提醒，并同时打开浏览器访问对应url，便于直接处理。

'''

import urllib 
import urllib.request 
import requests
import sys
import os
import time
import webbrowser
from urllib.parse import urljoin

company='eb03d7d6d9a911e796d85254005b9a60'

#下载文件第三种方法
url='https://lexiangla.com/?company_from=eb03d7d6d9a911e796d85254005b9a60'

cookies = {   'XSRF-TOKEN': 'LxK9zXf7nokr3DJK5qCVqSxuhBIYRdp9TRN8XqIl2QIHho6g%252BZEZDf0Ay461XMwKVc%252Bp3NyBtSQLHrMdUdeb0gU6xQZY5zfWHsao086kUs4%253D'
            , 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbGV4aWFuZ2xhLmNvbVwvYXV0aFwvd2VjaGF0X2xvZ2luX2NhbGxiYWNrIiwiaWF0IjoxNTg0MzI3NzgzLCJleHAiOjE1ODY5MTk3ODMsIm5iZiI6MTU4NDMyNzc4MywianRpIjoiU3lQcTNPd1FRakZBTkZQZiIsInN1YiI6ImI2MTJhM2Q4MDM3YzExZTk4ZjViNTI1NDAwMDVmNDM1IiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.OiRffc3b2eIPbYv1KXU_uwhgNjffV9QaARXuOLTvm_4'
            , 'company_server_type':'workwechat'
            , 'company_code':'eb03d7d6d9a911e796d85254005b9a60'
            , 'company_display_name':'%E4%B8%AD%E4%BF%A1%E9%93%B6%E8%A1%8C'
            , 'oneapmbiswitch':'event=0'
         }

# 在Cookie Version 0中规定空格、方括号、圆括号、等于号、逗号、双引号、斜杠、问号、@，冒号，分号等特殊符号都不能作为Cookie的内容。
r = requests.get(url, cookies=cookies)

#r = requests.get(url) 
#with open("citic_rainbow_1.txt", "wb") as code:
#     code.write(r.content)
print(sys.getdefaultencoding())
count=0
listen_action=['question_add','thread_add'] #need listening
# answer_add  回答问题 
latest_list=[]
title=[]
file='SoundTest.wav'
#url='https://lexiangla.com/questions?company_from=eb03d7d6d9a911e796d85254005b9a60'
while True:
    url="https://lexiangla.com/api/v1/feeds?limit=10&offset=0&scope=company"
    r2 = requests.get(url , cookies=cookies) 
    latest_data=r2.json()
# action: "thread_add" 新帖子  ，     action: "question_add" 新乐问
    i=1 
    for data in latest_data:       
        #print('第',i,'条动作记录！',type(data))
        #print(data['target'])
        #print('id=', data['id'] , '|action=' ,data['action'] )
        id=data['id']
        action=data['action']
        new_tar=data['target']
        
        if action in listen_action:
            #for key,value in data.items():
            #    print(key,'=',value)
            new_tar=data['target']['title']
            new_own=data['owner']['display_name']
            staff_id=data['owner']['id']
            staff_url='https://lexiangla.com/api/v1/staffs/'+staff_id
            r3 = requests.get(staff_url , cookies=cookies) 
            staff_info=r3.json()
           # print(type(staff_info),'|',staff_info)
            staff_dep=staff_info['organizations'] #.replace_all('"\"','')
           # print(type(staff_dep),'|',str(staff_dep))
            if action=='thread_add':               
                #print('时间是：',data['ago']) 
                print(data['ago'],staff_dep[0],'的',data['owner']['display_name'],'发表了：',data['target']['title'])  
                #print('帖子是：','id=',data['target']['id'],'标题是=',data['target']['title'])
                #print('帖子访问url为：'+ 'https://lexiangla.com/threads/',data['target']['id'].strip(),'?company_from=eb03d7d6d9a911e796d85254005b9a60')
                thr_url='https://lexiangla.com/threads/'+data['target']['id'].strip()+'?company_from=eb03d7d6d9a911e796d85254005b9a60'
                #webbrowser.open(thr_url, new=1, autoraise=True)
            if action=='question_add':               
                #print('时间是：',data['ago']) 
                #print('提问人是：',data['owner']['display_name'])  
                #print('问题是：','id=',data['target']['id'],'标题是=',data['target']['title'])
                #print('问题访问url为：'+ 'https://lexiangla.com/questions/',data['target']['id'].strip(),'?company_from=eb03d7d6d9a911e796d85254005b9a60') 
                print(data['ago'],staff_dep[0],'的',data['owner']['display_name'],'提出问题：',data['target']['title']) 
                que_url='https://lexiangla.com/questions/'+data['target']['id'].strip()+'?company_from=eb03d7d6d9a911e796d85254005b9a60'
                #webbrowser.open(que_url, new=1, autoraise=True) 
                #获取提问人的详细分行信息                
                #for key,value in staff_info.items():
                #    print(key,'=',value)
            if id not in latest_list:
                latest_list.append(id)
                title.append(staff_dep[0]+'|'+new_own+'|'+new_tar)
                os.system(file)
                if action=='thread_add':
                    webbrowser.open(thr_url, new=1, autoraise=True)
                else:
                    webbrowser.open(que_url, new=1, autoraise=True)      
                #os.system('"C:\Program Files (x86)\Windows Media Player\wmplayer.exe "' + file)
        i=i+1
    count=count+1
    print("####第",count,"次运行！时间是：",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print("####今日新问题的有： ",len(title) ,'个' , '具体为：' , title)
    print('----------------------------------end-----------------------------------')
    #break
    time.sleep(5)
    if count>5:
        break
    #300秒后继续第二次执行
"""with open('citic_rainbow_latest10.txt', 'wb') as fd:
    for chunk in r2.iter_content():
        fd.write(chunk)
"""

def main():
    print('here is main')

if __name__ == '__main__':
    print('go to main')
    pass