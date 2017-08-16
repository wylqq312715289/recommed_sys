# -*- coding:utf-8 -*-
import random
import os,copy,math
import numpy as np
import pandas as pd
import csv
from numpy import linalg as la  #用到别名
from DealFile import read_data,write_data_csv,read_data_csv
import time,datetime

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

# 使用ItemCF 进行推荐
# 输入：user 和 data评分表的合并表, 邻居的数量, 希望推荐的数量
# 输出：推荐的新闻的ID编号,输入用户的电影列表,电影对应用户的反序表，邻居列表
def recommendByItemCF(useridx, k=8, wantedNum=8):
    st = time.time()
    url = os.getcwd() + "/recommed_sys/recom/apps"
    pd_data = pd.read_csv( url + "/data/user_item_score.csv" )
    item_table = np.array( read_data_csv(url+"/data/item_nearest.csv") ) #获得列表
    movieitems_dist = dict()
    user_already_look_news = (pd_data[ pd_data.user_idx == useridx ])['item_idx'].values
    for itemidx in user_already_look_news: #枚举用户没看过的所有新闻
        nearitems_idx = item_table[itemidx][:k] #查找每个新闻的最近邻居
        a = (pd_data[pd_data.item_idx == itemidx]).loc[ :,['user_idx','rating'] ].values
        nearitems = []
        for idx in nearitems_idx:
            b = (pd_data[pd_data.item_idx == idx]).loc[ :,['user_idx','rating'] ].values
            nearitems.append([calcCosDistSpe(a, b), idx])
        #print "nearest=",itemidx,np.array(nearitems)[:,1]
        for item in nearitems:
            if item[1] in user_already_look_news: continue;
            if movieitems_dist.has_key(item[1]):
                movieitems_dist[item[1]] += item[0]
            else:
                movieitems_dist[item[1]] = item[0]
            run_time = time.time() - st
            if run_time >= 5.0: break
        run_time = time.time() - st
        if run_time >= 5.0: break
    #3. 基于推荐度，进行排序
    Seriesitems = pd.Series(movieitems_dist).order(ascending=0)
    #4. 输出
    recommned_moiveID_df = pd.DataFrame(Seriesitems.head(wantedNum).keys(), columns=['item_idx'] )
    recomm_merger = pd.merge(pd_data, recommned_moiveID_df, on='item_idx')
    recommend_ans = recomm_merger.loc[:, ['item_idx','title'] ].title.drop_duplicates()
    return list( recommend_ans )

#查看用户看过哪些新闻
def get_Have_Watched_News( useridx ):
	url = os.getcwd()
	user_item_score = pd.read_csv(url+"/recommed_sys/recom/apps/data/user_item_score.csv")
	titles = user_item_score[ user_item_score.user_idx == useridx ].title.drop_duplicates()
	#print list( titles )
	return list( titles )
