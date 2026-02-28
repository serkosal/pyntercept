from typing import TextIO

from .baseRendererMixin import BaseRendererMixin

class AnsiRendererMixin(BaseRendererMixin):
    
    def __init__(
        self, 
        src: TextIO | None = None, 
        dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(src, dest, err)
    
    
    def alt_scr(self, state = True, target: TextIO | None = None):
        if target is None:
            target = self.dest
        
        if state:
            target.write('\x1B[?1049h')
        else:
            target.write('\x1B[?1049l')
    
    
    def move_cursor(self, dx, dy):
        s: str = ''
        if dy > 0:
            s += f'\x1B[{dy}A'
        elif dy < 0:
            s += f'\x1B[{dy}B'
            
        if dx > 0:
            s += f'\x1B[{dx}C'
        elif dx < 0:
            s += f'\x1B[{dx}D'
            
        self.dest.write(s)
    
            
    def set_cursor(self, x, y):
        self.dest.write(f'\x1B[{y};{x}H') # move cursor to the position x,y
        
        
    def clear_scr(self):
        self.dest.write('\x1B[2J') # clear scr