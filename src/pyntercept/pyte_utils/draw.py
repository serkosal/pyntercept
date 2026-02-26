import curses
import sys
from typing import TextIO

import pyte

from .utils import pyte_colors

def draw_pyte_scr(
    screen: pyte.Screen, 
    dest: TextIO = sys.stdout
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

    
def draw_pyte_scr_curses(
    screen: pyte.Screen,
    window: curses.window
) -> None:
    
    window.clear()          # clear scr
    window.move(0, 0)       # move cursor to the position 0,0
    
    for y in screen.buffer:
        line = screen.buffer[y]
        for x in line:
            ch = screen.buffer[y][x]
            if ch.data.isprintable():
                try:
                    attrib = 0
                    if ch.blink:            attrib |= curses.A_BLINK
                    if ch.bold:             attrib |= curses.A_BOLD
                    if ch.underscore:       attrib |= curses.A_UNDERLINE
                    if ch.italics:          attrib |= curses.A_ITALIC
                    if ch.reverse:          attrib |= curses.A_REVERSE
                    # if ch.strikethrough:    attrib |= curses.A_
                    if ch.fg in pyte_colors:
                        attrib |= curses.color_pair(pyte_colors[ch.fg])
                    if ch.bg in pyte_colors:
                        attrib |= curses.color_pair(pyte_colors[ch.bg])
                    window.addch(y, x, ch.data, attrib)
                except Exception as _: pass
    try:
        window.move(screen.cursor.y, screen.cursor.x)
        window.refresh()
    except Exception as _: pass
