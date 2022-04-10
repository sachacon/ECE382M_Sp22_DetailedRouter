# ECE382M Class Project 
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
  

def main():
    """ Get num_nets, num_pins, num_terminals, num_nodes, num_rows,
        nets, pins, instances, and core_rows """

    print("Reading in results from LEF/DEF parser")
    out_root = "bookshelf_writer"
  
    out_files = read_out_aux(out_root)
    num_pins, num_nets, nets = read_out_nets(out_root)
    num_nodes, num_terminals, pins = read_out_nodes(out_root)
    instances = read_out_pl(out_root)
    net_names = read_out_wts(out_root)
    num_rows, core_rows = read_out_scl(out_root)
     
    print("out_files: ", out_files)
    #print("net_names: ", net_names)
    #for i in range(len(core_rows)):
    #    print(core_rows[i].coordinate) 

if __name__ == "__main__":
    main()


