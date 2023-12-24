import re

# Títulos
H1 = re.compile(r"^# (.+)$", re.MULTILINE)
H2 = re.compile(r"^## (.+)$", re.MULTILINE)
H3 = re.compile(r"^### (.+)$", re.MULTILINE)

# Negrito e itálico
BOLD = re.compile(r"\*\*(.*?)\*\*")
ITALIC = re.compile(r"\*(.*?)\*")

# Equações
INLINE_MATH = re.compile(r"\$(.*?)\$")
DISPLAY_MATH = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)

_ordered_item_lines = r"(.+(\n[ ]{4}.+\n|\n)*)"
_ordered_items = r"^\d+\.[ ]+" + _ordered_item_lines
ORDERED_LIST = re.compile(f"(({_ordered_items}" + r"\n?)+)", re.MULTILINE)
ORDERED_ITEM = re.compile(_ordered_items, re.MULTILINE)

_unordered_item_lines = _ordered_item_lines
_unordered_items = r"^[-*][ ]+" + _unordered_item_lines
UNORDERED_LIST = re.compile(f"(({_unordered_items}\n)+)", re.MULTILINE)
UNORDERED_ITEM = re.compile(_unordered_items, re.MULTILINE)

_special_starters = r"#|\d\.|[-*]"
_paragraph = r"(?:([ ]*)(.+)\n)+"
P = re.compile(r"(?<=\n\n)" + f"(?!{_special_starters})" + _paragraph + r"(?=\n)")

RULES = [
    P,
    H1,
    H2,
    H3,
    BOLD,
    ITALIC,
    INLINE_MATH,
    DISPLAY_MATH,
    ORDERED_LIST,
    ORDERED_ITEM,
    UNORDERED_LIST,
    UNORDERED_ITEM,
]
