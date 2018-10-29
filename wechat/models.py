from django.db import models


import re
import jieba
import pandas as pd
from django.db import connection
from zhon.hanzi import punctuation   #中文标点符号
import string

# Create your models here.


"""
def handler_data():
    '''
    建立分词字典
    :return:
    '''
    sql_asks = "select * from 'asks_answer'"
    df = pd.read_sql_query(sql_asks, connection)
    df.drop_duplicates("class4", inplace=True)     # 使用pandas丢弃重复值
    df = df[df['part'] == '0']

    # 停用词
    stop_words_file = 'stopwords.txt'
    stopwords = get_custom_stopwords(stop_words_file)

    # 获取class4的字典，keys: indexs, values: questions
    class4_dic = {}
    class4 = df['class4']
    class4_dic = class4.to_dict()
    word_dic = {}
    df_dict = df.to_dict(orient='index')

    # jieba分词，获得分词字典,
    for k, v in class4_dic.items():
        v = re.sub(r'[%s]+' % punctuation, '', v)         # 去除中文字符
        # v = re.sub(r'[%s]+' % string.punctuation, '', v)  # 去除英文字符
        # seg_list = jieba.cut_for_search(v)
        # word_cut = ','.join(seg_list)

        word_cut = re.sub(r'[%s]+' % string.punctuation, '',
                             " ".join([i for i in jieba.cut_for_search(v) if i not in stopwords]))  # 去除英文字符

        word_dic[k] = word_cut

    return word_dic, df_dict
"""


def handler_data():
    """
    建立分词字典
    :return:
    """
    word_dic = {}
    # 停用词
    stop_words_file = 'stopwords.txt'
    stopwords = get_custom_stopwords(stop_words_file)
    df_dict, class4_dic = Processing_Data()

    # jieba分词，获得分词字典,
    for k, v in class4_dic.items():

        # v = re.sub(r'[%s]+' % string.punctuation, '', v)  # 去除英文字符
        # seg_list = jieba.cut_for_search(v)
        # word_cut = ','.join(seg_list)
        v = re.sub('\s', '', v)                    # 去除空格
        v = re.sub(r'[%s]+' % punctuation, '', v)  # 去除中文字符
        word_cut = re.sub(r'[%s]+' % string.punctuation, '',
                          " ".join([i for i in jieba.cut_for_search(v) if i not in stopwords]))  # 去除英文字符

        word_dic[k] = word_cut

    return word_dic, df_dict


def Processing_Data():
    # conn = sqlite3.Connection('LZ_DB.db')
    sql = "select * from ask_answer"
    df = pd.read_sql_query(sql, connection)
    df.drop_duplicates('question', inplace=True)  # 使用pandas丢弃重复值
    question_dic = {}
    question = df['question']
    question_dic = question.to_dict()
    df_dict = df.to_dict(orient='index')

    return df_dict, question_dic


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

    return cutted_word