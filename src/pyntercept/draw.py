import sys
from typing import TextIO

import pyte
from rich.text import Text as rText
from rich.console import Console
from rich.control import Control

from rich.control import STRIP_CONTROL_CODES
print('draw', STRIP_CONTROL_CODES)

def draw_data(data: bytes, dest: TextIO | None) -> None:
    if dest is None:
        dest = sys.stdout
    
    try:
        dest.write(data.decode())
    except Exception as e:
        print(f"An error occurred: {e}")


def draw_pyte_scr(
    screen: pyte.Screen, 
    dest: TextIO | None = sys.stdout
) -> None:

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

def convert_pyte_color(s: str) -> str:
    try:
        int(s, 16)
        return '#' + s
    except ValueError:
        return s

def draw_pyte_scr_rich(
    screen: pyte.Screen, 
    console: Console
) -> None:
    
    console.control(Control.home())
    console.control(Control.clear())
    
    rtext = rText(end='')
    for y, line in screen.buffer.items():
        for x in line:
            ch = screen.buffer[y][x]
            fg = convert_pyte_color(ch.fg)
            bg = convert_pyte_color(ch.bg)
            # if ch.data in ['\n', '\v']:
            #     rtext.append(' \r\n')
            # else:
            rtext.append(ch.data, f'{fg} on {bg}')
        
        rtext.append('\r\n')
    # with open('draw.log', 'wt') as draw_log:
    #     draw_log.write(rtext.plain)
    console.print(rtext, end='')
    console.control(Control.move_to(screen.cursor.x, screen.cursor.y))


def draw_pyte_scr_curses(
    screen: pyte.Screen, 
    dest: TextIO | None = sys.stdout
) -> None:
    pass