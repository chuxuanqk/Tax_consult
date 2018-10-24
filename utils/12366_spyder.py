# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '19/10/18 下午3:19'

import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


def Get_Data(url, data):
    res = requests.post(url=url, data=data)
    soup = BeautifulSoup(res.content, "lxml").text
    soup_json = json.loads(soup)

    return soup_json


def Get_Code(soup_json):
    """
    获取每个页面的ZLCODE，每页有4个ZLCODE
    :param soup_json:
    :return:
    """
    pageContents = soup_json['pageContent']
    Code_list = []
    for i in range(len(pageContents)):
        pageContent = pageContents[i]
        ZLCODE = pageContent['ZLCODE']
        Code_list.append(ZLCODE)

    return Code_list


def Save_Codes():
    # 涉税查询页面
    search_pages = 'http://12366.chinatax.gov.cn/SearchBLH_search.do'

    # 问题解答data
    data = {
        'pageSize': 4,
        'zltype': 2,
        'zlflag': 2,
        'keywords': '',
        'order': 'desc',
        'sortField': 'ZLWFID',
    }
    code_lists = []

    for i in range(1, 1323):
        try:
            data['page'] = i
            soup_json = Get_Data(search_pages, data)
            code_list = Get_Code(soup_json)
            code_lists.extend(code_list)
        except Exception as e:
            print("e:{}".format(str(e)))

    df_code = pd.DataFrame(data=code_lists, columns=['code'])
    df_code.to_csv('code_lists.csv')

    return df_code


def progress(percent, width=50):
    '''进度打印功能'''
    if percent >= 100:
        percent = 100

    show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * ">")  # 字符串拼接的嵌套使用
    print('\r%s %d%%' % (show_str, percent), end='')


def timer(func):
    def wrapper(**kwargs):
        start = time.time()
        res = func(kwargs)
        end = time.time()
        print("speed time:{}".format(end - start))
        return res

    return wrapper


def save_knowledge(knowledge_list):
    knowledge_list = []
    for i in knowledge:
        knowledge_list.append((i['ZLCLJNR'],
                               i['ZLFBRQ'],
                               i['ZLFLAG'],
                               i['ZLGJZ'],
                               i['ZLHYTYPEMC'],
                               i['ZLNR'],
                               i['ZLNRZH'],
                               i['ZLTITLE'],
                               i['ZLTYPEMC'],
                               i['ZLSFYX']))

    column = ['ZLCLJNR', 'ZLFBRQ', 'ZLFLAG', 'ZLGJZ', 'ZLHYTYPEMC', 'ZLNR', 'ZLNRZH', 'ZLTITLE', 'ZLTYPEMC', 'ZLSFYX']
    df_knowledge = pd.DataFrame(data=knowledge_list, columns=column)
    df_knowledge.to_csv('knowledge.csv')



@timer
def Save_knowledge(knowledge):
    # 知识详情页
    knowledge_pages = 'http://12366.chinatax.gov.cn/SearchMxBLH_toDetail.do'

    knowledge_data = {
        'gjz': '',
        'ip': '116.25.147.247, 101.200.106.11',
    }

    codes = pd.read_csv('code_lists.csv')
    code_lists = list(codes.code)

    knowledge_list = []

    for code in code_lists:
        knowledge_data['code'] = code
        knowledge_json = Get_Data(knowledge_pages, knowledge_data)
        bean = knowledge_json['bean']
        knowledge_list.append(bean)

        recv_per = int(100 * len(knowledge_list) / len(code_lists))  # 接收的比例
        progress(recv_per)

    save_knowledge(knowledge_list)
    print("爬取完成")


if __name__ == '__main__':
    knowledge = Save_knowledge()
    print(knowledge)


