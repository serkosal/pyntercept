#!/usr/bin/env python3

from pyntercept.processes.process import PTYProcess
from pyntercept.renderers import UnixRenderer


def main():

    with PTYProcess(['bash'], renderer=UnixRenderer()) as pty_process:
        while pty_process.update():
            pass


if __name__ == "__main__":
    main()