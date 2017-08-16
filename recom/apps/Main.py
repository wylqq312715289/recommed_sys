# -*- coding:utf-8 -*-
import random
import os,copy,math
import numpy as np
import pandas as pd
import csv
from numpy import linalg as la  #用到别名
from DealFile import read_data, write_data_csv
import time

# 计算平均分
def calcAvg(items):
	# 输入是list, item是['movitemid','rating']
	avg = 0.0
	for item in items: avg += item[1]
	return (avg * 1.0 / len(items) )

# 使用 |A&B|/sqrt(|A || B |)计算余弦距离
def calcCosDistSpe(useritems, nearitems):
	user_avg = calcAvg( useritems )
	near_avg = calcAvg( nearitems )
	u1_u2 = 0 # 交集个数
	for u1 in useritems:
		for u2 in nearitems:
			if u1[0] == u2[0] and u1[1] > user_avg and u2[1] > near_avg:
				u1_u2 += 1
	u1u2 = len(useritems)*len(nearitems)*1.0
	return u1_u2 / math.sqrt(u1u2)

# 计算最近的K个邻居
def calcNears( pd_data, useridx, k = 6):
	#pdata:是user-item打分矩阵
	nears = []
	nears_list = []
	user2items =  pd_data[pd_data.user_idx == useridx]['item_idx'].values
	#1. 获取所有邻居
	for item in user2items:
		item2users =  pd_data[pd_data.item_idx == item]['user_idx'].values
		for user in item2users:
			if user != useridx and user not in nears:
				nears.append(user)
	#2. 计算每个邻居的邻近度
	useritems = (pd_data[pd_data.user_idx == useridx]).loc[ :,['item_idx','rating'] ].values
	for near in nears:
		nearitems = (pd_data[pd_data.user_idx == near]).loc[ :,['item_idx','rating'] ].values
		dist = calcCosDistSpe(useritems, nearitems) 
		#print "dis=",dist
		nears_list.append([dist, near])
	#3. 相近度排序只取前k个近邻
	nears_list.sort( reverse = True )
	return nears_list[:k]

# 使用UserFC进行推荐
# 输入：user 和 data评分表的合并表, 邻居的数量, 希望推荐的数量
# 输出：推荐的新闻的ID编号,输入用户的电影列表,电影对应用户的反序表，邻居列表
def recommendByUserCF(useridx, k = 10, wantedNum = 6):
	url = os.getcwd()
	pd_data = pd.read_csv(url+"/recommed_sys/recom/apps/data/user_item_score.csv")
	#1. 计算最近的K个邻居
	nears = calcNears(pd_data, useridx, k)
	#2. 对邻居的所有看过的电影，基于邻近情况，计算推荐度
	movieitems_dist = dict()
	user_already_look_movies = (pd_data[pd_data.user_idx == useridx ]) ['item_idx'].values
	for item in nears:
		nearitems = (pd_data[pd_data.user_idx == item[1] ]) ['item_idx'].values
		for movie in nearitems:
			if movie in user_already_look_movies: continue #用户看过的item不推荐
			if movieitems_dist.has_key(movie):
				movieitems_dist[movie] += item[0]
			else:
				movieitems_dist[movie] = item[0]
	#3. 基于推荐度，进行排序
	Seriesitems = pd.Series(movieitems_dist).order()
	#print '最值得推荐的几个新闻编号以及相似度为\n', Seriesitems.tail(wantedNum)
	#4. 输出
	recommned_moiveID_df = pd.DataFrame(Seriesitems.tail(wantedNum).keys(), columns=['item_idx'] )
	#print recommned_moiveID_df
	recomm_merger = pd.merge(pd_data, recommned_moiveID_df, on='item_idx')
	#print recomm_merger.loc[:, ['item_id','title'] ].groupby("title").count()
	recommend_ans = recomm_merger.loc[:, ['item_idx','title'] ].title.drop_duplicates()
	#print recommend_ans
	return list( recommend_ans )

def get_dic_file(url):
	df = pd.read_csv(url).values
	dic = dict()
	for value in df: dic[value[0]] = value[1]
	return dic

#查看用户看过哪些新闻
def get_Have_Watched_News( useridx ):
	url = os.getcwd()
	user_item_score = pd.read_csv(url+"/recommed_sys/recom/apps/data/user_item_score.csv")
	titles = (user_item_score[ user_item_score.user_idx == useridx ]).title.drop_duplicates()
	return list( titles )

if __name__ == '__main__':
	userid = 1
	get_Have_Watched_News( userid )
	recommendByUserCF(userid, 10, 4)