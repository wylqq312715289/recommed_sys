#-*- coding:utf-8 -*-
"""recommed_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from recom.views import index, search1_post, search2_post, search3_post
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', index),
    url(r'^search1-post/$', search1_post), #查看已经浏览过的新闻
    url(r'^search2-post/$', search2_post), #查看user_CF的新闻
    url(r'^search3-post/$', search3_post), #查看item_CF的新闻
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
