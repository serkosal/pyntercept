pyte_colors = {
    "black": 0,
    "red": 1,
    "yellow": 2,
    "green": 3,
    "blue": 4,
    "cyan": 5,
    "magenta": 6,
    "white": 7
}


def convert_pyte_color(s: str) -> str:
    try:
        int(s, 16)
        return '#' + s
    except ValueError:
        return s

