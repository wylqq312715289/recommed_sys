# -*- coding:utf-8 -*-
import numpy as np
import csv
from numpy import linalg as la  #用到别名

def read_data(url = "data/user_click_data_beta.txt"):
	lines = [ line.strip().split() for line in open(url, 'rb').readlines() ]
	data = []
	for line in lines:
		#获取第一列user_id和第二列item_id
		user_id = line[0]
		item_id = line[1]
		read_time =  line[2] 
		item_title = line[3]
		content = line[4]
		p_time = line[5]
		data.append( [user_id, item_id, read_time, item_title, content, p_time] )
	return data

def read_data_csv(url):
	csvfile = open(url,"rb")
	reader = csv.reader(csvfile)
	data = []
	for row in reader: data.append( row[0:-1] )
	for i in range(len(data)):
		for j in range(len(data[i])):
			data[i][j] = float(data[i][j])
	return data

def write_data_txt(data, url):
	file = open(url,"wb")
	for line in data: file.write("\t".join(line)) 
	file.close()


def write_data_csv(data, url):
	with open(url,'wb') as myFile:
		myWriter = csv.writer(myFile)
		for i in data:  
			myWriter.writerow(i)

if __name__ == '__main__':
	print read_data("data/user_click_data_beta.txt")