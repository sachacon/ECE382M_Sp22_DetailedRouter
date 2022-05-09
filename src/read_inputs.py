# ECE382M Class Project 
# Initial Detailed Routing 
# Sergio Chacon, Xiuhao Zhang

import os
import itertools
import globals

class Pin:
    def __init__(
        self,
        name,
        terminal
    ) -> None: 
        self.name = name 
        self.terminal = terminal 

class Net:
    def __init__(
        self,
        degree, 
        name,
        pin_instances,
        pin_directions,
        offset,
    ) -> None: 
        self.degree = degree 
        self.name = name # string
        self.pin_instances = pin_instances
        self.pin_directions = pin_directions
        self.offset = offset 

class Instance :
    def __init__(
        self,
        name, 
        width, 
        height, 
        orientation
    ) -> None: 
        self.name = name 
        self.width = width
        self.height = height 
        self.orientation = orientation 
        self.instance_type = None 

class InstanceType :
    def __init__(
        self,
        instance_name, 
        pin_names, 
        pin_shapes_list
    ) -> None: 
        self.instance_name = instance_name 
        self.pin_names = pin_names
        self.pin_shapes_list = pin_shapes_list

class CoreRow:
    def __init__(
        self,
        direction,
        coordinate,
        height, 
        site_width, 
        site_spacing, 
        site_orient, 
        site_symmetry,
        subrow_origin,
        num_sites 
    ) -> None: 
        self.direction = direction 
        self.coordinate = coordinate
        self.height = height 
        self.site_width = site_width 
        self.site_spacing = site_spacing 
        self.site_orient = site_orient 
        self.site_symmetry = site_symmetry
        self.subrow_origin = subrow_origin
        self.num_sites = num_sites 

class NetGuide:
    def __init__(
        self,
        name,
        guide
    ) -> None: 
        self.name = name 
        self.guide = guide

class MetalLayer:
    def __init__(
        self,
        layer, # int type, 1 or 2 etc. 
        direction, # "H" or "V"
        pref_dir_start, 
        pref_dir_step,
        pref_dir_num,
        wrong_dir_start,
        wrong_dir_step,
        wrong_dir_num
    ) -> None:
        self.layer = layer 
        self.direction = direction
        self.pref_dir_start = pref_dir_start
        self.pref_dir_step = pref_dir_step
        self.pref_dir_num = pref_dir_num
        self.wrong_dir_start = wrong_dir_start
        self.wrong_dir_step = wrong_dir_step
        self.wrong_dir_num = wrong_dir_num

# Grid Coordiante (5,5) for A* search coordinate system
# Routing Guide, need to divide by 2000, to get Innovus coordinate system
# pref_dir_start + 5 * pref_dir_step to get Innovus coordinate system 
# 

#isInsideGuideBox(layer (int), coordinate (int,int) ) 

#return True or False

# DONE 
def read_out_aux(path):
    filename = os.path.join(path, "out.aux")
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if("RowBasedPlacement" in line):
                del line[0]
                del line[0]
                break
    return(line)        

# DONE  
def read_out_nets(path):
    n_nets = 0;
    num_nets = 0; num_pins = 0; start = 0; nets = {} 
    pin_instances = []; pin_directions = []
    filename = os.path.join(path, "out.nets")
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if("NumNets" in line):
                num_nets = line[-1]
            if("NumPins" in line):
                num_pins = line[-1]
            if("NetDegree" in line):
                # Add previous net info to list 
                if(start == 0):
                    start = 1
                else:
                    #print("name = ", name, " pin_instances = ", pin_instances)
                    if not(any("pin" in s for s in pin_instances)):
                        nets[name] = Net(int(degree), name, pin_instances, pin_directions, 0.5)
               
                # Start updating info for new net
                pin_instances = []
                pin_directions = [] 
                degree = line[-2]
                #print("degree = ", degree)
                name = line[-1]  
            if(start == 1 and "NetDegree" not in line):
                pin_instances.append(line[0])
                pin_directions.append(line[1])                  

    # Add last net info to list 
    if not(any("pin" in s for s in pin_instances)):
        nets[name] = Net(int(degree), name, pin_instances, pin_directions, 0.5)

    return(len(nets.keys()), int(num_pins), nets)

# DONE 
def read_out_nodes(path):
    start = 0; num_nodes = 0; num_terminals = 0; pins = []
    filename = os.path.join(path, "out.nodes")
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if("NumNodes" in line):
                num_nodes = line[-1]
            if("NumTerminals" in line):
                num_terminals = line[-1]
                start = 1
            if(start == 1):
                name = line[0]
                if("terminal" not in line):
                    terminal = False 
                pins.append(Pin(name, terminal))

    return(num_nodes, num_terminals, pins)

# DONE 
def read_out_pl(path):
    instances = {} 
    filename = os.path.join(path, "out.pl")
    with open(filename, 'r') as f:
        for line in itertools.islice(f,3,None):
            line = line.split()
            name = line[0]
            width = line[1]
            height= line[2]
            orientation = line[-1]
            instances[name] = Instance(name, width, height, orientation)

    return(instances)
 
# DONE 
def read_out_wts(path):
    net_names = []
    filename = os.path.join(path, "out.wts")
    with open(filename, 'r') as f:
        for line in itertools.islice(f,3,None):
            line = line.split()
            net_names.append(line[0])
    return net_names

# DONE 
def read_out_scl(path):
    num_rows = 0; core_rows = []  
    filename = os.path.join(path, "out.scl")
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if("NumRows" in line):
                num_rows = line[-1]
            if("CoreRow" in line):
                direction = line[-1]
            if("Coordinate" in line):
                coordinate = line[-1]
            if("Height" in line):
                height = line[-1]
            if("Sitewidth" in line):
                site_width = line[-1]
            if("Sitespacing" in line):
                site_spacing = line[-1]
            if("Siteorient" in line):
                site_orient = line[-1]
            if("Sitesymmetry" in line):
                site_symmetry = line[-1]
            if("SubrowOrigin" in line):
                subrow_origin = line[2]
            if("NumSites" in line):
                num_sites = line[-1]
            if("End" in line):
                core_rows.append(CoreRow(direction, coordinate, height, site_width, site_spacing, site_orient, site_symmetry, subrow_origin, num_sites))

    return(num_rows, core_rows)              

 
def read_instance_type():
    prev_line = None
    start = 0 
    instance_types = {} 
    pin_names = []
    pin_shapes_list = [] 
    pin_shapes = []
    filename = "bookshelf_writer/out.lef"
    with open(filename, 'r', encoding="ISO-8859-1") as f:
        for line in f:

            # Instance Type 
            if("--pins" in line):

                # Create Object For Previous Instance Type 
                if(start == 1):
                    #print("pin_shapes_list = ", pin_shapes_list)
                    instance_types[instance_type] = InstanceType(instance_type,pin_names,pin_shapes_list)
                    pin_names = []
                    #pin_shapes_list = []
                start = 1 
                tmp_line = prev_line.split()
                instance_type = tmp_line[0]

            # Pin Name 
            if("use" in line):
                tmp_line = prev_line.split()
                pin_names.append(tmp_line[0])
                #print("instance_type = ", instance_type, " pin_name = ", tmp_line[0])
 
            if("shape" in line):
                if(len(pin_shapes) != 0):
                    pin_shapes_list.append(pin_shapes)
                    pin_shapes = [] 
                 
            if(": 0" in line):
                tmp_line = line.replace(": 0","")
                tmp_line = tmp_line.replace(":"," ")
                tmp_line = tmp_line.replace("("," ")
                tmp_line = tmp_line.replace(")"," ")
                tmp_line = tmp_line.replace("\n","")
                pin_shapes.append(tmp_line)

            prev_line = line 

    instance_types[instance_type] = InstanceType(instance_type,pin_names,pin_shapes_list)

    
    print(instance_type, " ", pin_names, " ", pin_shapes_list, "\n")

    return instance_types
 

def read_route_guide(filename):
    net_guides = {}; single_net_guide = []
    start = 0; net_name = "" 
    with open(filename, 'r') as f:
        for line in f:
            if("net" in line and start == 0):
                line = line.split()
                start = 1 
                net_name = line[0]
                single_net_guide = []
                continue 
            if("net" in line and start == 1):
                 net_guides[net_name] = NetGuide(net_name, single_net_guide)
                 line = line.split()
                 net_name = line[0]
                 single_net_guide = [] 
                 continue 
            else:
                 line = line.split()
                 if(len(line) == 5):
                     single_net_guide.append(line)

    net_guides[net_name] = NetGuide(net_name, single_net_guide)

    print(net_guides.keys())
    for key in net_guides.keys():
        print("key = ", key, " net guide = ", net_guides[key].guide) 
    return net_guides


def read_metal_layers():
    metal_layers = []
    grid_coordinates = []
    filename = "bookshelf_writer/out.lef"
    with open(filename, 'r', encoding="ISO-8859-1") as f:
        for line in f:
            if("Metal" in line):
                line = line.split()
                #print(line)
  
                # Metal Layer and Direction
                layer = line[0].replace("Metal","")
                direction = line[1].replace("(","")
                direction = direction.replace(")","")
                
                # Wrong Direction Tracks 
                wrong_dir_num = line[-1].replace("num","")
                wrong_dir_step = line[-2].replace("stp","")
                wrong_dir_start = line[-3].replace("srt","")

                # Preferred Direction Tracks 
                pref_dir_num = line[-5].replace("num","")
                pref_dir_step = line[-6].replace("stp","")
                pref_dir_start = line[-7].replace("srt","")
 
                # Create Metal Layer Object and Append 
                metal_layers.append(MetalLayer(int(layer), direction, int(pref_dir_start), int(pref_dir_step), int(pref_dir_num), int(wrong_dir_start), int(wrong_dir_step), int(wrong_dir_num) )) 

    print("len(metal_layers) = ", len(metal_layers))
    for n in range(len(metal_layers)):
        metal = metal_layers[n]
        print("metal.layer = ", metal.layer)
        if(metal.layer == 1):
           grid_size = (metal.wrong_dir_num, metal.pref_dir_num)
           
    return metal_layers, grid_size


# OUTDATED, DON'T USE 
def read_layers(def_filename):
    
    #direction = "HZ"
    direction = "VH" 
    num_layers = 9 
    layer_directions = {}
    metal_layers = []
    if(direction == "VH"):
        for layer in range(num_layers):
            if(layer % 2 == 0):
                layer_directions[layer] = "V"
            else:
                layer_directions[layer] = "H"
    else:
        for layer in range(num_layers):
            if(layer % 2 == 0):
                layer_directions[layer] = "H"
            else:
                layer_directions[layer] = "V"

    count = 0 
    with open(def_filename, 'r') as f:
        for line in f:
            if("GCELLGRID") in line:
                break
            if("TRACKS") in line: 
                line = line.split()
                layer = int(line[-2].replace("Metal",""))
                if(line[1]=="Y" and layer_directions[layer-1]=="H" or line[1]=="X" and layer_directions[layer-1]=="V"):
                    pref_start = line[2]
                    pref_step = line[4]
                    pref_num = line[6]
                else:
                    wrong_start = line[2]
                    wrong_step = line[4]
                    wrong_num = line[6]
                count += 1
                if(count == 2):
                    count == 0
                    metal_layers.append(MetalLayer(layer, layer_directions[layer-1], pref_start, pref_step, pref_num, wrong_start, wrong_step, wrong_num)) 
  

    return 


def update_instances():
    start = 0 
    filename = "bookshelf_writer/components.txt"
    with open(filename, 'r') as f:
        for line in f:
            if("PLACED" in line or "FIXED" in line):
                line_ = line.split()
                instance_name = line_[1]
                instance_type = line_[2]
                globals.instances[instance_name].instance_type = instance_type

                for i in range(len(line_)):
                    if("(" in line_[i]):
                        globals.instances[instance_name].width = line_[i+1]
                        globals.instances[instance_name].height = line_[i+2]
                

    return

def update_nets():
    filename = "bookshelf_writer/nets.txt"
    with open(filename, 'r') as f:
        for line in f:
            if("-" in line):
                tmp_line = line.split()
                net_name = tmp_line[1]
                #print("Found net name = ", net_name)
            if("(" and ")" in line):
                tmp_line = line.split()
                for i in range(len(tmp_line)):
                    if("(" in tmp_line[i]):
                        instance_name = tmp_line[i+1]
                        pin_name = tmp_line[i+2] 
               
                        if(net_name in globals.nets.keys()):
                            for j in range(globals.nets[net_name].degree):
                                if(instance_name == globals.nets[net_name].pin_instances[j]):
                                    globals.nets[net_name].pin_directions[j] = pin_name 
                                    break
 
                        #for j in range(globals.num_nets):
                        #    if(net_name == Nets[j].name):       
                        #        for k in range(Nets[j].degree):
                        #            if(instance_name == Nets[j].pin_instances[k]):
                        #                Nets[j].pin_directions[k] = pin_name
                        #        break

    return 

def read_inputs():
    """read routing info from LEF, DEF, Guide"""

    # Read in Routing Info 
    print("Reading in results from LEF/DEF parser and routing guide ...\n")
    out_root = "bookshelf_writer"
  
    # out_files = read_out_aux(out_root)

    print("Read nets")
    globals.num_nets, globals.num_pins, globals.nets = read_out_nets(out_root)
    print("Update nets")
    update_nets()

    #globals.num_nodes, globals.num_terminals, globals.pins = read_out_nodes(out_root)

    print("Read instances")
    globals.instances = read_out_pl(out_root)
    print("Update instances")
    update_instances()

    print("Read instance types")
    globals.instance_types = read_instance_type()

    #net_names = read_out_wts(out_root)
    #num_rows, core_rows = read_out_scl(out_root)
    
    print("Read routing guides")
    globals.net_guides = read_route_guide("bookshelf_writer/guide.txt")
    print("Read metal layers")
    globals.metal_layers, globals.grid_size = read_metal_layers()

    return


def read_inputs_test():

#    print("Reading in results from LEF/DEF parser")

    out_root = "bookshelf_writer"  

#    out_files = read_out_aux(out_root)
    
    num_nets, num_pins, nets = read_out_nets(out_root)
    #print("num_nets = ", num_nets)
    for i in range(num_nets):
        net = nets[i]
        #print("net.degree = ", net.degree)
        #for j in range(net.degree):
            #print("net.pin_instance = ", net.pin_instances[j])

    num_nodes, num_terminals, pins = read_out_nodes(out_root)

    instances = read_out_pl(out_root)
    update_instances(instances) 
    for i in instances.keys():
        instance = instances[i] 
        #print("instance.name = ", instance.name)
        #print("instance.instance_type = ", instance.instance_type)

    instance_types = read_instance_type()
    for i in instance_types.keys():
         instance_type = instance_types[i]
         #print("instance_type = ", instance_type.instance_name)
         for j in range(len(instance_type.pin_names)):
             #print("pin name = ", instance_type.pin_names[j])
             tmp_pin_shapes = instance_type.pin_shapes_list[j]
             #print("pin shape = ", instance_type.pin_shapes_list[j])

    nets = update_nets()
    for i in range(len(nets)):
        net = nets[i]
        #print("\nnet.name = ", net.name, " net.degree = ", net.degree)
        #print("net.pin_instances = ", net.pin_instances)
        #print("net.pin_directions = ", net.pin_directions)

#    metal_layers, grid_size = read_metal_layers()
#    for i in range(len(metal_layers)):
#        print(metal_layers[i].layer)
#        print(metal_layers[i].direction)


#    net_names = read_out_wts(out_root)
#    num_rows, core_rows = read_out_scl(out_root)
#     
#    print("Reading in input routing guide")
#    net_guides = read_route_guide("ispd19_test1.guide")
#
#    return

#read_inputs_test()


