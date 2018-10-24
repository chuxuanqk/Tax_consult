# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '22/10/18 上午10:50'

import time
import json
import asyncio
import aiohttp
import requests
import pandas as pd
from bs4 import BeautifulSoup


def timer(func):
    def wrapper(**kwargs):
        start = time.time()
        res = func(kwargs)
        end = time.time()
        print("speed time:{}".format(end-start))
        return res
    return wrapper


async def job(page):
    pages_url = 'http://12366.chinatax.gov.cn/SearchBLH_search.do'
    data = {
        'page': page,
        'pageSize': 4,
        'zltype': 2,
        'zlflag': 2,
        'keywords': '',
        'order': 'desc',
        'sortField': 'ZLWFID',
    }

    async with aiohttp.request('POST', pages_url, data=data) as resp:
        text = await resp.text()

    return text

@timer
async def main(loop):
    tasks = [loop.create_task(job(i)) for i in range(2)]
    finished, unfinished = await asyncio.wait(tasks)
    all_results = [r.result() for r in finished]  # 获取所有结果
    print(all_results)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

