from Rule import Rule
import re

FIGURE_COUNTER = 0
FIGURE_DICT = {}

SECTION_COUNTER = 0
SUBSECTION_COUNTER = 0
SUBSUBSECTION_COUNTER = 0

# TODO: Se livrar desse código duplicado
# TODO: Ambientes personalizados com contadores
# TODO: Metadados
# TODO: Ambiente com código

def pre_section(match: re.Match[str], string: str) -> str:
    global SECTION_COUNTER
    SECTION_COUNTER += 1
    return string


def post_section(match: re.Match[str], string: str) -> str:
    global SECTION_COUNTER
    string = re.sub("NUMHERE", f"{SECTION_COUNTER}. ", string)
    return string


H1 = Rule(
    "Header 1",
    r"^# (.+)$",
    r"<h1>NUMHERE\1</h1>",
    re.MULTILINE,
    pre_func=pre_section,
    post_func=post_section,
)


def pre_subsection(match: re.Match[str], string: str) -> str:
    # Incrementa o contador e adiciona uma entrada no dicionário
    global SUBSECTION_COUNTER
    SUBSECTION_COUNTER += 1
    return string


def post_subsection(match: re.Match[str], string: str) -> str:
    global SECTION_COUNTER, SUBSECTION_COUNTER
    string = re.sub("NUMHERE", f"{SECTION_COUNTER}.{SUBSECTION_COUNTER}. ", string)
    return string


H2 = Rule(
    "Header 2",
    r"^## (.+)$",
    r"<h2>NUMHERE\1</h2>",
    re.MULTILINE,
    pre_func=pre_subsection,
    post_func=post_subsection,
)


def pre_subsubsection(match: re.Match[str], string: str) -> str:
    # Incrementa o contador e adiciona uma entrada no dicionário
    global SUBSUBSECTION_COUNTER
    SUBSUBSECTION_COUNTER += 1
    return string


def post_subsubsubsection(match: re.Match[str], string: str) -> str:
    global SECTION_COUNTER, SUBSECTION_COUNTER, SUBSUBSECTION_COUNTER
    string = re.sub(
        "NUMHERE",
        f"{SECTION_COUNTER}.{SUBSECTION_COUNTER}.{SUBSUBSECTION_COUNTER}. ",
        string,
    )
    return string


H3 = Rule(
    "Header 3",
    r"^### (.+)$",
    r"<h3>NUMHERE\1</h3>",
    re.MULTILINE,
    pre_func=pre_subsubsection,
    post_func=post_subsubsubsection,
)


BOLD = Rule("Bold", r"\*\*(.*?)\*\*", r"<strong>\1</strong>")
ITALIC = Rule("Italic", r"\*(.*?)\*", r"<em>\1</em>")
DISPLAY_MATH = Rule("Display Math", r"\$\$(.+?)\$\$", r"\[\1\]", re.DOTALL)
INLINE_MATH = Rule("Inline Math", r"\$(.+?)\$", r"\(\1\)")

_special_patterns = r"#|\d\.|[-*]|\$\$|<figure|<p>"
_content = r"((?:(.+)\n)+)"
_paragraph = (
    r"(?<=\n\n)"  # Precisa ser precedido de uma linha vazia
    + f"(?!{_special_patterns + r"|[ ]{4}"})"  # Não pode começar com um pattern especial
    + _content  # Conteúdo do parágrafo
    + r"(?=\n)"
)  # Acaba quando uma linha vazia for encontrada
P = Rule("Paragraph", _paragraph, r"<p>\1</p>")

_paragraph_ident = (
    r"(?<=\n\n)" + r"(([ ]{4}" + f"(?!{_special_patterns})" + r".+\n)+)" + r"(?=\n)"
)
P_IDENT = Rule("Paragraph w Identation", _paragraph_ident, r"<p>\1</p>")

# Uma linha consiste em:
# - uma primeira linha não vazia
# - uma linha com 4 espaços iniciais e conteúdo
# - uma linha vazia
_ordered_item_lines = r"(.+\n([ ]{4}.+\n|\n)*)"
# Um conjunto de itens consiste em:
# - uma linha que começa com um digito+ponto e espacos vazios
# - uma linha da lista
_ordered_item = r"^\d+\.[ ]+" + _ordered_item_lines
_ordered_list = f"(({_ordered_item})+)"

ORDERED_LIST = Rule("Ordered List", _ordered_list, r"<ol>\1</ol>", re.MULTILINE)
ORDERED_ITEM = Rule("Ordered Item", _ordered_item, r"<li>\1</li>", re.MULTILINE)

# Uma linha consiste em:
# - uma primeira linha não vazia
# - uma linha com 4 espaços iniciais e conteúdo
# - uma linha vazia
_unordered_item_lines = _ordered_item_lines
# Um conjunto de itens consiste em:
# - uma linha que começa com um digito+ponto e espacos vazios
# - uma linha da lista
_unordered_item = r"^[-*][ ]+" + _unordered_item_lines
_unordered_list = f"(({_unordered_item})+)"

UNORDERED_LIST = Rule("Unordered List", _unordered_list, r"<ul>\1</ul>", re.MULTILINE)
UNORDERED_ITEM = Rule("Unordered Item", _unordered_item, r"<li>\1</li>", re.MULTILINE)


def pre_figure(match: re.Match[str], string: str) -> str:
    # Incrementa o contador e adiciona uma entrada no dicionário
    global FIGURE_COUNTER, FIGURE_DICT
    FIGURE_COUNTER += 1
    FIGURE_DICT[match.group(4)] = FIGURE_COUNTER
    return string


def post_figure(match: re.Match[str], string: str) -> str:
    global FIGURE_COUNTER
    fig_label = f"Fig. {FIGURE_COUNTER} - "
    string = re.sub("LABELHERE", fig_label, string)
    return string


_figure = r'<figure src="(.+)" size="(.+)" caption="(.+)" label="(.+)">'
_figure_repl = r'<figure><img src=\1 style="\2" id="fig-\4"><figcaption><span class="figurelabel">LABELHERE</span>\3</figcaption></figure>'
FIGURE = Rule(
    "Figure", _figure, _figure_repl, pre_func=pre_figure, post_func=post_figure
)


def post_reference(match: re.Match[str], string: str) -> str:
    # Obtém o número da referência
    global FIGURE_DICT
    try:
        fig_number = str(FIGURE_DICT[match.group(1)])
    except KeyError:
        fig_number = "??"
    string = re.sub("NUMHERE", fig_number, string)
    return string


REFERENCE = Rule(
    "Reference",
    r'<a label="(.+)" prefix="(.+)">',
    r'<a href="#fig-\1" class="reference">\2&nbsp;NUMHERE</a>',
    post_func=post_reference,
)


RULES = [
    P,
    P_IDENT,
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
    FIGURE,
    REFERENCE,
]
