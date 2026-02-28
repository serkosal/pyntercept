from typing import TextIO

import pyte

from .baseRendererMixin import BaseRendererMixin

class PyteRendererMixin(BaseRendererMixin):

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
        super().__init__(src, dest, err)
        
        self.screen = pyte.Screen(width, height)
        self.stream = pyte.ByteStream(self.screen)
    
    
    def update(self, data: bytes):
        self.stream.feed(data)