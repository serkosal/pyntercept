import os
import sys

def alt_buffer_on(fd):
    pass


def alt_buffer_off(fd):
    pass


def draw_data(data: bytes, dest_fd: int | None = None) -> None:
    if dest_fd is None:
        dest_fd = sys.stdout.fileno()
    
    try:
        os.write(dest_fd, data)
        # sys.stdout.flush()
    except Exception as e:
        print(f"An error occurred: {e}")