import pyte

from rich.text import Text as rText
from rich.console import Console as rConsole
from rich.control import Control as rControl

from pyntercept.pyte_utils.utils import convert_pyte_color

def draw_pyte_scr_rich(
    screen: pyte.Screen,
    console: rConsole
) -> None:    
    console.control(rControl.home())
    console.control(rControl.clear())
    
    rtext = rText(end='')
    for y, line in screen.buffer.items():
        for x in line:
            ch = screen.buffer[y][x]
            fg = convert_pyte_color(ch.fg)
            bg = convert_pyte_color(ch.bg)
            rtext.append(ch.data, f'{fg} on {bg}')
        
        rtext.append('\r\n')
    
    console.print(rtext, end='')
    console.control(rControl.move_to(screen.cursor.x, screen.cursor.y))