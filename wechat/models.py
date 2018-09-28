from django.db import models


import re
import jieba
import pandas as pd
from django.db import connection
from zhon.hanzi import punctuation   #中文标点符号
import string

# Create your models here.

def handler_data():
    """
    建立分词字典
    :return:
    """
    sql_asks = "select * from 'asks_answer'"
    df = pd.read_sql_query(sql_asks, connection)
    df.drop_duplicates("class4", inplace=True)     # 使用pandas丢弃重复值
    df = df[df['part'] == '0']
    # 获取class4的字典，keys: indexs, values: questions
    class4_dic = {}
    class4 = df['class4']
    class4_dic = class4.to_dict()
    word_dic = {}
    df_dict = df.to_dict(orient='index')

    # jieba分词，获得分词字典,
    for k, v in class4_dic.items():
        v = re.sub(r'[%s]+' % punctuation, '', v)         # 去除中文字符
        v = re.sub(r'[%s]+' % string.punctuation, '', v)  # 去除英文字符
        seg_list = jieba.cut_for_search(v)
        word = ','.join(seg_list)
        word_dic[k] = word

    return word_dic, df_dict


# 从中文停用词表里面，把停用词作为列表格式保存并返回, 使用的哈工大停用词表文件
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list


def pd_search(sql="select * from 'asks_answer'"):
    df = pd.read_sql_query(sql, connection)

    return df


def chinese_word_cut(mytext):
    """
    对文本进行切词，并过滤掉中文字符和停用词。
    """
    stop_words_file = 'stopwords.txt'
    stopwords = get_custom_stopwords(stop_words_file)

    cutted_word = re.sub(r'[%s]+' % punctuation, '',
                         " ".join([i for i in jieba.cut_for_search(mytext) if i not in stopwords]))

    str_len = len(cutted_word)
    return cutted_word, str_len