#ICECN

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time
#from p1_NDN_5 import NDN, get_FIBs, print_FIBs, initial_Global_FIB, update_Global_FIB, delete_Global_FIB
from E1_2_NDN import NDN, get_FIBs, print_FIBs, initial_Global_FIB, update_Global_FIB, delete_Global_FIB
from global_init_var import *

'''
class ICECN:
	__init__(self,local_label,node_type,service_set,init_com_CAP,init_cache_CAP=1000)
	implement_services(self)
	search_CS(self,cur_pac)
	cache_CS(self,wait_cache_content)
	PIT_pro(self,cur_pac)
	search_FIB(self,cur_pac)
	decide_local_process_i(self,cur_pac)
	local_process_d(self,cur_pac)
'''
class ICECN(NDN):
	
	# NDN attributes:
	# node_queue : (('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),('pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
	# CS : ('content_name1',size_of_content1,'content_name2',size_of_content2,...)
		
	## PIT : ('pac_name1',('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	# PIT : ('pac_name1',('A1','A2',...),('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
	#thus, packet format-tuple: ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', size_of_pac = 0 or size_of_data, accu_size_of_content_trans = 0 or accu_size_of_content_trans, delay_account1 = 0 or current delay account, respectively for interest and data packets. Thereinto, delay_account = 节点处理时延 + 服务处理时延 + 链路传输时延
		
	## content_respond : (('pac_name1','pac_type1','pac_info1',accu_size_of_content_trans1,delay_account1,cur_time1_%float),('pac_name2','pac_type2','pac_info2',accu_size_of_content_trans2,delay_account2,cur_time2_%float),...)
	
	# content_respond : (('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),('pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
		
	## requests : (('pac_name1','pac_type1','pac_info1',0,cur_time1_%float),('pac_name2','pac_type2','pac_info2',0,cur_time2_%float),...)
	# self.requests可以由'__main__'函数直接指定
	# requests : (('pac_name1','pac_type1','pac_info1',0,0,0),('pac_name2','pac_type2','pac_info2',0,0,0),...)	
	
	## respond_delay : (('pac_name1',request_time1_%float,respond_time1_%float,respond_delay1_%float),('pac_name2',request_time2_%float,respond_time2_%float,respond_delay2_%float),...)
	
	## local_pro_record : (('pac_name1','pac_name1_1','pac_name1_2',issue_time1_%float),(),...) -> (('pac_name1','pac_name1_1',hop_account,'pac_name1_2',hop_account,issue_time1_%float,respond_time1_%float),(),...)
	
	## local_pro_record : (('pac_name1','pac_name1_1','pac_name1_2',issue_time1_%float),(),...) -> (('pac_name1','pac_name1_1',size_of_content1_1,accu_size_of_content_trans1_1,delay_account1_1,'pac_name1_2',size_of_content1_2,accu_size_of_content_trans1_2,delay_account1_2,issue_time1_%float,respond_time1_%float),(),...)
	
	# local_pro_record : (('pac_name1','pac_name1_1',0,0,0,0,'pac_name1_2',0,0,0,0),(),...) -> (('pac_name1','pac_name1_1',hop_account1_1,size_of_content1_1,accu_size_of_content_trans1_1,delay_account1_1,'pac_name1_2',hop_account1_2,size_of_content1_2,accu_size_of_content_trans1_2,delay_account1_2),(),...)
	local_pro_record = tuple()
	service_set = tuple()
	
	Computation_Task_record = 0 # 记录每个router的计算任务量
	
	
	
	def __init__(self,local_label,node_type,v_comp,init_comp_CAP=0,init_cache_CAP=1000):
			NDN.__init__(self,local_label,node_type,init_cache_CAP=1000)
			self.v_comp = v_comp # 本地节点服务计算速度默认为1.8GHZ，单个文件的大小一般在500MB左右
			self.comp_CAP = init_comp_CAP

	
	# CS : ('content_name1',size_of_content1,'content_name2',size_of_content2,...)
	def search_CS_i(self,cur_pac_name): # '('F_F', 's0', ('p2', 'p4', 'p5')), or ('P_F', 's0', ('p2',))
		#print('%s CS:' % self.label)
		#self.print__content_store()
		print('ICECN_class \'search_CS_i\' print:')
		if cur_pac_name[0] == 'F_F': # 'F_F'
			if cur_pac_name in self.CS:
				tem_index = self.CS.index(cur_pac_name) + 1
				return (cur_pac_name,self.CS[tem_index],cur_pac_name)
			else:
				return False
		else: # 'P_F'
			temp_l_1 = ('F_F',) + cur_pac_name[1:]
			if temp_l_1 in self.CS:
				tem_index = self.CS.index(temp_l_1) + 1
				return (temp_l_1,self.CS[tem_index],temp_l_1)
			else:
				#temp_l_1 = cur_pac_name[2][0]
				temp_l_1 = cur_pac_name
				'''
				if self.label == 'P1':
					print('P1 CS:')
					self.print__content_store()
					print(temp_l_1)
				'''
				if temp_l_1 in self.CS:
					#print('yes!!')
					tem_index = self.CS.index(temp_l_1) + 1
					#print(self.CS[tem_index])
					return (cur_pac_name,self.CS[tem_index],temp_l_1)
				else:
					
					if len(cur_pac_name) > 3:
						temp_l_1 = cur_pac_name[2:]
						if temp_l_1 in self.CS:
							#print('yes!!')
							tem_index = self.CS.index(temp_l_1) + 1
							#print(self.CS[tem_index])
							return (cur_pac_name,self.CS[tem_index],temp_l_1)
					
					return False
			
		
	#def shortest_path_FIB(self,trans_content): # inherited from class NDN
			
		
	# PIT : ('pac_name1',('A1','A2',...),('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	# cur_pac like ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account)
	def PIT_pro_i(self,cur_pac):
		print('ICECN_class \'PIT_pro_i\' print:')
		l_PIT = list(self.PIT)
		
		Flag_exec = True
		
		if cur_pac[0] in l_PIT:
			tem_index = l_PIT.index(cur_pac[0])+1
			l_PIT_i = list(l_PIT[tem_index])
			#l_PIT_i.append(cur_pac[2])
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
			# 非本地处理，转发出去
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

			
			
		'''	
			if cur_pac[0][0] == 'F_F':
				tem_succ_node = self.shortest_path_FIB(cur_pac[0][1])
				if tem_succ_node:
					self.transfer = (((tem_succ_node,),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
				else:
					self.transfer = (((),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
			else: # 'P_F'
				#tem_succ_node = self.shortest_path_FIB(cur_pac[0][2][0])
				tem_succ_node = self.shortest_path_FIB(cur_pac[0])
				if tem_succ_node:
					self.transfer = (((tem_succ_node,),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
				else:
					tem_succ_node = self.shortest_path_FIB(cur_pac[0][2:])
					print('tem_succ_node:')
					print(tem_succ_node)
					if tem_succ_node:
						self.transfer = (((tem_succ_node,),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
					else:
						self.transfer = (((),cur_pac[0],cur_pac[1],self.label,cur_pac[3],cur_pac[4],cur_pac[5],cur_pac[6]),)
		'''
		
		
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
	
	# '/exec/dec/s1|/p1|/p2/' or '/exec/und/s1|/p1|/p2/'
	## local_pro_record : (('pac_name1','pac_name1_1','pac_name1_2',issue_time1_%float),(),...) -> (('pac_name1',issue_time1_%float,respond_time1_%float),(),...)
	# local_pro_record : (('pac_name1','pac_name1_1',0,0,0,0,'pac_name1_2',0,0,0,0),(),...) -> (('pac_name1','pac_name1_1',hop_account1_1,size_of_content1_1,accu_size_of_content_trans1_1,delay_account1_1,'pac_name1_2',hop_account1_2,size_of_content1_2,accu_size_of_content_trans1_2,delay_account1_2),(),...)
	# cur_pac : ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account)
	def local_process_i(self,cur_pac): # ('F_F', 's0', ('p2', 'p4', 'p5')) -> ('P_F', 's0', ('p2',)), ('P_F', 's0', ('p4',)), ('P_F', 's0', ('p5',))
		print('ICECN_class \'local_process_i\' print:')
		
		if cur_pac[0][2] != ('Default',): # ('F_F', 's0', ('p2', 'p4', 'p5'))
			tem_local_pro = (cur_pac[0],cur_pac[4],cur_pac[5],cur_pac[6],0) # for local_pro_record;cur_pac[6]为energy_accountd,最后加的0是服务计时开始。
			print('tem_local_pro!!:')
			print(tem_local_pro)
			print(cur_pac)
			'''
			tem_pac_name = cur_pac[0] # ('F_F', 's0', ('p2', 'p4', 'p5'))
			tem_p_set = list(cur_pac[0][2]) # ['p2', 'p4', 'p5']
			tem_para_requests = tuple()
			while tem_p_set:
				tem_para_i_name = ('P_F',tem_pac_name[1]) + ((tem_p_set.pop(),),)
				tem_para_requests += ((tem_para_i_name,'i',self.label,0,0,0,0),)
				tem_local_pro += (tem_para_i_name,0,0,0,0,0)
			'''
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
			#print(self.requests)
			self.packet_arrive_set(tem_index_1,len(self.requests)) # inherited from parent class NDN
			
			#self.transfer = () # 本地计算直接重新转发，不经过self.transfer
			
			self.local_pro_record += (tem_local_pro,)
			print('%s self.local_pro_record!!:' % self.label)
			print(self.local_pro_record)
		
		else: # ('F_F','s0','Default')
			pre_size = size_para # 5e5
			temp_size = pre_size/1000 # 计算结果的大小：Ci -> Ci/100
			delay_account = cur_pac[5] + 10*pre_size/self.v_comp # 累计服务处理时延
			self.Computation_Task_record += 10*pre_size # 累计本地计算任务量
			back_pac = (cur_pac[0],'d',0,temp_size,cur_pac[4],delay_account,cur_pac[6],'local_process')
			
			#print(back_pac)

			l_node_queue = list(self.node_queue)
			l_node_queue.insert(len(l_node_queue), back_pac)
			self.node_queue = tuple(l_node_queue)
			
			
		print('ICECN_class \'local_process_i\' end:')
	
	# requests : (('pac_name1','pac_type1','pac_info1',0,0,0),('pac_name2','pac_type2','pac_info2',0,0,0),...)
	# cur_pac like ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account)			
	# local_pro_record : (('pac_name1','pac_name1_1',0,0,0,0,'pac_name1_2',0,0,0,0),(),...) -> (('pac_name1','pac_name1_1',hop_account1_1,size_of_content1_1,accu_size_of_content_trans1_1,delay_account1_1,'pac_name1_2',hop_account1_2,size_of_content1_2,accu_size_of_content_trans1_2,delay_account1_2),(),...)
	# trans_pac : ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account)
	
	def local_process_d(self,trans_pac,G,Global_FIB):
		print('ICECN_class \'local_process_d\' print:')
		print('self.local_pro_record:')
		print(self.local_pro_record)
		#l_local_pro_record = (('/exec/dec/s1|/p1/', '/p1|/exec/dec/s1/', 1550642005.3422499),)
		#l_local_pro_record[0] = ('/exec/dec/s1|/p1/', '/p1|/exec/dec/s1/', 1550642005.3422499)
		#trans_pac = ('/exec/dec/s1|/p1/', 'd', '1' , size_of_pac1 , accu_size_of_content_trans1 , delay_account1 , 'swap')
		#print('trans_pac:')
		#print(trans_pac)
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
				self.Computation_Task_record += 10 * size_of_pac # 累计本地计算任务量
				print(self.Computation_Task_record)

				
				if trans_pac[0][0] == 'P_F': # 'P_F', 本地处理：local processing
					
					delay_account += 10 * size_of_pac/self.v_comp # 累计服务处理时延
					
					comp_task_dur = 10 * size_of_pac/self.v_comp # 服务处理时延，用于E_co计算
					P_static = 30
					energy_account += P_static * comp_task_dur # 附加E_co,static

					size_of_pac = size_of_pac/1000 # 计算结果的大小：Ci -> Ci/1000


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
		


	'''
	def local_process_d(self,trans_pac,G,Global_FIB):
		print('ICECN_class \'local_process_d\' print:')
		print('self.local_pro_record:')
		print(self.local_pro_record)
		#l_local_pro_record = (('/exec/dec/s1|/p1/', '/p1|/exec/dec/s1/', 1550642005.3422499),)
		#l_local_pro_record[0] = ('/exec/dec/s1|/p1/', '/p1|/exec/dec/s1/', 1550642005.3422499)
		#trans_pac = ('/exec/dec/s1|/p1/', 'd', '1' , size_of_pac1 , accu_size_of_content_trans1 , delay_account1 , 'swap')
		#print('trans_pac:')
		#print(trans_pac)
		l_local_pro_record = list(self.local_pro_record)
		for i in range(len(l_local_pro_record)):
			l_record_i = l_local_pro_record[i]
			
			if trans_pac[0][0] == 'F_F':
				#temp_pac_name = ('P_F',trans_pac[0][1],trans_pac[0][2])
				temp_pac_name = ('P_F',) + trans_pac[0][1:]
				print(temp_pac_name)
			else:
				temp_pac_name = ()
			
			tem_index = -2 # none	
			if trans_pac[0] in l_record_i[1:]:
				tem_index = l_record_i.index(trans_pac[0]) + 1
			elif temp_pac_name in l_record_i[1:]:
				tem_index = l_record_i.index(temp_pac_name) + 1
				
			if (tem_index > -2) and (l_record_i[tem_index+1] == 0):
				l_li = list(l_record_i)
				l_li[tem_index-1] = trans_pac[0] # data packet name
				l_li[tem_index] = int(trans_pac[2]) # data packet hop account
				l_li[tem_index+1] = trans_pac[3] # data packet size
				l_li[tem_index+2] = trans_pac[4] # data packet size accumulate
				l_li[tem_index+3] = trans_pac[5] # data packet delay
				l_li[tem_index+4] = trans_pac[6] # data packet energy
				l_record_i = tuple(l_li)
				#print(l_record_i)

			# local_pro_record : (('pac_name1','pac_name1_1',0,0,0,0,'pac_name1_2',0,0,0,0),(),...) -> (('pac_name1','pac_name1_1',hop_account1_1,size_of_content1_1,accu_size_of_content_trans1_1,delay_account1_1,'pac_name1_2',hop_account1_2,size_of_content1_2,accu_size_of_content_trans1_2,delay_account1_2),(),...)
			# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
			# '/exec/dec/s1|/p1/'
			#if test_label: # 如果参数都聚齐了，就进行最终的计算
			
			test_flag = False
			if (len(l_record_i) != 0) and (l_record_i[-1] != 'complete'):
				test_flag = True
				for k in range(5,len(l_record_i),6):
					if l_record_i[k+2] == 0:
						test_flag = False
						break
			
			
			if test_flag: # 如果之前没有处理过，并且参数都聚齐了，就进行最终的计算
			#if (0 in l_record_i) == False: # 如果参数都聚齐了，就进行最终的计算
				#l_record_i += (time.time(),)
				total_hop_account = 0
				size_of_pac = 0
				accu_size_of_content_trans = l_record_i[1]
				p_delay_account_set = ()
				delay_account = l_record_i[2]
				
				energy_account = l_record_i[3]
				comp_task_dur = l_record_i[4]
				
				for j in range(5,len(l_record_i),6):
					total_hop_account += l_record_i[j+1]
					accu_size_of_content_trans += l_record_i[j+3]
					p_delay_account_set += (l_record_i[j+4],)
					energy_account += l_record_i[j+5]
					if l_record_i[j][0] == 'F_F': # 处理之后的
						size_of_pac += l_record_i[j+2]
					else: # 本地处理：local processing, '/p1|/exec/dec/s1' or '/p1|/exec/und/s2'
						
						print('Computation_Task_record:')
						print(self.label)
						print(self.Computation_Task_record)
						self.Computation_Task_record += 10*l_record_i[j+2] # 累计本地计算任务量
						print(self.Computation_Task_record)
						
						size_of_pac += l_record_i[j+2]/1000 # 计算结果的大小：Ci -> Ci/100
						delay_account += 10*l_record_i[j+2]/self.v_comp # 累计服务处理时延
						
						comp_task_dur += 10*l_record_i[j+2]/self.v_comp # 累计服务处理时延，用于E_co计算
						
						temp_cache_content_name = ('F_F',) + l_record_i[j][1:]
						
						energy_cache = self.decide_cache(temp_cache_content_name,l_record_i[j+2]/1000,G,Global_FIB) # 中间计算结果缓存
						energy_account += energy_cache
				
				# 最终处理
				
				print('Computation_Task_record:')
				print(self.label)
				print(self.Computation_Task_record)
				self.Computation_Task_record += 10*size_of_pac*1000 # 累计本地计算任务量
				print(self.Computation_Task_record)
				
				delay_account += 10*size_of_pac/self.v_comp # 累计服务处理时延
				
				comp_task_dur += 10*size_of_pac/self.v_comp # 累计服务处理时延，用于E_co计算
				
				size_of_pac = size_of_pac/10 # 计算结果的大小：Ci -> Ci/10 (最终处理)
				delay_account += max(p_delay_account_set)
				
				comp_task_dur += max(p_delay_account_set)
				P_static = 30
				energy_account += P_static * comp_task_dur # 附加E_co,static
				

				#back_pac = (l_record_i[0],'d',total_hop_account,size_of_pac,accu_size_of_content_trans,delay_account,'retrans')
				
				#back_pac = (l_record_i[0],'d',total_hop_account,size_of_pac,accu_size_of_content_trans,delay_account,energy_account)
				
				back_pac = (l_record_i[0],'d',total_hop_account,size_of_pac,accu_size_of_content_trans,delay_account,energy_account,'local_process')
				
				#print(back_pac)

				l_node_queue = list(self.node_queue)
				l_node_queue.insert(len(l_node_queue), back_pac)
				self.node_queue = tuple(l_node_queue)
				#print('processed packet back:')
				#print(self.node_queue)
				
				l_record_i += ('complete',)
				
			l_local_pro_record[i] = l_record_i
		
		self.local_pro_record = tuple(l_local_pro_record)
		#print('self.local_pro_record:')
		#print(self.local_pro_record)
		#print(self.node_queue)
		#print('ICECN_class \'local_process_d\' end:')
		
		'''
		
		
		
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
	def pro_interest(self,cur_pac,G,Global_FIB): # cur_pac like ('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1)
		print('ICECN_class \'pro_interest\' print:')
		tem_search_CS_i = self.search_CS_i(cur_pac[0]) # tem_search_CS_i = (content_item_name,size_of_content)
		#print(tem_search_CS_i)
		if (self.node_type != 'h') and (tem_search_CS_i != False):
			self.transfer = (((cur_pac[2],),tem_search_CS_i[0],'d',0,tem_search_CS_i[1],0,cur_pac[5],cur_pac[6]),)

			l_CS = list(self.CS)
			del l_CS[l_CS.index(tem_search_CS_i[2])+1]		#LRU
			del l_CS[l_CS.index(tem_search_CS_i[2])]		#LRU
			l_CS.insert(0,tem_search_CS_i[1])
			l_CS.insert(0,tem_search_CS_i[2])
			self.CS = tuple(l_CS)
			
		else:
			self.PIT_pro_i(cur_pac)
		print('ICECN_class \'pro_interest\' end:')
					
				
	# PIT : ('pac_name1',('A1','A2',...),('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)	
	# cur_pac like ('pac_name','pac_type','pac_info',size_of_pac,accu_size_of_content_trans,delay_account)	
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)		
	
	
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
					
					#cur_pac = cur_pac[:-1]
					
				else:
					
					tem_l_PIT_node_set = list(l_PIT[tem_index])
					#print('tem_l_PIT_node_set:')
					#print(tem_l_PIT_node_set)
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
					
					
					'''
					
					tem_l_PIT_node_set = list(l_PIT[tem_index])
					print('tem_l_PIT_node_set:')
					print(tem_l_PIT_node_set)
					tem_l_PIT_index = ()
					while 'local_process' in tem_l_PIT_node_set:
						tem_l_PIT_index += (tem_l_PIT_node_set[tem_l_PIT_node_set.index('local_process')-1],'local_process')
						tem_l_PIT_node_set.pop(tem_l_PIT_node_set.index('local_process'))
						
						l_back_nodes_1.pop(l_back_nodes_1.index('local_process')-1)
						l_back_nodes_1.pop(l_back_nodes_1.index('local_process'))
						'''
					
					#print('tem_l_PIT_index:')
					#print(tem_l_PIT_index)
					l_PIT[tem_index] = tem_l_PIT_index
					
				back_nodes_1 = tuple(l_back_nodes_1)
				
			else:
				l_PIT.pop(tem_index-1)
				l_PIT.pop(tem_index-1)
			
			self.PIT = tuple(l_PIT)
		
		print('back_nodes_1:')
		print(back_nodes_1)
		
		if  cur_pac[0][0] == 'F_F':
			#temp_pac_name = ('P_F',cur_pac[0][1],cur_pac[0][2])
			temp_pac_name = ('P_F',) + cur_pac[0][1:]
			
			if temp_pac_name in self.PIT:
				tem_index = self.PIT.index(temp_pac_name) + 1
				back_nodes_1 += self.PIT[tem_index]
				l_PIT = list(self.PIT)
				l_PIT.pop(tem_index-1)
				l_PIT.pop(tem_index-1)
				self.PIT = tuple(l_PIT)
				print('dottt1')
				l_back_nodes_1 = list(back_nodes_1)
				while 'local_process' in l_back_nodes_1:
					l_back_nodes_1.pop(l_back_nodes_1.index('local_process'))
				back_nodes_1 = tuple(l_back_nodes_1)
		
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
				
	# CS : ('content_name1','content_name2',...)
	def decide_cache(self,wait_cache_content,content_size,G,Global_FIB):
		print('ICECN_class \'decide_cache\' print:')
		#print(wait_cache_content)
		'''
		if wait_cache_content[0] == 'P_F':
			c_wait_cache_content = wait_cache_content[2][0]
		else:
			c_wait_cache_content = wait_cache_content
		'''
		c_wait_cache_content = wait_cache_content
		
		if (self.node_type == 'r') and (c_wait_cache_content in self.CS) == False:

			self.cache_CS(c_wait_cache_content,content_size,G,Global_FIB) # cache_CS is inherited from NDN class
			
			P_ca = 2.5e-9 # P_ca = 2.5e-9 J/(bit*s)
			S_ca = 1.28e10 # S_ca = 1.28e10 bit/s
			
			energy_cache = content_size * content_size * P_ca / S_ca
			
			return energy_cache
		else:
			
			return 0
			
		print('ICECN_class \'decide_cache\' end:')
	
	# '/p1|/exec/dec/s1/'
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
	
	def local_onpath_process_d(self,cur_pac):
		print('ICECN_class \'local_onpath_process_d\' print:')
		
		print('Computation_Task_record:')
		print(self.label)
		print(self.Computation_Task_record)
		self.Computation_Task_record += 10*cur_pac[3] # 累计本地计算任务量
		print(self.Computation_Task_record)
		
		#proc_pac_name = ('F_F',cur_pac[0][1],cur_pac[0][2]) # on-path processing
		
		proc_pac_name = ('F_F',) + cur_pac[0][1:] # on-path processing
		
		Inst = 10*cur_pac[3] # Instructions
		proc_pac_delay = cur_pac[5] + Inst/self.v_comp # 累计服务处理时延
		proc_pac_size = cur_pac[3]/1000 # 计算结果的大小：Ci -> Ci/100
		
		pro_pac_energy = cur_pac[6]
		
		#proc_pac = (proc_pac_name,cur_pac[1],cur_pac[2],proc_pac_size,cur_pac[4],proc_pac_delay,'retrans')
		
		proc_pac = (proc_pac_name,cur_pac[1],cur_pac[2],proc_pac_size,cur_pac[4],proc_pac_delay,pro_pac_energy)
		
		l_node_queue = list(self.node_queue)
		l_node_queue.insert(len(l_node_queue), proc_pac)
		self.node_queue = tuple(l_node_queue)
		print(self.node_queue)
		
		print('ICECN_class \'local_onpath_process_d\' end:')
	
	
	# PIT : ('pac_name1',('A1','A2',...),('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)	
	# cur_pac like ('pac_name1','pac_type1','pac_info1')	
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1'),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2'),...) | thus, packet format-tuple: ('pac_name','pac_type','pac_info'), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', respectively for interest and data packets
	# transfer[0] : (('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1')
	'''
	def pro_data(self,cur_pac,G,Global_FIB):
		print('%s ICECN_class \'pro_data\' print:' % self.label)
		
		if (cur_pac[0][0] == 'P_F') and (cur_pac[0][1] in self.service_set):
			energy_cache = self.decide_cache(cur_pac[0],cur_pac[3],G,Global_FIB)
			cur_pac = cur_pac[:-1] + (cur_pac[6] + energy_cache,)
			self.local_onpath_process_d(cur_pac) # local on-path processing
			
		else:
			self.PIT_pro_d(cur_pac)
			if len(self.transfer[0][0]) != 0:
				energy_cache = self.decide_cache(self.transfer[0][1],self.transfer[0][4],G,Global_FIB)
				trans_pac = self.transfer[0][:-1] + (self.transfer[0][7] + energy_cache,)
				self.transfer = (trans_pac,)
				
		print('ICECN_class \'pro_data\' end:')
		
	'''
	def pro_data(self,cur_pac,G,Global_FIB):
		print('%s ICECN_class \'pro_data\' print:' % self.label)
		
		if (cur_pac[0][0] == 'P_F'):
			temp_name = ('F_F',) + cur_pac[0][1:]
			tem_search_CS_i = self.search_CS_i(temp_name)
			print('dotttt')
			print(cur_pac)
			print('CS:')
			self.print__content_store()
			print('service:')
			print(self.service_set)
			if (self.node_type != 'h') and (tem_search_CS_i != False):
				#energy_cache = self.decide_cache(cur_pac[0],cur_pac[3],G,Global_FIB)
				#cur_pac = cur_pac[:-1] + (cur_pac[6] + energy_cache,)
				
				proc_pac = (tem_search_CS_i[0],cur_pac[1],cur_pac[2],tem_search_CS_i[1],cur_pac[4],cur_pac[5],cur_pac[6])
				print('proc_pac:')
				print(proc_pac)
				
				l_node_queue = list(self.node_queue)
				l_node_queue.insert(len(l_node_queue), proc_pac)
				self.node_queue = tuple(l_node_queue)
				#print(self.node_queue)
			elif (cur_pac[0][1] in self.service_set):
				energy_cache = self.decide_cache(cur_pac[0],cur_pac[3],G,Global_FIB)
				cur_pac = cur_pac[:-1] + (cur_pac[6] + energy_cache,)
				self.local_onpath_process_d(cur_pac) # local on-path processing
			
			else:
				self.PIT_pro_d(cur_pac)
				if len(self.transfer[0][0]) != 0:
					energy_cache = self.decide_cache(self.transfer[0][1],self.transfer[0][4],G,Global_FIB)
					trans_pac = self.transfer[0][:-1] + (self.transfer[0][7] + energy_cache,)
					self.transfer = (trans_pac,)
		else:
			self.PIT_pro_d(cur_pac)
			if len(self.transfer[0][0]) != 0:
				energy_cache = self.decide_cache(self.transfer[0][1],self.transfer[0][4],G,Global_FIB)
				trans_pac = self.transfer[0][:-1] + (self.transfer[0][7] + energy_cache,)
				self.transfer = (trans_pac,)
				
		print('ICECN_class \'pro_data\' end:')
		
	#'''	
	
	def issue_init_interests(self,t_operation_parameter_requests):
		for ti_re in t_operation_parameter_requests:
			self.requests += ((ti_re,'i',self.label,0,0,0),)
	
		
	#def pro_pac(self): # inherited from class NDN
		
	# t_operation_parameter_requests: ('/exec/dec/s1|/p1|/p2/','/exec/und/s2|/p3|/p2/',...)
	# requests : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...), where 'pac_name' like '/exec/dec/s1|/p1|/p2/'
	# requests : (('pac_name1','pac_type1','pac_info1',0,0,0),('pac_name2','pac_type2','pac_info2',0,0,0),...)
	
	#def packet_arrive_set(self,range_start,range_stop): # inherited from class NDN
	
	#def get_respond_delay(self,responded_content): # inherited from class NDN
	
	#def prov_content(self,num_content): # 直接由main函数指定self.CS，因为是content provider，所以self.CS不会改变，例如：P1.CS = ('p1',)
	
	#def print__content_store(self): # inherited from class NDN

	#def cache_CS(self,wait_cache_content): # inherited from class NDN
	
# -----------------------------------------------generate FIB start-----------------------------------------------

#Global_FIB = {}
# Global_FIB : {'R1': ['prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...], 'R2': [],...}
# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)

#def get_FIBs(): # inherited from class NDN

#def print_FIBs(): # inherited from class NDN

def initial_Global_FIB(G,Global_FIB):
	#print('ini_FIB:')
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


#def update_Global_FIB(tar_node,new_cache_content):	# inherited from class NDN

#def delete_Global_FIB(tar_node,poped_content):	# inherited from class NDN


# -----------------------------------------------generate FIB end...-----------------------------------------------

