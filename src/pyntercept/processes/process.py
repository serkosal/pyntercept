import termios
import os
import select
from typing import TextIO

from pyntercept.pseudo_tty import create_pty
from pyntercept.renderers.abstractRenderer import AbstractRenderer
from .basePty import BasePTYProcess, DataHandler

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
        
        renderer: AbstractRenderer,
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