# ECE382M Class Project
# Initial Detailed Routing 
# Sergio Chacon, Xiuhao Zhang

import argparse 
import globals
import read_inputs 
import build_grids 
import route_nets 

def build_grids():
    """store routing info in grid structures"""
    print("TODO: build and store routing info in data structures")
    return

def write_def():
    """write updated routing to new DEF file"""
    print("TODO: write A* star results back to new DEF file")
    return 


def main():
    """main function to route design"""

    globals.initialize()
    read_inputs.read_inputs()
    #build_grids()
    route_nets.route_nets()
    write_def()

    return 

if __name__ == "__main__":
    main()


