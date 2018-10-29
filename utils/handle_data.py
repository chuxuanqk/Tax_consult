# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '18/10/18 上午11:05'

import re
import jieba
import time
import string
import sqlite3
import pandas as pd
from django.db import connection
from zhon.hanzi import punctuation   #中文标点符号


def timer(func):
    def wrapper():
        start = time.time()
        res = func()
        end = time.time()
        print("speed time:{}".format(end-start))
        return res
    return wrapper


def chinese_word_cut(mytext):
    """
    对文本进行切词，并过滤掉中文字符和停用词。
    """
    stop_words_file = '../stopwords.txt'
    stopwords = get_custom_stopwords(stop_words_file)
    mytext = re.sub('\s', '', mytext)                       # 去除空格符
    mytext = re.sub(r'[%s]+' % punctuation, '', mytext)    # 去除中文标点符号
    # 去除英文标点符号，处理停用词，分词
    cutted_word = re.sub(r'[%s]+' % string.punctuation, '',
                         " ".join([i for i in jieba.cut_for_search(mytext) if i not in stopwords]))

    return cutted_word


@timer
def handler_data():
    """
    建立分词字典
    :return:
    word_dic:问句字典，key-->id, value-->question
    df_dict:数据字典
    """
    word_dic = {}

    df_dict, class4_dic = Processing_Data()

    # jieba分词，获得分词字典,
    for k, v in class4_dic.items():
        word_cut = chinese_word_cut(v)
        word_dic[k] = word_cut

    return word_dic, df_dict


def Processing_Data(sql="select * from ask_answer", column='question'):
    connection = sqlite3.Connection('../LZ_DB.db')

    df = pd.read_sql_query(sql, connection)
    df.drop_duplicates(column, inplace=True)  # 使用pandas丢弃重复值
    question_dic = {}
    question = df[column]
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





