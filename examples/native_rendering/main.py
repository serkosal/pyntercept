#!/usr/bin/env python3

import sys

from pyntercept.draw import draw_data
from pyntercept.tty_utils import ( enter_raw_mode, exit_raw_mode, 
    alternate_scr_on, alternate_scr_off, switch_echo 
)
from pyntercept.process import PTYProcess

stdin = sys.stdin
stdout = sys.stdout

def on_out_upd(
    process: PTYProcess
) -> bytes:
    data = process.read()

    draw_data(data, stdout)
    
    return data

def main():    
    pty_process = PTYProcess(
        ['bash'],
        on_child_out_upd=on_out_upd
    )
    
    try:
        alternate_scr_on()
        old_stdin = enter_raw_mode()
        old_stdout = enter_raw_mode(stdout)
        switch_echo(False)

        initial_data = pty_process.read() 
        draw_data(initial_data, stdout)

        while pty_process.update():
            pass
    except OSError: # this happens when child process dies
        pass
    finally:
        exit_raw_mode(old_stdin)
        exit_raw_mode(old_stdout, stdout)
        switch_echo(True)
        alternate_scr_off()


if __name__ == "__main__":
    main() 