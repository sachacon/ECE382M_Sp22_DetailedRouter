'''
Description:
Author: Jiaqi Gu (jqgu@utexas.edu)
Date: 2022-03-07 16:42:12
LastEditors: Jiaqi Gu (jqgu@utexas.edu)
LastEditTime: 2022-03-08 16:04:28
'''
#######################################################################
# Implementation of A Star Search
# You need to implement initialize() and route_one_net()
# All codes should be inside A Star Search class
# Name: Xiuhao Zhang, Sergio Chacon
#######################################################################

import dis
#from importlib.resources import path
#from tkinter import Grid
#from turtle import hideturtle
from typing import List, Tuple
from xmlrpc.client import Boolean

import numpy as np

# from route_nets import route_nets
import route_nets

# from .p2_routing_base import A_Star_Search_Base, GridAstarNode, PriorityQueue
from p2_routing_base import A_Star_Search_Base, GridAstarNode, PriorityQueue


__all__ = ["A_Star_Search"]

class A_Star_Search(A_Star_Search_Base):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self):
        """Initialize necessary data structures before starting solving the problem
        """
        # TODO initialize any auxiliary data structure you need

        self.source_node = (self.pin_pos_x[0], self.pin_pos_y[0]) # the first node in all nodes as the source

        self.source_node_array = np.ndarray(shape = (1, 2))
        self.source_node_array[0][0] = self.pin_pos_x[0]
        self.source_node_array[0][1] = self.pin_pos_y[0]
        # print("source_node_array:", self.source_node_array)

        self.sink_node_array = np.ndarray(shape = (self.n_pins - 1, 2)) # all other nodes as sinks
        for i in range(1, self.n_pins):
            self.sink_node_array[i - 1][0] = self.pin_pos_x[i]
            self.sink_node_array[i - 1][1] = self.pin_pos_y[i]
        self.sink_node_array_list = self.sink_node_array.tolist()
        # print(self.sink_node_array_list)
        #print("sink_node_array:", self.sink_node_array)

        self.sink_node = (self.pin_pos_x[1], self.pin_pos_y[1]) # for two pins only

        #print("source: ", self.source_node)
        #print("sink: ", self.sink_node)

    def if_node_outside_grid(self, node: Tuple[int]) -> bool: # check if the node is outside the grid map, node is (x, y) positions
        if node[0] < 0: # if outside the left border, x
            return True
        elif node[0] >= self.grid_size[0]: # if outside the right border, x
            return True
        elif node[1] < 0: # if outside the bottom border, y
            return True
        elif node[1] >= self.grid_size[1]: # if outside the top border, y
            return True
        return False
    
    def compute_g(self, node: GridAstarNode) -> int: # compute g using Manhattan distance, node is (x, y) positions
        return len(self._backtrack(node)) - 1

    # def compute_f(self, node: GridAstarNode) -> int: # compute f(n) = g(n) + h(n), node is (x, y) positions, for two pins only
    #     cost_f = self.compute_g(node) + self._find_manhattan_dist_to_target(node.pos, self.sink_node)
    #     return cost_f

    def compute_f_array(self, source: GridAstarNode, target: np.ndarray): # source is always a single node
        source_array = np.ndarray(shape = (1, 2))
        source_array[0][0] = source.pos[0]
        source_array[0][1] = source.pos[1]
        cost_f_array = self.compute_g(source) + 10 * self._find_nearest_target_dist(source_array, target)
        return cost_f_array
    
    def bend_count_number(self, node: GridAstarNode) -> int: # count bend numbers so far after propagation
        if node.parent is None: # no parent, must be the source node, no bending
            count = 1
        else: # has parent node
            if self._has_bend(node.parent, node): # if has bending
                count = node.parent.bend_count + 1
            else: # if no bending
                count = node.parent.bend_count
        return count
    
    def find_neighbors(self, node: GridAstarNode): # find neighbors of current node of Class GridAstarNode, considering bonding box
        # left, right -> horizontal: m3, 5, 7, 9 > m2, 4, 6, 8, for horizontal routing, metal 3, 5, 7, 9 have higher priority over metal 2, 4, 6, 8
        # top, bottom -> vertical: m2, 4, 6, 8 > m3, 5, 7, 9, for vertical routing, metal 2, 4, 6, 8 have higher priority over metal 3, 5, 7, 9
        neighbor_list = []
        if not(self.if_node_outside_grid((node.pos[0] - 1, node.pos[1]))): # left neighbor (x - 1, y) isn't outside grid
            if not(self.m3_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 3, (node.pos[0] - 1, node.pos[1])): # no metal 3 blockage and is inside metal 3 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 3
                neighbor_list.append(left_neighbor)
            elif not(self.m5_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 5, (node.pos[0] - 1, node.pos[1])): # no metal 5 blockage and is inside metal 5 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 5
                neighbor_list.append(left_neighbor)
            elif not(self.m7_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 7, (node.pos[0] - 1, node.pos[1])): # no metal 7 blockage and is inside metal 7 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 7
                neighbor_list.append(left_neighbor)
            elif not(self.m9_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 9, (node.pos[0] - 1, node.pos[1])): # no metal 9 blockage and is inside metal 9 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 9
                neighbor_list.append(left_neighbor)
            elif not(self.m2_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 2, (node.pos[0] - 1, node.pos[1])): # no metal 2 blockage and is inside metal 2 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 2
                neighbor_list.append(left_neighbor)
            elif not(self.m4_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 4, (node.pos[0] - 1, node.pos[1])): # no metal 4 blockage and is inside metal 4 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 4
                neighbor_list.append(left_neighbor)
            elif not(self.m6_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 6, (node.pos[0] - 1, node.pos[1])): # no metal 6 blockage and is inside metal 6 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 6
                neighbor_list.append(left_neighbor)
            elif not(self.m8_blockage_map[node.pos[1]][node.pos[0] - 1]) and route_nets.isInsideGuideBox(self.net_name, 8, (node.pos[0] - 1, node.pos[1])): # no metal 8 blockage and is inside metal 8 bonding box 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 8
                neighbor_list.append(left_neighbor)
            elif not(self.m3_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 3 blockage 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 3
                neighbor_list.append(left_neighbor)
            elif not(self.m5_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 5 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 5
                neighbor_list.append(left_neighbor)
            elif not(self.m7_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 7 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 7
                neighbor_list.append(left_neighbor)
            elif not(self.m9_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 9 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 9
                neighbor_list.append(left_neighbor)
            elif not(self.m2_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 2 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 2
                neighbor_list.append(left_neighbor)
            elif not(self.m4_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 4 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 4
                neighbor_list.append(left_neighbor)
            elif not(self.m6_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 6 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 6
                neighbor_list.append(left_neighbor)
            elif not(self.m8_blockage_map[node.pos[1]][node.pos[0] - 1]): # no metal 8 blockage
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                left_neighbor.layer = 8
                neighbor_list.append(left_neighbor)
        if not(self.if_node_outside_grid((node.pos[0], node.pos[1] - 1))): # top neighbor (x, y - 1) isn't outside grid
            if not(self.m2_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 2, (node.pos[0], node.pos[1] - 1)): # no metal 2 blockage and is inside metal 2 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 2
                neighbor_list.append(top_neighbor)
            elif not(self.m4_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 4, (node.pos[0], node.pos[1] - 1)): # no metal 4 blockage and is inside metal 4 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 4
                neighbor_list.append(top_neighbor)
            elif not(self.m6_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 6, (node.pos[0], node.pos[1] - 1)): # no metal 6 blockage and is inside metal 6 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 6
                neighbor_list.append(top_neighbor)
            elif not(self.m8_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 8, (node.pos[0], node.pos[1] - 1)): # no metal 8 blockage and is inside metal 8 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 8
                neighbor_list.append(top_neighbor)
            elif not(self.m3_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 3, (node.pos[0], node.pos[1] - 1)): # no metal 3 blockage and is inside metal 3 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 3
                neighbor_list.append(top_neighbor)
            elif not(self.m5_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 5, (node.pos[0], node.pos[1] - 1)): # no metal 5 blockage and is inside metal 5 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 5
                neighbor_list.append(top_neighbor)
            elif not(self.m7_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 7, (node.pos[0], node.pos[1] - 1)): # no metal 7 blockage and is inside metal 7 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 7
                neighbor_list.append(top_neighbor)
            elif not(self.m9_blockage_map[node.pos[1] - 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 9, (node.pos[0], node.pos[1] - 1)): # no metal 9 blockage and is inside metal 9 bonding box
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 9
                neighbor_list.append(top_neighbor)
            elif not(self.m2_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 2 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 2
                neighbor_list.append(top_neighbor)
            elif not(self.m4_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 4 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 4
                neighbor_list.append(top_neighbor)
            elif not(self.m6_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 6 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 6
                neighbor_list.append(top_neighbor)
            elif not(self.m8_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 8 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 8
                neighbor_list.append(top_neighbor)
            elif not(self.m3_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 3 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 3
                neighbor_list.append(top_neighbor)
            elif not(self.m5_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 5 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 5
                neighbor_list.append(top_neighbor)
            elif not(self.m7_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 7 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 7
                neighbor_list.append(top_neighbor)
            elif not(self.m9_blockage_map[node.pos[1] - 1][node.pos[0]]): # no metal 9 blockage
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                top_neighbor.layer = 9
                neighbor_list.append(top_neighbor)
        if not(self.if_node_outside_grid((node.pos[0] + 1, node.pos[1]))): # right neighbor (x + 1, y) isn't outside grid
            if not(self.m3_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 3, (node.pos[0] + 1, node.pos[1])): # no metal 3 blockage and is inside metal 3 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 3
                neighbor_list.append(right_neighbor)
            elif not(self.m5_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 5, (node.pos[0] + 1, node.pos[1])): # no metal 5 blockage and is inside metal 5 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 5
                neighbor_list.append(right_neighbor)
            elif not(self.m7_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 7, (node.pos[0] + 1, node.pos[1])): # no metal 7 blockage and is inside metal 7 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 7
                neighbor_list.append(right_neighbor)
            elif not(self.m9_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 9, (node.pos[0] + 1, node.pos[1])): # no metal 9 blockage and is inside metal 9 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 9
                neighbor_list.append(right_neighbor)
            elif not(self.m2_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 2, (node.pos[0] + 1, node.pos[1])): # no metal 2 blockage and is inside metal 2 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 2
                neighbor_list.append(right_neighbor)
            elif not(self.m4_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 4, (node.pos[0] + 1, node.pos[1])): # no metal 4 blockage and is inside metal 4 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 4
                neighbor_list.append(right_neighbor)
            elif not(self.m6_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 6, (node.pos[0] + 1, node.pos[1])): # no metal 6 blockage and is inside metal 6 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 6
                neighbor_list.append(right_neighbor)
            elif not(self.m8_blockage_map[node.pos[1]][node.pos[0] + 1]) and route_nets.isInsideGuideBox(self.net_name, 8, (node.pos[0] + 1, node.pos[1])): # no metal 8 blockage and is inside metal 8 bonding box
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 8
                neighbor_list.append(right_neighbor)
            elif not(self.m3_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 3 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 3
                neighbor_list.append(right_neighbor)
            elif not(self.m5_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 5 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 5
                neighbor_list.append(right_neighbor)
            elif not(self.m7_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 7 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 7
                neighbor_list.append(right_neighbor)
            elif not(self.m9_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 9 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 9
                neighbor_list.append(right_neighbor)
            elif not(self.m2_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 2 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 2
                neighbor_list.append(right_neighbor)
            elif not(self.m4_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 4 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 4
                neighbor_list.append(right_neighbor)
            elif not(self.m6_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 6 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 6
                neighbor_list.append(right_neighbor)
            elif not(self.m8_blockage_map[node.pos[1]][node.pos[0] + 1]): # no metal 8 blockage
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                right_neighbor.layer = 8
                neighbor_list.append(right_neighbor)
        if not(self.if_node_outside_grid((node.pos[0], node.pos[1] + 1))): # bottom neighbor (x, y + 1) isn't outside grid
            if not(self.m2_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 2, (node.pos[0], node.pos[1] + 1)): # no metal 2 blockage and is inside metal 2 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 2
                neighbor_list.append(bottom_neighbor)
            elif not(self.m4_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 4, (node.pos[0], node.pos[1] + 1)): # no metal 4 blockage and is inside metal 4 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 4
                neighbor_list.append(bottom_neighbor)
            elif not(self.m6_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 6, (node.pos[0], node.pos[1] + 1)): # no metal 6 blockage and is inside metal 6 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 6
                neighbor_list.append(bottom_neighbor)
            elif not(self.m8_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 8, (node.pos[0], node.pos[1] + 1)): # no metal 8 blockage and is inside metal 8 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 8
                neighbor_list.append(bottom_neighbor)
            elif not(self.m3_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 3, (node.pos[0], node.pos[1] + 1)): # no metal 3 blockage and is inside metal 3 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 3
                neighbor_list.append(bottom_neighbor)
            elif not(self.m5_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 5, (node.pos[0], node.pos[1] + 1)): # no metal 5 blockage and is inside metal 5 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 5
                neighbor_list.append(bottom_neighbor)
            elif not(self.m7_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 7, (node.pos[0], node.pos[1] + 1)): # no metal 7 blockage and is inside metal 7 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 7
                neighbor_list.append(bottom_neighbor)
            elif not(self.m9_blockage_map[node.pos[1] + 1][node.pos[0]]) and route_nets.isInsideGuideBox(self.net_name, 9, (node.pos[0], node.pos[1] + 1)): # no metal 9 blockage and is inside metal 9 bonding box
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 9
                neighbor_list.append(bottom_neighbor)
            elif not(self.m2_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 2 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 2
                neighbor_list.append(bottom_neighbor)
            elif not(self.m4_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 4 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 4
                neighbor_list.append(bottom_neighbor)
            elif not(self.m6_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 6 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 6
                neighbor_list.append(bottom_neighbor)
            elif not(self.m8_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 8 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 8
                neighbor_list.append(bottom_neighbor)
            elif not(self.m3_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 3 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 3
                neighbor_list.append(bottom_neighbor)
            elif not(self.m5_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 5 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 5
                neighbor_list.append(bottom_neighbor)
            elif not(self.m7_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 7 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 7
                neighbor_list.append(bottom_neighbor)
            elif not(self.m9_blockage_map[node.pos[1] + 1][node.pos[0]]): # no metal 9 blockage
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                bottom_neighbor.layer = 9
                neighbor_list.append(bottom_neighbor)

        node.neighbors = neighbor_list


    def route_one_net(self) -> Tuple[List[Tuple[int]], List[int], int, int, List[int], List[int]]:
        """route one multi-pin net using the A star search algorithm

        Return:
            # path (List[Tuple[Tuple[int], Tuple[int]]]): the vector-wise routing path described by a list of (src, dst) position pairs
            path (List[Tuple[int]]): the point-wise routing path described by a list of node positions
            metal_layer (List[int]): the point-wise metal layer of each node
            wl (int): total wirelength of the routing path
            via count (int): total via count
            wl_list (List[int]): a list of wirelength of each routing path
            n_visited_list (List[int]): the number of visited nodes in the grid in each iteration
        """
        # TODO implement your A star search algorithm for one multi-pin net.
        # To make this method clean, you can extract subroutines as methods of this class
        # But do not override methods in the parent class
        # Please strictly follow the return type requirement.
        
        sink_node = GridAstarNode() # initialize class
        path_list = [] # record path to output
        metal_list = [] # record metal layer to output
        sink_node_array_as_list = self.sink_node_array.tolist()
        wirelength_list = [] # output
        visited_node_list = [] # output
        connect_net = np.ndarray(shape = (0, 2)) # record routed paths
        
        counter = 0

        via_list = []

        for j in range(0, self.n_pins - 1):
            node_path = PriorityQueue() # open list for nodes to be visited, green
            node_record = {} # keep track of visited nodes, green node number
            path = [] # closed list for nodes explored, red
            visited_node = 0

            trackmetal = []

           # print("j: ", j)

            # if source_node.pos in sink_node_array_as_list:
            #     continue

            if j == 0: # initial source node
                source_node = GridAstarNode()
                source_node.pos = self.source_node
                source_node.cost_g = self.compute_g(source_node)
                source_node.cost_f = self.compute_f_array(source_node, self.sink_node_array)
                source_node.bend_count = self.bend_count_number(source_node)
                source_node.visited = True ##

                node_path.put(source_node) # add source node to open list
                node_record[source_node.pos] = source_node

                while True:
                    node = node_path.get() # get a priority node from queue based on f(n)

                    # counter += 1
                    
                    # if (counter % 200 == 0):
                    #     print("counter: ", counter)

                    #if self.net_name == "net374":
                    #    print("1st node pos: ", node.pos, "1st node metal: ", node.layer)

                    #print("1st node pos: ", node.pos, "1st node metal: ", node.layer)

                    if node.pos not in path:
                        visited_node += 1

                    path.append(node.pos) # node is explored, red

                    node_pos_as_list = list(node.pos) # node position: tuple to list
                    
                    if node_pos_as_list in sink_node_array_as_list: # check if this node is in the sink array -> if this node is one of the sink nodes
                        # print("sink node:", node_pos_as_list)
                        # print("backtrack:", self._backtrack(node))
                        self.sink_node_array = np.delete(self.sink_node_array, sink_node_array_as_list.index(node_pos_as_list), axis = 0) # remove the connected sink node from sink node arrays

                        sink_node = node
                        tracknode = self._backtrack(sink_node) # connected path from source to sink

                        for k in range(0, len(tracknode)):
                            connect_net = np.append(connect_net, [list(tracknode[k])], axis = 0) # make connected net
                            trackmetal.append(node_record[tracknode[k]].layer) # record metal layer of the node

                        break

                    self.find_neighbors(node) # find neighbors of the current node
                    for i in range(0, len(node.neighbors)): # for each neighbor
                        neighbor = node.neighbors[i]

                        if neighbor.pos in path: # if the neighbor is in the closed list, meaning the neighbor has been explored, red
                            continue # move onto the next neighbor
                        else: # if the neighbor isn't in the closd list, green
                            if neighbor.pos in node_record: # if neighbor.visited == True, went into the queue before
                                neighbor_copy = GridAstarNode() # make a temporary copy of the current neighbor node
                                neighbor_copy.pos = neighbor.pos
                                neighbor_copy.visited = node_record[neighbor.pos].visited
                                neighbor_copy.neighbors = node_record[neighbor.pos].neighbors
                                neighbor_copy.parent = node
                                neighbor_copy.bend_count = self.bend_count_number(neighbor_copy)
                                neighbor_copy.cost_g = self.compute_g(neighbor_copy)
                                neighbor_copy.cost_f = self.compute_f_array(neighbor_copy, self.sink_node_array)
                                neighbor_copy.layer = neighbor.layer

                                if neighbor_copy.cost_g < node_record[neighbor.pos].cost_g: # if potentially a smaller cost_g
                                    # update node
                                    # 
                                    node_record[neighbor.pos].parent = neighbor_copy.parent
                                    node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                                    node_record[neighbor.pos].cost_g = neighbor_copy.cost_g
                                    node_record[neighbor.pos].cost_f = neighbor_copy.cost_f
                                    node_record[neighbor.pos].layer = neighbor_copy.layer
                                else:
                                    if neighbor_copy.cost_g == node_record[neighbor.pos].cost_g:
                                        if neighbor_copy.bend_count < node_record[neighbor.pos].bend_count: # if potentially a smaller bend
                                            # update node
                                            #
                                            node_record[neighbor.pos].parent = neighbor_copy.parent
                                            node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                                            node_record[neighbor.pos].layer = neighbor_copy.layer
                            else: # if neighbor.visited == False, didn't go into the queue before
                                neighbor.parent = node
                                neighbor.bend_count = self.bend_count_number(neighbor)
                                neighbor.cost_g = self.compute_g(neighbor)
                                # neighbor.cost_f = self.compute_f(neighbor)
                                neighbor.cost_f = self.compute_f_array(neighbor, self.sink_node_array)
                                neighbor.visited = True
                                node_path.put(neighbor) # add neighbor to open list, green
                                node_record[neighbor.pos] = neighbor

            else: # sink nodes as the source to connect to connected net
                # find the closest sink node to routed path
                distance_sink_to_connect_net = []
                left_sink_list = self.sink_node_array.tolist()
                # print("left sink list:", left_sink_list)
                for i in range(len(left_sink_list)):
                    node = GridAstarNode()
                    node.pos = (int(left_sink_list[i][0]), int(left_sink_list[i][1]))
                    distance_sink_to_connect_net.append(self.compute_f_array(node, connect_net)[0])
                # print("left sink distance:", distance_sink_to_connect_net)
                close_node = distance_sink_to_connect_net.index(min(distance_sink_to_connect_net))

                source_node = GridAstarNode()
                source_node.pos = (int(self.sink_node_array[close_node][0]), int(self.sink_node_array[close_node][1]))
                # print("? node pos:", source_node.pos)
                source_node.cost_g = self.compute_g(source_node)
                source_node.cost_f = self.compute_f_array(source_node, connect_net)
                source_node.bend_count = self.bend_count_number(source_node)
                source_node.visited = True

                node_path.put(source_node) # add source node to open list
                node_record[source_node.pos] = source_node

                while True:
                    node = node_path.get() # get a priority node from queue based on f(n)

                    # counter += 1
                    
                    # if (counter % 200 == 0):
                    #     print("counter: ", counter)

                    #if self.net_name == "net374":
                    #    print("2nd node pos: ", node.pos, "2nd node metal: ", node.layer)
                    #    print("queue length: ", node_path.qsize())

                    #print("2nd node pos: ", node.pos, "2nd node metal: ", node.layer)

                    if node.pos not in path:
                        visited_node += 1

                    path.append(node.pos) # node is explored, red

                    node_pos_as_list = list(node.pos) # node position: tuple to list

                    # print("connect net:", connect_net.tolist())
                    if node_pos_as_list in connect_net.tolist(): # check if this node is in the connect net -> if source node has been connected to the net
                        # print("sink node:", node_pos_as_list)
                        # print("backtrack:", self._backtrack(node))
                        self.sink_node_array = np.delete(self.sink_node_array, close_node, axis = 0) # remove the connected sink node from sink node arrays

                        sink_node = node
                        tracknode = self._backtrack(sink_node) # connected path from source to sink

                        for k in range(0, len(tracknode)):
                            trackmetal.append(node_record[tracknode[k]].layer) # record metal layer of the node

                        for k in range(0, len(self._backtrack(sink_node)) - 1):
                            connect_net = np.append(connect_net, [list(tracknode[k])], axis = 0) # make connected net
                        
                        break
                    #if node.pos == (1464, 580):
                    #        print('hi')

                    self.find_neighbors(node) # find neighbors of the current node
                    for i in range(0, len(node.neighbors)): # for each neighbor
                        neighbor = node.neighbors[i]
                         
                        #if node.pos == (1464, 580):
                        #        print("neighbor pos: ", node.neighbors[i].pos)

                        if neighbor.pos in path: # if the neighbor is in the closed list, meaning the neighbor has been explored, red
                            continue # move onto the next neighbor
                        else: # if the neighbor isn't in the closd list, green
                            if neighbor.pos in node_record: # if neighbor.visited == True, went into the queue before
                                neighbor_copy = GridAstarNode() # make a temporary copy of the current neighbor node
                                neighbor_copy.pos = neighbor.pos
                                neighbor_copy.visited = node_record[neighbor.pos].visited
                                neighbor_copy.neighbors = node_record[neighbor.pos].neighbors
                                neighbor_copy.parent = node
                                neighbor_copy.bend_count = self.bend_count_number(neighbor_copy)
                                neighbor_copy.cost_g = self.compute_g(neighbor_copy)
                                neighbor_copy.cost_f = self.compute_f_array(neighbor_copy, connect_net)
                                neighbor_copy.layer = neighbor.layer

                                if neighbor_copy.cost_g < node_record[neighbor.pos].cost_g: # if potentially a smaller cost_g
                                    # update node
                                    # 
                                    node_record[neighbor.pos].parent = neighbor_copy.parent
                                    node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                                    node_record[neighbor.pos].cost_g = neighbor_copy.cost_g
                                    node_record[neighbor.pos].cost_f = neighbor_copy.cost_f
                                    node_record[neighbor.pos].layer = neighbor_copy.layer
                                else:
                                    if neighbor_copy.cost_g == node_record[neighbor.pos].cost_g:
                                        if neighbor_copy.bend_count < node_record[neighbor.pos].bend_count: # if potentially a smaller bend
                                            # update node
                                            #
                                            node_record[neighbor.pos].parent = neighbor_copy.parent
                                            node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                                            node_record[neighbor.pos].layer = neighbor_copy.layer
                            else: # if neighbor.visited == False, didn't go into the queue before
                                neighbor.parent = node
                                neighbor.bend_count = self.bend_count_number(neighbor)
                                neighbor.cost_g = self.compute_g(neighbor)
                                neighbor.cost_f = self.compute_f_array(neighbor, connect_net)
                                neighbor.visited = True
                                node_path.put(neighbor) # add neighbor to open list, green
                                node_record[neighbor.pos] = neighbor
            
            # path_list as point_wise output

            # print("path: ", tracknode, len(tracknode))
            # print("metal: ", trackmetal, len(trackmetal))

            if j == 0:
                for k in range(len(tracknode)):
                    path_list.append(tracknode[k])
                    metal_list.append(trackmetal[k])
                    if k == 0:
                        via_list.append(node_record[tracknode[k]].layer - 1) # source node layer - m1
                    else:
                        via_list.append(abs(node_record[tracknode[k]].layer - node_record[tracknode[k]].parent.layer))
                wirelength_list.append(len(tracknode) - 1)
            else:
                for k in range(len(tracknode)):
                    if k == 0:
                        via_list.append(node_record[tracknode[k]].layer - 1) # sink node layer - m1
                    else:
                        via_list.append(abs(node_record[tracknode[k]].layer - node_record[tracknode[k]].parent.layer))

                tracknode.reverse()
                trackmetal.reverse()

                for k in range(len(tracknode)):
                    path_list.append(tracknode[k])
                    metal_list.append(trackmetal[k])
                wirelength_list.append(len(tracknode) - 1)

            # if j != 0:
            #     tracknode.reverse()

            # for k in range(len(self._merge_path(tracknode))):
            #     path_list.append(self._merge_path(tracknode)[k]) # path_list as vector-wise output
            # wirelength_list.append(len(tracknode) - 1)

            # print("tracknode: ", tracknode)
            # print("merge tracknode: ", self._merge_path(tracknode))
            

            visited_node_list.append(visited_node)

        # wirelength = len(path_list) - 1 # point-wise
        wirelength = sum(wirelength_list) # vector-wise
        via_count = sum(via_list)

        # print(connect_net)
        # print("path list:", path_list)
        # print("merge path:", self._merge_path(path_list))

        # return (self._merge_path(path_list), wirelength, wirelength_list, visited_node_list) # point-wise
        # return (path_list, wirelength, wirelength_list, visited_node_list) # vector-wise
        return (path_list, metal_list, wirelength, via_count, wirelength_list, visited_node_list) # point-wise
