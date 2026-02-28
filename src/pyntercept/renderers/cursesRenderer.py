import curses
from typing import TextIO

from .pyteRenderer import PyteRenderer
from .helpers import set_raw

class CursesRenderer(PyteRenderer):
    
    __slots__ = ('cwin', '_old_term_attrib')
    cwin: curses.window | None = None
    
    def __init__(
        self, width: int, height: int, 
        src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(width, height, src, dest, err)
        
    
    def _init_colors():
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
                        # if ch.strikethrough:    attrib |= curses.A_
                        if ch.fg in pyte_colors:
                            attrib |= curses.color_pair(pyte_colors[ch.fg])
                        if ch.bg in pyte_colors:
                            attrib |= curses.color_pair(pyte_colors[ch.bg])
                        window.addch(y, x, ch.data, attrib)
                    except Exception as _: pass
        try:
            window.move(screen.cursor.y, screen.cursor.x)
            window.refresh()
        except Exception as _: pass
    
    
    @abstractmethod
    def alt_scr(self, state = True, target: TextIO | None = None):
        pass
    
    
    @abstractmethod
    def set_echo(self, state = False, target: TextIO | None = None):
        pass
    
    
    def set_raw(self, state = True, target: TextIO | None = None):
        if target is None:
            target = self.src
            
        set_raw(target, self._old_term_attrib, state)