import re
from rule import Rule
from jff_globals import METADATA, RULES
import metadata

#=====================================================
# Adicionando nova regra
#=====================================================

metadata.set_counter("CHAPTER")
metadata.update(
    {
        "CHAPTER_FORMAT": "Chapter COUNTER(CHAPTER,=)"
    }
)

def chapter_formattig(self: Rule, match) -> str:
    replace = '<hr>\n<div COUNTER(CHAPTER,+) class="chapter_format">CHAPTER_FORMAT</div>\n' + r'<div class="chapter_name">\1</div>' + '\n<hr>'
    
    pattern = re.compile("CHAPTER_FORMAT")
    chap_match = pattern.search(replace)
    if chap_match:
        chapter_format = METADATA[chap_match.group(0)].strip("'")
        replace = (
            replace[: chap_match.start()]
            + chapter_format
            + replace[chap_match.end() :]
        )
    replace = match.expand(replace)
    return replace

CHAPTER = Rule(
    "Numbered Chapter",
    r"^#! (.+?)$",
    "",
    flags=re.MULTILINE,
    formatting=chapter_formattig
)

RULES.append(CHAPTER)
print("Imported CHAPTER")

#=====================================================
# Editando regra padrão
#=====================================================

def h1_formattig(self: Rule, match) -> str:
    replace = '<div COUNTER(H1,+) class="h1_format">H1_FORMAT</div>\n' + r'<h1>\1</h1>' + '\n<hr>'
    
    pattern = re.compile("H1_FORMAT")
    chap_match = pattern.search(replace)
    if chap_match:
        chapter_format = METADATA[chap_match.group(0)].strip("'")
        replace = (
            replace[: chap_match.start()]
            + chapter_format
            + replace[chap_match.end() :]
        )
    replace = match.expand(replace)
    return replace

h1rule = next(filter(lambda r: r.name == "Header 1", RULES))
h1rule.formatting = h1_formattig