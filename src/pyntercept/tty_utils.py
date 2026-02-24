import termios
import tty
import os
from typing import TextIO

def enter_raw_mode(target: TextIO):
    """Enters raw mode for the given file descriptor."""
    
    fd = target.fileno()
    
    old_settings = termios.tcgetattr(fd) #
    tty.setraw(fd) #
    return old_settings


def alternate_scr_on(target: TextIO):
    os.write(target.fileno(), b'\x1B[?1049h')


def alternate_scr_off(target: TextIO):
    os.write(target.fileno(), b'\x1B[?1049l')


def exit_raw_mode(target: TextIO, settings):
    """Restores the terminal to its original settings."""
    termios.tcsetattr(target.fileno(), termios.TCSADRAIN, settings) #


def switch_echo(target: TextIO, enabled):
    fd = target.fileno()
    
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) \
        = termios.tcgetattr(fd)

    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)
