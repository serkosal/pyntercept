import os
import sys


def alt_buffer_on(fd):
    pass


def alt_buffer_off(fd):
    pass


def draw_data(data: bytes) -> None:
    try:
        os.write(sys.stdout.fileno(), data)
        # sys.stdout.flush()
    except Exception as e:
        print(f"An error occurred: {e}")