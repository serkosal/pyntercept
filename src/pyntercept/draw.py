import sys
from typing import TextIO


def draw_data(data: bytes, dest: TextIO | None) -> None:
    if dest is None:
        dest = sys.stdout
    
    try:
        dest.write(data.decode())
        dest.flush()
    except Exception as e:
        print(f"An error occurred: {e}")
