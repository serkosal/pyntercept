#!/usr/bin/env python3

from pyntercept.processes.process import PTYProcess
from pyntercept.renderers.cursesRenderer import CursesRenderer

def main():

    with PTYProcess(
        ['bash'], renderer=CursesRenderer(80, 20)) as pty_process:
    
        while pty_process.update():
            pass
                

if __name__ == "__main__":
    main() 