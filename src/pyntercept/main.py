#!/usr/bin/env python3

import sys

from pyntercept.process import PTYProcess
from pyntercept.renderers import RawRenderer


def main():
    if len(sys.argv) < 2:
        print('you must specify executable program!')
        return

    with PTYProcess(sys.argv[1:], renderer=RawRenderer()) as pty_process:
        while pty_process.update():
            pass
                

if __name__ == "__main__":
    main()