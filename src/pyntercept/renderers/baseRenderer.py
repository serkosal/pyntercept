from abc import ABC, abstractmethod
import sys
from typing import TextIO

class BaseRenderer(ABC):
    
    __slots__ = ('src', 'dest', 'err', 'render_data')
    
    src: TextIO
    dest: TextIO
    render_data: bytes
    
    def __init__(
        self, src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        self.src  = src   or sys.stdin
        self.dest = dest  or sys.stdout
        self.err  = err   or sys.stderr
        
    
    @abstractmethod
    def init(self):
        pass
    
    
    @abstractmethod
    def post_init(self, data: bytes):
        pass
    
    
    @abstractmethod
    def exit(self):
        pass
    
    
    @abstractmethod
    def update(self, data: bytes): 
        pass
    
    
    @abstractmethod
    def render(self): 
        pass
    
    
    @abstractmethod
    def alt_scr(self, state = True, target: TextIO | None = None):
        pass
    
    
    @abstractmethod
    def set_echo(self, state = False, target: TextIO | None = None):
        pass
    
    
    @abstractmethod
    def set_raw(self, state = True, target: TextIO | None = None):
        pass