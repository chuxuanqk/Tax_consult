# -*- coding:utf-8 -*-
__author__ = 'Saber'
__date__ = '16/10/18 上午11:46'

from django.conf.urls import url, include

from Tax_cal.views import Tax_calculator


urlpatterns = [
    url('geshui/', Tax_calculator.as_view(), name='个税计算器')
        ]