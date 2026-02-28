from typing import TextIO

from .baseRendererMixin import BaseRendererMixin

class RawRendererMixin(BaseRendererMixin):
    
    # __slots__ = ('render_data')
    
    render_data: bytes
    
    def __init__(
        self, 
        src: TextIO | None = None, 
        dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(src, dest, err)
        self.render_data = b''
    
    def update(self, data: bytes):
        self.render_data = data
    
    
    def render(self):
        self.dest.buffer.write(self.render_data)
        self.dest.buffer.flush()
    