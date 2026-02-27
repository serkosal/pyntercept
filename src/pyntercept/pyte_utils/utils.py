import pyte

from pyntercept.process import BasePTYProcess

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
    

def on_child_out_upd(pr: BasePTYProcess) -> bytes:
    data = pr.read()
    
    stream: pyte.ByteStream = pr.data["stream"]
    stream.feed(data)
    
    return data


def post_init(pr: BasePTYProcess, data: bytes):
    h, w = pr.get_size()
    pr.data["screen"] = pyte.Screen(w, h)
    pr.data["stream"] = pyte.ByteStream(pr.data["screen"])
    pr.data["stream"].feed(data)
    
    pr.render()