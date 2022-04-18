# ECE382M Class Project
# Initial Detailed Routing 
# Sergio Chacon, Xiuhao Zhang

import argparse 
from read_inputs import * 
from build_grids import * 

def read_inputs():
    """read routing info from LEF, DEF, Guide"""

    global num_pins; global pins; 
    global num_nets; global net_names; global nets
    global num_nodes; global num_terminals
    global num_rows; global core_rows; 
    global instances
    global net_guides

    # Read in Routing Info 
    print("Reading in results from LEF/DEF parser and routing guide")
    out_root = "bookshelf_writer"  
    # out_files = read_out_aux(out_root)
    num_pins, num_nets, nets = read_out_nets(out_root)
    num_nodes, num_terminals, pins = read_out_nodes(out_root)
    instances = read_out_pl(out_root)
    net_names = read_out_wts(out_root)
    num_rows, core_rows = read_out_scl(out_root)
    net_guides = read_route_guide("ispd19_test1.guide")

    return

def build_grids():
    """store routing info in grid structures"""
    print("TODO: build and store routing info in data structures")
    return

def route_nets():
    """implement A* routing for local grids"""
    print("TODO: extend A* search algorithm for routing")
    # astar_search()
    return


def write_def():
    """write updated routing to new DEF file"""
    print("TODO: write A* star results back to new DEF file")
    return 


def main():
    """main function to route design"""

    parser = argparse.ArgumentParser()


    read_inputs()
    build_grids()
    route_nets()
    write_def()

    return 

if __name__ == "__main__":
    main()


