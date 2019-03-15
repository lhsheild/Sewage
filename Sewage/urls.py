"""Sewage URL Configuration

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
from ding_callback import views as callback_views

urlpatterns = [
    # 注册回调
    url(r'^register_callback/', callback_views.register_callback),
    # 获取回调
    url(r'^get_bms_callback/', callback_views.get_bms_callback),
    # 获取失败回调
    url(r'^get_failed_callback/', callback_views.get_failed_callback),
    # 查询回调接口
    url(r'^check_callback_api/', callback_views.check_callback_api),
    # 更新回调接口
    url(r'^update_callback_api/', callback_views.update_callback_api),
    url(r'^admin/', admin.site.urls),
]
