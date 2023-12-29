import re

def rawString(string: str) -> str:
    return repr(string)[1:-1]

class Rule:
    def __init__(
        self, name: str, pattern: str, repl: str, flags: re.RegexFlag = re.NOFLAG
    ):
        self.name = name
        self.pattern = re.compile(pattern, flags)
        self.repl = repl

    def __repr__(self):
        return f"Rule({self.name}, {self.get_pattern_string()})"

    def apply(self, string: str) -> str:
        """Aplica a regra na `string`. Aplicar a regra consiste em:
        - Encontrar o padrão com `self.pattern`
        - Substituir o padrão com `self.repl`

        Args:
            string (str): String que é alvo da aplicação da regra
        """

        # Cria a cópia da string
        new_string = string
        match = self.pattern.search(new_string)
        span = (0, 0)
        while match:
            # Resultado encontrado (match != None)
            new_string, span = self.replace(match, new_string)
            match = self.pattern.search(new_string, span[1])
        return new_string

    def replace(self, match: re.Match[str], string: str) -> tuple[str, tuple[int, int]]:
        """Substitui na `string` o padrão `match` por `self.repl` com
        as devidas substituições de grupos.

        Args:
            match (re.Match[str]): Padrão encontrado
            string (str): String onde será feita a substituição

        Returns:
            str: _description_
        """
        pos, endpos = match.span()
        replace = match.expand(self.repl)
        replace = self.strip(replace)
        replace = self.pad(replace)
        new_string = string[:pos] + replace + string[endpos:]
        return new_string, (pos, pos + len(replace))

    def strip(self, string: str) -> str:
        new_string = string
        if self.name == "Paragraph" or self.name == "Paragraph w Identation":
            match = re.search(r"(.*?)(<p>)(.+?)(</p>)(.*)", string, re.DOTALL)
            if match:
                middle = match.group(3)
                middle = middle.rstrip("\n")
                middle = middle.lstrip()
                new_string = match.expand(r"\1\2" + rawString(middle) + r"\4\5")
        elif self.name == "Ordered Item" or self.name == "Unordered Item":
            match = re.search(r"(.*?)(<li>)(.+?)(</li>)(.*)", string, re.DOTALL)
            if match:
                middle = match.group(3)
                middle = middle.rstrip("\n")
                new_string = match.expand(r"\1\2" + rawString(middle) + r"\4\5")

        return new_string

    def pad(self, string: str) -> str:
        new_string = string
        if self.name == "Paragraph":
            new_string = new_string + "\n"
        elif self.name == "Paragraph w Identation":
            new_string = (" " * 4) + new_string + "\n"
        elif self.name == "Ordered List" or self.name == "Unordered List":
            match = re.search(r"(.*?)(<[ou]l>)(.+?)(</[ou]l>)(.*)", string, re.DOTALL)
            if match:
                new_string = match.expand(r"\1\2" + "\n\n" + r"\3" + r"\4\5" + "\n\n")
        elif self.name == "Ordered Item" or self.name == "Unordered Item":
            match = re.search(r"(.*?)(<li>)(.+?)(</li>)(.*)", string, re.DOTALL)
            if match:
                new_string = match.expand(r"\1\2" + r"\3" + "\n" + r"\4\5" + "\n\n")

        return new_string

    def get_pattern_string(self) -> str:
        return self.pattern.pattern


H1 = Rule("Header 1", r"^# (.+)$", r"<h1>\1</h1>", re.MULTILINE)
H2 = Rule("Header 2", r"^## (.+)$", r"<h2>\1</h2>", re.MULTILINE)
H3 = Rule("Header 3", r"^### (.+)$", r"<h3>\1</h3>", re.MULTILINE)
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

RULES = [
    P,
    P_IDENT,
    H1, H2, H3,
    BOLD, ITALIC,
    INLINE_MATH, DISPLAY_MATH,
    ORDERED_LIST, ORDERED_ITEM,
    UNORDERED_LIST, UNORDERED_ITEM
]
