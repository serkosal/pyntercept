import curses
from typing import TextIO

from .mixins.pyteRendererMixin import PyteRendererMixin
from .mixins.unixBaseRendererMixin import UnixBaseRendererMixin

class CursesRenderer(PyteRendererMixin, UnixBaseRendererMixin):
    
    # __slots__ = ('cwin', '_old_term_attrib')
    cwin: curses.window | None
    
    COLORS = {
        "black": 0,
        "red": 1,
        "yellow": 2,
        "green": 3,
        "blue": 4,
        "cyan": 5,
        "magenta": 6,
        "white": 7
    }
    
    def __init__(
        self, width: int, height: int, 
        src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(width, height, src, dest, err)
        self.cwin = None
        
    
    def _init_colors(self):
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

    
    def init(self):
        if self.cwin is not None:
            raise RuntimeError

        self.cwin = curses.initscr()
        self._init_colors()
        self.set_raw(True, self.src)
        curses.noecho()
        curses.cbreak()
        self.cwin.keypad(True)
    
    
    def exit(self):        
        self.set_raw(False, self.src)
        curses.nocbreak()
        self.cwin.keypad(False)
        curses.echo()
        curses.endwin()
    
    
    def set_echo(self, state = False, target: TextIO | None = None):
        
        if target != self.src:
            super().set_echo(state, target)
        
        if not state:
            curses.noecho()
        else:
            curses.echo()
    
    
    def alt_scr(self, state=True, target = None):
        raise NotImplementedError
        # super().alt_scr(state, target)
    
    
    def clear_scr(self):
        self.cwin.clear()
        
    
    def set_cursor(self, x, y):
        self.cwin.move(y, x)
        
        
    def move_cursor(self, dx, dy):
        x = self.screen.cursor.x
        y = self.screen.cursor.y
        return super().move_cursor(dx + x, dy + y)
    
    
    def render(self): 
        self.cwin.clear()          # clear scr
        self.cwin.move(0, 0)       # move cursor to the position 0,0
        
        for y in self.screen.buffer:
            line = self.screen.buffer[y]
            for x in line:
                ch = self.screen.buffer[y][x]
                if ch.data.isprintable():
                    try:
                        attrib = 0
                        if ch.blink:            attrib |= curses.A_BLINK
                        if ch.bold:             attrib |= curses.A_BOLD
                        if ch.underscore:       attrib |= curses.A_UNDERLINE
                        if ch.italics:          attrib |= curses.A_ITALIC
                        if ch.reverse:          attrib |= curses.A_REVERSE
                        if ch.strikethrough:    attrib |= curses.A_
                        if ch.fg in self.COLORS:
                            attrib |= curses.color_pair(self.COLORS[ch.fg])
                        if ch.bg in self.COLORS:
                            attrib |= curses.color_pair(self.COLORS[ch.bg])
                        self.cwin.addch(y, x, ch.data, attrib)
                    except Exception as _: pass
        try:
            self.cwin.move(self.screen.cursor.y, self.screen.cursor.x)
            self.cwin.refresh()
        except Exception as _: pass