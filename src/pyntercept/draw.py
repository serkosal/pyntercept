import sys
from typing import TextIO


from pyntercept.pyte_utils.utils import pyte_colors

def draw_data(data: bytes, dest: TextIO | None) -> None:
    if dest is None:
        dest = sys.stdout
    
    try:
        dest.write(data.decode())
    except Exception as e:
        print(f"An error occurred: {e}")
