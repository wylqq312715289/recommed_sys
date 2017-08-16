# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
import os
#from django.core.context_processors import csrf
# Create your views here.
#from apps.Main import get_Have_Watched_News, recommendByUserCF

from apps.Main5_CF_item import recommendByItemCF,get_Have_Watched_News
from apps.Main5_CF_user import recommendByUserCF

#判断输入的内容是否为0到9999的数字
def is_num_by_except(num):
	flag = 1
	try: num = int(num)
	except ValueError: flag = 0
	return flag and (num>=0 and num <= 9999) 

#主界面
def index(request):
	#return HttpResponse("Hello world！ This is my first trial. [Poll的笔记]")
	#return Http404
	url = os.getcwd()
	dic = dict()
	useridx = "NULL"
	dic["useridx"] = useridx
	#return render(request, "homepage.html")
	return render(request, url +"/recommed_sys/recom/static/homepage.html", dic)

#查看已经浏览过的新闻
def search1_post(request):
	url = os.getcwd()
	#dic.update(csrf(request))
	dic = dict()
	useridx = "NULL"
	
	if request.POST:
		try:
			useridx = request.POST.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.POST.get('useridx') )
		except: return index(request)
	else: 
		try:
			print request.GET
			useridx = request.GET.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.GET.get('useridx') )
		except: return index(request)
		
	have_ans = []
	have_ans = get_Have_Watched_News( useridx )
	dic["useridx"] = useridx
	dic["have_ans"] = have_ans
	return render(request, url +"/recommed_sys/recom/static/have_already_watched_news.html", dic)

#查看user_CF的新闻
def search2_post(request):
	url = os.getcwd()
	#dic.update(csrf(request))
	dic = dict()
	useridx = "NULL"
	if request.POST:
		try:
			useridx = request.POST.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.POST.get('useridx') )
		except: return index(request)
	else: 
		try:
			print request.GET
			useridx = request.GET.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.GET.get('useridx') )
		except: return index(request)
	#if is_num_by_except(useridx) == False:
	have_ans = []
	recommend_byuser_ans = []
	recommend_byitem_ans = []
	#have_ans = get_Have_Watched_News( useridx )
	recommend_byuser_ans = recommendByUserCF( useridx )
	#recommend_byitem_ans = recommendByItemCF( useridx )
	dic["useridx"] = useridx
	dic["have_ans"] = have_ans
	dic["recommend_byuser_ans"] = recommend_byuser_ans
	dic["recommend_byitem_ans"] = recommend_byitem_ans
	return render(request, url +"/recommed_sys/recom/static/user_CF.html", dic)

#查看item_CF的新闻
def search3_post(request):
	url = os.getcwd()
	#dic.update(csrf(request))
	dic = dict()
	useridx = "NULL"
	if request.POST:
		try:
			useridx = request.POST.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.POST.get('useridx') )
		except: return index(request)
	else: 
		try:
			print request.GET
			useridx = request.GET.get('useridx')
			if is_num_by_except(useridx) == False:
				return index(request)
			useridx = int( request.GET.get('useridx') )
		except: return index(request)
	#if is_num_by_except(useridx) == False:
	have_ans = []
	recommend_byuser_ans = []
	recommend_byitem_ans = []
	#have_ans = get_Have_Watched_News( useridx )
	#recommend_byuser_ans = recommendByUserCF( useridx )
	recommend_byitem_ans = recommendByItemCF( useridx )
	dic["useridx"] = useridx
	dic["have_ans"] = have_ans
	dic["recommend_byuser_ans"] = recommend_byuser_ans
	dic["recommend_byitem_ans"] = recommend_byitem_ans
	return render(request, url +"/recommed_sys/recom/static/item_CF.html", dic)
