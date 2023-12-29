from rules import RULES
from rules import FIGURE, REFERENCE, FIGURE_T, REFERENCE_T
import re
from sys import argv
import os

FIGURE_COUNTER = 0
FIGURE_DICT = {}

def subs_figures(string: str) -> str:
    global FIGURE_COUNTER, FIGURE_DICT
    
    # Enquanto o retorno de search for diferente de `None`
    # Substitui pela figura e armazena uma entrada no dicionário
    # com a numeração adequada
    match = FIGURE.search(string)
    while match:
        FIGURE_COUNTER += 1
        # group(4) é o label da figura
        FIGURE_DICT[match.group(4)] = FIGURE_COUNTER
        string = FIGURE.sub(FIGURE_T, string, count=1)
        match = FIGURE.search(string)
    
    # Substitui todas as referências pela numeração adequada
    match = REFERENCE.search(string)
    while match:
        # group(1) é o label da figura
        try:
            figure_number = str(FIGURE_DICT[match.group(1)])
        except KeyError:
            figure_number = "??"
        string = REFERENCE.sub(REFERENCE_T, string, count=1)
        string = re.sub('NUMHERE', figure_number, string)
        match = REFERENCE.search(string)
    
    return string

def md2html(buffer: str) -> str:
    new_string = buffer
    for r in RULES:
        new_string = r.apply(new_string)
        
    # TODO Unificar essa solução
    new_string = subs_figures(new_string)
    
    return new_string

def main():
    try:
        filename = argv[1]
    except IndexError:
        print(f"Uso: {argv[0]} <filename>")
        return
    
    with open(filename, mode='r', encoding='utf8') as file:
        buffer = file.read()
        # Adicionando duas quebras de linha no final 
        # para garantir que as regras funcionem de forma apropriada
        buffer += '\n\n'
    
    htmlBuffer = md2html(buffer)
    
    # Arquivo base, contendo `head` e `body`
    with open('assets/base.html', mode='r', encoding='utf8') as file:
        htmlFile = file.read()
    
    # Conteúdo do arquivo
    pattern = re.compile("INSERTHERE")
    # Transforma string htmlBuffer para 'rawString' sem as aspas produzidas
    # ao obter a forma canônica de representação da string com repr()
    htmlFile = pattern.sub(repr(htmlBuffer)[1:-1], htmlFile)
    
    # Estilo do arquivo
    pattern = re.compile("STYLEHERE")
    htmlFile = pattern.sub('style.css', htmlFile)
    
    filenameHtml = os.path.splitext(filename)[0]
    with open(f'{filenameHtml}.html', mode='w', encoding='utf8') as file:
        file.write(htmlFile)

if __name__ == '__main__':
    main()