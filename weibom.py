#!/bin/env python
# coding:utf-8


import time
import os
import requests
import re
import json
import sys
import time
from bs4 import BeautifulSoup
import csv
import codecs
from get_uid import get_excel_uid

reload(sys)
sys.setdefaultencoding('utf-8')


#此处填写需要下载的用户id


class UserClient:
    def __init__(self, uid):
        self.session = requests.Session()
        self.uid = uid

    def get_info(self):
        url="http://m.weibo.cn/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s&type=uid&value=%s" % (self.uid,self.uid,self.uid)
        response = self.session.get(url)
        if response.status_code == 200:
            text = response.content
            print(text)
            jsondata = json.loads(text)
            cards = jsondata["cards"]

            with open(infofile,'ab') as f:
                for card in cards:
                    card_group = card['card_group']
                    for card in card_group:
                        print(card['item_name']+":"+card['item_content'])
                        writer = csv.writer(f, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(
                            [card['item_name'],card['item_content']])
        else:
            return None

    def get_weibos(self,page_start=1,page_end=None):
        curpage = page_start
        fetching = True
        err_count = 0
        while fetching:

            url = "http://m.weibo.cn/container/getIndex?uid=%s&luicode=20000174&type=uid&value=%s&containerid=107603%s&page=%d" % (self.uid,self.uid,self.uid,curpage)
            print(url)
            response = self.session.get(url)
            print(response.status_code)
            if response.status_code == 200:

                jsondata = response.json()

                cardlistInfo = jsondata['cardlistInfo']
                total = cardlistInfo['total']
                page = cardlistInfo['page']
                print(page)

                if page is None:
                    fetching=False
                else:
                    cards = jsondata['cards']
                    lines=[]
                    with open(weibofile, 'ab') as f:
                        for card in cards:
                            mblog = card['mblog']
                            created_at = mblog['created_at']
                            id = mblog['id']
                            text = mblog['text']
                            print("text的内容是：",text)
                            soup = BeautifulSoup(text,'html.parser')
                            try:
                                place = soup.find(attrs = {'class':"surl-text"}).text
                            except:
                                place = "None"
                            #print(place)
                            newtext=''.join(soup.stripped_strings)
                            source = mblog['source']
                            reposts_count = mblog['reposts_count']
                            comments_count = mblog['comments_count']
                            attitudes_count = mblog['attitudes_count']

                            writer = csv.writer(f, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            print(newtext.encode('utf-8'))
                            writer.writerow(
                                [str(id),str(created_at),attitudes_count,comments_count,reposts_count,newtext.encode('utf-8'),place.encode("utf-8")])

                    curpage += 1

                time.sleep(0.5)

            else:
                time.sleep(5)
                err_count += 1
                if err_count ==3:
                    curpage += 1
                    err_count=0

            if curpage == page_end:
                fetching = False




if __name__ == '__main__':
    uid_list = get_excel_uid("uid_file.xlsx")  # 接收一个uid列表
    for uid in uid_list:
        if not os.path.exists(uid):
            os.mkdir(uid)

        infofile = os.path.join(uid, 'info.csv')
        if os.path.exists(infofile):
            os.remove(infofile)
        with open(infofile, 'wb') as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.writer(f, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['属性', '值'])

        weibofile = os.path.join(uid, 'weibo.csv')
        if os.path.exists(weibofile):
            os.remove(weibofile)
        with open(weibofile, 'wb') as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.writer(f, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['微博ID', '创建时间', '点赞', '评论', '转发', '内容', '地点'])

            # 遍历uid列表
        user = UserClient(uid)
        try:
            user.get_info()
        except:
            pass
        user.get_weibos(1)


