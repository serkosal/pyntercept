#!/usr/bin/env python3

import sys

from pyntercept.process import PTYProcess
from pyntercept.curses_utils.init import start, stop
from pyntercept.pyte_utils.draw import draw_pyte_scr_curses
from pyntercept.pyte_utils.utils import post_init, on_child_out_upd

def main():
    
    if len(sys.argv) < 2:
        print('you must specify executable program!')
        return

    with PTYProcess(
        sys.argv[1:], on_child_out_upd=on_child_out_upd, 
        init_cb=start, post_init_cb=post_init, exit_cb=stop,
        renderer=draw_pyte_scr_curses
    ) as pty_process:
    
        while pty_process.update():
            pass
                

if __name__ == "__main__":
    main() 