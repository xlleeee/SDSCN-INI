# Node engine: NDN

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time

class NDN:		# NDN router
	node_queue = tuple()
	CS = tuple()
	
	PIT = tuple()
	FIB = tuple()
	transfer = tuple()
		
	content_respond = tuple()
	
	# ------Host node attribute------------
	requests = tuple()
	
	respond_delay = tuple()
	# -------Host node attribute-end------------------------------	
	
	def __init__(self,local_label,node_type,init_cache_CAP=1000):
		self.label = local_label
		self.node_type = node_type
		self.content_respond = (self.label,)
		self.cache_CAP = init_cache_CAP
	
	# ------for in-network computing------------
	def local_processing(self,trans_pac):
		pass

	def issue_init_interests(self,t_operation_parameter_requests):
		pass
	
	
	def packet_arrive_set(self,range_start,range_stop):
		for i in range(range_start,range_stop):

			l_node_queue = list(self.node_queue)
			l_node_queue.insert(0, self.requests[i])
			self.node_queue = tuple(l_node_queue)
			
			l_requests = list(self.requests)
			l_requests[i] = (time.time(),) + l_requests[i]
			self.requests = tuple(l_requests)
			
	
	def just_responded_content(slef,trans_pac):
		return trans_pac[0]
	
	
	def get_respond_delay(self,trans_pac):
		print('ICECN_class \'get_respond_delay\' print:')
		tem_index_r = 0
		j_respond_content = self.just_responded_content(trans_pac)
		
		for ri in self.respond_delay:
			if (j_respond_content in ri) and (len(ri) == 2):
				break
			else:
				tem_index_r += 1
				continue
		
		tem_index_c = 0
		tem_reverse_content_respond = self.content_respond[::-1]	# reverse
		for ci in tem_reverse_content_respond:
			if trans_pac[0] in ci:
				break
			else:
				tem_index_c += 1
				continue
		
		l_respond_delay = list(self.respond_delay)
		l_respond_delay_i = list(l_respond_delay[tem_index_r])
		l_respond_delay_i.append(tem_reverse_content_respond[tem_index_c][-1])
		l_respond_delay_i.append(l_respond_delay_i[2]-l_respond_delay_i[1])
		l_respond_delay[tem_index_r] = tuple(l_respond_delay_i)
		self.respond_delay = tuple(l_respond_delay)
		
		num_complete_req = 0
		
		print('ICECN_class \'get_respond_delay\' end:')
			
	
	# ------Host node operation-end-------------------
	
	def print__content_store(self):
		for li in self.CS:
			print(li)

	
	def cache_CS(self,wait_cache_content,content_size,G,Global_FIB):
		l_CS = list(self.CS)
		l_CS.insert(0,content_size)
		l_CS.insert(0,wait_cache_content)
		update_Global_FIB(self.label,wait_cache_content,G,Global_FIB)
		if len(l_CS) > 2*self.cache_CAP:
			l_CS.pop()
			delete_Global_FIB(self.label,l_CS.pop(),G,Global_FIB)
		self.CS = tuple(l_CS)
		
		get_FIBs(G,Global_FIB)
	
	
	def shortest_path_FIB(self,trans_content):
		print('NDN_class \'shortest_path_FIB\' print:')
		path_len_FIB = list()
		
		if trans_content in self.FIB:
			tem_index = self.FIB.index(trans_content) + 1
			for i in range(len(self.FIB[tem_index])):
				path_len_FIB.append(len(self.FIB[tem_index][i]))
			succ_node = self.FIB[tem_index][path_len_FIB.index(min(path_len_FIB))][1]
			
			return succ_node
		else:
			return False
		print('NDN_class \'shortest_path_FIB\' end:')
		
		
		
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
	
		
	def pro_data(self,cur_pac,G,Global_FIB):
		if cur_pac[0] in self.PIT:
			tem_index = self.PIT.index(cur_pac[0]) + 1
			self.transfer = ((self.PIT[tem_index],cur_pac[0],'d',cur_pac[2]),)
			l_PIT = list(self.PIT)
			l_PIT.pop(tem_index-1)
			l_PIT.pop(tem_index-1)
			self.PIT = tuple(l_PIT)
			if (self.node_type == 'r') and ((cur_pac[0] in self.CS) == False):

				self.cache_CS(cur_pac[0],G,Global_FIB)
		else:
			self.transfer = (((),cur_pac[0],cur_pac[1],cur_pac[2]),)
	
	
	
	def pro_pac(self,G,Global_FIB):
		
		print('T- %s :' % self.label)
		
		tem_time_node_start = time.time()
		
		
		while True:
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
			
			if len(self.node_queue) != 0:
				
				l_self_node_queue = list(self.node_queue)
				cur_pac = l_self_node_queue.pop()
				self.node_queue = tuple(l_self_node_queue)
				print('cur_pac:')
				print(cur_pac)
				
				tem_time_pac_start = time.time()
				
				if cur_pac[1] == 'i':
					self.pro_interest(cur_pac,G,Global_FIB)
				else:
					self.pro_data(cur_pac,G,Global_FIB)
				
				
				if len(self.transfer) > 0:
					
					l_transfer = list(self.transfer)
					while l_transfer:
						
						trans_pac = l_transfer[0][1:]
						l_transfer_succ_nodes = list(l_transfer[0][0])
						l_transfer.pop(0)
						
						while l_transfer_succ_nodes:
							temp_succ_node = l_transfer_succ_nodes.pop()
							print('temp_succ_node')
							print(temp_succ_node)
							if temp_succ_node == self.label:
								
								tem_content_respond = trans_pac
								for k in range(len(self.requests)):
									if type(self.requests[k][0]) == float:
										if self.requests[k][1] == trans_pac[0]:
											tem_content_respond = (self.requests[k][0],) + trans_pac
											break
								
								self.content_respond += (tem_content_respond,)
								
								self.local_process_d(trans_pac,G,Global_FIB)
								
							else:

								l_other_node_queue = list(G.nodes[temp_succ_node]['model'].node_queue)
								
								if trans_pac[-1] == 'retrans':
									trans_pac = trans_pac[:-1]
								else:
									l_trans_pac = list(trans_pac)
									
									l_trans_pac[4] += l_trans_pac[3]
									
									tem_time_pac_end = time.time()
									tem_node_delay = tem_time_pac_end - tem_time_node_start
									
									rand_node_delay = (random.random()*2+4)*1e-4
									
									l_trans_pac[5] += rand_node_delay
									
									Dist = 10
									S_prop = 3e8
									D_prop = Dist/S_prop
									l_trans_pac[5] += D_prop
									
									
									f_up = 0.01
									B_up = 50e6
									f_down = 0.15
									B_down = 150e6
									
									p_tr_link = 1.5e-9
									p_tr_node = 2e-8 

									if trans_pac[1] == 'd':
										l_trans_pac[2] += 1
										
										Data_size = l_trans_pac[3]
										D_trans_down = (1+f_down)*(Data_size/B_down)
										l_trans_pac[5] += D_trans_down
										
										l_trans_pac[6] += Data_size * (p_tr_link + p_tr_node)
										
									else: # 'i'
										
										Inte_size = 100
										D_trans_up = (1+f_up)*(Inte_size/B_up)
										l_trans_pac[5] += D_trans_up
										
										l_trans_pac[6] += Inte_size * (p_tr_link + p_tr_node)
										
									trans_pac = tuple(l_trans_pac)
								
								l_other_node_queue.insert(0,trans_pac)
								
								
								G.nodes[temp_succ_node]['model'].node_queue = tuple(l_other_node_queue)
				self.transfer = ()										
			else:
				#continue
				break
			print('%s-NDN_class \'pro_pac\' end this round:' % self.label)	
			print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# -----------------------------------------------generate FIB start-----------------------------------------------

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

def update_Global_FIB(tar_node,new_cache_content,G,Global_FIB):
	for rj in G.nodes(data=True):
		local_node_label = rj[0]
		temp_shortest_path = tuple(nx.shortest_path(G, source= local_node_label, target= tar_node))
		if (local_node_label in Global_FIB) == False:
			Global_FIB[local_node_label] = []
		if len(temp_shortest_path) > 1:
			if new_cache_content in Global_FIB[local_node_label]:
				tem_index = Global_FIB[local_node_label].index(new_cache_content) + 1
				l_paths = list(Global_FIB[local_node_label][tem_index])
				l_paths.append(temp_shortest_path)
				Global_FIB[local_node_label][tem_index] = tuple(l_paths)
			else:
				Global_FIB[local_node_label].append(new_cache_content)
				Global_FIB[local_node_label].append((temp_shortest_path,))
				


def delete_Global_FIB(tar_node,poped_content,G,Global_FIB):
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
