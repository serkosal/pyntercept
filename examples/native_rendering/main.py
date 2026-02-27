#!/usr/bin/env python3

from pyntercept.process import PTYProcess
from pyntercept.draw import draw_data
from pyntercept.tty_utils import start, post_start, stop, on_child_out_upd


def main():

    with PTYProcess(
        ['bash'],
        on_child_out_upd=on_child_out_upd,
        init_cb=start, post_init_cb=post_start, exit_cb=stop,
        renderer=draw_data
    ) as pty_process:
    
        while pty_process.update():
            pass
        


if __name__ == "__main__":
    main() 