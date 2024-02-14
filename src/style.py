import re
from jff_globals import METADATA

def add_style(stylesheet: str, string: str) -> str:
    match = re.search("/[*] STYLEHERE [*]/", string)
    if match:
        style = ""
        with open(stylesheet) as file:
            style = file.read()
        string = (
            string[: match.start()]
            + style
            + "\n/* STYLEHERE */"
            + string[match.end() :]
        )
    return string

def add_default_style(string: str) -> str:
    return add_style(METADATA["STYLESHEET"], string)