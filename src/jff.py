from sys import argv
from pathlib import Path
import re
import os
import importlib.util

from counter import resolve_numbering
from jff_globals import APPDIR, METADATA, CWD, RULES
from rules import add_default_rules
from default_rules.code import apply_code, resolve_code
from metadata import read_metadata
from style import add_style, add_default_style


def custom_imports():
    """
    Importa o módulo com caminho especificado nos metadados "IMPORTS"
    """
    importname = METADATA.get("IMPORTS", None)
    if importname:
        importname = importname.strip(".py")
        importpath = CWD + "\\" + METADATA["IMPORTS"]
        spec = importlib.util.spec_from_file_location(importname, importpath)
        module = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(module)  # type: ignore


def md2html(buffer: str) -> str:
    """
    Converte a string passada no formato jff para uma string em html.

    O processo é dividido em 3 etapas:
    - Isolar os trechos de código, para que padrões especiais não seja capturados
    - Aplicar as regras e substituir os padrões especiais
    - Resolver as numerações (contadores e referências)

    Args:
        buffer (str): String em JFF

    Returns:
        str: String em HTML
    """
    new_string = buffer

    # Substitui os trechos de código por referências
    new_string = apply_code(new_string)

    for r in RULES:
        new_string = r.apply(new_string)

    new_string = resolve_numbering(new_string)
    
    # Resolve as referências dos código  
    new_string = resolve_code(new_string)

    return new_string


def set_docname(filename: str, string: str) -> str:
    pattern = re.compile("DOCNAME")
    docname = Path(filename).stem.replace("_", " ").title()
    string = pattern.sub(docname, string)
    return string


def main():
    try:
        filename = argv[1]
    except IndexError:
        print(f"Uso: {argv[0]} <filename>")
        return

    if filename == "DEBUGMODE":
        # No modo de debug eu consigo editar o conteúdo da variável filename
        filename = "computer_graphics.md"

    with open(filename, mode="r", encoding="utf8") as file:
        string = file.read()
        # Para garantir que as regras funcionem de forma apropriada
        # adiciono dois newlines no final.
        string += "\n\n"

    string = read_metadata(string)

    # Preenche a lista RULES
    add_default_rules()

    # Importa módulos python adicionais (declarar ambientes customizados)
    custom_imports()

    # Faz a conversão
    htmlString = md2html(string)

    # Arquivo base, contendo `head` e `body`
    with open(APPDIR + "\\assets\\base.html", mode="r", encoding="utf8") as file:
        htmlFile = file.read()

    # Substituir o conteudo do arquivo HTML no template base
    match = re.search("INSERTHERE", htmlFile)
    if match:
        htmlFile = htmlFile[: match.start()] + htmlString + htmlFile[match.end() :]

    # Adicionar estilo
    htmlFile = add_default_style(htmlFile)
    htmlFile = add_style(APPDIR + "\\assets\\dracula.css", htmlFile)

    # Aplicar outros metadados
    htmlFile = set_docname(filename, htmlFile)

    # Escreve o novo arquivo
    filename_wo_ext = os.path.splitext(filename)[0]
    with open(f"{filename_wo_ext}_new.html", mode="w", encoding="utf8") as file:
        file.write(htmlFile)


if __name__ == "__main__":
    main()
