#!/usr/bin/env python3

from pyntercept.process import PTYProcess
from pyntercept.renderers import RawRenderer


def main():

    with PTYProcess(['bash'], renderer=RawRenderer()) as pty_process:
        while pty_process.update():
            pass


if __name__ == "__main__":
    main()