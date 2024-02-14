from rule import Rule
from jff_globals import METADATA
import re
import os
import metadata

metadata.set_counter("FIG")
metadata.update(
    {
        "FIG_FORMAT": "'Figure COUNTER(FIG,=) - '",
        "FIG_REF": r"'Fig.&nbsp;COUNTER(FIG,=,\1)'",
        "FIG_STYLE": "width: 50%",
    }
)


def figure_formatting(self: Rule, match) -> str:
    # match.group(1) é somente a parte da figura, sem legenda
    figure_string = match.group(1)
    # TODO: Adicionar suporte para múltiplos caminhos
    figpath = METADATA["MEDIA_PATH"]

    figname = match.group(2)
    name, ext = os.path.splitext(figname)

    full_figname = os.path.join(figpath, figname)

    if ext == "":
        if figpath == "":
            figpath = "./"
            
        arquivos = [arquivo for arquivo in os.listdir(figpath) if os.path.splitext(arquivo)[0] == name]
        
        if arquivos:
            arquivo = arquivos[0]
            full_figname = os.path.join(figpath, arquivo)
        else:
            print(f"Arquivo não encontrado. '{full_figname}'")
        
        

    # Trantando o estilo
    figstyle_match = re.search(r' style="(.+?)"', figure_string)
    figstyle = (
        f'style="{figstyle_match.group(1)}"'
        if figstyle_match
        else f'style="{METADATA['FIG_STYLE']}"'
    )

    # Tratando a legenda
    figformat = METADATA["FIG_FORMAT"].strip("'")
    full_figcaption = ""
    if match.group(5):
        # Tem legenda na forma de <caption></caption>
        figcaption = match.group(5).strip()
        full_figcaption = f'<figcaption><span class="figurelabel">{figformat}</span>{figcaption}</figcaption>'
    else:
        # Busca tag caption=""
        figcaption_match = re.search(r' caption="(.+?)"', figure_string)
        if figcaption_match:
            figcaption = figcaption_match.group(1)
            full_figcaption = f'<figcaption><span class="figurelabel">{figformat}</span>{figcaption}</figcaption>'

    # Tratando o label
    figlabel_match = re.search(r' label="(.+?)"', figure_string)
    figlabel = figlabel_match.group(1) if figlabel_match else figname
    
    if full_figcaption == "":
        # Se não tem legenda, não adiciona contador
        replace = f'<figure><img src="{full_figname}" {figstyle} id="{figlabel}">{full_figcaption}</figure>'
    else:
        # Do contrário, incrementa o contador
        replace = f'<figure COUNTER(FIG,+,{figlabel})><img src="{full_figname}" {figstyle} id="{figlabel}">{full_figcaption}</figure>'

    return replace


_figure_params = r'(?: (.+?)="(.+?)")*'
_figure = r'(<fig(?:ure)? src="(.+?)"' + _figure_params + r">)" + r"(?:\n<caption>(.+?)</caption>)?"
FIGURE = Rule("Figure", _figure, "", formatting=figure_formatting, flags= re.DOTALL)
