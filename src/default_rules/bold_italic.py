from rule import Rule

_empty_space = r"(?<=[ ]|\n)"
BOLD = Rule("Bold", _empty_space + r"\*\*(.*?)\*\*", r"<strong>\1</strong>")
ITALIC = Rule("Italic",  _empty_space + r"\*(.*?)\*", r"<em>\1</em>")
