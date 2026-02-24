_CONTROL_STRIP_TRANSLATE = {
    7 : None, # Bell
    8 : None, # Backspace
    11: None,  # Vertical tab
    12: None,  # Form feed
    # 13: None,  # Carriage return
}

def patched_strip_control_codes(
    text: str, _translate_table: dict[int, None] = _CONTROL_STRIP_TRANSLATE
) -> str:
    return text.translate(_translate_table)

import rich.control
rich.control.strip_control_codes = patched_strip_control_codes

# strip_control_codes = patched_strip_control_codes
