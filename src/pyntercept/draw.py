import sys
from typing import TextIO

import pyte

def draw_data(data: bytes, dest: TextIO | None) -> None:
    if dest is None:
        dest = sys.stdout
    
    try:
        dest.write(data.decode())
    except Exception as e:
        print(f"An error occurred: {e}")


def draw_pyte_scr(screen: pyte.Screen, dest: TextIO | None) -> None:
    
    dest = sys.stdout

    dest.write('\x1B[2J') # clear scr
    dest.write(f'\x1B[H') # move cursor to the position 0,0 
    
    for y in screen.buffer:
        line = screen.buffer[y]
        for x in line:
            ch = screen.buffer[y][x]
            dest.write(ch.data)
        if y != len(screen.buffer) - 1: 
            dest.write('\r\n')

    dest.write(f'\x1B[{screen.cursor.y+1};{screen.cursor.x+1}H')
    dest.flush()