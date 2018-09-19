from django.db import models


import re
import jieba
import pandas as pd
from django.db import connection
from zhon.hanzi import punctuation   #中文标点符号

# Create your models here.

def handler_data():
    sql_asks = "select * from 'asks_answer'"
    df = pd.read_sql_query(sql_asks, connection)
    df = df[df['part'] == '0']
    # 获取class4的字典，keys: indexs, values: questions
    class4_dic = {}
    class4 = df['class4']
    class4_dic = class4.to_dict()
    word_dic = {}
    df_dict = df.to_dict(orient='index')

    # jieba分词，获得分词字典,
    for k, v in class4_dic.items():
        v = re.sub(r'[%s]+' % punctuation, '', v)
        seg_list = jieba.cut_for_search(v)
        word = ','.join(seg_list)
        word_dic[k] = word

    return word_dic, df_dict
