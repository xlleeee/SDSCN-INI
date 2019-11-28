# global environment initial..

import math
import random
import sys

from scipy.special import comb, perm
from topo_3 import *
from global_init_var import *
from globalenvi_init_2_1 import *

#req_p_num = int(sys.argv[1])
req_p_num = 1

#req_s_num = 0

req_s_num = int(sys.argv[1])

s_dup = int(sys.argv[2])

'''
def init_produce_requests(req_num_total,Num_para,node_set_h,req_p_num): # 每个host的requests数目随机
	f = open('init_produce_requests.txt','w')
	
	rand_num_set = ()
	chose_f_accu = ()
	chose_p = ()
	
	for i in range(req_num_total):
		
		if req_p_num == -1: # <P_F,None,pi>,只请求内容
			temp_name = ('P_F','None')
			p_record = ()
			# 按照Zipf分布选一个p
			while True:
				rand_num = random.random()
				for k in range(Num_para):
					if t_p_f_accu[k] >= rand_num:
						break
					else:
						continue
				temp_p = 'p' + str(t_p[k])
				if (temp_p in p_record) == False:
					rand_num_set += (rand_num,)
					chose_f_accu += (t_p_f_accu[k],)
					chose_p += (t_p[k],)
					break	
			
			p_record += (temp_p,)
			
		elif req_p_num ==0: # <F_F,fi,Default>,只请求计算
			rand_num_s = random.random()
			for h in range(len(Global_service_set)):
				if t_s_f_accu[h] >= rand_num_s:
					break
				else:
					continue
			chose_s = Global_service_set[h] # 按照Zipf分布选一个s
			temp_name = ('F_F',chose_s)
			p_record = ('Default',)
			
		else: # <F_F,fi,(p1,p2,..)>,请求计算和内容
			rand_num_s = random.random()
			for h in range(len(Global_service_set)):
				if t_s_f_accu[h] >= rand_num_s:
					break
				else:
					continue
			chose_s = Global_service_set[h] # 按照Zipf分布选一个s
			temp_name = ('F_F',chose_s)
			
			#temp_name = ('F_F',random.choice(Global_service_set))
			
			p_record = ()
			#for j in range(random.randint(4,4)):
			for j in range(req_p_num):

				# 按照Zipf分布选一个p
				while True:
					rand_num = random.random()
					for k in range(Num_para):
						if t_p_f_accu[k] >= rand_num:
							break
						else:
							continue
					temp_p = 'p' + str(t_p[k])
					if (temp_p in p_record) == False:
						rand_num_set += (rand_num,)
						chose_f_accu += (t_p_f_accu[k],)
						chose_p += (t_p[k],)
						break	
				
				p_record += (temp_p,)
		
		temp_name += (p_record,)
		temp_h = random.choice(node_set_h) # 随机选一个host，把这个request给这个host	
		temp_write_req = str(temp_h) + ',' + str(temp_name[0]) + ',' + str(temp_name[1])
		for pi in temp_name[2]:
			temp_write_req = temp_write_req + ',' + str(pi)
		f.write(temp_write_req)
		f.write('\n')
		
	f.close()
'''



def init_produce_requests(req_num_total,Num_para,Num_Global_service,node_set_h,req_p_num): # 每个host的requests数目随机
	f = open('init_produce_requests.txt','w')
	
	rand_num_set = ()
	chose_f_accu = ()
	chose_p = ()
	
	
	s_record = ()
	temp_name = ()
	temp_name_s = ()
	for j in range(req_s_num):
		while True:
			rand_num_s = random.random()
			for h in range(len(Global_service_set)):
				if t_s_f_accu[h] >= rand_num_s:
					break
				else:
					continue
			chose_s = Global_service_set[h] # 按照Zipf分布选一个s
			if (chose_s in s_record) == False:
				s_record += (chose_s,)
				temp_name_s += ('F_F',chose_s)
				break
	print(temp_name_s)
	#temp_name = ('F_F',chose_s)
	
	#temp_name = ('F_F',random.choice(Global_service_set))

	for i in range(req_num_total):
		
		
		p_record = ()
		#for j in range(random.randint(4,4)):
		for j in range(req_p_num):

			# 按照Zipf分布选一个p
			while True:
				rand_num = random.random()
				for k in range(Num_para):
					if t_p_f_accu[k] >= rand_num:
						break
					else:
						continue
				temp_p = 'p' + str(t_p[k])
				if (temp_p in p_record) == False:
					rand_num_set += (rand_num,)
					chose_f_accu += (t_p_f_accu[k],)
					chose_p += (t_p[k],)
					break	
			
			#p_record += (temp_p,)
		
		#temp_name += (p_record,)
		temp_name = temp_name_s +  ('P_F','ANY',temp_p)
		temp_h = random.choice(node_set_h) # 随机选一个host，把这个request给这个host	
		'''
		temp_write_req = str(temp_h) + ',' + str(temp_name[0]) + ',' + str(temp_name[1])
		for pi in temp_name[2]:
			temp_write_req = temp_write_req + ',' + str(pi)
		'''
		temp_write_req = str(temp_h)
		for pi in temp_name:
			temp_write_req = temp_write_req + ',' + str(pi)
		
		f.write(temp_write_req)
		f.write('\n')
		
	f.close()


# implement service for each router in G from Global_service_set
def init_implement_service(node_set_r,Global_service_set,s_dup):
	f = open('init_implement_service.txt','w')
	l_r_s_record = list(range(len(node_set_r)))

	for i in range(len(node_set_r)):
		l_r_s_record[i] = 0
	
	#Num_K_s = 8 * len(Global_service_set)
	
	num_s_r = s_dup
	
	for si in Global_service_set:
		
		l_node_set_r = list(node_set_r)
		'''
		num_s_r = round(Num_K_s * t_s_f[int(si[1:])])
		if num_s_r == 0:
			num_s_r = 1
		elif num_s_r > len(node_set_r):
			num_s_r = len(node_set_r)
		'''
		
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
	


if __name__ == '__main__':

	# __main__
	Global_service_set = init_produce_Global_service_set(Num_Global_service)
	init_produce_requests(req_num_total,Num_para,Num_Global_service,node_set_h,req_p_num)
	
	# implement services for each router
	init_implement_service(node_set_r,Global_service_set,s_dup)


	print('req_p_num:')
	print(req_p_num)