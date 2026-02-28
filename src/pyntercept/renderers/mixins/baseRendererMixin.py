from typing import TextIO
import sys

from ..abstractRenderer import AbstractRenderer

class BaseRendererMixin(AbstractRenderer):
    src: TextIO
    dest: TextIO
    err: TextIO
    
    def __init__(
        self, 
        src: TextIO | None = None, 
        dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__()
        self.src  = src   or sys.stdin
        self.dest = dest  or sys.stdout
        self.err  = err   or sys.stderr

     
    def init(self):
        self.alt_scr()
        self.set_raw(True, self.src)
        self.set_raw(True, self.dest)
        self.set_echo(False)
    
    
    def post_init(self, data: bytes):
        self.update(data)
        self.render()
    
    
    def exit(self):
        self.alt_scr()
        self.set_raw(True, self.src)
        self.set_raw(True, self.dest)
        self.set_echo(False)