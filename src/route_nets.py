
import globals
import numpy as np
# from a_star import A_Star_Search 
import a_star
from read_inputs import * 

def route_nets():

    print("Routing Nets ...\n")
    print("grid_size = ", globals.grid_size)
    print("num_nets = ", globals.num_nets)
 
    blockages = []
    n_pins = None 
    n_blockages = None 
    pin_pos_x = [] 
    pin_pos_y = []

    # Horizontal for sample1
    # m2_blockage_pos_x = [] 
    # m2_blockage_pos_y = []
    # m2_blockages_size_x = []
    # m2_blockages_size_y = []   
   
    # Vertical for sample1
    # m3_blockage_pos_x = [] 
    # m3_blockage_pos_y = []
    # m3_blockages_size_x = []
    # m3_blockages_size_y = []

    m2_blockage_map = [] # V
    m3_blockage_map = [] # H
    m4_blockage_map = [] # V
    m5_blockage_map = [] # H
    m6_blockage_map = [] # V
    m7_blockage_map = [] # H
    m8_blockage_map = [] # V
    m9_blockage_map = [] # H

    # build blockage map

    # blockage_map_row = []
    # for w in range(globals.grid_size[0]): # width
    #     blockage_map_row.append(0) # no blockage

    for h in range(globals.grid_size[1]): # height
        # m2_blockage_map.append(blockage_map_row)
        # m3_blockage_map.append(blockage_map_row)
        # m4_blockage_map.append(blockage_map_row)
        # m5_blockage_map.append(blockage_map_row)
        # m6_blockage_map.append(blockage_map_row)
        # m7_blockage_map.append(blockage_map_row)
        # m8_blockage_map.append(blockage_map_row)
        # m9_blockage_map.append(blockage_map_row)

        m2_blockage_map.append([0] * globals.grid_size[0])
        m3_blockage_map.append([0] * globals.grid_size[0])
        m4_blockage_map.append([0] * globals.grid_size[0])
        m5_blockage_map.append([0] * globals.grid_size[0])
        m6_blockage_map.append([0] * globals.grid_size[0])
        m7_blockage_map.append([0] * globals.grid_size[0])
        m8_blockage_map.append([0] * globals.grid_size[0])
        m9_blockage_map.append([0] * globals.grid_size[0])

    # m2_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m3_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m4_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m5_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m6_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m7_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m8_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    # m9_blockage_map.append([[0] * globals.grid_size[0]] * globals.grid_size[1])
    
    blockage_map = {}
    blockage_map[2] = m2_blockage_map
    blockage_map[3] = m3_blockage_map
    blockage_map[4] = m4_blockage_map
    blockage_map[5] = m5_blockage_map
    blockage_map[6] = m6_blockage_map
    blockage_map[7] = m7_blockage_map
    blockage_map[8] = m8_blockage_map
    blockage_map[9] = m9_blockage_map


    for n in globals.nets.keys():

        print("net name = ", globals.nets[n].name)

        n_pins, pin_pos_x, pin_pos_y = format_net(globals.nets[n])
        if n_pins == 1:
             continue

        #if globals.nets[n].name != "net374":
        #    continue
        # print("net name = ", globals.nets[n].name)

        # print("n_pins = ", n_pins)
        # print("pin_pos_x = ", pin_pos_x)
        # print("pin_pos_y = ", pin_pos_y)  

        # A* search routing 
        # If a pin position is (0,0), net isn't formatted correclty, skip routing that net

        routing = a_star.A_Star_Search()
        routing.grid_size = list(globals.grid_size)
        routing.n_pins = n_pins
        # routing.n_blockages = 
        routing.pin_pos_x = pin_pos_x
        routing.pin_pos_y = pin_pos_y

        routing.m2_blockage_map = m2_blockage_map
        routing.m3_blockage_map = m3_blockage_map
        routing.m4_blockage_map = m4_blockage_map
        routing.m5_blockage_map = m5_blockage_map
        routing.m6_blockage_map = m6_blockage_map
        routing.m7_blockage_map = m7_blockage_map
        routing.m8_blockage_map = m8_blockage_map
        routing.m9_blockage_map = m9_blockage_map

        # print("block M2: ", blockage_map[2])
        # print("block M3: ", blockage_map[3])
        # print("block M4: ", blockage_map[4])
        # print("block M5: ", blockage_map[5])

        routing.net_name = n

        routing.initialize()
        #break
        (path_list, metal_list, wirelength, wirelength_list, visited_node_list) = routing.route_one_net()

        # update_blockages for metal
        for m in range(len(metal_list)):
            blockage_map[metal_list[m]][path_list[m][1]][path_list[m][0]] = 1
        
        # print("path list: ", path_list)
        # print("metal list: ", metal_list)
        
        # print("block M2: ", blockage_map[2])
        # print("block M3: ", blockage_map[3])
        # print("block M4: ", blockage_map[4])
        # print("block M5: ", blockage_map[5])

        # print(blockage_map[2] == blockage_map[3])

        # break
        
    return 

def isInsideGuideBox(net_name, layer, grid_coordinate):
    # Expect layer to be integer for ex. 1 or 4 
    # Expect grid_coordiante to be tuple for ex. (5, 5) or (21, 43) 

    print("\nnet name = ", net_name, "metal layer = ", layer, "grid_xy = ", grid_coordinate)

    guide_boxes = globals.net_guides[net_name].guide
    isInside = False 

    if(layer > 3):
        return True 

    for m in range(len(globals.metal_layers)):
        if(globals.metal_layers[m].layer == 1):
            m_layer = globals.metal_layers[m]
            break

    for i in range(len(guide_boxes)):
        tmp = guide_boxes[i]
        tmp_layer = tmp[-1]
        tmp_layer = tmp_layer.replace("Metal","")
        tmp_layer = int(tmp_layer)
       
        if(tmp_layer == layer):
            # Grid Coordinate Must Be Within This Box Range
            llx = int(tmp[0]) / 2000
            lly = int(tmp[1]) / 2000
            urx = int(tmp[2]) / 2000
            ury = int(tmp[3]) / 2000

            # Convert Grid Coordinate 
            if(m_layer.direction == "H"):
                grid_x = (m_layer.wrong_dir_start / 2000) + (grid_coordinate[0] *  (m_layer.wrong_dir_step/2000))
                grid_y = (m_layer.pref_dir_start / 2000) + (grid_coordinate[1] * (m_layer.pref_dir_step/2000))
            else: 
                grid_y = (m_layer.wrong_dir_start / 2000) + (grid_coordinate[1] *  (m_layer.wrong_dir_step/2000))
                grid_x = (m_layer.pref_dir_start / 2000) + (grid_coordinate[0] * (m_layer.pref_dir_step/2000))
     
            #print("grid_x = ", grid_x, " grid_y = ", grid_y)
            #print("llx = ", llx, " lly = ", lly, " urx = ", urx, " ury = ", ury)       
            # Grid Coordinate has to be inside Box Range
            # Has to be inside at least one guide box  
            if( (grid_x >= llx) and (grid_x <= urx) and (grid_y >= lly) and (grid_y <= ury) ):
                isInside = True
                break 
    
    #print("isInside = ", isInside)

    # return True
    return isInside 

 

# - Get grid track system beforehand  
# For each net:
# - Get net degree (out.*) READY 
#     For each pin:
#     - Get instance name (out.*)  
#     - Get pin name (new parser)
#     - Get instance lower left coordinate and orientation (out.*) READY
#     - For instance name get instance type (components.txt) READY
#     - Look up pin offset (lef.txt)
#     - Calulate location = LL coordiante + pin offset
#     - Find nearest point on grid of tracks
#     - Final Output is Coordinate System 

# TODO Some nets have are connected to pins and not inst 
 
def format_net(Net):

    #print("\nFormatting ", Net.name)

    n_pins = Net.degree
    pin_pos_x = []; pin_pos_y = [];
    pos_x = 0; pos_y = 0;
   
    # Get Metal Layer Information
    for m in range(len(globals.metal_layers)):
        if(globals.metal_layers[m].layer == 1):
            m1 = globals.metal_layers[m]
            break 

    pref_dir_start = m1.pref_dir_start / 2000
    pref_dir_step = m1.pref_dir_step / 2000
    pref_dir_num = m1.pref_dir_num
    wrong_dir_start = m1.wrong_dir_start / 2000
    wrong_dir_step = m1.wrong_dir_step / 2000
    wrong_dir_num = m1.wrong_dir_num

    if(m1.direction == 'H'):
        #print("Testing")
        grid_x = np.arange(start=wrong_dir_start, step=wrong_dir_step, stop=(wrong_dir_start + (wrong_dir_step*(wrong_dir_num))) ) 
        grid_y = np.arange(start=pref_dir_start, step=pref_dir_step, stop=(pref_dir_start + (pref_dir_step*(pref_dir_num) ) ) )
    else:
        grid_y = np.arange(start=wrong_dir_start, step=wrong_dir_step, stop=(wrong_dir_start + (wrong_dir_step*(wrong_dir_num))) ) 
        grid_x = np.arange(start=pref_dir_start, step=pref_dir_step, stop=(pref_dir_start + (pref_dir_step*(pref_dir_num) ) ) )

    #print("grid_x = ", grid_x)
    #print("grid_y = ", grid_y) 
       
    for n in range(n_pins):
      
        # Get Name of Pin
        pin_name = Net.pin_directions[n]
        #print("pin_name = ", pin_name)

        # Get Name of Instance for Pin  
        instance_name = Net.pin_instances[n]
        #print("instance_name = ", instance_name)
        #print("instances[instance_name].instance_type = ", globals.instances[instance_name].instance_type)
        #print("instances[instance_name].orientation = ", globals.instances[instance_name].orientation)
       
        # Get Coordinates and Orientation of Instance 
        instance = globals.instances[instance_name]
        instance_coordinates = (int(instance.width)/2000, int(instance.height)/2000)
        instance_orientation = instance.orientation
        #print("instance_coordinates = ", instance_coordinates)
        #print("instance_orientation = ", instance_orientation)

        # Get Type of Instance for Instance Name 
        inst_type = globals.instances[instance_name].instance_type
  
        #print("inst_type = ", inst_type)
        #print("instance_types keys = ", globals.instance_types.keys())
        instance_type = globals.instance_types[inst_type]
        #print("instance_type = ", inst_type)

        # Get Pin Shapes  
        for m in instance_type.pin_shapes.keys():
            if(m == pin_name):
                pin_shapes = instance_type.pin_shapes[m]
                break    
        #print("pin_shapes = ", pin_shapes)

        # Convert Pin Shapes
        found = 0 
        for m in range(len(pin_shapes)):
            _pin_shape = pin_shapes[m]
            _pin_shape = _pin_shape.replace(","," ")
            _pin_shape = _pin_shape.split()

            # Calculate Pin Shape Range
            if(instance_orientation == 'N'): 
                llx = (int(_pin_shape[0]) / 2000) + instance_coordinates[0]
                lly = (int(_pin_shape[1]) / 2000) + instance_coordinates[1]
                urx = (int(_pin_shape[2]) / 2000) + instance_coordinates[0]
                ury = (int(_pin_shape[3]) / 2000) + instance_coordinates[1]    
            else:  # FS Orientation
                llx = (instance_coordinates[0]) + (int(_pin_shape[0]) / 2000)                       # tlx
                ury = (instance_coordinates[1] + globals.FS_Height) - (int(_pin_shape[1]) / 2000)   # tly 
                urx = (instance_coordinates[0]) + (int(_pin_shape[2]) / 2000)                       # brx
                lly = (instance_coordinates[1] + globals.FS_Height) - (int(_pin_shape[3]) / 2000)   # bry
              

            #print("m = ", m, " llx = ", llx, " lly = ", lly, " urx = ", urx, " ury = ", ury)
            #print("len(grid_x)) = ", len(grid_x))
            #print("len(grid_y)) = ", len(grid_y))

            found = 0 
            for i in range(len(grid_x)):
                if((grid_x[i] >= llx) and (grid_x[i] <= urx)):
                    for j in range(len(grid_y)):
                        if((grid_y[j] >= lly) and (grid_y[j] <= ury)):
                            pos_x = i
                            pos_y = j
                            found = 1
                            #print("Found Track Point")
                        if(found == 1):
                            break
                if(found == 1):
                    break 
            if(found == 1):
                break
       
        if(found == 0):
            pos_x = (np.abs(grid_x - llx)).argmin()
            pos_y = (np.abs(grid_y - lly)).argmin()
        
        pin_pos_x.append(pos_x)
        pin_pos_y.append(pos_y)

    return n_pins, pin_pos_x, pin_pos_y
