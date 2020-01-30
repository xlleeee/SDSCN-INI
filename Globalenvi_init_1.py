# global environment initial..

import math
import random
import sys

from scipy.special import comb, perm
from Topo import *
from Global_init_var import *


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


# produce Global_service_set
def init_produce_Global_service_set(Num_Global_service):
	Global_service_set = ()
	for i in range(Num_Global_service):
		temp_s = 's' + str(i)
		Global_service_set += (temp_s,)
	return Global_service_set



def init_produce_ps(Num_para,node_set_p):
	f = open('init_produce_ps.txt','w')
	each_num = Num_para/len(node_set_p)
	for i in range(Num_para):
		temp_p = 'P' + str(int(i/each_num)+1)
		temp_name = 'p' + str(i)
		temp_size = random.uniform(size_para,size_para)
		temp_write_p = temp_p + ',' + str(temp_name) + ',' + str(temp_size)
		f.write(temp_write_p)
		f.write('\n')
	f.close()



if __name__ == '__main__':

	# __main__
	
	Global_service_set = init_produce_Global_service_set(Num_Global_service)
	
	# produce parameter files for each P
	init_produce_ps(Num_para,node_set_p)
	
	
	