from abc import ABC, abstractmethod
import termios
import os
import select
import sys
from typing import Protocol, TextIO
from types import TracebackType

from pyntercept.pseudo_tty import create_pty

class FD_UpdCallback(Protocol):
    def __call__(self, process: "PTYProcess", *args, **kwargs) -> bytes | None: 
        ...


class BasePTYProcess(ABC):
    
    __slots__ = ('src_fd', 'dest_fd', 'err_fd', 'on_parent_src_upd', 
        'on_parent_src_upd', 'on_child_out'
    )
    
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
    def update(self, *args, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def read(self) -> bytes:
        pass
    
    @abstractmethod
    def write(self) -> int:
        pass


def default_on_src_upd(process: BasePTYProcess, *args, **kwargs) -> bytes:
    '''Reads input from source (default stdin) and pass to the child.'''
    data = os.read(process.src_fd, 2048)   # read user input
    process.write(data)     # pass it into the child process
    
    return data


def default_on_child_out(process: BasePTYProcess, *args, **kwargs) -> bytes:
    '''Does nothing, just reads data from child and returns it.'''
    
    return process.read()                 # read output from editor


class PTYProcess(BasePTYProcess):
    '''Encapsulate child process and PTY related utilities.   
    '''
    
    __slots__ = ('_pid', '_parent_fd', '_child_fd')
    
    def __init__(
        self, 
        argv: list[str], 
        
        width: int | None = None, 
        height: int | None = None,
        
        source:         TextIO | None = None, 
        desination:     TextIO | None = None, 
        error:          TextIO | None = None,
        
        on_parent_src_upd: FD_UpdCallback = default_on_src_upd,
        on_child_out_upd:  FD_UpdCallback = default_on_child_out,
    ):
        pid, parent_fd, child_fd = create_pty(argv)
        
        self._pid = pid
        
        self._parent_fd = parent_fd
        self._child_fd  = child_fd
        self.src_fd     = (source        or sys.stdin).fileno() 
        self.dest_fd    = (desination    or sys.stdout).fileno()
        self.err_fd     = (error         or sys.stderr).fileno()
        
        self.on_parent_src_upd = on_parent_src_upd
        self.on_child_out      = on_child_out_upd
        
        if width is None or height is None:
            rows, cols = termios.tcgetwinsize(self.dest_fd)
            
            width = width or cols
            height = height or rows
        
        self.set_size(width, height)
    
    
    # def __enter__(self):
    #     pass
    
    
    # def __exit__(
    #     self, 
    #     exc_type: type[BaseException] | None, 
    #     exc: BaseException | None, 
    #     tb: TracebackType | None
    # ) -> bool | None:
    #     pass
    
    
    
    def set_size(self, width = 60, height = 20):
        termios.tcsetwinsize(self._child_fd, (height, width))
    
    
    def get_size(self) -> tuple[int, int]:
        return termios.tcgetwinsize(self._child_fd)
    
    
    def child_alive(self) -> bool:
        # Availability: Unix, Windows, not WASI, not Android, not iOS.
        rpid, _ = os.waitpid(self._pid, os.WNOHANG)
        return rpid == 0
    
    
    def update(self, *args, **kwargs) -> bool:
        # aks OS for file descriptors updates
        rlist, _, _ = select.select([self.src_fd, self._parent_fd], [], [], 0)
        
        # returns False if process terminated
        if not self.child_alive():
            return False
        
        return_status = True
        if self.src_fd in rlist:
            data = self.on_parent_src_upd(self, *args, **kwargs)
            return_status *= bool(data)
        
        if self._parent_fd in rlist:
            data = self.on_child_out(self, *args, **kwargs)
            return_status *= bool(data)
            
        return return_status
    
    
    def read(self) -> bytes:
        return os.read(self._parent_fd, 2048)
    
    
    def write(self, data: bytes) -> int:
        return os.write(self._parent_fd, data)