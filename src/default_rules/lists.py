from rule import Rule
import re


def list_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    """
    Ajustar quebra de linhas
    """
    replace = match.expand(self.repl)
    match = re.search(r"(<[ou]l>)(.+?)(</[ou]l>)", replace, re.DOTALL)
    if match:
        replace = match.expand(r"\1" + "\n\n" + r"\2" + r"\3" + "\n\n")
    return replace


def item_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    replace = match.expand(self.repl)
    match = re.search(r"(<li>)(.+?)(</li>)", replace, re.DOTALL)
    if match:
        middle = match.group(2).rstrip("\n")
        replace = match.group(1) + "\n" + middle + "\n" + match.group(3) + "\n\n"
    return replace


_ordered_item_lines = r"(.+\n([ ]{4}.+\n|\n)*)"
_ordered_item = r"^\d+\.[ ]+" + _ordered_item_lines
_ordered_list = f"(({_ordered_item})+)"

ORDERED_LIST = Rule(
    "Ordered List",
    _ordered_list,
    r"<ol>\1</ol>",
    re.MULTILINE,
    formatting=list_formatting,
)

ORDERED_ITEM = Rule(
    "Ordered Item",
    _ordered_item,
    r"<li>\1</li>",
    re.MULTILINE,
    formatting=item_formatting,
)

_unordered_item_lines = _ordered_item_lines
_unordered_item = r"^[-*][ ]+" + _unordered_item_lines
_unordered_list = f"(({_unordered_item})+)"

UNORDERED_LIST = Rule(
    "Unordered List",
    _unordered_list,
    r"<ul>\1</ul>",
    re.MULTILINE,
    formatting=list_formatting,
)

UNORDERED_ITEM = Rule(
    "Unordered Item",
    _unordered_item,
    r"<li>\1</li>",
    re.MULTILINE,
    formatting=item_formatting,
)
