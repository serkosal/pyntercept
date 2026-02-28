from typing import TextIO

import pyte

from .mixins.unixBaseRendererMixin import UnixBaseRendererMixin
from .mixins.ansiRendererMixin import AnsiRendererMixin
from .mixins.pyteRendererMixin import PyteRendererMixin

class PyteRenderer(PyteRendererMixin, AnsiRendererMixin, UnixBaseRendererMixin):
    __slots__ = ('screen', 'stream')
    
    screen: pyte.Screen
    stream: pyte.ByteStream
    
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
    
    @classmethod
    def convert_pyte_color(s):
        try:
            int(s, 16)
            return '#' + s
        except ValueError:
            return s
    
    
    def __init__(self, 
        width, height, 
        src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(width, height, src, dest, err)
        
        
    def render(self):

        self.clear_scr()
        self.set_cursor(0, 0)
        
        for y in self.screen.buffer:
            line = self.screen.buffer[y]
            for x in line:
                ch = self.screen.buffer[y][x]
                if ch.data.isprintable():
                    # self.set_cursor(x, y)
                    self.dest.write(ch.data)
                else:
                    self.dest.write(' ')
            if y != len(self.screen.buffer) - 1: 
                self.dest.write('\r\n')
                # self.move_cursor(0, 1)

        # self.set_cursor(self.screen.cursor.x+1, self.screen.cursor.y+1)
        self.dest.flush()