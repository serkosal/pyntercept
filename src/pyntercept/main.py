#!/usr/bin/env python3

import os
import sys
import select
import termios

from pyntercept.draw import draw_data
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode, switch_echo
from pyntercept.pseudo_tty import create_pty

def child_alive(pid):
    # Availability: Unix, Windows, not WASI, not Android, not iOS.
    rpid, _ = os.waitpid(pid, os.WNOHANG)
    return rpid == 0


def main():
    stdin_fd = sys.stdin.fileno()
    stdout_fd = sys.stdin.fileno()
    
    print(sys.argv)
    if len(sys.argv) < 2:
        print('you must specify executable program!')
        return
    pid, master_fd, child_fd = create_pty(sys.argv[1], *sys.argv[1:])
    termios.tcsetwinsize(child_fd, (20, 60))
    
    if pid == 0:
        return
    
    try:
        switch_echo(stdin_fd, False)
        old_stdin = enter_raw_mode(stdin_fd)
        old_stdout = enter_raw_mode(stdout_fd)
        
        output_data = os.read(master_fd, 1024)
        draw_data(output_data)
        
        while True:
            if not child_alive(pid):
                break
            
            # aks OS for file descriptors updates
            rlist, _, _ = select.select([stdin_fd, master_fd], [], [], 0)
            
            if stdin_fd in rlist:
                data = os.read(stdin_fd, 2048)  # read user input
                os.write(master_fd, data)       # pass input into editor process
                # if not child_alive(pid):
                #     break
                
            if master_fd in rlist:
                data = os.read(master_fd, 2048) # read output from editor
                if not data:
                    break
                draw_data(data)                 # draw that output
    except OSError: # this happens when child process dies
        pass
    finally:
        exit_raw_mode(stdin_fd, old_stdin)
        exit_raw_mode(stdout_fd, old_stdout)
        switch_echo(stdin_fd, True)


if __name__ == "__main__":
    main() 