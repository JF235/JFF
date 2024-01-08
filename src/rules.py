from rule import Rule
import re
import os


def header_formattig(self: Rule, metadata: dict[str, str], match) -> str:
    """
    Substituir HN_FORMAT pelo formato especificado nos metadados.
    """
    replace = self.repl
    pattern = re.compile("H._FORMAT")
    hformat_match = pattern.search(self.repl)
    if hformat_match:
        header_format = metadata[hformat_match.group(0)].strip("'")
        replace = (
            replace[: hformat_match.start()]
            + header_format
            + replace[hformat_match.end() :]
        )
    replace = match.expand(replace)
    return replace


H1 = Rule(
    "Header 1",
    r"^# (.+)$",
    r"<h1 COUNTER(H1,+) COUNTER(H2,0) COUNTER(H3,0)>H1_FORMAT\1</h1>",
    re.MULTILINE,
    formatting=header_formattig,
)

H2 = Rule(
    "Header 2",
    r"^## (.+)$",
    r"<h2 COUNTER(H2,+) COUNTER(H3,0)>H2_FORMAT\1</h2>",
    re.MULTILINE,
    formatting=header_formattig,
)

H3 = Rule(
    "Header 3",
    r"^### (.+)$",
    r"<h3 COUNTER(H3,+)>H3_FORMAT\1</h3>",
    re.MULTILINE,
    formatting=header_formattig,
)

BOLD = Rule("Bold", r"\*\*(.*?)\*\*", r"<strong>\1</strong>")
ITALIC = Rule("Italic", r"\*(.*?)\*", r"<em>\1</em>")
DISPLAY_MATH = Rule("Display Math", r"\$\$(.+?)\$\$", r"\[\1\]", re.DOTALL)
INLINE_MATH = Rule("Inline Math", r"\$(.+?)\$", r"\(\1\)")


def paragraph_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    """
    Ajustar identação, remover espaços em branco e adicionar uma quebra no final.
    """
    replace = match.expand(self.repl)
    match = re.search(r"([ ]{4})*(<p>)(.+?)(</p>)", replace, re.DOTALL)
    if match:
        middle = match.group(3).strip()
        ident = match.group(1) if match.group(1) else ""
        replace = ident + match.group(2) + middle + match.group(4) + "\n"
    return replace


_padroes_especiais = r"#|\d\.|[-*][ ]|\$\$|```|<fig|<p"
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


def figure_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    replace = self.repl
    figure_string = match.group(0)

    # Obter caminho/nome da figura
    figname_match = re.search(r' src="(.+?)"', figure_string)
    if figname_match:
        figpath = metadata["FIGPATH"]
        figname, figext = os.path.splitext(figname_match.group(1))
        full_figname = figname + figext
        
        for arquivo in os.listdir(figpath):
            if figext and os.path.splitext(arquivo) == (figname, figext):
                full_figname =  os.path.join(figpath, arquivo)
                break
            elif figext == '' and os.path.splitext(arquivo)[0] == figname:
                full_figname =  os.path.join(figpath, arquivo)
                break

        m = re.search("FIGNAME", replace)
        if m:
            replace = replace[: m.start()] + full_figname + replace[m.end() :]
    else:
        raise (FileNotFoundError)

    # Trantando o estilo
    figstyle_match = re.search(r' size="(.+?)"', figure_string)
    figstyle = (
        f' style="{figstyle_match.group(1)}"'
        if figstyle_match
        else f' style="{metadata['FIGSTYLE']}"'
    )
    replace = re.sub(" FIGSTYLE", figstyle, replace)

    # Tratando a legenda
    figcaption_match = re.search(r' caption="(.+?)"', figure_string)
    full_figcaption = ""
    if figcaption_match:
        figcaption = figcaption_match.group(1)
        figformat = metadata["FIG_FORMAT"].strip("'")
        full_figcaption = f'<figcaption><span class="figurelabel">{figformat}</span>{figcaption}</figcaption>'
    replace = re.sub("FIG_CAPTION", full_figcaption, replace)

    # Tratando o label
    figlabel_match = re.search(r' label="(.+?)"', figure_string)
    figlabel = figlabel_match.group(1) if figlabel_match else figname
    replace = re.sub("FIGLABEL", figlabel, replace)

    return replace


_figure_params = r'(?: (.+?)="(.+?)")*'
_figure = r'<fig(?:ure)? src="(.+?)"' + _figure_params + r">"
_figure_repl = r'<figure COUNTER(FIG,+,FIGLABEL)><img src="FIGNAME" FIGSTYLE id="fig-FIGLABEL">FIG_CAPTION</figure>'
FIGURE = Rule("Figure", _figure, _figure_repl, formatting=figure_formatting)


def reference_formattig(self: Rule, metadata: dict[str, str], match) -> str:
    replace = self.repl
    pattern = re.compile("REF_FORMAT")
    refmatch = pattern.search(self.repl)
    if refmatch:
        reference_format = metadata[refmatch.group(0)].strip("'")
        replace = (
            replace[: refmatch.start()] + reference_format + replace[refmatch.end() :]
        )
    replace = match.expand(replace)
    return replace


REFERENCE = Rule(
    "Reference",
    r'<a label="(.+)">',
    r'<a href="#fig-\1" class="reference">REF_FORMAT</a>',
    formatting=reference_formattig,
)

CODE = Rule(
    "Code",
    r"\`\`\`(.+?)\n(.+?)\`\`\`",
    '<pre><code class="language-\\1">\\2</code></pre>',
    flags=re.DOTALL,
)

RULES = [
    P,
    P_IDENT,
    H1,
    H2,
    H3,
    BOLD,
    ITALIC,
    DISPLAY_MATH,
    INLINE_MATH,
    ORDERED_LIST,
    ORDERED_ITEM,
    UNORDERED_LIST,
    UNORDERED_ITEM,
    CODE,
    FIGURE,
    REFERENCE,
]
