from rule import Rule
import re

_empty_space = r"(?<=[ ]|\n)"
DISPLAY_MATH = Rule(
    "Display Math", _empty_space + r"\$\$(.+?)\$\$", r"\[\1\]", re.DOTALL
)
INLINE_MATH = Rule("Inline Math", _empty_space + r"\$(.+?)\$", r"\(\1\)")

# Deve ser aplicada antes que as últimas duas
NUMBERED_MATH = Rule(
    "Numbered Math", _empty_space + r"\\\[(.+?)\\\]", '<div COUNTER(EQ,+) id="eq-numCOUNTER(EQ,=)">\n' + r"\\[\n\1\n\\tag{COUNTER(EQ,=)}\\]\n" + "</div>", re.DOTALL
)
