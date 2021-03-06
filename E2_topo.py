# E2_topo, implement the SCN node engine in nodes constructed by Base_topo.py

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time

from E2_SCN import *
from Base_topo import *
from Global_init_var import *

def set_CAP():
	for ri in G.nodes(data=True):
		ri[1]['model'].comp_CAP = comp_CAP
		ri[1]['model'].cache_CAP = cache_CAP
		
# __main__

v_comp = 1e10

#Implement SCN node engine

R1 = SCN('R1','r',v_comp)
R2 = SCN('R2','r',v_comp)
R3 = SCN('R3','r',v_comp)
R4 = SCN('R4','r',v_comp)
R5 = SCN('R5','r',v_comp)
R6 = SCN('R6','r',v_comp)
R7 = SCN('R7','r',v_comp)
R8 = SCN('R8','r',v_comp)
R9 = SCN('R9','r',v_comp)
R10 = SCN('R10','r',v_comp)
R11 = SCN('R11','r',v_comp)
R12 = SCN('R12','r',v_comp)
R13 = SCN('R13','r',v_comp)
R14 = SCN('R14','r',v_comp)
R15 = SCN('R15','r',v_comp)
R16 = SCN('R16','r',v_comp)
R17 = SCN('R17','r',v_comp)
R18 = SCN('R18','r',v_comp)
R19 = SCN('R19','r',v_comp)
R20 = SCN('R20','r',v_comp)
R21 = SCN('R21','r',v_comp)
R22 = SCN('R22','r',v_comp)
R23 = SCN('R23','r',v_comp)
R24 = SCN('R24','r',v_comp)
R25 = SCN('R25','r',v_comp)
R26 = SCN('R26','r',v_comp)
R27 = SCN('R27','r',v_comp)
R28 = SCN('R28','r',v_comp)
R29 = SCN('R29','r',v_comp)
R30 = SCN('R30','r',v_comp)
R31 = SCN('R31','r',v_comp)
R32 = SCN('R32','r',v_comp)
R33 = SCN('R33','r',v_comp)
R34 = SCN('R34','r',v_comp)
R35 = SCN('R35','r',v_comp)
R36 = SCN('R36','r',v_comp)
R37 = SCN('R37','r',v_comp)
R38 = SCN('R38','r',v_comp)
R39 = SCN('R39','r',v_comp)
R40 = SCN('R40','r',v_comp)
R41 = SCN('R41','r',v_comp)
R42 = SCN('R42','r',v_comp)
R43 = SCN('R43','r',v_comp)
R44 = SCN('R44','r',v_comp)
R45 = SCN('R45','r',v_comp)
R46 = SCN('R46','r',v_comp)
R47 = SCN('R47','r',v_comp)
R48 = SCN('R48','r',v_comp)
R49 = SCN('R49','r',v_comp)
R50 = SCN('R50','r',v_comp)


H1 = SCN('H1','h',v_comp)
H2 = SCN('H2','h',v_comp)
H3 = SCN('H3','h',v_comp)
H4 = SCN('H4','h',v_comp)
H5 = SCN('H5','h',v_comp)
H6 = SCN('H6','h',v_comp)
H7 = SCN('H7','h',v_comp)
H8 = SCN('H8','h',v_comp)
H9 = SCN('H9','h',v_comp)
H10 = SCN('H10','h',v_comp)
H11 = SCN('H11','h',v_comp)
H12 = SCN('H12','h',v_comp)
H13 = SCN('H13','h',v_comp)
H14 = SCN('H14','h',v_comp)
H15 = SCN('H15','h',v_comp)
H16 = SCN('H16','h',v_comp)
H17 = SCN('H17','h',v_comp)
H18 = SCN('H18','h',v_comp)
H19 = SCN('H19','h',v_comp)
H20 = SCN('H20','h',v_comp)


P1 = SCN('P1','p',v_comp)
P2 = SCN('P2','p',v_comp)
P3 = SCN('P3','p',v_comp)
P4 = SCN('P4','p',v_comp)
P5 = SCN('P5','p',v_comp)
P6 = SCN('P6','p',v_comp)
P7 = SCN('P7','p',v_comp)
P8 = SCN('P8','p',v_comp)
P9 = SCN('P9','p',v_comp)
P10 = SCN('P10','p',v_comp)
P11 = SCN('P11','p',v_comp)
P12 = SCN('P12','p',v_comp)
P13 = SCN('P13','p',v_comp)
P14 = SCN('P14','p',v_comp)
P15 = SCN('P15','p',v_comp)
P16 = SCN('P16','p',v_comp)
P17 = SCN('P17','p',v_comp)
P18 = SCN('P18','p',v_comp)
P19 = SCN('P19','p',v_comp)
P20 = SCN('P20','p',v_comp)


G.nodes['R1']['model'] = R1
G.nodes['R2']['model'] = R2
G.nodes['R3']['model'] = R3
G.nodes['R4']['model'] = R4
G.nodes['R5']['model'] = R5
G.nodes['R6']['model'] = R6
G.nodes['R7']['model'] = R7
G.nodes['R8']['model'] = R8
G.nodes['R9']['model'] = R9
G.nodes['R10']['model'] = R10
G.nodes['R11']['model'] = R11
G.nodes['R12']['model'] = R12
G.nodes['R13']['model'] = R13
G.nodes['R14']['model'] = R14
G.nodes['R15']['model'] = R15
G.nodes['R16']['model'] = R16
G.nodes['R17']['model'] = R17
G.nodes['R18']['model'] = R18
G.nodes['R19']['model'] = R19
G.nodes['R20']['model'] = R20
G.nodes['R21']['model'] = R21
G.nodes['R22']['model'] = R22
G.nodes['R23']['model'] = R23
G.nodes['R24']['model'] = R24
G.nodes['R25']['model'] = R25
G.nodes['R26']['model'] = R26
G.nodes['R27']['model'] = R27
G.nodes['R28']['model'] = R28
G.nodes['R29']['model'] = R29
G.nodes['R30']['model'] = R30
G.nodes['R31']['model'] = R31
G.nodes['R32']['model'] = R32
G.nodes['R33']['model'] = R33
G.nodes['R34']['model'] = R34
G.nodes['R35']['model'] = R35
G.nodes['R36']['model'] = R36
G.nodes['R37']['model'] = R37
G.nodes['R38']['model'] = R38
G.nodes['R39']['model'] = R39
G.nodes['R40']['model'] = R40
G.nodes['R41']['model'] = R41
G.nodes['R42']['model'] = R42
G.nodes['R43']['model'] = R43
G.nodes['R44']['model'] = R44
G.nodes['R45']['model'] = R45
G.nodes['R46']['model'] = R46
G.nodes['R47']['model'] = R47
G.nodes['R48']['model'] = R48
G.nodes['R49']['model'] = R49
G.nodes['R50']['model'] = R50

G.nodes['H1']['model'] = H1
G.nodes['H2']['model'] = H2
G.nodes['H3']['model'] = H3
G.nodes['H4']['model'] = H4
G.nodes['H5']['model'] = H5
G.nodes['H6']['model'] = H6
G.nodes['H7']['model'] = H7
G.nodes['H8']['model'] = H8
G.nodes['H9']['model'] = H9
G.nodes['H10']['model'] = H10
G.nodes['H11']['model'] = H11
G.nodes['H12']['model'] = H12
G.nodes['H13']['model'] = H13
G.nodes['H14']['model'] = H14
G.nodes['H15']['model'] = H15
G.nodes['H16']['model'] = H16
G.nodes['H17']['model'] = H17
G.nodes['H18']['model'] = H18
G.nodes['H19']['model'] = H19
G.nodes['H20']['model'] = H20


G.nodes['P1']['model'] = P1
G.nodes['P2']['model'] = P2
G.nodes['P3']['model'] = P3
G.nodes['P4']['model'] = P4
G.nodes['P5']['model'] = P5
G.nodes['P6']['model'] = P6
G.nodes['P7']['model'] = P7
G.nodes['P8']['model'] = P8
G.nodes['P9']['model'] = P9
G.nodes['P10']['model'] = P10
G.nodes['P11']['model'] = P11
G.nodes['P12']['model'] = P12
G.nodes['P13']['model'] = P13
G.nodes['P14']['model'] = P14
G.nodes['P15']['model'] = P15
G.nodes['P16']['model'] = P16
G.nodes['P17']['model'] = P17
G.nodes['P18']['model'] = P18
G.nodes['P19']['model'] = P19
G.nodes['P20']['model'] = P20


node_set_r = ()
node_set_p = ()
node_set_h = ()
for ri in G.nodes(data=True):
	if ri[1]['model'].node_type == 'r':
		node_set_r += (ri[1]['model'].label,)
	elif ri[1]['model'].node_type == 'p':
		node_set_p += (ri[1]['model'].label,)
	else:
		node_set_h += (ri[1]['model'].label,)

set_CAP()
		
#nx.draw(G)
#plt.show()