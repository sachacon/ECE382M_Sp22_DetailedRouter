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
# Name: Xiuhao Zhang
# UT EID: xz7622
#######################################################################

from importlib.resources import path
from tkinter import Grid
from typing import List, Tuple
from xmlrpc.client import Boolean

import numpy as np

from .p2_routing_base import A_Star_Search_Base, GridAstarNode, PriorityQueue

__all__ = ["A_Star_Search"]

class A_Star_Search(A_Star_Search_Base):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self):
        """Initialize necessary data structures before starting solving the problem
        """
        # TODO initialize any auxiliary data structure you need

        self.visited_node_count = 0
        self.source_node = (self.pin_pos_x[0], self.pin_pos_y[0]) # the first node in all nodes as the source

        self.source_node_array = np.ndarray(shape = (1, 2))
        self.source_node_array[0][0] = self.pin_pos_x[0]
        self.source_node_array[0][1] = self.pin_pos_y[0]
        print("source_node_array:", self.source_node_array)

        self.sink_node_array = np.ndarray(shape = (self.n_pins - 1, 2)) # all other nodes as sinks
        for i in range(1, self.n_pins):
            self.sink_node_array[i - 1][0] = self.pin_pos_x[i]
            self.sink_node_array[i - 1][1] = self.pin_pos_y[i]
        print("sink_node_array:", self.sink_node_array)
        
        p1 = np.ndarray(shape = (1, 2))
        p1[0][0] = 0
        p1[0][1] = 8
        print(p1 in self.sink_node_array)

        # self.pin_positions = np.append(self.pin_positions, p1, axis = 0)
       
        # print(self._find_nearest_target_dist(p1, self.pin_positions))

        p2 = GridAstarNode()
        p2.pos = self.source_node
        print(self.compute_f_array(p2, p1))

        self.sink_node = (self.pin_pos_x[1], self.pin_pos_y[1])

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

    def compute_f(self, node: GridAstarNode) -> int: # compute f(n) = g(n) + h(n), node is (x, y) positions
        cost_f = self.compute_g(node) + self._find_manhattan_dist_to_target(node.pos, self.sink_node)
        return cost_f

    def compute_f_array(self, source: GridAstarNode, target: np.ndarray): # source is always a single node
        source_array = np.ndarray(shape = (1, 2))
        source_array[0][0] = source.pos[0]
        source_array[0][1] = source.pos[1]
        cost_f_array = self.compute_g(source) + self._find_nearest_target_dist(source_array, target)
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
    
    def find_neighbors(self, node: GridAstarNode): # find neighbors of current node of Class GridAstarNode
        neighbor_list = []
        if not(self.if_node_outside_grid((node.pos[0] - 1, node.pos[1]))): # left neighbor (x - 1, y) isn't outside grid
            if not(self.blockage_map[node.pos[1]][node.pos[0] - 1]): 
                left_neighbor = GridAstarNode()
                left_neighbor.pos = (node.pos[0] - 1, node.pos[1])
                neighbor_list.append(left_neighbor)
        if not(self.if_node_outside_grid((node.pos[0], node.pos[1] - 1))): # top neighbor (x, y - 1) isn't outside grid
            if not(self.blockage_map[node.pos[1] - 1][node.pos[0]]): 
                top_neighbor = GridAstarNode()
                top_neighbor.pos = (node.pos[0], node.pos[1] - 1)
                neighbor_list.append(top_neighbor)
        if not(self.if_node_outside_grid((node.pos[0] + 1, node.pos[1]))): # right neighbor (x + 1, y) isn't outside grid
            if not(self.blockage_map[node.pos[1]][node.pos[0] + 1]): 
                right_neighbor = GridAstarNode()
                right_neighbor.pos = (node.pos[0] + 1, node.pos[1])
                neighbor_list.append(right_neighbor)
        if not(self.if_node_outside_grid((node.pos[0], node.pos[1] + 1))): # bottom neighbor (x, y + 1) isn't outside grid
            if not(self.blockage_map[node.pos[1] + 1][node.pos[0]]):
                bottom_neighbor = GridAstarNode()
                bottom_neighbor.pos = (node.pos[0], node.pos[1] + 1)
                neighbor_list.append(bottom_neighbor)

        node.neighbors = neighbor_list


    def route_one_net(self) -> Tuple[List[Tuple[Tuple[int], Tuple[int]]], int, List[int], List[int]]:
        """route one multi-pin net using the A star search algorithm

        Return:
            path (List[Tuple[Tuple[int], Tuple[int]]]): the vector-wise routing path described by a list of (src, dst) position pairs
            wl (int): total wirelength of the routing path
            wl_list (List[int]): a list of wirelength of each routing path
            n_visited_list (List[int]): the number of visited nodes in the grid in each iteration
        """
        # TODO implement your A star search algorithm for one multi-pin net.
        # To make this method clean, you can extract subroutines as methods of this class
        # But do not override methods in the parent class
        # Please strictly follow the return type requirement.

        node_path = PriorityQueue() # open list for nodes to be visited, green
        node_record = {} # keep track of visited nodes, green node number

        source_node = GridAstarNode()
        source_node.pos = self.source_node
        source_node.cost_g = self.compute_g(source_node)
        # source_node.cost_f = self.compute_f(source_node)
        source_node.cost_f = self.compute_f_array(source_node, self.sink_node_array)
        source_node.bend_count = self.bend_count_number(source_node)
        source_node.visited = True ##

        node_path.put(source_node) # add source node to open list
        node_record[source_node.pos] = source_node
        
        sink_node = GridAstarNode()
        sink_node.pos = self.sink_node

        path = [] # closed list for nodes explored, red

        connect_net = np.ndarray(shape = (0, 2))

        while True:
            node = node_path.get() # get a priority node from queue based on f(n)

            if node.pos not in path:
                self.visited_node_count += 1

            path.append(node.pos) # node is explored, red
            connect_net = np.append(connect_net, [node.pos], axis = 0)

            if node.pos == sink_node.pos: # if popped out node is sink node, done
                sink_node = node
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
                        neighbor_copy.cost_f = self.compute_f(neighbor_copy)

                        if neighbor_copy.cost_g < node_record[neighbor.pos].cost_g: # if potentially a smaller cost_g
                            # update node
                            # 
                            node_record[neighbor.pos].parent = neighbor_copy.parent
                            node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                            node_record[neighbor.pos].cost_g = neighbor_copy.cost_g
                            node_record[neighbor.pos].cost_f = neighbor_copy.cost_f
                        else:
                            if neighbor_copy.cost_g == node_record[neighbor.pos].cost_g:
                                if neighbor_copy.bend_count < node_record[neighbor.pos].bend_count: # if potentially a smaller bend
                                    # update node
                                    #
                                    node_record[neighbor.pos].parent = neighbor_copy.parent
                                    node_record[neighbor.pos].bend_count = neighbor_copy.bend_count
                    else: # if neighbor.visited == False, didn't go into the queue before
                        neighbor.parent = node
                        neighbor.bend_count = self.bend_count_number(neighbor)
                        neighbor.cost_g = self.compute_g(neighbor)
                        neighbor.cost_f = self.compute_f(neighbor)
                        neighbor.visited = True
                        node_path.put(neighbor) # add neighbor to open list, green
                        node_record[neighbor.pos] = neighbor
        
        path_list = self._backtrack(sink_node)
        wirelength = len(path_list) - 1

        print(connect_net)

        return (self._merge_path(path_list), wirelength, [wirelength], [self.visited_node_count])