from rule import RULES
import re
from sys import argv
import os

def md2html(buffer: str):
    new_string = buffer
    for r in RULES:
        new_string = r.apply(new_string)
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