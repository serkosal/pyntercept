#!/usr/bin/env python3

import curses

import pyte

from pyntercept.pyte_utils.draw import draw_pyte_scr_curses
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode
from pyntercept.process import PTYProcess
import pyntercept.curses_utils.init as curses_init

def on_out_upd(
    process: PTYProcess,
    screen: pyte.Screen,
    stream: pyte.ByteStream,
    curses_window: curses.window
) -> bytes:
    data = process.read()

    stream.feed(data)
    draw_pyte_scr_curses(screen, curses_window)
    
    return data

def main():
    pty_process = PTYProcess(
        ['bash'],
        on_child_out_upd=on_out_upd
    )
    
    h, w = pty_process.get_size()
    screen = pyte.Screen(w, h)
    
    try:
        old_stdin = enter_raw_mode()
        cwin = curses_init.start()
        curses_init.init_colors()
        
        stream = pyte.ByteStream(screen)
        init_data = pty_process.read()
        stream.feed(init_data)
        draw_pyte_scr_curses(screen, cwin)
        
        while pty_process.update(screen, stream, cwin):
            pass
                
    
    except OSError: # this happens when child process dies
        pass
    finally:
        exit_raw_mode(old_stdin)
        curses_init.stop(cwin)


if __name__ == "__main__":
    main()