import sys

from scipy.special import comb, perm

# environment variable
Num_Global_service = 5

Num_para = 200

size_para = 5e5

req_num_total = 500

comp_CAP = 0.5 * Num_Global_service
temp_req_p_num = 10
Num_req_file = comb(Num_Global_service,1) * comb(Num_para,temp_req_p_num)
cache_CAP = 0.02 * Num_req_file

print(Num_para)
