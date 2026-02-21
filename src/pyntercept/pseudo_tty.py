import pty
import os
import errno


# code is mainly taken away from ptyprocess
# 

def pty_make_controlling_tty(tty_fd):
    child_name = os.ttyname(tty_fd)
        
    # Disconnect from controlling tty, if any.  Raises OSError of ENXIO
    # if there was no controlling tty to begin with, such as when
    # executed by a cron(1) job.
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
        os.close(fd)
    except OSError as err:
        if err.errno != errno.ENXIO:
            raise
            
    os.setsid()

    # Verify we are disconnected from controlling tty by attempting to open
    # it again.  We expect that OSError of ENXIO should always be raised.
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
        os.close(fd)
        raise RuntimeError("OSError of errno.ENXIO should be raised.")
    except OSError as err:
        if err.errno != errno.ENXIO:
            raise
    
    # Verify we can open child pty.
    fd = os.open(child_name, os.O_RDWR)
    os.close(fd)

    # Verify we now have a controlling tty.
    fd = os.open("/dev/tty", os.O_WRONLY)
    os.close(fd)


def create_pty(argv: list[str]) -> tuple[int, int, int]:
    parent_fd, child_fd = os.openpty()
    
    if parent_fd < 0 or child_fd < 0:
        raise OSError("os.openpty() failed")
    
    pid = os.fork()
    if pid == pty.CHILD:
        os.close(parent_fd)
        pty_make_controlling_tty(child_fd)
        
        os.dup2(child_fd, pty.STDIN_FILENO)
        os.dup2(child_fd, pty.STDOUT_FILENO)
        os.dup2(child_fd, pty.STDERR_FILENO)
        
        os.execlp(argv[0], *argv)
    # we keep child_fd opening to be able to resize it
    # else: 
    #     os.close(child_fd)
        
    return pid, parent_fd, child_fd

