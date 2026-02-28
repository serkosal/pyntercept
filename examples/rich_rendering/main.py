#!/usr/bin/env python3

from pyntercept.processes.process import PTYProcess
from pyntercept.renderers.richRenderer import RichRenderer


def main():

    with PTYProcess(['bash'], renderer=RichRenderer(120, 30)) as pty_process:
        while pty_process.update():
            pass


if __name__ == "__main__":
    main()