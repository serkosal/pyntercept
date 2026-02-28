from typing import TextIO

# Availability Unix: Linux, MacOS, iOS, android
import termios 
import tty

from .mixins.unixBaseRendererMixin import UnixBaseRendererMixin
from .mixins.ansiRendererMixin import AnsiRendererMixin
from .mixins.rawRendererMixin import RawRendererMixin

class UnixRenderer(UnixBaseRendererMixin, RawRendererMixin, AnsiRendererMixin):
    

    def __init__(self, src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(src, dest, err)
    
    
    def set_echo(self, state = False, target: TextIO | None = None):
        
        if target is None:
            target = self.src
        
        (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) \
            = termios.tcgetattr(target)

        if state:
            lflag |= termios.ECHO
        else:
            lflag &= ~termios.ECHO

        new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        termios.tcsetattr(target, termios.TCSANOW, new_attr)
    
    
    def set_raw(self, state = True, target: TextIO | None = None):
        
        if target is None:
            target = self.src

        if state:
            self._old_term_attrib[target] = termios.tcgetattr(target)
            tty.setraw(target)
        else:
            settings = self._old_term_attrib.pop(target)
            termios.tcsetattr(target.fileno(), termios.TCSADRAIN, settings)
    

