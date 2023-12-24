import rules_md as md
import rules_html as html
from sys import argv
from pathlib import Path

def md2html(markdownBuffer):
    """Converte uma string Markdown para uma string HTML

    Args:
        markdownBuffer (String): Um buffer com o texto de um arquivo em Markdown

    Returns:
        String: Um buffer com o texto do arquivo convertido em HTML
    """
    
    assert len(html.TARGET_RULES) == len(md.RULES)
    htmlBuffer = markdownBuffer
    
    # Para cada "rule" em Markdown, é feita a troca
    # pelo respectivo "target" em HTML
    for rule, target in zip(md.RULES, html.TARGET_RULES):
        htmlBuffer = rule.sub(target, htmlBuffer)
    
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
    
    # Stripped Extension
    filenameStem = Path(filename).stem
    with open(f'{filenameStem}.html', mode='w', encoding='utf8') as file:
        file.write(htmlBuffer)

if __name__ == '__main__':
    main()
