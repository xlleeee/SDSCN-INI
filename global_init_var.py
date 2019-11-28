import sys

from scipy.special import comb, perm

# 环境变量
Num_Global_service = 5 # 10 services or applications

Num_para = 200 # 60*100=6000 files

size_para = 5e5

req_num_total = 500 # 1000 requests, 10次重复实验

'''
Num_Global_service = 10 # 10 services or applications

Num_para = 600 # 60*100=6000 files

size_para = 5e5

req_num_total = 200 # 1000 requests, 5次重复实验
'''
#req_p_num = 2 # range from 1 to 12; from -1 to 12
#req_p_num = int(sys.argv[1]) # range from 1 to 12; from -1 to 12

comp_CAP = 0.5 * Num_Global_service
temp_req_p_num = 10
Num_req_file = comb(Num_Global_service,1) * comb(Num_para,temp_req_p_num)
cache_CAP = 0.02 * Num_req_file

print(Num_para)
#print(req_p_num)