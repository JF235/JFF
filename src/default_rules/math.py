from rule import Rule
from jff_globals import METADATA
import re

METADATA["COUNTERS"] += ", EQ"
METADATA.update(
    {
        "EQ_FORMAT": r"'COUNTER(EQ,=)'",
        "EQ_REF": r"'Eq.&nbsp;COUNTER(EQ,=,\1)'",
    }
)


_empty_space = r"(?<=[ ]|\n)"
DISPLAY_MATH = Rule(
    "Display Math", _empty_space + r"\$\$(.+?)\$\$", r"\[\1\]", re.DOTALL
)
INLINE_MATH = Rule("Inline Math", _empty_space + r"\$(.+?)\$", r"\(\1\)")


def numbered_math_formatting(self: Rule, match) -> str:
    if match.group(2):
        replace = (
            f'<div COUNTER(EQ,+,{match.group(2)}) id="{match.group(2)}">'
            + "\n"
            + r"\\[\n\1\n\\tag{"
            + METADATA["EQ_FORMAT"].strip("'")
            + r"}\\]\n"
            + "</div>"
        )
    else:
        replace = (
            "<div COUNTER(EQ,+)>"
            + "\n"
            + r"\\[\n\1\n\\tag{"
            + METADATA["EQ_FORMAT"].strip("'")
            + r"}\\]\n"
            + "</div>"
        )
    replace = match.expand(replace)

    return replace


# Deve ser aplicada antes que as últimas duas
NUMBERED_MATH = Rule(
    "Numbered Math",
    _empty_space + r"\\\[(.+?)\\\]" + r"(?:\\label{(.+?)})?",
    "",
    re.DOTALL,
    formatting=numbered_math_formatting,
)
