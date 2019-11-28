#ICECN：在路由节点上进行网内计算和缓存，能够进行沿路缓存和计算。

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
import csv
import sys

#from p1_NDN_5 import NDN, get_FIBs, print_FIBs, initial_Global_FIB, update_Global_FIB, delete_Global_FIB
#from p1_NDN_5_unlock import NDN, get_FIBs, print_FIBs, initial_Global_FIB, update_Global_FIB, delete_Global_FIB
from E2_SDSCN import *
from E2_topo_3 import *

#req_p_num = int(sys.argv[1])
#req_p_num = 1

req_s_num = int(sys.argv[1])

s_dup = int(sys.argv[2])

def implement_service():
	f = open('init_implement_service.txt','r')
	tem_line = f.readline()
	while tem_line:
		tem_node_r = tem_line[:tem_line.index(',')]
		tem_s = tem_line[tem_line.index(',')+1:-1]
		for ri in G.nodes(data=True):
			if ri[1]['model'].label == tem_node_r:
				ri[1]['model'].service_set += (tem_s,)
		tem_line = f.readline()
	f.close()

def produce_ps():
	f = open('init_produce_ps.txt','r')
	tem_line = f.readline()
	while tem_line:
		tem_node_p = tem_line[:tem_line.index(',')]
		tem_c = tem_line[tem_line.index(',')+1:-1]
		for ri in G.nodes(data=True):
			if ri[1]['model'].label == tem_node_p:
				tem_c_name = tem_c[:tem_c.index(',')]
				
				tem_c_name_full = ('P_F','ANY',tem_c_name)
				
				tem_c_size = float(tem_c[tem_c.index(',')+1:])
				ri[1]['model'].CS += (tem_c_name_full,tem_c_size)
		tem_line = f.readline()
	f.close()
	'''
	for ri in G.nodes(data=True):
		print('%s CS:' % ri[1]['model'].label)
		ri[1]['model'].print__content_store()
	'''
	
	
# __main__

if __name__ == '__main__':
		
	#---------------initial implement------------------
	
	# implement services for each router
	implement_service()
	# produce parameter contents for each Pi
	produce_ps()
	
	'''
	print('service_set:')
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'r':
			print(ri[1]['model'].label)
			print(ri[1]['model'].service_set)
	
	print('parameters for each Pi:')
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'p':
			print(ri[1]['model'].label)
			print(ri[1]['model'].CS)
	
	print('requests for each host:')
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'h':
			print(ri[1]['model'].label)
			print(ri[1]['model'].requests)
	'''
	# ----------------FIB initial --------------------
	
	Global_FIB = {}
	# Global_FIB : {'R1': ['prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...], 'R2': [],...}
	# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)issue_init_interests(('/exec/dec/s1|/p1|/p2|/p3/',))
	
	# 初始化每个节点的FIB
	initial_Global_FIB(G,Global_FIB)
	
	'''
	print('Global_FIB:')
	print('-----------')
	for di in Global_FIB:
		print('%s:' % di)
		print(Global_FIB[di])
	print('---------------------')
	print('FIB for each node:')
	for ri in G.nodes(data=True):
		print('%s:' % ri[1]['model'].label)
		print(ri[1]['model'].FIB)
	print('----------FIB initial end-----------')
	'''
	
	# ----------------Exp1 running--------------------
	
	
	for rj in G.nodes(data=True):
		print(rj[1]['model'].node_queue)
		print(rj[1]['model'].requests)
	
	
	f = open('init_produce_requests.txt','r')
	tem_line = f.readline()
	time_start = time.time()
	pac_arri_time_start = time.time()
	file_closed_flag = False
	while True:
		print('issue packet start...')
		print(file_closed_flag)
		if (time.time() - pac_arri_time_start > 0.01) and (file_closed_flag == False):
			print(tem_line)
			if tem_line:
				tem_node_hi = tem_line[:tem_line.index(',')]
				tem_line = tem_line[tem_line.index(',')+1:-1]
				
				'''
				tem_type = tem_line[:tem_line.index(',')]
				tem_line = tem_line[tem_line.index(',')+1:]
				tem_s = tem_line[:tem_line.index(',')]
				tem_line = tem_line[tem_line.index(',')+1:]
				tem_p = ()
				while ',' in tem_line:
					tem_p += (tem_line[:tem_line.index(',')],)
					tem_line = tem_line[tem_line.index(',')+1:]
				tem_p += (tem_line,)
				'''
				tem_req_name = ()
				while ',' in tem_line:
					tem_req_name += (tem_line[:tem_line.index(',')],)
					tem_line = tem_line[tem_line.index(',')+1:]
				tem_req_name += (tem_line,)
				
				#tem_req_name = (tem_type,tem_s,tem_p)
				tem_req = ((tem_req_name,'i',tem_node_hi,0,0,0,0),)
				print('tem_req:')
				print(tem_req)
				for ri in G.nodes(data=True):
					if ri[1]['model'].label == tem_node_hi:
						tem_index_1 = len(ri[1]['model'].requests)
						ri[1]['model'].requests += tem_req
						print(ri[1]['model'].requests)
						ri[1]['model'].packet_arrive_set(tem_index_1,tem_index_1 + 1)
						
				tem_line = f.readline()
				pac_arri_time_start = time.time()
			else:
				f.close()
				file_closed_flag = True
			
		print('issue packet end...')
		print('new round process start...')
		count_1 = 0
		for ri in G.nodes(data=True):
			if len(ri[1]['model'].node_queue) == 0:
				count_1 += 1
			else:
				count_1 = 0
			ri[1]['model'].pro_pac(G,Global_FIB)
		if count_1 != len(G.nodes):
			time_start = time.time()
		if time.time() - time_start > 2:
			print('exp end..')
			break
		print('this round process end...')
	


	total_content_respond_num = 0
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'h':
			print('content_respond:')
			print(ri[1]['model'].content_respond)
			total_content_respond_num += (len(ri[1]['model'].content_respond)-1)
	print('the total content respond num is: % d' % total_content_respond_num)
	
	
	print('----------------------------')
	
	f = open('E1_results.txt','w')
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'h':
			for ci in ri[1]['model'].content_respond[1:]:
				temp_write_c = str(ci[0]) + ',' + str(ci[3]) + ',' + str(ci[5]) + ',' + str(ci[6]) + ',' + str(ci[7])
				f.write(temp_write_c)
				f.write('\n')
	f.close()
	
	style = 'SDSCN, FC=' + str(req_s_num)
	solution = 'SDSCN'
	FC = 'FC=' + str(req_s_num)

	with open('Results_delay_energy.csv','a') as f:
		for ri in G.nodes(data=True):
			if ri[1]['model'].node_type == 'h':
				for ci in ri[1]['model'].content_respond[1:]:
					row = [str(s_dup),str(ci[6]*1000),str(ci[7]),style,solution,FC]
					write = csv.writer(f)
					write.writerow(row)
		
	
	'''
	for ri in G.nodes(data=True):
		print(ri[1]['model'].comp_CAP)
		print(ri[1]['model'].cache_CAP)
	'''
	
	if req_s_num > 0:
		temp_s_num = req_s_num
		accu_ct = 10 * size_para * temp_s_num * req_num_total
		print(size_para)
		print(req_num_total)
		print('accu_ct: %d' % accu_ct)
		with open('Results_computation_task.csv','a') as f:
			for ri in G.nodes(data=True):
				if ri[1]['model'].node_type == 'r' and ri[1]['model'].label[0] == 'R':
					temp_cp = ri[1]['model'].Computation_Task_record
					if temp_cp > 0:
						temp_cp_percent = temp_cp/accu_ct * 100
						row = [str(s_dup),str(temp_cp_percent),style,solution,FC]
						write = csv.writer(f)
						write.writerow(row)
		
		
		CPt = tuple()
		
		for ri in G.nodes(data=True):
			if ri[1]['model'].node_type == 'r':
				print(ri[1]['model'].label)
				print(ri[1]['model'].Computation_Task_record)
				CPt += (ri[1]['model'].Computation_Task_record,)
		
		print('CPt:')
		print(CPt)

		sum_CPt = sum(CPt)
		print('sum_CPt:')
		print(sum_CPt)

		CPt_percent = tuple()

		for i in range(len(CPt)):
			CPt_percent += ((CPt[i]/sum_CPt),)

		print('CPt_percent:')
		print(CPt_percent)

		#求均值
		CPt_percent_mean = np.mean(CPt_percent)

		#求方差
		CPt_percent_var = np.var(CPt_percent)

		#求标准差
		CPt_percent_std = np.std(CPt_percent,ddof=1)

		print("平均值为：%.9f" % CPt_percent_mean)
		print("方差为：%.9f" % CPt_percent_var)
		print("样本标准差为:%.9f" % CPt_percent_std)

		print("样本方差为:%.9f" % pow(CPt_percent_std, 2))
		
		print('最大值为：%.9f' % max(CPt_percent))
		
