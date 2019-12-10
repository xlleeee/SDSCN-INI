# base_topo_3, Construct node topology to identify the connection relationships among nodes.

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import time

# __main__

v_trans = 3e8

#Construct Topology

G = nx.Graph()
# router: 50
G.add_node('R1')
G.add_node('R2')
G.add_node('R3')
G.add_node('R4')
G.add_node('R5')
G.add_node('R6')
G.add_node('R7')
G.add_node('R8')
G.add_node('R9')
G.add_node('R10')
G.add_node('R11')
G.add_node('R12')
G.add_node('R13')
G.add_node('R14')
G.add_node('R15')
G.add_node('R16')
G.add_node('R17')
G.add_node('R18')
G.add_node('R19')
G.add_node('R20')
G.add_node('R21')
G.add_node('R22')
G.add_node('R23')
G.add_node('R24')
G.add_node('R25')
G.add_node('R26')
G.add_node('R27')
G.add_node('R28')
G.add_node('R29')
G.add_node('R30')
G.add_node('R31')
G.add_node('R32')
G.add_node('R33')
G.add_node('R34')
G.add_node('R35')
G.add_node('R36')
G.add_node('R37')
G.add_node('R38')
G.add_node('R39')
G.add_node('R40')
G.add_node('R41')
G.add_node('R42')
G.add_node('R43')
G.add_node('R44')
G.add_node('R45')
G.add_node('R46')
G.add_node('R47')
G.add_node('R48')
G.add_node('R49')
G.add_node('R50')


# hosts: 
G.add_node('H1')
G.add_node('H2')
G.add_node('H3')
G.add_node('H4')
G.add_node('H5')
G.add_node('H6')
G.add_node('H7')
G.add_node('H8')
G.add_node('H9')
G.add_node('H10')
G.add_node('H11')
G.add_node('H12')
G.add_node('H13')
G.add_node('H14')
G.add_node('H15')
G.add_node('H16')
G.add_node('H17')
G.add_node('H18')
G.add_node('H19')
G.add_node('H20')

# parameter nodes:
G.add_node('P1')
G.add_node('P2')
G.add_node('P3')
G.add_node('P4')
G.add_node('P5')
G.add_node('P6')
G.add_node('P7')
G.add_node('P8')
G.add_node('P9')
G.add_node('P10')
G.add_node('P11')
G.add_node('P12')
G.add_node('P13')
G.add_node('P14')
G.add_node('P15')
G.add_node('P16')
G.add_node('P17')
G.add_node('P18')
G.add_node('P19')
G.add_node('P20')


# add links among routers

G.add_edges_from([('R1','R44'),('R2','R46'),('R3','R48'),('R4','R41'),('R5','R42'),('R6','R50'),('R7','R50'),('R8','R24'),('R9','R38'),('R10','R32'),('R11','R39'),('R12','R48'),('R13','R49'),('R14','R49'),('R15','R35'),('R16','R33'),('R17','R23'),('R18','R30'),('R19','R29'),('R20','R37')],weight=v_trans)

G.add_edges_from([('R21','R22'),('R21','R50'),('R22','R49'),('R23','R48'),('R24','R34'),('R25','R47'),('R25','R50'),('R26','R38'),('R26','R46'),('R27','R38'),('R27','R40'),('R28','R29'),('R28','R33'),('R30','R45'),('R31','R43'),('R31','R45')],weight=v_trans)

G.add_edges_from([('R32','R37'),('R32','R39'),('R33','R49'),('R34','R47'),('R34','R50'),('R35','R40'),('R35','R49'),('R36','R42'),('R36','R46'),('R36','R47'),('R37','R43'),('R39','R48'),('R40','R47'),('R41','R44'),('R41','R49'),('R42','R43')],weight=v_trans)

G.add_edges_from([('R43','R50'),('R44','R45'),('R44','R47'),('R45','R47')],weight=v_trans)

G.add_edges_from([('R46','R48'),('R46','R50')],weight=v_trans)

G.add_edges_from([('R48','R50')],weight=v_trans)

G.add_edges_from([('R49','R50')],weight=v_trans)

# add links between routers and hosts

G.add_edges_from([('R1','H1'),('R2','H2'),('R3','H3'),('R4','H4'),('R5','H5'),('R6','H6'),('R7','H7'),('R8','H8'),('R9','H9'),('R10','H10'),('R11','H11'),('R12','H12'),('R13','H13'),('R14','H14'),('R15','H15'),('R16','H16'),('R17','H17'),('R18','H18'),('R19','H19'),('R20','H20')],weight=v_trans)

# add links between routers and parameter nodes

G.add_edges_from([('R1','P1'),('R2','P2'),('R3','P3'),('R4','P4'),('R5','P5'),('R6','P6'),('R7','P7'),('R8','P8'),('R9','P9'),('R10','P10'),('R11','P11'),('R12','P12'),('R13','P13'),('R14','P14'),('R15','P15'),('R16','P16'),('R17','P17'),('R18','P18'),('R19','P19'),('R20','P20')],weight=v_trans)


#nx.draw(G)
#plt.show()