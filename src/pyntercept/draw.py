from pyntercept.process import BasePTYProcess


def draw_data(pr: BasePTYProcess) -> None:
    data = pr.data["data"]
    
    try:
        pr.dest.write(data.decode())
        pr.dest.flush()
    except Exception as e:
        print(f"An error occurred: {e}")
