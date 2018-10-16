
from django.views import View
from django.shortcuts import render

# Create your views here.


class Tax_calculator(View):
    """
    个人所得税计算器
    """

    def get(self, request):
        return render(request, 'geshui.html', {})


class Get_Inovice(View):
    """
    获取发票代开网页
    """
    def get(self, request):
        return render(request, 'test.html', {})