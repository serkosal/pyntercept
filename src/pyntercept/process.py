from abc import ABC, abstractmethod
import termios
import os
import select
import sys
from typing import TextIO, Callable, Any
from types import TracebackType

from pyntercept.pseudo_tty import create_pty
from pyntercept.renderers.baseRenderer import BaseRenderer

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
    renderer:       BaseRenderer
    
    
    def __init__(self,
        renderer: BaseRenderer,
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


class PTYProcess(BasePTYProcess):
    '''Encapsulate child process and PTY related utilities.   
    '''
    
    __slots__ = ('_pid', '_parent_fd', '_child_fd')
    
    _pid: int
    _parent_fd: int
    _child_fd: int
    
    def __init__(
        self, 
        argv: list[str],
        
        renderer: BaseRenderer,
        auto_render: bool = True,
        
        width: int | None = None,
        height: int | None = None,
        
        source:         TextIO | None = None, 
        destination:    TextIO | None = None,
        error:          TextIO | None = None,
        
        src_transforms: list[DataHandler] = [],
        out_transforms: list[DataHandler] = [],
    ):
        pid, parent_fd, child_fd = create_pty(argv)
        
        self._pid = pid
        
        self._parent_fd = parent_fd
        self._child_fd  = child_fd
        
        super().__init__(renderer, auto_render, width, height, 
            source, destination, error, src_transforms, out_transforms
        )
    
    
    def set_size(self, width = 60, height = 20):
        termios.tcsetwinsize(self._child_fd, (height, width))
    
    
    def get_size(self) -> tuple[int, int]:
        return termios.tcgetwinsize(self._child_fd)
    
    
    def child_alive(self) -> bool:
        # Availability: Unix, Windows, not WASI, not Android, not iOS.
        rpid, _ = os.waitpid(self._pid, os.WNOHANG)
        return rpid == 0
    
    
    def update(self, *args, **kwargs) -> bool:
        if not super().update(*args, **kwargs): return False
        
        src_fd = self.src.fileno()
        # ask OS for file descriptors updates
        rlist, _, _ = select.select([src_fd, self._parent_fd], [], [], 0)
        
        status = True
        if src_fd in rlist:
            status *= self.on_src_upd(*args, **kwargs)
        
        if self._parent_fd in rlist:
            status *= self.on_child_out(*args, **kwargs)
        
        return status
    
    
    def read(self) -> bytes:
        return os.read(self._parent_fd, 2048)
    
    
    def write(self, data: bytes) -> int:
        return os.write(self._parent_fd, data)