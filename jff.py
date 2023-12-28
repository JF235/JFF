import re
import rules_md as md
import rules_html as html
from sys import argv
import os

FIGURE_COUNTER = 0
FIGURE_DICT = {}

def md2html(markdownBuffer):
    """Converte uma string Markdown para uma string HTML

    Args:
        markdownBuffer (String): Um buffer com o texto de um arquivo em Markdown

    Returns:
        String: Um buffer com o texto do arquivo convertido em HTML
    """
    global FIGURE_COUNTER, FIGURE_DICT
    
    assert len(html.TARGET_RULES) == len(md.RULES)
    htmlBuffer = markdownBuffer
    
    # Para cada "rule" em Markdown, é feita a troca
    # pelo respectivo "target" em HTML
    for rule, target in zip(md.RULES, html.TARGET_RULES):
        
        # Forma de depurar os resultados
        #if rule is md.P:
        #    print(rule.findall(htmlBuffer))
            
        htmlBuffer = rule.sub(target, htmlBuffer)
    
    # Enquanto o retorno de search for diferente de `None`
    # Substitui pela figura e armazena uma entrada no dicionário
    # com a numeração adequada
    match = md.FIGURE.search(htmlBuffer)
    while match:
        FIGURE_COUNTER += 1
        # group(4) é o label da figura
        FIGURE_DICT[match.group(4)] = FIGURE_COUNTER
        htmlBuffer = md.FIGURE.sub(html.FIGURE_T, htmlBuffer, count=1)
        match = md.FIGURE.search(htmlBuffer)
    
    # Substitui todas as referências pela numeração adequada
    match = md.REFERENCE.search(htmlBuffer)
    while match:
        # group(1) é o label da figura
        try:
            figure_number = str(FIGURE_DICT[match.group(1)])
        except KeyError:
            figure_number = "??"
        htmlBuffer = md.REFERENCE.sub(html.REFERENCE_T, htmlBuffer, count=1)
        htmlBuffer = re.sub('NUMHERE', figure_number, htmlBuffer)
        match = md.REFERENCE.search(htmlBuffer)
    
    return htmlBuffer

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
        buffer +=  '\n\n'

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
