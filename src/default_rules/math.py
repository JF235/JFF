from rule import Rule
import re

_empty_space = r"(?<=[ ]|\n)"
DISPLAY_MATH = Rule("Display Math", _empty_space + r"\$\$(.+?)\$\$", r"\[\1\]", re.DOTALL)
INLINE_MATH = Rule("Inline Math", _empty_space + r"\$(.+?)\$", r"\(\1\)")
