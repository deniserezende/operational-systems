'''This project consists of writing a program that translates logical to physical addresses for a virtual address space of size 216 = 65,536 bytes.'''

import logging
import sys
from globals import BS_FILE, PHYSICAL_MEMORY_SIZE, TLB_SIZE

class TLB:
    def __init__(self, tlb_page: list, tlb_frame: list, index: int) -> None:
        """This function initializes a TLB."""
        self.TLB_page = tlb_page
        self.TLB_frame = tlb_frame
        self.index = index
        self.first_available_frame = 0
        # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def read_from_disk(self, physical_memory : list, page_number: int) -> list:
        """This function reads from BACKING_STORE.bin"""

        buffer = open(BS_FILE, 'rb')
        buffer.seek(PHYSICAL_MEMORY_SIZE * page_number)

        for i in range(0, PHYSICAL_MEMORY_SIZE):
            physical_memory[self.first_available_frame][i] = buffer.read(1)[0]

        self.first_available_frame += 1
        return physical_memory

    def find_page(self, virtual_address: int, page_faults: int, page_table: list, physical_memory: list, open_frame: int, tlb_hits: int) -> list:
        """This function finds the page using both TLB and PageTable."""
        mask = 0xFF
        tlb_hit = False
        frame = 0
        print(f'Virtual address: {virtual_address}', end='\t')

        # Shifts the 8 bits to the right and adds the mask
        page_number = (virtual_address >> 8) & mask
        offset = virtual_address & mask
        logging.info(f'page_number: {page_number}')
        logging.info(f'offset: {offset}')

        # Checking if in TLB
        for i in range(0, TLB_SIZE):
            if self.TLB_page[i] == page_number:
                frame = self.TLB_frame[i]
                tlb_hit = True
                tlb_hits += 1

        # Checking if in PageTable
        if not tlb_hit:
            if page_table[page_number] == -1:
                physical_memory = self.read_from_disk(physical_memory, page_number)
                open_frame += 1
                page_table[page_number] = open_frame - 1
                page_faults += 1

            frame = page_table[page_number]
            self.TLB_page[self.index] = page_number
            self.TLB_frame[self.index] = page_table[page_number]
            self.index = (self.index + 1) % TLB_SIZE

            logging.info(f'frame: {frame}')
            logging.info(f'offset: {offset}')
        index = (frame * PHYSICAL_MEMORY_SIZE) + offset
        logging.info(f'index: {index}')
        value = physical_memory[frame][offset]
        if value > 127:
            value -= 256
        print(f'Physical address: {index}\tValue (Bytes):{value}')

        return physical_memory, open_frame, page_faults, tlb_hits

    def print_tlb(self) -> None:
        """This function prints the page number and frame if used."""
        for i in range(0, len(self.TLB_page)):
            if self.TLB_page[i] != 255:
                print(f'Page number: {self.TLB_page[i]}\tFrame number: {self.TLB_frame[i]}')

    def print_page_table_not_minus_one(self, page_table: list) -> None:
        """This function prints the page numbers unused."""
        for i in range(0, len(page_table)):
            if page_table[i] == -1:
                print(f'Page number: {i}')

    def print_page_table_bigger_than_zero(self, page_table: list) -> None:
        """This function prints the page number used in order."""
        for i in range(0, len(page_table)):
            if page_table[i] >= 0:
                print(f'Page number: {i}')
