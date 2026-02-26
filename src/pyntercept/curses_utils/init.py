import curses

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


def start():
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    win.keypad(True)
    
    return win


def stop(win: curses.window):
    curses.nocbreak()
    win.keypad(False)
    curses.echo()
    curses.endwin()