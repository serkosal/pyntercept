from abc import ABC, abstractmethod
from typing import TextIO

class AbstractRenderer(ABC):
    '''Abstract base class for rendering.'''
    
    __slots__ = ()
    
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
    def move_cursor(self, dx, dy):
        pass
    
    
    @abstractmethod
    def set_cursor(self, x, y):
        pass
    
    
    @abstractmethod
    def clear_scr(self):
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