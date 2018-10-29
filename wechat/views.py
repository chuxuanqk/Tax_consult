
# Create your views here.
import re
import time
import jieba
import string
import logging
import hashlib
import pandas as pd
import xml.etree.ElementTree as ET

from .models import *
from .tuling import TL

from django.views import View
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

#在服务器启动的时候进行好分词
word_dic, df_dict = handler_data()

logger = logging.getLogger("django")

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


class Tax_Bot(View):
    """
    网页版聊天机器人
    """
    def post(self, request):

        content = autoreply(request)
        return HttpResponse(content)



# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，
# 就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
def autoreply(request):
    try:
        webData = request.body

        xmlData = ET.fromstring(webData)

        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        msg_type = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            Content = xmlData.find('Content').text
            ask_message = Content
            list_dic = []
            list_dic = query_answer(ask_message)
            list_4 = list_dic[:4]
            message = "\n".join(list_4)

            replyMsg = TextMsg(toUser, fromUser, message)
            print("成功了!!!!!!!!!!!!!!!!!!!")
            print(replyMsg)
            return replyMsg.send()

        elif msg_type == 'image':
            PicUrl = xmlData.find('PicUrl').text
            MediaId = xmlData.find('MediaId').text
            message = 'hello'

            replyMsg = TextMsg(toUser, fromUser, message)

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

        return render(request, 'answer.html', locals())


class GetListView(View):
    """
    获取答案超链接
    """

    def get(self, request, param):
        list_dic = query_answer(param)
        print("成功了!!!!!!!!!!!!!!!!!!!")
        re = {
            'code': '200',
            'message': '成功',
            'data': list_dic[:4],
        }

        return JsonResponse(re, content_type='application/json')


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
        content = "{i}、<a href='http://telent.pythonanywhere.com/GetInfoView/{id_1}/'>{question}</a>" \
            .format(i=i, id_1=key, question=value[0])
        list_dic.append(content)

    return list_dic


class talkView(View):
    def get(self, request):

        return render(request, 'talk.html', {})


class Get_talkView(View):
    """
    新版
    """

    def get(self, request):
        return render(request, 'talk.html', {})

    def post(self, request):
        source = request.POST.get('msg')
        num_id = request.POST.get('num_id','-1')

        list_res = self.get_list_res(num_id, source)

        rew = {
            'code': '200',
            'message': '成功',
            'data': list_res,
        }
        return JsonResponse(rew, content_type='application/json')

    def search_id(self, num_id):
        sql_asks = "select * from 'ask_answer' where id={id}".format(id=num_id)
        df = pd.read_sql_query(sql_asks, connection)
        data_dict = df.to_dict(orient='index')
        for k, v in data_dict.items():
            answer = v['answer']

        return answer

    def search(self, question, number=4):
        # 提问处理
        question = chinese_word_cut(question)

        logger.info("搜索关键词：{}".format(question))

        word_list = question.split(' ')

        # 对word_count进行初始化赋值
        word_count = {}
        for k, v in word_dic.items():
            word_count[k] = 0

        # 对word_list在问句中出现的词频进行排序
        for word in word_list:
            for k, v in word_dic.items():
                v = v.split(' ')
                if word in v:
                    word_count[k] += 1

        answer = sorted(word_count.items(), key=lambda word_count: word_count[1], reverse=True)
        idex_list = []

        for value in answer[:number]:
            if value[1] != 0:
                idex_list.append(value[0])

        id_list = []
        answer_list = []
        question_list = []
        answer_dic = {}
        question_dic = {}

        # for i in idex_list:
        #     id_dic = df_dict[i]
        #     id_list.append(id_dic['id'])
        #     answer_list.append(id_dic['answer'])
        #     question_list.append(id_dic['class4'])
        #     answer_dic[id_dic['id']] = id_dic['answer']
        #     question_dic[id_dic['id']] = id_dic['class4']
        for i in idex_list:
            id_dic = df_dict[i]
            id_list.append(id_dic['id'])
            answer_list.append(id_dic['answer'])
            question_list.append(id_dic['question'])
            answer_dic[id_dic['id']] = id_dic['answer']
            question_dic[id_dic['id']] = id_dic['question']

        logger.info("答案：{}".format(answer_dic))
        return answer_dic, question_dic, question_list

    def get_list_res(self, num_id, source):

        if num_id == '-1':
            answer_dic, question_dic, question_list = self.search(source)
            list_len = len(question_list)

            content = []
            list_res = []
            if list_len == 1:
                head = "以下是您咨询的答案:"
                list_res.append(head)
                for k, v in answer_dic.items():
                    content = v
                list_res.append(content)
                list_res = '<br>'.join(list_res)
            elif list_len > 1:
                head = "以下是您可能想要咨询的问题:"
                list_res.append(head)
                for k, v in question_dic.items():
                    v = re.sub('\s', '', v)  # 去除空格符
                    link = "<a href='#' onclick=showAsk('{id}','{question}')>{question_1}</a>" \
                        .format(question=v, id=k, question_1=v)
                    content.append(link)
                list = '<br>'.join(content)
                list_res.append(list)
                list_res = '<br>'.join(list_res)
            else:
                # 图灵
                list_res = TL(source)
        else:
            list_res = self.search_id(num_id)

        return list_res


'''
class Get_talkView_old(View):
    """
    网页版聊天
    """

    def get(self, request):
        msg = "您好！税务智能客服很高兴为您服务，请问您有什么问题需要咨询的？"
        return render(request, 'talk.html', {'msg':msg})

    def post(self, request):
        source = request.POST.get('msg')
        num_id=request.POST.get('num_id',-1)

        list_count, list_dic = self.talk_query(source)

        print("成功了!!!!!!!!!!!!!!!!!!!")
        content = []
        list_res = []

        if list_count == 1:
            head = "以下是您咨询的答案:"
            list_res.append(head)
            for k, v in list_dic.items():
                content = v['answer']
            list_res.append(content)
            list_res = '<br>'.join(list_res)
        elif list_count > 1:
            head = "以下是您可能想要咨询的问题:"
            list_res.append(head)
            for k, v in list_dic.items():
                link = "<a href='#' onclick=showAsk('{id}','{question}')>{question_1}</a>" \
                    .format(question=v['class4'], id=v['id'],question_1=v['class4'])
                content.append(link)
            content = content[:4]
            list = '<br>'.join(content)
            list_res.append(list)
            list_res = '<br>'.join(list_res)
        else:
            list_res = TL(source)
            print(list_res)

        rew = {
            'code': '200',
            'message': '成功',
            'data': list_res,
        }

        return JsonResponse(rew, content_type='application/json')

    def talk_query(self, param):
        question = param
        sql = "select  * from 'asks_answer' where class4 LIKE '%{ask}%'".format(ask=question)
        df = pd.read_sql_query(sql, connection)
        df.drop_duplicates("class4",inplace=True)
        df = df[df['part'] == '0']
        # df = df[['class4', 'id']]
        # dataframe类型转换为字典类型
        # dict_id = {}
        # dict_id = df.set_index('id').T.to_dict('list')
        data_count = df.iloc[:, 0].size
        data_dict = df.to_dict(orient='index')
        return data_count, data_dict
'''