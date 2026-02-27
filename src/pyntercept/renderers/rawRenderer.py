from typing import TextIO
import termios
import tty

from .baseRenderer import BaseRenderer

# from pyntercept.process import BasePTYProcess
# from pyntercept.tty_utils

class RawRenderer(BaseRenderer):
    
    __slots__ = ('_old_term_attrib')
    
    _old_term_attrib: dict[int, list] # fd -> old_settings
    
    def __init__(self, src: TextIO | None = None, dest: TextIO | None = None,
        err: TextIO | None = None
    ):
        super().__init__(src, dest, err)
        self._old_term_attrib = {}
    
    
    def update(self, data: bytes):
        self.render_data = data
    
     
    def alt_scr(self, state = True, target: TextIO | None = None):
        
        if target is None:
            target = self.dest
        
        if state:
            target.write('\x1B[?1049h')
        else:
            target.write('\x1B[?1049l')
        
        # os.write(, b'\x1B[?1049h')
    
    
    def set_echo(self, state = False, target: TextIO | None = None):
        
        if target is None:
            target = self.src
        
        fd = target.fileno()
        
        (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) \
            = termios.tcgetattr(fd)

        if state:
            lflag |= termios.ECHO
        else:
            lflag &= ~termios.ECHO

        new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        termios.tcsetattr(fd, termios.TCSANOW, new_attr)
    
    
    def set_raw(self, state = True, target: TextIO | None = None):
        if target is None:
            target = self.src
        
        fd = target.fileno()

        if state:
            self._old_term_attrib[fd] = termios.tcgetattr(fd)
            tty.setraw(fd)
        else:
            settings = self._old_term_attrib.pop(fd)
            termios.tcsetattr(target.fileno(), termios.TCSADRAIN, settings)
    
    
    def init(self):
        self.alt_scr()
        self.set_raw(True, self.src)
        self.set_raw(True, self.dest)
        self.set_echo(False)
    
    
    def post_init(self, data: bytes):
        self.update(data)
        self.render()
    
    
    def exit(self):
        self.alt_scr()
        self.set_raw(True, self.src)
        self.set_raw(True, self.dest)
        self.set_echo(False)
    
    
    def render(self):
        self.dest.write(self.render_data.decode())
        self.dest.flush()
        