#!/usr/bin/env python3

import sys
import curses

import pyte

from pyntercept.pyte_utils.draw import draw_pyte_scr_curses
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode
from pyntercept.process import PTYProcess

stdin = sys.stdin
stdout = sys.stdout

def on_out_upd(
    process: PTYProcess,
    screen: pyte.Screen,
    stream: pyte.ByteStream,
    curses_window: curses.window
) -> bytes:
    data = process.on_out_fd_upd()

    stream.feed(data)
    draw_pyte_scr_curses(screen, curses_window)
    
    return data

def main():    
    if len(sys.argv) < 2:
        print('you must specify executable program!')
        return
    
    pty_process = PTYProcess(
        sys.argv[1:],
        out_upd_callback=on_out_upd
    )
    
    h, w = pty_process.get_size()
    
    screen = pyte.Screen(w, h)
    
    try:
        old_stdin = enter_raw_mode(stdin)
        curses_win = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses_win.keypad(True)
        
        COLORS = [
            curses.COLOR_BLACK,
            curses.COLOR_RED,
            curses.COLOR_YELLOW,
            curses.COLOR_GREEN,
            curses.COLOR_BLUE,
            curses.COLOR_CYAN,
            curses.COLOR_MAGENTA,
            curses.COLOR_WHITE,
        ]
        curses.start_color()
        curses.use_default_colors()
        for i in range(1, min( len(COLORS), curses.COLORS) ):
            curses.init_pair(i, COLORS[i], -1)
        
        stream = pyte.ByteStream(screen)
        init_data = pty_process.on_out_fd_upd()
        stream.feed(init_data)
        draw_pyte_scr_curses(screen, curses_win)

        
        while pty_process.update(screen, stream, curses_win):
            pass
                
    
    except OSError: # this happens when child process dies
        pass
    # finally:
        exit_raw_mode(stdin, old_stdin)
        curses.nocbreak()
        curses_win.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    main() 