from sys import argv
from pathlib import Path
import re
import os

from counter import resolve_numbering
from default_metadata import get_default_metadata
from default_rules.code import apply_code, resolve_code
from rules import RULES

CWD = os.getcwd()
APPDIR = os.path.realpath(os.path.dirname(__file__)) + "\\.."


def read_metadata(string: str) -> tuple[dict[str, str], str]:
    """Define os metadados baseados nos valores padrões definidos no arquivo `get_dafault_metadata()` e nos valores declarados no arquivo (que tem maior precedência).

    Args:
        string (str): conteúdo do arquivo

    Returns:
        tuple[dict[str, str], str]: Dicionário de metadados e string do arquivo sem os metadados
    """
    metadata = get_default_metadata()
    pattern = re.compile(r"METADATA\n---\n(.+?)\n---\n\n", re.DOTALL)
    match = pattern.search(string)

    if match:
        # Lê cada linha no formato NOME: VALOR
        metadata_str = match.group(1)
        metadata_arguments = metadata_str.split("\n")
        for line in metadata_arguments:
            arg_name, arg_option_str = tuple(line.split(":"))
            arg_option = arg_option_str.strip()
            if arg_name == "COUNTERS":
                metadata[arg_name] += f", {arg_option}"
            else:
                metadata[arg_name] = arg_option
        # Remove os metadados do arquivo
        string = string[: match.start()] + string[match.end() :]

    return metadata, string


def md2html(buffer: str, metadata: dict) -> str:
    new_string = buffer

    new_string = apply_code(new_string, metadata)

    for r in RULES:
        new_string = r.apply(new_string, metadata)

    new_string = resolve_numbering(new_string, metadata)
    new_string = resolve_code(new_string)

    return new_string


def set_style(stylesheet: str, string: str) -> str:
    match = re.search("/[*] STYLEHERE [*]/", string)
    if match:
        style = ""
        with open(stylesheet) as file:
            style = file.read()
        string = (
            string[: match.start()]
            + style
            + "\n/* STYLEHERE */"
            + string[match.end() :]
        )
    return string


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
        filename = ""

    with open(filename, mode="r", encoding="utf8") as file:
        string = file.read()
        # Para garantir que as regras funcionem de forma apropriada...
        string += "\n\n"

    metadata, string = read_metadata(string)

    htmlString = md2html(string, metadata)

    # Arquivo base, contendo `head` e `body`
    with open(APPDIR + "\\assets\\base.html", mode="r", encoding="utf8") as file:
        htmlFile = file.read()

    # Conteúdo do arquivo
    match = re.search("INSERTHERE", htmlFile)
    if match:
        htmlFile = htmlFile[: match.start()] + htmlString + htmlFile[match.end() :]

    # Informações adicionais
    # TODO: Adicionar isso nos metadados
    htmlFile = set_style(APPDIR + "\\assets\\style.css", htmlFile)
    # Adicionar informação do estilo de código
    htmlFile = set_style(APPDIR + "\\assets\\dracula.css", htmlFile)
    htmlFile = set_docname(filename, htmlFile)

    filename_wo_ext = os.path.splitext(filename)[0]
    with open(f"{filename_wo_ext}_new.html", mode="w", encoding="utf8") as file:
        file.write(htmlFile)


if __name__ == "__main__":
    main()
