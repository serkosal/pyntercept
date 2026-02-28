#!/usr/bin/env python3

from pyntercept.processes.process import PTYProcess
from pyntercept.pyte_utils.draw import draw_pyte_scr_curses

def main():

    with PTYProcess(
        ['bash'], on_child_out_upd=on_child_out_upd,
    ) as pty_process:
    
        while pty_process.update():
            pass
                

if __name__ == "__main__":
    main() 