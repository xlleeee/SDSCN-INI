# NDN

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time

'''
NDN node model:
class NDN:
	node_queue: list[arrived_packet_name]
	CS: list[name]
	PIT: dictionary{name:pred_node}
	FIB: dictionary{prefix:succ_node_list}
	def pro_interest(...):
		interest packet processing
		...
		pop in node_queue
		find in CS
		find in PIT
		find in FIB
		...
	def pro_data():
		data packet processing
		...
		pop in node_queue
		find in PIT
		cache in CS
		increase hop account
		...
'''

class NDN:		# NDN router
	node_queue = tuple()		# node_queue : (('pac_name1','pac_type1','pac_info1'),('pac_name2','pac_type2','pac_info2'),...)
	CS = tuple()		# CS : ('content_name1','content_name2',...)
	
	PIT = tuple()		# PIT : ('pac_name1',('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	FIB = tuple()		# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)
	transfer = tuple()		# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1'),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2'),...) | thus, packet format-tuple: ('pac_name','pac_type','pac_info'), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', respectively for interest and data packets
	
	content_respond = tuple()	# content_respond : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
	
	# ------Host node attribute------------
	requests = tuple()	# requests : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
	
	respond_delay = tuple()		# respond_delay : (('pac_name1',request_time1_%float,respond_time1_%float,respond_delay1_%float),('pac_name2',request_time2_%float,respond_time2_%float,respond_delay2_%float),...)
	# -------Host node attribute-end------------------------------	
	
	def __init__(self,local_label,node_type,init_cache_CAP=1000):
		self.label = local_label
		self.node_type = node_type		# node_type : 'r', or 'h', or 'p', where 'r' stands for a NDN router node, 'h' stands for a host node, and 'p' stands for a service provider node
		self.content_respond = (self.label,) # content_respond : (self.label,('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
		self.cache_CAP = init_cache_CAP
	
	# ------for in-network computing------------
	def local_processing(self,trans_pac):
		pass

	def issue_init_interests(self,t_operation_parameter_requests):
		pass
	# requests: (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
	# node_queue : (('pac_name1','pac_type1','pac_info1'),('pac_name2','pac_type2','pac_info2'),...)
	# respond_delay : (('pac_name1',request_time1_%float,respond_time1_%float,respond_delay1_%float),('pac_name2',request_time2_%float,respond_time2_%float,respond_delay2_%float),...)

	def packet_arrive_set(self,range_start,range_stop):		# 将生成的请求以0.01s的时间间隔发送到节点队列
		for i in range(range_start,range_stop):

			l_node_queue = list(self.node_queue)
			l_node_queue.insert(0, self.requests[i])
			self.node_queue = tuple(l_node_queue)
			#print('packet_arrive:')
			#print(self.node_queue)
			
			# 为requests加上请求时间
			# requests : ((cur_time1_%float,'pac_name1','pac_type1','pac_info1'),(cur_time2_%float,'pac_name2','pac_type2','pac_info2'),...)
			l_requests = list(self.requests)
			l_requests[i] = (time.time(),) + l_requests[i]
			self.requests = tuple(l_requests)
			
			#time.sleep(random.random()*3)
				
	# content_respond : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
	# requests : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
	# respond_delay : (('pac_name1',request_time1_%float,respond_time1_%float,respond_delay1_%float),('pac_name2',request_time2_%float,respond_time2_%float,respond_delay2_%float),...)
	
	def just_responded_content(slef,trans_pac):
		return trans_pac[0]
	
	# trans_pac : ('/exec/dec/s1|/p1/', 'd', '1', 'swap')
	def get_respond_delay(self,trans_pac):
		print('ICECN_class \'get_respond_delay\' print:')
		#print('self.respond_delay:')
		#print(self.respond_delay)
		#print(trans_pac)
		tem_index_r = 0
		j_respond_content = self.just_responded_content(trans_pac)
		#print(j_respond_content)
		for ri in self.respond_delay:
			if (j_respond_content in ri) and (len(ri) == 2):
				break
			else:
				tem_index_r += 1
				continue
		#print('tem_index_r in respond_delay: %d' % tem_index_r)
		#self.content_respond : (('/exec/dec/s1|/p1/', 'd', '1', 'swap', 1550641124.834903),)
		tem_index_c = 0
		tem_reverse_content_respond = self.content_respond[::-1]	# reverse
		for ci in tem_reverse_content_respond:
			if trans_pac[0] in ci:
				break
			else:
				tem_index_c += 1
				continue
		#print('tem_index_c in content_respond: %d' % tem_index_c)
		l_respond_delay = list(self.respond_delay)
		l_respond_delay_i = list(l_respond_delay[tem_index_r])
		l_respond_delay_i.append(tem_reverse_content_respond[tem_index_c][-1])
		l_respond_delay_i.append(l_respond_delay_i[2]-l_respond_delay_i[1])
		l_respond_delay[tem_index_r] = tuple(l_respond_delay_i)
		self.respond_delay = tuple(l_respond_delay)
		
		
		#print('respond_delay:')
		#print(self.respond_delay)
		num_complete_req = 0
		
		#print('The num of completed requests: %d' % num_complete_req)
		#print('The num of completed requests: %d' % len(self.respond_delay))
		
		print('ICECN_class \'get_respond_delay\' end:')
			
	
	# ------Host node operation-end-------------------
	
	def print__content_store(self):
		for li in self.CS:
			print(li)

	
	# CS : ('content_name1',size_of_content1,'content_name2',size_of_content2,...)
	def cache_CS(self,wait_cache_content,content_size,G,Global_FIB):		# CS容量有限时的缓存替换策略
		l_CS = list(self.CS)
		l_CS.insert(0,content_size)
		l_CS.insert(0,wait_cache_content)
		update_Global_FIB(self.label,wait_cache_content,G,Global_FIB)		# 节点CS有缓存时更新其他节点的FIB
		if len(l_CS) > 2*self.cache_CAP:		# cache_CAP为CS容量
			l_CS.pop() # pop出最后一个值
			delete_Global_FIB(self.label,l_CS.pop(),G,Global_FIB)		# 节点CS缓存的内容有被替换删除时也需要更新其他节点的FIB
		self.CS = tuple(l_CS)
		#print('%s CS:' % self.label)
		#self.print__content_store()
		get_FIBs(G,Global_FIB)

# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)	
	def shortest_path_FIB(self,trans_content):		# find the optimal succ_node for the shortest path in FIB
		print('NDN_class \'shortest_path_FIB\' print:')
		path_len_FIB = list()
		#print(self.label)
		#print('FIB:')
		#print(self.FIB)
		#print(trans_content)
		if trans_content in self.FIB:
			tem_index = self.FIB.index(trans_content) + 1
			for i in range(len(self.FIB[tem_index])):
				path_len_FIB.append(len(self.FIB[tem_index][i]))
			succ_node = self.FIB[tem_index][path_len_FIB.index(min(path_len_FIB))][1]
			#print('succ_node: %s' % succ_node)
			return succ_node
		else:
			return False
		print('NDN_class \'shortest_path_FIB\' end:')
		
		# PIT : ('pac_name1',('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
		# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)
		# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1'),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2'),...) | thus, packet format-tuple: ('pac_name','pac_type','pac_info'), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', respectively for interest and data packets
		# CS : ('content_name1','content_name2',...)
		# node_queue : (('pac_name1','pac_type1','pac_info1'),('pac_name2','pac_type2','pac_info2'),...)
		# content_respond : ((('pac_name1','pac_type1','pac_info1'),cur_time1_%float),(('pac_name2','pac_type2','pac_info2'),cur_time2_%float),...)
		
	def pro_interest(self,cur_pac):		# Interest packet processing
		if (self.node_type != 'h') and (cur_pac[0] in self.CS):
			self.transfer = (((cur_pac[2],),cur_pac[0],'d','0'),)
			l_CS = list(self.CS)
			del l_CS[l_CS.index(cur_pac[0])]		#LRU
			l_CS.insert(0,cur_pac[0])
			self.CS = tuple(l_CS)
		else:
			l_PIT = list(self.PIT)
			if cur_pac[0] in l_PIT:
				tem_index = l_PIT.index(cur_pac[0]) + 1
				l_PIT_i = list(l_PIT[tem_index])
				l_PIT_i.append(cur_pac[2])
				l_PIT[tem_index] = tuple(l_PIT_i)
				self.transfer = (((),cur_pac[0],cur_pac[1],self.label),)
			else:
				l_PIT.append(cur_pac[0])
				l_PIT.append((cur_pac[2],))
				tem_succ_node = self.shortest_path_FIB(cur_pac[0])
				if tem_succ_node:
					self.transfer = (((tem_succ_node,),cur_pac[0],cur_pac[1],self.label),)
				else:
					self.transfer = (((),cur_pac[0],cur_pac[1],self.label),)
			self.PIT = tuple(l_PIT)
	
	# PIT : ('pac_name1',('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1'),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2'),...) | thus, packet format-tuple: ('pac_name','pac_type','pac_info'), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', respectively for interest and data packets
	# CS : ('content_name1','content_name2',...)
	# node_queue : (('pac_name1','pac_type1','pac_info1'),('pac_name2','pac_type2','pac_info2'),...)
	# content_respond : ((('pac_name1','pac_type1','pac_info1'),cur_time1_%float),(('pac_name2','pac_type2','pac_info2'),cur_time2_%float),...)
	
	def pro_data(self,cur_pac,G,Global_FIB):		# Data packet processing
		if cur_pac[0] in self.PIT:
			tem_index = self.PIT.index(cur_pac[0]) + 1
			self.transfer = ((self.PIT[tem_index],cur_pac[0],'d',cur_pac[2]),)
			l_PIT = list(self.PIT)
			l_PIT.pop(tem_index-1)
			l_PIT.pop(tem_index-1)
			self.PIT = tuple(l_PIT)
			if (self.node_type == 'r') and ((cur_pac[0] in self.CS) == False):

				self.cache_CS(cur_pac[0],G,Global_FIB)		# cache arrived content, and update FIB for all other nodes because of caching content locally, meanwhile, delete FIB for all other nodes because of pop cached content
		else:
			self.transfer = (((),cur_pac[0],cur_pac[1],cur_pac[2]),)

	# PIT : ('pac_name1',('prod_node1','prod_node2',...),'pac_name2',('prod_node3',...),...)
	# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)
	# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1'),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2'),...) | thus, packet format-tuple: ('pac_name','pac_type','pac_info'), where 'pac_type' = 'i' or 'd', 'pac_info' = 'prod_node' or 'hop_account', respectively for interest and data packets
	# CS : ('content_name1','content_name2',...)
	# node_queue : (('pac_name1','pac_type1','pac_info1'),('pac_name2','pac_type2','pac_info2'),...)
	# content_respond : ((('pac_name1','pac_type1','pac_info1'),cur_time1_%float),(('pac_name2','pac_type2','pac_info2'),cur_time2_%float),...)
		
	def pro_pac(self,G,Global_FIB):		# 节点包处理流程
		
		print('T- %s :' % self.label)
		
		tem_time_node_start = time.time() # 节点处理开始计时
		
		
		while True:		# 时刻监控本节点队列是否为空，如果不为空，则进行包处理；如果为空，则不进行任何处理，继续监控
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
			'''
			print('%s-NDN_class \'pro_pac\' print node_queue for each node:' % self.label)
			for ri in G.nodes(data=True):
				print('%s:' % ri[1]['model'].label)
				print(ri[1]['model'].node_queue)
			print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
			print('%s-NDN_class \'pro_pac\' print PIT for each node:' % self.label)
			for ri in G.nodes(data=True):
				print('%s:' % ri[1]['model'].label)
				print(ri[1]['model'].PIT)
			print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
			'''
			
			if len(self.node_queue) != 0:

				# node_queue : (('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),('pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
				# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
				l_self_node_queue = list(self.node_queue)
				cur_pac = l_self_node_queue.pop()
				self.node_queue = tuple(l_self_node_queue)
				print('cur_pac:')
				print(cur_pac)
				
				tem_time_pac_start = time.time() # 包处理计时开始
				
				if cur_pac[1] == 'i':		# Interest packet
					self.pro_interest(cur_pac,G,Global_FIB)
				else:			# Data packet
					self.pro_data(cur_pac,G,Global_FIB)
				
				# node_queue : (('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),('pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
				# transfer : ((('succ_node1','succ_node2',..),'pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),(('succ_node1','succ_node2',..),'pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
				#print('self.transfer:')
				#print(self.transfer)
				
				if len(self.transfer) > 0:
					
					l_transfer = list(self.transfer)
					while l_transfer:
						#trans_pac = (l_transfer[0][1],l_transfer[0][2],l_transfer[0][3],l_transfer[0][4],l_transfer[0][5],l_transfer[0][6])
						trans_pac = l_transfer[0][1:]
						l_transfer_succ_nodes = list(l_transfer[0][0])
						l_transfer.pop(0)
						#print(trans_pac)
						#print(l_transfer_succ_nodes)
						#print(l_transfer)
						while l_transfer_succ_nodes:
							temp_succ_node = l_transfer_succ_nodes.pop()
							print('temp_succ_node')
							print(temp_succ_node)
							if temp_succ_node == self.label:		# back to interest request node

								# content_respond : (('pac_name1','pac_type1','pac_info1',cur_time1_%float),('pac_name2','pac_type2','pac_info2',cur_time2_%float),...)
								# content_respond : (('pac_name1','pac_type1','pac_info1',size_of_pac1,accu_size_of_content_trans1,delay_account1),('pac_name2','pac_type2','pac_info2',size_of_pac2,accu_size_of_content_trans2,delay_account2),...)
								
								
								#print('self.requests: %s' % self.label)
								#print(self.requests)
								
								# 为content_respond添加时间
								tem_content_respond = trans_pac
								for k in range(len(self.requests)):
									if type(self.requests[k][0]) == float:
										if self.requests[k][1] == trans_pac[0]:
											tem_content_respond = (self.requests[k][0],) + trans_pac
											break
								
								self.content_respond += (tem_content_respond,)
								
								#self.content_respond += (trans_pac,)
								#print('self.content_respond:')
								#print(self.content_respond)

								#print('cur_pac:')
								#print(cur_pac)
								#print('trans_pac')
								#print(trans_pac)
								
								# for in-network process
								#self.local_processing(cur_pac)
								self.local_process_d(trans_pac,G,Global_FIB)
								
							else:		# 尚未返回到请求Interest的节点

								l_other_node_queue = list(G.nodes[temp_succ_node]['model'].node_queue)
								#print('trans_pac:')
								#print(trans_pac)
								
								if trans_pac[-1] == 'retrans':
									trans_pac = trans_pac[:-1]
								else:
									l_trans_pac = list(trans_pac)
									
									l_trans_pac[4] += l_trans_pac[3] # accu_size_of_content_trans += size_of_pac
									
									tem_time_pac_end = time.time()
									tem_node_delay = tem_time_pac_end - tem_time_node_start # 包的节点时延=排队时延+节点处理时延
									#l_trans_pac[5] += tem_node_delay # delay_account += 节点时延
									
									rand_node_delay = (random.random()*2+4)*1e-4
									
									
									l_trans_pac[5] += rand_node_delay # delay_account += 节点时延
									
									Dist = 10 # 10-50 m
									S_prop = 3e8 # 3*10^8 m/s
									D_prop = Dist/S_prop # propagation delay
									l_trans_pac[5] += D_prop # delay_account += 传播时延
									
									
									f_up = 0.01 # 0.005-0.01
									B_up = 50e6 # 50-80 Mbps
									f_down = 0.15 # 0.15-0.2
									B_down = 150e6 # 100-300 Mbps
									
									p_tr_link = 1.5e-9 # 1.5e-9 J/bit
									p_tr_node = 2e-8 # 2e-8 J/bit

									if trans_pac[1] == 'd':
										l_trans_pac[2] += 1 # hop account++
										
										Data_size = l_trans_pac[3] # 40-160 MB, 即 320-1280 Mbit
										D_trans_down = (1+f_down)*(Data_size/B_down) # 下行链路传输时延
										l_trans_pac[5] += D_trans_down # delay_account += 下行链路传输时延
										
										l_trans_pac[6] += Data_size * (p_tr_link + p_tr_node) # energy_account += E_tr,link + E_tr,node
										
									else: # 'i'
										
										Inte_size = 100 # constant size: 500bit
										D_trans_up = (1+f_up)*(Inte_size/B_up) # 上行链路传输时延
										l_trans_pac[5] += D_trans_up # delay_account += 上行链路传输时延
										
										l_trans_pac[6] += Inte_size * (p_tr_link + p_tr_node) # energy_account += E_tr,link + E_tr,node
										
									trans_pac = tuple(l_trans_pac)
								
								l_other_node_queue.insert(0,trans_pac)	# 将包转发到下一节点
								#print('l_other_node_queue:')
								#print(l_other_node_queue)
								
								G.nodes[temp_succ_node]['model'].node_queue = tuple(l_other_node_queue)
				self.transfer = ()										
			else:
				#continue
				break
			print('%s-NDN_class \'pro_pac\' end this round:' % self.label)	
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# -----------------------------------------------generate FIB start-----------------------------------------------

#global Global_FIB = {}
#Global_FIB = {}
# Global_FIB : {'R1': ['prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...], 'R2': [],...}
# FIB : ('prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...)

def get_FIBs(G,Global_FIB):
	for ri in G.nodes(data=True):
		if ri[1]['model'].label in Global_FIB:
			ri[1]['model'].FIB = tuple(Global_FIB[ri[1]['model'].label])

def print_FIBs(G):
	for ri in G.nodes(data=True):
		print('%s FIB:' % ri[1]['model'].label)
		print(ri[1]['model'].FIB)
		

def initial_Global_FIB(G,Global_FIB):
	for ri in G.nodes(data=True):
		if ri[1]['model'].node_type == 'p':
			if len(ri[1]['model'].CS) != 0 :
				for content_i in ri[1]['model'].CS:
					if type(content_i) == str:
						update_Global_FIB(ri[0], content_i,G,Global_FIB)
					else:
						continue
	get_FIBs(G,Global_FIB)

def update_Global_FIB(tar_node,new_cache_content,G,Global_FIB):		# 更新其他节点的FIB
	for rj in G.nodes(data=True):
		local_node_label = rj[0]
		temp_shortest_path = tuple(nx.shortest_path(G, source= local_node_label, target= tar_node))
		if (local_node_label in Global_FIB) == False:
			Global_FIB[local_node_label] = []
		if len(temp_shortest_path) > 1:
			if new_cache_content in Global_FIB[local_node_label]:		#如果已有此条目，则附加上此路径
				tem_index = Global_FIB[local_node_label].index(new_cache_content) + 1
				l_paths = list(Global_FIB[local_node_label][tem_index])
				l_paths.append(temp_shortest_path)
				Global_FIB[local_node_label][tem_index] = tuple(l_paths)
			else:		#如果没有此条目，则添加新条目
				Global_FIB[local_node_label].append(new_cache_content)
				Global_FIB[local_node_label].append((temp_shortest_path,))
				

# Global_FIB : {'R1': ['prefix1',(('H1','P1'),('H1','R1','R3'),..),'prefix2',(('H1','R1'),..),...], 'R2': [],...}
def delete_Global_FIB(tar_node,poped_content,G,Global_FIB):		# 节点CS缓存的内容有被替换删除时也需要更新其他节点的FIB	
	for rj in G.nodes(data=True):
		if poped_content in Global_FIB[rj[1]['model'].label]:
			tem_index = Global_FIB[rj[1]['model'].label].index(poped_content) + 1
			l_paths = list(Global_FIB[rj[1]['model'].label][tem_index])
			for i in range(len(l_paths)):
				if l_paths[i][-1] == tar_node:
					l_paths[i] = '***'
			while '***' in l_paths:
				l_paths.remove('***')
			Global_FIB[rj[1]['model'].label][tem_index] = tuple(l_paths)

# -----------------------------------------------generate FIB end...-----------------------------------------------
#lock = threading.Lock()
