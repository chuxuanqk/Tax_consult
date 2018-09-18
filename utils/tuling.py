# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '18/9/18 下午1:48'

import json
import urllib.request

api_url = "http://openapi.tuling123.com/openapi/api/v2"
# text_input = input('我：')


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
            "apiKey": "0780c0fa34924d07b615add8b52cdcaa",
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
    text = TL()