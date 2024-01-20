from rule import Rule
import re
import os


def figure_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    replace = self.repl
    figure_string = match.group(0)

    # Obter caminho/nome da figura
    figname_match = re.search(r' src="(.+?)"', figure_string)
    if figname_match:
        figpath = metadata["MEDIAPATH"]
        figname, figext = os.path.splitext(figname_match.group(1))
        full_figname = figname + figext

        for arquivo in os.listdir(figpath):
            if figext and os.path.splitext(arquivo) == (figname, figext):
                full_figname = os.path.join(figpath, arquivo)
                break
            elif figext == "" and os.path.splitext(arquivo)[0] == figname:
                full_figname = os.path.join(figpath, arquivo)
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
