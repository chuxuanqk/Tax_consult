from django.shortcuts import render

# Create your views here.
import logging
import hashlib
import json
import time
import xml.etree.ElementTree as ET

from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import response



# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
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
            logging.error("token=%s" % token)
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()

            logging.error("nonce=%s" % nonce)
            logging.error("echostr=%s" % echostr)
            logging.error("timestamp=%s" % timestamp)
            logging.error("hashcode=%s" % hashcode)
            logging.error("signature=%s" % signature)
            if hashcode == signature:
                logging.error(hashcode)
                return HttpResponse(echostr)
            else:
                return HttpResponse("field")
        except Exception as e:
            logging.error('%s' % e)
            return HttpResponse(echostr)
    # else:
    #     othercontent = autoreply(request)
    #     return HttpResponse(othercontent)



#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，
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

        toUser = FromUserName
        fromUser = ToUserName


        if msg_type == 'text':
            content = "您好,欢迎来到Python大学习!希望我们可以一起进步!"
            replyMsg = TextMsg(toUser, fromUser, content)
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
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
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