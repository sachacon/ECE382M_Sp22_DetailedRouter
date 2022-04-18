# ECE382M Class Project 
# Initial Detailed Routing 
# Sergio Chacon, Xiuhao Zhang

import os
import itertools

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
        self.name = name 
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
        layer,
        pref_direction,
        pref_start,
        pref_step,
        pref_num,
        wrong_start,
        wrong_step,
        wrong_num
    ) -> None:
        self.layer = layer 
        self.pref_direction = pref_direction
        self.pref_start = pref_start
        self.pref_step = pref_step
        self.pref_num = pref_num
        self.wrong_start = wrong_start
        self.wrong_step = wrong_step
        self.wrong_num = wrong_num
 

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
    num_nets = 0; num_pins = 0; start = 0; nets = [] 
    pin_instances = []; pin_directions = []
    filename = os.path.join(path, "out.nets")
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if("NumNets :" in line):
                num_nets = line[-1]
            if("NumPins :" in line):
                num_pins = line[-1]
            if("NetDegree" in line):
                # Add previous net info to list 
                if(start == 0):
                    start = 1
                else:
                    nets.append(Net(degree, name, pin_instances, pin_directions, 0.5))
               
                # Start updating info for new net
                pin_instances = []
                pin_directions = [] 
                degree = [-2]
                name = [-1]  
            if(start == 1 and "NetDegree" not in line):
                pin_instances.append(line[0])
                pin_directions.append(line[1])                  

    return(num_nets, num_pins, nets)

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
    instances = [] 
    filename = os.path.join(path, "out.pl")
    with open(filename, 'r') as f:
        for line in itertools.islice(f,3,None):
            line = line.split()
            name = line[0]
            width = line[1]
            height= line[2]
            orientation = line[-1]
            instances.append(Instance(name, width, height, orientation))

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
  

def read_route_guide(filename):
    net_guides = []; single_net_guide = []
    start = 0; net_name = "" 
    with open(filename, 'r') as f:
        for line in f:
            if("net" in line and start == 0):
                line = line.split()
                start = 1 
                net_name = line[0]
                single_net_guide = []
            elif("net" in line and start == 1):
                 line = line.split()
                 net_name = line[0]
                 net_guides.append(NetGuide(net_name, single_net_guide))
                 single_net_guide = [] 
            else:
                 line = line.split()
                 if(len(line) == 5):
                     single_net_guide.append(line)
 
    return net_guides

def read_layers(def_filename):
    
    # inputs: def_filename 

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


#def main():
#    """ Get num_nets, num_pins, num_terminals, num_nodes, num_rows,
#        nets, pins, instances, and core_rows """
#
#    print("Reading in results from LEF/DEF parser")
#    out_root = "bookshelf_writer"  
#    out_files = read_out_aux(out_root)
#    num_pins, num_nets, nets = read_out_nets(out_root)
#    num_nodes, num_terminals, pins = read_out_nodes(out_root)
#    instances = read_out_pl(out_root)
#    net_names = read_out_wts(out_root)
#    num_rows, core_rows = read_out_scl(out_root)
#     
#    print("Reading in input routing guide")
#    net_guides = read_route_guide("ispd19_test1.guide")
#
#    return

#if __name__ == "__main__":
#    main()


