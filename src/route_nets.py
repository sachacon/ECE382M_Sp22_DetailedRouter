
import globals
import numpy as np
#from eid_xz7622 import A_Star_Search 
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
    blockage_pos_x = [] 
    blockage_pos_y = []
    blockages_size_x = []
    blockages_size_y = []    
   
    for n in range(globals.num_nets):
        n_pins, pin_pos_x, pin_pos_y = format_net(globals.nets[n])
        print("n_pins = ", n_pins)
        print("pin_pos_x = ", pin_pos_x)
        print("pin_pos_y = ", pin_pos_y)  

        
    return 



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
def format_net(Net):

    print("\nFormatting ", Net.name)

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
        print("Testing")
        grid_x = np.arange(start=wrong_dir_start, step=wrong_dir_step, stop=(wrong_dir_start + (wrong_dir_step*(wrong_dir_num))) ) 
        grid_y = np.arange(start=pref_dir_start, step=pref_dir_step, stop=(pref_dir_start + (pref_dir_step*(pref_dir_num) ) ) )
    else:
        grid_x = np.arange(start=wrong_dir_start, step=wrong_dir_step, stop=(wrong_dir_start + (wrong_dir_step*(wrong_dir_num))) ) 
        grid_y = np.arange(start=pref_dir_start, step=pref_dir_step, stop=(pref_dir_start + (pref_dir_step*(pref_dir_num) ) ) )

    #print("grid_x = ", grid_x)
    #print("grid_y = ", grid_y) 
       
    for n in range(n_pins):
      
        # Get Name of Pin
        pin_name = Net.pin_directions[n]
        #print("pin_name = ", pin_name)

        # Get Name of Instance for Pin  
        instance_name = Net.pin_instances[n]
        #print("instance_name = ", instance_name)

        # Get Coordinates and Orientation of Instance 
        instance = globals.instances[instance_name]
        #print("instance.width = ", instance.width, "instance.height = ", instance.height)
        instance_coordinates = (int(instance.width)/2000, int(instance.height)/2000)
        instance_orientation = instance.orientation
        print("instance_coordinates = ", instance_coordinates)
        print("instance_orientation = ", instance_orientation)

        # Get Type of Instance for Instance Name 
        inst_type = globals.instances[instance_name].instance_type
  
        #print("instance_types keys = ", globals.instance_types.keys())
        instance_type = globals.instance_types[inst_type]
        #print("instance_type = ", inst_type)

        # Get Pin Shapes  
        for m in range(len(instance_type.pin_names)):
            if(instance_type.pin_names[m] == pin_name):
                pin_shapes_list = instance_type.pin_shapes_list[m]
                break    
        #print("pin_shapes_list = ", pin_shapes_list)

        # Convert Pin Shapes
        found = 0 
        for m in range(len(pin_shapes_list)):
            _pin_shape = pin_shapes_list[m]
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
              

            print("m = ", m, " llx = ", llx, " lly = ", lly, " urx = ", urx, " ury = ", ury)

            print("len(grid_x)) = ", len(grid_x))
            print("len(grid_y)) = ", len(grid_y))

            found = 0 
            for i in range(len(grid_x)):
                if((grid_x[i] >= llx) and (grid_x[i] <= urx)):
                    for j in range(len(grid_y)):
                        if((grid_y[j] >= lly) and (grid_y[j] <= ury)):
                            pos_x = i
                            pos_y = j
                            found = 1
                            print("Found Track Point")
                        if(found == 1):
                            break
                if(found == 1):
                    break 
            if(found == 1):
                break
          
       
        pin_pos_x.append(pos_x)
        pin_pos_y.append(pos_y)


    return n_pins, pin_pos_x, pin_pos_y
