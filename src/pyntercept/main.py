#!/usr/bin/env python3

import sys

import pyte

from pyntercept.draw import draw_pyte_scr
from pyntercept.tty_utils import (enter_raw_mode, exit_raw_mode, switch_echo,
    alternate_scr_on, alternate_scr_off
)
from pyntercept.process import PTYProcess

stdin_fd = sys.stdin.fileno()
stdout_fd = sys.stdin.fileno()

def on_out_upd(
    process: PTYProcess,
    screen: pyte.Screen,
    stream: pyte.ByteStream
) -> bytes:
    data = process.on_out_fd_upd()

    stream.feed(data)
    draw_pyte_scr(screen, stdout_fd)
    
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
        alternate_scr_on(stdout_fd)
        switch_echo(stdin_fd, False)
        old_stdin = enter_raw_mode(stdin_fd)
        old_stdout = enter_raw_mode(stdout_fd)
        
        stream = pyte.ByteStream(screen)
        stream.feed(pty_process.on_out_fd_upd())
        draw_pyte_scr(screen, stdout_fd)
        
        while pty_process.update(screen, stream):
            pass
                
    
    except OSError: # this happens when child process dies
        pass
    finally:
        exit_raw_mode(stdin_fd, old_stdin)
        exit_raw_mode(stdout_fd, old_stdout)
        switch_echo(stdin_fd, True)
        alternate_scr_off(stdout_fd)


if __name__ == "__main__":
    main() 