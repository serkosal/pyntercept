#!/usr/bin/env python3

from pyntercept.processes.process import PTYProcess
from pyntercept.renderers import PyteRenderer


def main():

    with PTYProcess(['bash'], renderer=PyteRenderer(80, 15)) as pty_process:
        while pty_process.update():
            pass


if __name__ == "__main__":
    main()