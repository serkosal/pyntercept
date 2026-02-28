from abc import ABC, abstractmethod
import termios
from types import TracebackType
from typing import TextIO, Callable
import sys
import os

from pyntercept.renderers.abstractRenderer import AbstractRenderer 

type DataHandler = Callable[[bytes], bytes]

class BasePTYProcess(ABC):
    
    __slots__ = ('src', 'dest', 'err',
        'src_transforms', 'out_transforms', 
        'renderer', 'auto_render',
    )
    
    src: TextIO
    dest: TextIO
    err: TextIO
    
    src_transforms: list[DataHandler]
    out_transforms: list[DataHandler]
    renderer:       AbstractRenderer
    
    
    def __init__(self,
        renderer: AbstractRenderer,
        auto_render: bool,
        width: int | None = None,
        height: int | None = None,
        
        source: TextIO | None = None,
        destination: TextIO | None = None,
        error: TextIO | None = None,
        
        src_transforms: list[DataHandler] = [],
        out_transforms: list[DataHandler] = [],
    ):
        self.renderer = renderer
        self.auto_render = auto_render
        
        self.src     = source        or sys.stdin
        self.dest    = destination   or sys.stdout
        self.err     = error         or sys.stderr
        
        self.src_transforms = src_transforms
        self.out_transforms = out_transforms
        
        if width is None or height is None:
            dest_fd = self.dest.fileno()
            rows, cols = termios.tcgetwinsize(dest_fd)
            
            width = width or cols
            height = height or rows
        
        self.set_size(width, height)
    
    
    def update(self, *args, **kwargs) -> bool:
        return self.child_alive()
    
    
    def on_src_upd(self, *args, **kwargs) -> bool:        
        # data = process.src.read(2048).encode()  # read user input
        data = os.read(self.src.fileno(), 2048)
        
        for transform in self.src_transforms:
            data = transform(data, *args, **kwargs)
        
        self.write(data)
        
        return True
    
    
    def on_child_out(self, *args, **kwargs) -> bool:
        data = self.read()
        
        status = bool(data)
                
        for transform in self.out_transforms:
            data = transform(data, *args, **kwargs)

        if data:
            self.renderer.update(data)
            if self.auto_render:
                self.renderer.render()
                
        return status

    
    def __enter__(self):
        self.renderer.init()
        
        init_data = self.read()
        self.renderer.post_init(init_data)
        
        return self
    
    
    def __exit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc: BaseException | None, 
        tb: TracebackType | None
    ) -> bool | None:
        self.renderer.exit()
    
    
    @abstractmethod
    def set_size(self, width, height) -> None: 
        pass
    
    @abstractmethod
    def get_size(self, width, height) -> tuple[int, int]:
        '''Returns size as tuple[height, width].'''
        pass
    
    @abstractmethod
    def child_alive(self) -> bool:
        pass
    
    @abstractmethod
    def read(self) -> bytes:
        pass
    
    @abstractmethod
    def write(self) -> int:
        pass

