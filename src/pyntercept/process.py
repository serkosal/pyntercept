from abc import ABC, abstractmethod
import termios
import os
import select
import sys
from typing import TextIO, Callable, Any
from types import TracebackType

from pyntercept.pseudo_tty import create_pty

type ProcessDestUpd     = Callable[["BasePTYProcess"], bytes]
type ProcessCB          = Callable[["BasePTYProcess"], None]
type ProcessPostInitCB  = Callable[["BasePTYProcess", bytes], None]

class BasePTYProcess(ABC):
    
    __slots__ = ('src', 'dest', 'err', 'on_parent_src_upd', 'on_child_out', 
        '_init_cb', '_post_init_cb', '_exit_cb', 'renderer', 'auto_render',
        'data'
    )
    
    src: TextIO
    dest: TextIO
    err: TextIO
    
    on_parent_src_upd:  ProcessDestUpd
    on_child_out:       ProcessDestUpd
    _init_cb:           ProcessCB
    _post_init_cb:      ProcessCB
    renderer:           ProcessCB
    
    data: dict[str, Any]
    
    def render(self) -> None:
        if self.renderer:
            self.renderer(self)
    
    def update(self) -> bool:
        return self.child_alive()
    
    
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


def default_on_src_upd(process: BasePTYProcess) -> bytes:
    '''Reads input from source (default stdin) and pass to the child.'''
    # data = process.src.read(2048).encode()  # read user input
    data = os.read(process.src.fileno(), 2048)
    process.write(data)                 # pass it into the child process
    
    return data


def default_on_child_out(process: BasePTYProcess) -> bytes:
    '''Does nothing, just reads data from child and returns it.'''
    
    return process.read()                 # read output from editor


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
        
        width: int | None = None,
        height: int | None = None,
        
        source:         TextIO | None = None, 
        destination:    TextIO | None = None,
        error:          TextIO | None = None,
        
        on_parent_src_upd:  ProcessDestUpd = default_on_src_upd,
        on_child_out_upd:   ProcessDestUpd = default_on_child_out,
        renderer:           ProcessCB | None = None,
        auto_render: bool = True,
        init_cb:            ProcessCB | None = None,
        post_init_cb:       ProcessCB | None = None,
        exit_cb:            ProcessCB | None = None,
    ):
        pid, parent_fd, child_fd = create_pty(argv)
        
        self._pid = pid
        
        self._parent_fd = parent_fd
        self._child_fd  = child_fd
        self.src     = source        or sys.stdin  
        self.dest    = destination   or sys.stdout
        self.err     = error         or sys.stderr
        
        self.on_parent_src_upd = on_parent_src_upd
        self.on_child_out      = on_child_out_upd
        self.renderer          = renderer
        self.auto_render       = auto_render
        self._post_init_cb     = post_init_cb
        self._init_cb          = init_cb
        self._exit_cb          = exit_cb
        self.data = {}
        
        if width is None or height is None:
            dest_fd = self.dest.fileno()
            rows, cols = termios.tcgetwinsize(dest_fd)
            
            width = width or cols
            height = height or rows
        
        self.set_size(width, height)
    
    
    def __enter__(self):
        self._init_cb(self)
        
        init_data = self.read()
        if self._post_init_cb:
            self._post_init_cb(self, init_data)
        return self
    
    
    def __exit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc: BaseException | None, 
        tb: TracebackType | None
    ) -> bool | None:
        self._exit_cb(self)
    
    
    
    def set_size(self, width = 60, height = 20):
        termios.tcsetwinsize(self._child_fd, (height, width))
    
    
    def get_size(self) -> tuple[int, int]:
        return termios.tcgetwinsize(self._child_fd)
    
    
    def child_alive(self) -> bool:
        # Availability: Unix, Windows, not WASI, not Android, not iOS.
        rpid, _ = os.waitpid(self._pid, os.WNOHANG)
        return rpid == 0
    
    
    def update(self) -> bool:
        if not super().update(): return False
        
        src_fd = self.src.fileno()
        # aks OS for file descriptors updates
        rlist, _, _ = select.select([src_fd, self._parent_fd], [], [], 0)
        
        return_status = True
        if src_fd in rlist:
            data = self.on_parent_src_upd(self)
            return_status *= bool(data)
        
        if return_status and self._parent_fd in rlist:
            data = self.on_child_out(self)
            if data and self.auto_render:
                self.render()
            return_status *= bool(data)
        
        return return_status
    
    
    def read(self) -> bytes:
        return os.read(self._parent_fd, 2048)
    
    
    def write(self, data: bytes) -> int:
        return os.write(self._parent_fd, data)