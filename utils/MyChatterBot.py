# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '22/10/18 下午6:16'

#!/usr/bin/python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


my_bot = ChatBot(
    "Training demo",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3',
    # 输入输出插件
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    # 特殊的逻辑插件
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter',
        "chatterbot.logic.BestMatch",
    ],
)

conversation = [
    "你叫什么名字？",
    "我叫ChatterBot。",
    "今天天气真好",
    "是啊，这种天气出去玩再好不过了。",
    "那你有没有想去玩的地方？",
    "我想去有山有水的地方。你呢？",
    "没钱哪都不去",
    "哈哈，这就比较尴尬了",
]

my_bot.set_trainer(ListTrainer)
my_bot.train(conversation)
my_bot.train("chatterbot.corpus.chinese")

while True:
    try:
        # input("user:\n")
        bot_input = my_bot.get_response(None)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
    # print(my_bot.get_response(input("user:\n")))
