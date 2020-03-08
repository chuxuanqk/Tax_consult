# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '18/9/18 下午1:48'

import json
import requests
import urllib.request

api_url = "http://openapi.tuling123.com/openapi/api/v2"
# text_input = input('我：')
# 使用前请先前往 http://www.tuling123.com/register/index.jhtml
# 申请 API key 谢谢
# 另外需要 requests 支持
# 修改成调用图灵官方接口
url = "http://www.tuling123.com/openapi/api"
# apikey = '308ea23fe1254113aad1017164274a84'
apikey = "517a329a26474e9c94a963b2d8a839d3"

#使用初版api
def tuling(content):
    querystring = {
        "key": apikey,
        "info": content,
    }

    response = requests.request("GET", url, params=querystring)

    response_json = response.json()
    msg = response_json.get('text')

    return msg


# 使用V2版api
def TL(msg):
    req = {
        "perception":
        {
            "inputText":
            {
                "text": msg,
            },

            # "selfInfo":
            # {
            #     "location":
            #     {
            #         "city": "深圳",
            #         "province": "上海",
            #         "street": "文汇路"
            #     }
            # }
        },

        "userInfo":
        {
            "apiKey": apikey,
            "userId": "OnlyUseAlphabet"
        }
    }
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')

    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    # print('Turing的回答：')
    # print('code：' + str(intent_code))
    # print('text：' + results_text)
    return results_text


if __name__ == '__main__':
    text = tuling("hello")
    print(text)