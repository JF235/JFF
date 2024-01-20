from rule import Rule
import re


def paragraph_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    """
    Ajustar identação, remover espaços em branco e adicionar uma quebra no final.
    """
    replace = match.expand(self.repl)
    match = re.search(r"([ ]{4})*(<p>)(.+?)(</p>)", replace, re.DOTALL)
    if match:
        middle = match.group(3).strip()
        ident = match.group(1) if match.group(1) else ""
        replace = ident + match.group(2) + " " + middle + " " + match.group(4) + "\n"
    return replace


# TODO: Acrescentar somente alguns padroes especiais validos e nao desconsierar os invalidos
# Por exemplo, padroes_validos = '*', '$', '<em>', ...
_padroes_especiais = r"#|\d\.|[-*][ ]|\$\$|```|<|\\\["
_conteudo = r"((.+\n)+)"
_paragrafo = (
    r"(?<=\n\n)" + f"(?!{_padroes_especiais + r"|[ ]{4}"})" + _conteudo + r"(?=\n)"
)

P = Rule("Paragraph", _paragrafo, r"<p>\1</p>", formatting=paragraph_formatting)

_paragrafo_ident = (
    r"(?<=\n\n)" + r"(([ ]{4}" + f"(?!{_padroes_especiais})" + r".+\n)+)" + r"(?=\n)"
)

P_IDENT = Rule(
    "Paragraph w Identation",
    _paragrafo_ident,
    "    " + r"<p>\1</p>",
    formatting=paragraph_formatting,
)
