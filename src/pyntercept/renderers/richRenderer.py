from typing import TextIO

from rich.console import Console as rConsole
from rich.control import Control
from rich.text import Text as rText
from rich.style import Style as rStyle
from rich.errors import MissingStyle
from rich.color import Color, ColorParseError

from .mixins.pyteRendererMixin import PyteRendererMixin
from .mixins.unixBaseRendererMixin import UnixBaseRendererMixin


class RichRenderer(PyteRendererMixin, UnixBaseRendererMixin):
    
    def __init__(self, 
        width, height, src: TextIO | None = None, 
        dest: TextIO | None = None, err: TextIO | None = None
    ):
        super().__init__(width, height, src, dest, err)
        self.rconsole = rConsole(
            width=width, height=height,
            # force_terminal=True,
            # force_interactive=True,
        )
    
    
    def init(self):
        self.alt_scr(True, self.dest)
        self.set_cbreak(True, self.src)
        self.set_cbreak(True, self.dest)
        # self.set_raw(True, self.dest)
        self.set_echo(False)
    
    def exit(self):
        self.alt_scr(False, self.dest)
        self.set_cbreak(False, self.src)
        self.set_cbreak(False, self.dest)
        # self.set_raw(False, self.dest)
        self.set_echo(True)
    
    
    def alt_scr(self, state=True, target = None):
        self.rconsole.set_alt_screen(state)
    
    
    def clear_scr(self):
        self.rconsole.clear()
    
    
    def move_cursor(self, dx, dy):
        self.screen.cursor.x += dx
        self.screen.cursor.y += dy
        self.rconsole.control(Control.move(dx, dy))
        
        
    def set_cursor(self, x, y):
        self.rconsole.control(Control.move_to(x, y))
        self.screen.cursor.x = x
        self.screen.cursor.y = y
        
    
    def render(self):
        self.move_cursor(0, 0)
        self.clear_scr()
        
        rtext = rText(end='')
        
        for y, line in self.screen.buffer.items():
            for x in line:
                ch = self.screen.buffer[y][x]
                
                if ch.data.isprintable() and not ch.data.isspace():
                    fg = self.convert_pyte_color(ch.fg)
                    bg = self.convert_pyte_color(ch.bg)
                    try: 
                        rstyle = rStyle(color=fg, bgcolor=bg)
                        rtext.append(ch.data, rstyle)
                    except (MissingStyle, ColorParseError):
                        rtext.append(ch.data, 'white on default')
                else:
                    bg = self.convert_pyte_color(ch.bg)
                    try: 
                        rstyle = rStyle(bgcolor=bg)
                        rtext.append(' ', rstyle)
                    except (MissingStyle, ColorParseError):
                        rtext.append(' ', 'on default')
            rtext.append('\n')
        
        self.rconsole.print(rtext, end='', no_wrap=True)
        self.set_cursor(self.screen.cursor.x, self.screen.cursor.y)