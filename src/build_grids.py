from bst import * 
import numpy as np 



def build_M2_grid(m2_layer):
    """build M2 grid based on tracks, only for early test version,
       DO NOT use for final version"""
   
    # m2 layer is class object containing start, step, num of tracks 
    # in both preferred and wrong directions 
    
    m2_grid_size = (m2_layer.pref_num, m2_layer.wrong_num)
    

    return m2_grid_size  

def build_global_grid(num_layers, layers):
    """build global grid to store routing info"""

    # 2D table with dim of (# of layers, # of tracks nonpreferred direction)
    # For each track
    #    - 2 BSTs for storing vias
    #    - 1 interval BST for storing routed nets 

    x = []
    for i in range(num_layers):
        tracks = np.empty(layers[i].wrong_num, dtype=object)
        x.append(tracks)

    global_grid = np.array([np.array(xi) for xi in x])

    return global_grid  


def build_local_grid():


    return 


