from collections.abc import Callable, Awaitable
import termios
import os
import select
import sys
from typing import Self

from pyntercept.pseudo_tty import create_pty

class PTYProcess:
    # width: int
    # height: int
    
    def __init__(
        self, 
        argv: list[str], 
        
        width: int | None = None, height: int | None = None,
        
        in_fd: int | None = None, out_fd: int | None = None, 
        err_fd: int | None = None,
        
        in_upd_callback: Callable[ [Self], bytes | None] | None = None,
        out_upd_callback: Callable[ [Self], bytes | None] | None = None,
    ):
        pid, master_fd, child_fd = create_pty(argv)
        
        self.pid = pid
        self.master_fd = master_fd
        self.child_fd = child_fd
        
        self.in_fd  = (in_fd or sys.stdin.fileno())
        self.out_fd = (out_fd or sys.stdout.fileno())
        self.err_fd = (err_fd or sys.stderr.fileno())
        
        self.in_upd_callback = in_upd_callback
        self.out_upd_callback = out_upd_callback
        
        if width is None or height is None:
            rows, cols = termios.tcgetwinsize(sys.stdout.fileno())
            
            width = width or cols
            height = height or rows
        
        self.set_size(width, height)
    
    
    def set_size(self, width = 60, height = 20):
        termios.tcsetwinsize(self.child_fd, (height, width))
    
    
    def get_size(self) -> tuple[int, int]:
        return termios.tcgetwinsize(self.child_fd)
    
    
    def child_alive(self) -> bool:
        # Availability: Unix, Windows, not WASI, not Android, not iOS.
        rpid, _ = os.waitpid(self.pid, os.WNOHANG)
        return rpid == 0
    
    
    def update(self) -> bool:
        # returns False if process terminated
        
        if not self.child_alive():
            return False
            
        # aks OS for file descriptors updates
        rlist, _, _ = select.select([self.in_fd, self.master_fd], [], [], 0)
        
        return_status = True
        if self.in_fd in rlist:
            if self.in_upd_callback:
                res = self.in_upd_callback(self)
            else:    
                res = self.on_in_fd_upd()
            return_status *= res is not None
            
        if self.master_fd in rlist:
            if self.out_upd_callback:
                res = self.out_upd_callback(self)
            else:
                res = self.on_out_fd_upd()
            return_status *= res is not None
            
        return return_status
    
    
    def on_in_fd_upd(process) -> bytes:
        data =  os.read(process.in_fd, 2048)    # read user input
        os.write(process.master_fd, data)       # pass input into editor process
        
        return data
    
    
    def on_out_fd_upd(process) -> bytes:
        return os.read(process.master_fd, 2048) # read output from editor