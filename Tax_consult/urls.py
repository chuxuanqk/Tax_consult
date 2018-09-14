"""Tax_consult URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Tax_consult import settings
from django.views import static

from wechat.views import weixin_main, GetInfoView, GetListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^wechat/$', weixin_main, name='wechat'),

    url(r'^GetInfoView/(.+)/$', GetInfoView.as_view(), name='GetInfoView'),
    url(r'^GetListView/(.*?)/$', GetListView.as_view(), name='获取问题列表'),
]
