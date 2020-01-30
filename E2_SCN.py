# Node engine: SCN

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time

from Base_NDN import BaseNDN, get_FIBs, print_FIBs, initial_Global_FIB, update_Global_FIB, delete_Global_FIB
from Global_init_var import *


class SCN(BaseNDN):
	
	local_pro_record = tuple()
	service_set = tuple()
	
	Computation_Task_record = 0
	
	
	def __init__(self,local_label,node_type,v_comp,init_comp_CAP=0,init_cache_CAP=1000):
			BaseNDN.__init__(self,local_label,node_type,init_cache_CAP=1000)
			self.v_comp = v_comp
			self.comp_CAP = init_comp_CAP

	
	def search_CS_i(self,cur_pac_name):
		
		print('ICECN_class \'search_CS_i\' print:')
		if cur_pac_name[0] == 'F_F':
			if cur_pac_name in self.CS:
				tem_index = self.CS.index(cur_pac_name) + 1
				return (cur_pac_name,self.CS[tem_index],cur_pac_name)
			else:
				return False
		else:
			
			temp_l_1 = cur_pac_name
			
			if self.label == 'P1':
				print('P1 CS:')
				self.print__content_store()
				print(temp_l_1)
			
			if temp_l_1 in self.CS:
				print('yes!!')
				tem_index = self.CS.index(temp_l_1) + 1
				print(self.CS[tem_index])
				return (cur_pac_name,self.CS[tem_index],temp_l_1)
			else:
				
				if len(cur_pac_name) > 3:
					temp_l_1 = cur_pac_name[2:]
					if temp_l_1 in self.CS:
						print('yes!!')
						tem_index = self.CS.index(temp_l_1) + 1
						print(self.CS[tem_index])
						return (cur_pac_name,self.CS[tem_index],temp_l_1)
				
				return False

	
	def PIT_pro_i(self,cur_pac):
		print('ICECN_class \'PIT_pro_i\' print:')
		l_PIT = list(self.PIT)
		
		Flag_exec = True
		
		if cur_pac[0] in l_PIT:
			tem_index = l_PIT.index(cur_pac[0])+1
			l_PIT_i = list(l_PIT[tem_index])
			l_PIT_i.insert(0,cur_pac[2])
			l_PIT[tem_index] = tuple(l_PIT_i)
			self.transfer = (((),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
			
			Flag_exec = False
			
		else:
			l_PIT.append(cur_pac[0])
			l_PIT.append((cur_pac[2],))
		self.PIT = tuple(l_PIT)
		
		temp_judge_name = ()
		
		if (cur_pac[0][0] == 'P_F') and (len(cur_pac[0]) > 5):
			temp_judge_name = cur_pac[0][2:]
		else:
			temp_judge_name = cur_pac[0]
		
		print('temp_judge_name:')
		print(temp_judge_name)
		print(self.service_set)
		
		if (temp_judge_name[0] == 'F_F') and (temp_judge_name[1] in self.service_set):
			
			l_PIT = list(self.PIT)
			tem_index = l_PIT.index(cur_pac[0]) + 1
			l_PIT_i = list(l_PIT[tem_index])
			l_PIT_i.remove(cur_pac[2])
			l_PIT_i.append(cur_pac[2])
			l_PIT_i.append('local_process')
			l_PIT[tem_index] = tuple(l_PIT_i)
			self.PIT = tuple(l_PIT)
			
			if Flag_exec:
				self.local_process_i(cur_pac) # local processing
			
		elif Flag_exec:
			temp_name = cur_pac[0]
			while True:
				
				if temp_name[0] == 'F_F':
					tem_succ_node = self.shortest_path_FIB(temp_name[1])
					break
				else: # 'P_F'
					tem_succ_node = self.shortest_path_FIB(temp_name)
					if tem_succ_node:
						break
					else:
						if len(temp_name) > 3:
							temp_name = temp_name[2:]
							continue
						else:
							break
			
			print('temp_name:::')
			print(temp_name)
			
			if tem_succ_node:
				self.transfer = (((tem_succ_node,),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
			else:
				self.transfer = (((),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
		
		
		print('%s PIT:' % self.label)
		print(self.PIT)
		print('transfer:')
		print(self.transfer)
		print('ICECN_class \'PIT_pro_i\' end:')
		
		
	def search_FIB(self,cur_pac_name):
		if cur_pac_name in self.FIB:
			return True
		else:
			return False
	
	
	def local_process_i(self,cur_pac):
		print('ICECN_class \'local_process_i\' print:')
		
		if cur_pac[0][2] != ('Default',):
			tem_local_pro = (cur_pac[0],cur_pac[4],cur_pac[5],cur_pac[6],0)
			print('tem_local_pro!!:')
			print(tem_local_pro)
			print(cur_pac)
			
			if cur_pac[0][0] == 'F_F':
				tem_para_i_name = ('P_F',) + cur_pac[0][1:]
			else:
				tem_para_i_name = cur_pac[0][2:]
			
			tem_local_pro += (tem_para_i_name,0,0,0,0,0)
			tem_req_1 = (tem_para_i_name,'i',self.label,0,0,0,0)
			
			tem_para_requests = (tem_req_1,)
			
			print('tem_para_requests:')
			print(tem_para_requests)
			print(tem_local_pro)
			
			tem_index_1 = len(self.requests)
			self.requests += tem_para_requests
			
			self.packet_arrive_set(tem_index_1,len(self.requests)) # inherited from parent class BaseNDN
			
			self.local_pro_record += (tem_local_pro,)
			print('%s self.local_pro_record!!:' % self.label)
			print(self.local_pro_record)
		
		else:
			pre_size = size_para
			temp_size = pre_size/1000
			delay_account = cur_pac[5] + 10*pre_size/self.v_comp
			self.Computation_Task_record += 10*pre_size
			back_pac = (cur_pac[0],'d',0,temp_size,cur_pac[4],delay_account,cur_pac[6],'local_process')

			l_node_queue = list(self.node_queue)
			l_node_queue.insert(len(l_node_queue), back_pac)
			self.node_queue = tuple(l_node_queue)
			
			
		print('ICECN_class \'local_process_i\' end:')
	
	
	def local_process_d(self,trans_pac,G,Global_FIB):
		print('ICECN_class \'local_process_d\' print:')
		print('self.local_pro_record:')
		print(self.local_pro_record)
		
		l_local_pro_record = list(self.local_pro_record)
		for i in range(len(l_local_pro_record)):
			l_record_i = l_local_pro_record[i]
			
			if trans_pac[0] in l_record_i:
				print('l_record_i:')
				print(l_record_i)
				
				total_hop_account = trans_pac[2]
				size_of_pac = trans_pac[3] + l_record_i[1]
				accu_size_of_content_trans = trans_pac[4] + l_record_i[2]
				delay_account = trans_pac[5] + l_record_i[3]
				energy_account =trans_pac[6] + l_record_i[4]
				
				print('Computation_Task_record:')
				print(self.label)
				print(self.Computation_Task_record)
				self.Computation_Task_record += 10 * size_of_pac
				print(self.Computation_Task_record)

				
				if trans_pac[0][0] == 'P_F': # 'P_F',local processing
					
					delay_account += 10 * size_of_pac/self.v_comp
					
					comp_task_dur = 10 * size_of_pac/self.v_comp
					P_static = 30
					energy_account += P_static * comp_task_dur

					size_of_pac = size_of_pac/1000


				back_pac = (l_record_i[0],'d',total_hop_account,size_of_pac,accu_size_of_content_trans,delay_account,energy_account,'local_process')
				
				print(back_pac)

				l_node_queue = list(self.node_queue)
				l_node_queue.insert(len(l_node_queue), back_pac)
				self.node_queue = tuple(l_node_queue)
				print('processed packet back:')
				print(self.node_queue)
				
				l_record_i += ('complete',)
				
			l_local_pro_record[i] = l_record_i
		
		self.local_pro_record = tuple(l_local_pro_record)
		print('self.local_pro_record:')
		print(self.local_pro_record)
		print(self.node_queue)
		print('ICECN_class \'local_process_d\' end:')
		
	
	def pro_interest(self,cur_pac,G,Global_FIB):
		print('ICECN_class \'pro_interest\' print:')
		tem_search_CS_i = self.search_CS_i(cur_pac[0])
		if (self.node_type != 'h') and (tem_search_CS_i != False):
			self.transfer = (((cur_pac[2],),tem_search_CS_i[0],'d',0,tem_search_CS_i[1],0,cur_pac[5],cur_pac[6]),)

			l_CS = list(self.CS)
			del l_CS[l_CS.index(tem_search_CS_i[2])+1]
			del l_CS[l_CS.index(tem_search_CS_i[2])]
			l_CS.insert(0,tem_search_CS_i[1])
			l_CS.insert(0,tem_search_CS_i[2])
			self.CS = tuple(l_CS)
			
		else:
			self.PIT_pro_i(cur_pac)
		print('ICECN_class \'pro_interest\' end:')		
	
	
	def PIT_pro_d(self,cur_pac):
		print('%s ICECN_class \'PIT_pro_d\' print:' % self.label)
		print('self.PIT:')
		print(self.PIT)
		
		back_nodes_1 = tuple()
		if cur_pac[0] in self.PIT:
			tem_index = self.PIT.index(cur_pac[0]) + 1
			back_nodes_1 = self.PIT[tem_index]
			print(back_nodes_1)
			
			l_PIT = list(self.PIT)
			if 'local_process' in back_nodes_1:
				l_back_nodes_1 = list(back_nodes_1)
				print(cur_pac)
				if cur_pac[-1] == 'local_process':
					l_back_nodes_1.remove('local_process')
					
					while 'local_process' in l_back_nodes_1:
						l_back_nodes_1.remove('local_process')
					
					l_PIT.pop(tem_index-1)
					l_PIT.pop(tem_index-1)
					
				else:
					
					tem_l_PIT_node_set = list(l_PIT[tem_index])
					
					tem_l_PIT_index = ()
					print('tem_l_PIT_node_set:')
					print(tem_l_PIT_node_set)
					while 'local_process' in tem_l_PIT_node_set:
						tem_l_PIT_index += (tem_l_PIT_node_set[tem_l_PIT_node_set.index('local_process')-1],'local_process')
						print('tem_l_PIT_index:')
						print(tem_l_PIT_index)
						
						tem_l_PIT_node_set.pop(tem_l_PIT_node_set.index('local_process'))
						print('tem_l_PIT_node_set:')
						print(tem_l_PIT_node_set)
					l_back_nodes_1 = tem_l_PIT_node_set
					
					
					l_PIT[tem_index] = tem_l_PIT_index
					
				back_nodes_1 = tuple(l_back_nodes_1)
				
			else:
				l_PIT.pop(tem_index-1)
				l_PIT.pop(tem_index-1)
			
			self.PIT = tuple(l_PIT)
		
		print('back_nodes_1:')
		print(back_nodes_1)
		
		
		if back_nodes_1:
			t_tem_transfer_1 = (back_nodes_1,) + cur_pac
			self.transfer = (t_tem_transfer_1,)
		else:
			t_tem_transfer = ((),) + cur_pac
			self.transfer = (t_tem_transfer,)		
		
		print('%s back_nodes_1:' % self.label)
		print(back_nodes_1)
		print('%s transfer_d33:' % self.label)
		print(self.transfer)
		print('ICECN_class \'PIT_pro_d\' end:')
				
	
	def decide_cache(self,wait_cache_content,content_size,G,Global_FIB):
		print('ICECN_class \'decide_cache\' print:')
		
		c_wait_cache_content = wait_cache_content
		
		if (self.node_type == 'r') and (c_wait_cache_content in self.CS) == False:

			self.cache_CS(c_wait_cache_content,content_size,G,Global_FIB) # cache_CS is inherited from BaseNDN class
			
			P_ca = 2.5e-9 # P_ca = 2.5e-9 J/(bit*s)
			S_ca = 1.28e10 # S_ca = 1.28e10 bit/s
			
			energy_cache = content_size * content_size * P_ca / S_ca
			
			return energy_cache
		else:
			
			return 0
			
		print('ICECN_class \'decide_cache\' end:')
	
	
	def local_onpath_process_d(self,cur_pac):
		print('ICECN_class \'local_onpath_process_d\' print:')
		
		print('Computation_Task_record:')
		print(self.label)
		print(self.Computation_Task_record)
		self.Computation_Task_record += 10*cur_pac[3]
		print(self.Computation_Task_record)
		
		
		proc_pac_name = ('F_F',) + cur_pac[0][1:]
		
		Inst = 10*cur_pac[3] # Instructions
		proc_pac_delay = cur_pac[5] + Inst/self.v_comp
		proc_pac_size = cur_pac[3]/1000
		
		pro_pac_energy = cur_pac[6]
		
		proc_pac = (proc_pac_name,cur_pac[1],cur_pac[2],proc_pac_size,cur_pac[4],proc_pac_delay,pro_pac_energy)
		
		l_node_queue = list(self.node_queue)
		l_node_queue.insert(len(l_node_queue), proc_pac)
		self.node_queue = tuple(l_node_queue)
		print(self.node_queue)
		
		print('ICECN_class \'local_onpath_process_d\' end:')
	
	
	def pro_data(self,cur_pac,G,Global_FIB):
		print('%s ICECN_class \'pro_data\' print:' % self.label)
		
		self.PIT_pro_d(cur_pac)
		if len(self.transfer[0][0]) != 0:
			energy_cache = self.decide_cache(self.transfer[0][1],self.transfer[0][4],G,Global_FIB)
			trans_pac = self.transfer[0][:-1] + (self.transfer[0][7] + energy_cache,)
			self.transfer = (trans_pac,)
		
		print('ICECN_class \'pro_data\' end:')
			
	
	def issue_init_interests(self,t_operation_parameter_requests):
		for ti_re in t_operation_parameter_requests:
			self.requests += ((ti_re,'i',self.label,0,0,0),)
	
		
	#def pro_pac(self): # inherited from class BaseNDN
			
	#def packet_arrive_set(self,range_start,range_stop): # inherited from class BaseNDN
	
	#def get_respond_delay(self,responded_content): # inherited from class BaseNDN
		
	#def print__content_store(self): # inherited from class BaseNDN

	#def cache_CS(self,wait_cache_content): # inherited from class BaseNDN
	
# -----------------------------------------------generate FIB start-----------------------------------------------

#def get_FIBs(): # inherited from class BaseNDN

#def print_FIBs(): # inherited from class BaseNDN

def initial_Global_FIB(G,Global_FIB):
	
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'p':
			if len(ri[1]['model'].CS) != 0 :
				for content_i in ri[1]['model'].CS:
					if type(content_i) == tuple:
						#print(content_i)
						update_Global_FIB(ri[0], content_i,G,Global_FIB)
					else:
						continue
		elif ri[1]['model'].node_type == 'r':
			if len(ri[1]['model'].service_set) != 0 :
				for s_i in ri[1]['model'].service_set:
					update_Global_FIB(ri[0], s_i,G,Global_FIB)
	get_FIBs(G,Global_FIB)


#def update_Global_FIB(tar_node,new_cache_content):	# inherited from class BaseNDN

#def delete_Global_FIB(tar_node,poped_content):	# inherited from class BaseNDN


# -----------------------------------------------generate FIB end...-----------------------------------------------

