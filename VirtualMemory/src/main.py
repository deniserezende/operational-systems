'''This project consists of writing a program that translates logical to physical addresses for a virtual address space of size 216 = 65,536 bytes. 

To execute this program: python[version] main.py [path_to_txt_file].txt <table size> <algorithm [FIFO or LRU]>'''

import logging
import sys
from VirtualMemory import TLB
from globals import TLB_SIZE, PAGE_TABLE_SIZE, PHYSICAL_MEMORY_SIZE, DEFAULT_VALUE, PHYSICAL_MEMORY_SIZE_Q, change_attributes

txt_file = None
algorithm = None
command = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error(f'Not enough arguments.')
        exit(0)
    try:
        txt_file = open(sys.argv[1], 'r')

    except FileNotFoundError:
        logging.error(f'File not found.')
        exit(0)

    if len(sys.argv) > 3:
        change_attributes(int(sys.argv[2]))
        if sys.argv[3] == 'FIFO' or sys.argv[3] == 'LRU':
            algorithm = sys.argv[3]

# Creating table
page_table = [-1] * PAGE_TABLE_SIZE

# Creating tlb
tlb = TLB(tlb_page=[DEFAULT_VALUE] * TLB_SIZE, tlb_frame=[DEFAULT_VALUE] * TLB_SIZE, index=0)

page_faults = 0
open_frame = 0
input_count = 0
tlb_hits = 0

# Creating table PHYSICAL_MEMORY_SIZExPHYSICAL_MEMORY_SIZE_Q
physical_memory = [[0] * PHYSICAL_MEMORY_SIZE] * PHYSICAL_MEMORY_SIZE_Q

if txt_file is not None:
    for line in txt_file.readlines():
        logging.info(f'line: {line}')
        if line == '\n':
            pass
        elif int(line) == -1:
            print("Comando -1")
            tlb.print_tlb()
            pass
        elif int(line) == -2:
            print("Comando -2")
            tlb.print_page_table_not_minus_one(page_table)
            pass
        elif int(line) == -3:
            print("Comando -3")
            tlb.print_page_table_bigger_than_zero(page_table)
            pass
        else:
            physical_memory, open_frame, page_faults, tlb_hits = tlb.find_page(virtual_address=int(line),
                                                                               page_faults=page_faults,
                                                                               page_table=page_table,
                                                                               physical_memory=physical_memory,
                                                                               open_frame=open_frame, tlb_hits=tlb_hits)
            input_count += 1
    page_fault_rate = page_faults / input_count
    tlb_hit_rate = tlb_hits / input_count
    print(f'Page Fault Rate: {round(page_fault_rate, 4)}\nTLB hit rate: {round(tlb_hit_rate, 4)}')
    txt_file.close()
