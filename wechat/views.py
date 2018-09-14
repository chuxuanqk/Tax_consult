from django.shortcuts import render

# Create your views here.
import logging
import hashlib
import json
import time
import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET

from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from django.db import connection


# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        try:
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)
            # 服务器配置中的token = 'hello'
            token = "hello"
            # 把参数放到list中排序后合成一个字符串，
            # 再用sha1加密得到新的字符串与微信发来的signature对比，
            # 如果相同就返回echostr给服务器，校验通过
            list = [token, timestamp, nonce]
            list.sort()
            list = ''.join(list)
            hashcode = hashlib.sha1(list.encode("utf-8")).hexdigest()

            if hashcode == signature:
                logging.error(hashcode)
                return HttpResponse(echostr)
            else:
                return HttpResponse("field")
        except Exception as e:
            return HttpResponse(echostr)
    # 微信正常的收发消息是用POST方法。
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)


# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，
# 就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text
        Content = xmlData.find('Content').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':

            ask_message = Content
            list_dic = []
            list_dic = query_answer(ask_message)
            list_4 = list_dic[:4]
            message = "\n".join(list_4)

            replyMsg = TextMsg(toUser, fromUser, message)
            print("成功了!!!!!!!!!!!!!!!!!!!")
            print(replyMsg)
            return replyMsg.send()

    except Exception as Argment:
        return Argment


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    """
    将要发送的信息转换成为xml的格式
    """

    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        """
        发送信息给微信服务器
        :return:
        """
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)


class GetInfoView(View):
    """
    超链接文本信息
    """

    def get(self, request, param1):
        id = param1
        sql = "select * from 'asks_answer' where id={id}".format(id=id)
        df = pd.read_sql_query(sql, connection)
        answer = df['answer']
        answer = answer.values
        answer = answer[0]
        print('answer{}'.format(answer))

        return render(request,'answer.html',locals())



class GetListView(View):
    """
    获取答案超链接
    """
    def get(self, request, param):
        list_dic = query_answer(param)
        print("成功了!!!!!!!!!!!!!!!!!!!")
        return HttpResponse(list_dic[:4])

def query_answer(param):
    """
    获取回答链接列表
    :param param: question
    :return:
    """

    question = param
    sql = "select * from 'asks_answer' where class4 LIKE '%{ask}%'".format(ask=question)
    df = pd.read_sql_query(sql, connection)
    df = df[df['part'] == '0']
    df = df[['class4', 'id']]
    # dataframe类型转换为字典类型
    dict_id = {}
    dict_id = df.set_index('id').T.to_dict('list')

    head = "您是否是想要咨询以下问题?"
    list_dic = [head]
    i = 0
    for key, value in dict_id.items():
        i += 1
        # content = "{i}、<a href='http://0.0.0.0:8000/GetInfoView/{id_1}/'>{question}</a>" \
        #     .format(i=i, id_1=key, question=value[0])
        content = "{i}、<a href='http://telent.pythonanywhere.com/GetInfoView/{id_1}/'>{question}</a>" \
            .format(i=i, id_1=key, question=value[0])

        list_dic.append(content)

    return list_dic