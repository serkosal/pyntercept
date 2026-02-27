import curses

from pyntercept.process import BasePTYProcess
from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode

def init_colors():
    
    COLORS = [
        curses.COLOR_BLACK,
        curses.COLOR_RED,
        curses.COLOR_YELLOW,
        curses.COLOR_GREEN,
        curses.COLOR_BLUE,
        curses.COLOR_CYAN,
        curses.COLOR_MAGENTA,
        curses.COLOR_WHITE,
    ]
    
    curses.start_color()
    curses.use_default_colors()
    for i in range(1, min( len(COLORS), curses.COLORS) ):
        curses.init_pair(i, COLORS[i], -1)


def start(pr: BasePTYProcess):
    
    win = curses.initscr()
    pr.data = {
        "cwin": win,
        "old_stdin": enter_raw_mode(pr.src)
    }
    init_colors()

    curses.noecho()
    curses.cbreak()
    win.keypad(True)


def stop(pr: BasePTYProcess):
    
    old_stdin = pr.data["old_stdin"]
    cwin: curses.window = pr.data["cwin"]
    
    exit_raw_mode(old_stdin, pr.src)
    curses.nocbreak()
    cwin.keypad(False)
    curses.echo()
    curses.endwin()