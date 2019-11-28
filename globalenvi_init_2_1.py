# global environment initial..

import math
import random
import sys

from scipy.special import comb, perm
from topo_3 import *
from global_init_var import *


alpha = 0.8

t_p = tuple(range(Num_para))
t_p_k_alpha = ()
for i in range(Num_para):
	t_p_k_alpha += (pow(i+1,-alpha),)
t_p_k_alpha_sum = sum(t_p_k_alpha)
t_p_f = ()
for i in range(Num_para):
	t_p_f += (t_p_k_alpha[i]/t_p_k_alpha_sum,)
t_p_f_accu = ()
for i in range(Num_para):
	t_p_f_accu += (sum(t_p_f[:i+1]),)

#print("t_p_f_accu:")
#print(t_p_f_accu)

t_s = tuple(range(Num_Global_service))
t_s_k_alpha = ()
for i in range(Num_Global_service):
	t_s_k_alpha += (pow(i+1,-alpha),)
t_s_k_alpha_sum = sum(t_s_k_alpha)
t_s_f = ()
for i in range(Num_Global_service):
	t_s_f += (t_s_k_alpha[i]/t_s_k_alpha_sum,)
t_s_f_accu = ()
for i in range(Num_Global_service):
	t_s_f_accu += (sum(t_s_f[:i+1]),)

#print("t_s_f_accu:")
#print(t_s_f_accu)

# produce Global_service_set
def init_produce_Global_service_set(Num_Global_service):
	Global_service_set = ()
	for i in range(Num_Global_service):
		temp_s = 's' + str(i)
		#temp_s = 's' + str(i)
		Global_service_set += (temp_s,)
	return Global_service_set

'''
# implement service for each router in G from Global_service_set
def init_implement_service(node_set_r,Global_service_set):
	f = open('init_implement_service.txt','w')
	l_r_s_record = list(range(len(node_set_r)))

	for i in range(len(node_set_r)):
		l_r_s_record[i] = 0
	
	Num_K_s = 8 * len(Global_service_set)
	
	for si in Global_service_set:
		l_node_set_r = list(node_set_r)
		
		num_s_r = round(Num_K_s * t_s_f[int(si[1:])])
		if num_s_r == 0:
			num_s_r = 1
		elif num_s_r > len(node_set_r):
			num_s_r = len(node_set_r)
		
		for j in range(num_s_r): # 流行服务部署在更多的节点上
		#for j in range(random.randint(2,4)):
			while True:
				temp_r = random.choice(l_node_set_r)
				if l_r_s_record[int(temp_r[1:])-1] < comp_CAP: # router的comp_CAP有限制，也就是不能将所有的服务都放到一个节点上
					l_r_s_record[int(temp_r[1:])-1] += 1
					temp_write_s = str(temp_r) + ',' + str(si)
					f.write(temp_write_s)
					f.write('\n')
					l_node_set_r.remove(temp_r)
					break
				else:
					continue
	f.close()
'''
	
'''
def init_produce_ps(Num_para,each_num): # 在P节点上顺序安排参数p
	# Pi.CS = ('pj',size_j,'pk',size_k,...)
	f = open('init_produce_ps.txt','w')
	for i in range(Num_para):
		temp_p = 'P' + str(int(i/each_num)+1)
		temp_name = 'p' + str(i)
		temp_size = random.uniform(10e6,50e6)
		temp_write_p = temp_p + ',' + str(temp_name) + ',' + str(temp_size)
		f.write(temp_write_p)
		f.write('\n')
	f.close()
'''

'''
def init_produce_ps(Num_para,node_set_p): # 在P节点上随机安排参数p
	# Pi.CS = ('pj',size_j,'pk',size_k,...)
	f = open('init_produce_ps.txt','w')
	
	l_p_cache_record = list(range(len(node_set_p)))
	
	for i in range(len(node_set_p)):
		l_p_cache_record[i] = 0
	
	for i in range(Num_para):
		while True:
			l_temp_p = random.sample(node_set_p,1)
			temp_p = l_temp_p[0]
			if l_p_cache_record[int(temp_p[1:])-1] < cache_CAP: # P的cache_CAP有限制，也就是不能将所有的p都放到一个P节点上
				temp_name = 'p' + str(i)
				temp_size = random.uniform(5e5,5e5)
				temp_write_p = temp_p + ',' + str(temp_name) + ',' + str(temp_size)
				f.write(temp_write_p)
				f.write('\n')
				break
			else:
				continue
	f.close()
'''

def init_produce_ps(Num_para,node_set_p): # 在P节点上顺序安排参数p
	# Pi.CS = ('pj',size_j,'pk',size_k,...)
	f = open('init_produce_ps.txt','w')
	each_num = Num_para/len(node_set_p)
	for i in range(Num_para): # i: 0~5999
		temp_p = 'P' + str(int(i/each_num)+1)
		temp_name = 'p' + str(i)
		temp_size = random.uniform(size_para,size_para)
		temp_write_p = temp_p + ',' + str(temp_name) + ',' + str(temp_size)
		f.write(temp_write_p)
		f.write('\n')
	f.close()



if __name__ == '__main__':

	# __main__
	
	#set_CAP()

	Global_service_set = init_produce_Global_service_set(Num_Global_service)

	# implement services for each router
	#init_implement_service(node_set_r,Global_service_set)
	# produce parameter contents for each Pi
	#init_produce_ps(Num_para,each_num)
	init_produce_ps(Num_para,node_set_p)
	# produce requests for each host
	
	'''
	for ri in G.nodes(data=True):
		print(ri[1]['model'].comp_CAP)
		print(ri[1]['model'].cache_CAP)
	
	print(Num_para)
	print(len(node_set_p))
	'''
	
