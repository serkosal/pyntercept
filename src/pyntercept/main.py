#!/usr/bin/env python3

import sys
from pyntercept import patch_rich


import pyte
from rich.console import Console


from pyntercept.draw import draw_pyte_scr_rich
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode
from pyntercept.process import PTYProcess

stdin = sys.stdin
stdout = sys.stdout

def on_out_upd(
    process: PTYProcess,
    screen: pyte.Screen,
    stream: pyte.ByteStream,
    console: Console
) -> bytes:
    data = process.on_out_fd_upd()

    stream.feed(data)
    draw_pyte_scr_rich(screen, console)
    
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
    console = Console(width=w, height=h)
    
    try:
        # alternate_scr_on(stdout)
        # switch_echo(stdin, False)
        old_stdin = enter_raw_mode(stdin)
        old_stdout = enter_raw_mode(stdout)
        
        # attrs = termios.tcgetattr(stdin.fileno())
        # # enable implementation-defined output processing.
        # attrs[1] |= termios.OPOST
        # attrs[1] |= termios.ONLCR # enable NL -> CRNL
        # termios.tcsetattr(stdin.fileno(), termios.TCSANOW, attrs)
        
        stream = pyte.ByteStream(screen)
        stream.feed(pty_process.on_out_fd_upd())
        draw_pyte_scr_rich(screen, console)
        
        while pty_process.update(screen, stream, console):
            pass
                
    
    except OSError: # this happens when child process dies
        pass
    # finally:
        exit_raw_mode(stdin, old_stdin)
        exit_raw_mode(stdout, old_stdout)
        # switch_echo(stdin, True)
        # alternate_scr_off(stdout)


if __name__ == "__main__":
    main() 