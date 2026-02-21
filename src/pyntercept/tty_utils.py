import termios
import tty

def enter_raw_mode(fd):
    """Enters raw mode for the given file descriptor."""
    old_settings = termios.tcgetattr(fd) #
    tty.setraw(fd) #
    return old_settings


def exit_raw_mode(fd, settings):
    """Restores the terminal to its original settings."""
    termios.tcsetattr(fd, termios.TCSADRAIN, settings) #


def switch_echo(fd, enabled):
    (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) \
        = termios.tcgetattr(fd)

    if enabled:
        lflag |= termios.ECHO
    else:
        lflag &= ~termios.ECHO

    new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    termios.tcsetattr(fd, termios.TCSANOW, new_attr)
