#!/usr/bin/env python3

import sys

from io import TextIOWrapper

from pyntercept.draw import draw_data
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode, switch_echo
from pyntercept.process import PTYProcess

stdin_fd = sys.stdin.fileno()
stdout_fd = sys.stdin.fileno()

def on_out_upd(process: PTYProcess, file: TextIOWrapper) -> bytes:
    data = process.on_out_fd_upd()

    draw_data(data, stdout_fd)
    file.write(data.decode() + '\n')
    
    return data

def main():    
    if len(sys.argv) < 2:
        print('you must specify executable program!')
        return
    
    pty_process = PTYProcess(
        sys.argv[1:],
        out_upd_callback=on_out_upd
    )
    
    try:
        switch_echo(stdin_fd, False)
        old_stdin = enter_raw_mode(stdin_fd)
        old_stdout = enter_raw_mode(stdout_fd)
        
        with open('out.log', 'wt') as out_log:
            draw_data(pty_process.on_out_fd_upd())
        
            while pty_process.update(out_log):
                pass
    
    except OSError: # this happens when child process dies
        pass
    finally:
        exit_raw_mode(stdin_fd, old_stdin)
        exit_raw_mode(stdout_fd, old_stdout)
        switch_echo(stdin_fd, True)


if __name__ == "__main__":
    main() 