from typing import TextIO

import pyte

from .baseRendererMixin import BaseRendererMixin

class PyteRendererMixin(BaseRendererMixin):

    screen: pyte.Screen
    stream: pyte.ByteStream
    
    @classmethod
    def convert_pyte_color(self, s):
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