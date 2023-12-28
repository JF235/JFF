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

# Uma linha consiste em:
# - uma primeira linha não vazia
# - uma linha com 4 espaços iniciais e conteúdo
# - uma linha vazia
_ordered_item_lines = r"(.+\n([ ]{4}.+\n|\n)*)"
# Um conjunto de itens consiste em:
# - uma linha que começa com um digito+ponto e espacos vazios
# - uma linha da lista
_ordered_items = r"^\d+\.[ ]+" + _ordered_item_lines
# Uma lista consiste em diversos itens
ORDERED_LIST = re.compile(f"(({_ordered_items})+)", re.MULTILINE)
ORDERED_ITEM = re.compile(_ordered_items, re.MULTILINE)

_unordered_item_lines = _ordered_item_lines
_unordered_items = r"^[-*][ ]+" + _unordered_item_lines
UNORDERED_LIST = re.compile(f"(({_unordered_items})+)", re.MULTILINE)
UNORDERED_ITEM = re.compile(_unordered_items, re.MULTILINE)

_special_starters = r"#|\d\.|[-*]|<figure"
_paragraph = r"((?:([ ]*)(.+)\n)+)"
P = re.compile(r"(?<=\n\n)" + f"(?!{_special_starters})" + _paragraph + r"(?=\n)")

FIGURE = re.compile(r'<figure src="(.+)" size="(.+)" caption="(.+)" label="(.+)">')

REFERENCE = re.compile(r'<a label="(.+)" prefix="(.+)">')

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
