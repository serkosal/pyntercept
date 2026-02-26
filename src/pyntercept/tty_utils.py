import termios
import sys
import tty
import os

def enter_raw_mode(target = sys.stdin):
    """Enters raw mode for the given file descriptor."""
    
    fd = target.fileno()

    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    
    return old_settings


def alternate_scr_on(target = sys.stdout):
    os.write(target.fileno(), b'\x1B[?1049h')


def alternate_scr_off(target = sys.stdout):
    os.write(target.fileno(), b'\x1B[?1049l')


def exit_raw_mode(settings, target = sys.stdin):
    """Restores the terminal to its original settings."""
    termios.tcsetattr(target.fileno(), termios.TCSADRAIN, settings) #


def switch_echo(enabled: bool = True, target = sys.stdin):
    fd = target.fileno()
    
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) \
        = termios.tcgetattr(fd)

    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)
