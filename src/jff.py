from sys import argv
from rules import RULES
from rule import rawString
from counter import resolve_numbering
from default_metadata import get_default_metadata
import re
import os


def parse_metadata(metadata:dict, metadata_str: str):
    metadata_arguments = metadata_str.split('\n')
    for line in metadata_arguments:
        arg_name, arg_option_str = tuple(line.split(':'))
        arg_option = arg_option_str.strip()
        metadata[arg_name] = arg_option

def read_metadata(string: str):
    pattern = re.compile(r"METADATA\n---\n(.+?)\n---\n\n", re.DOTALL)
    match = pattern.search(string)
    metadata = get_default_metadata()
    if match:
        metadata_str = match.group(1)
        parse_metadata(metadata, metadata_str)
        # Remove os metadados do arquivo
        string = string[:match.start()] + string[match.end():]
    return metadata, string

def md2html(buffer: str, metadata: dict) -> str:
    new_string = buffer
    
    for r in RULES:
        r.format_repl(metadata)
        new_string = r.apply(new_string)
    
    new_string = resolve_numbering(new_string, metadata)
        
    return new_string


def set_style(string: str) -> str:
    pattern = re.compile("STYLEHERE")
    string = pattern.sub("style.css", string)
    return string


def main():
    try:
        filename = argv[1]
    except IndexError:
        print(f"Uso: {argv[0]} <filename>")
        return

    with open(filename, mode="r", encoding="utf8") as file:
        buffer = file.read()
        # Adicionando duas quebras de linha no final
        # para garantir que as regras funcionem de forma apropriada
        buffer += "\n\n"

    metadata, buffer = read_metadata(buffer)
    
    htmlBuffer = md2html(buffer, metadata)

    # Arquivo base, contendo `head` e `body`
    with open("assets/base.html", mode="r", encoding="utf8") as file:
        htmlFile = file.read()

    # Conteúdo do arquivo
    pattern = re.compile("INSERTHERE")
    # Transforma string htmlBuffer para 'rawString' sem as aspas produzidas
    # ao obter a forma canônica de representação da string com repr()
    htmlFile = pattern.sub(rawString(htmlBuffer), htmlFile)

    htmlFile = set_style(htmlFile)

    filenameHtml = os.path.splitext(filename)[0]
    with open(f"{filenameHtml}.html", mode="w", encoding="utf8") as file:
        file.write(htmlFile)


if __name__ == "__main__":
    main()
