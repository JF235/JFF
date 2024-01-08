import re
from rule import Rule
from rules import RULES

EXAMPLE = Rule(
    "Numbered Example", 
    r'<example>(.+?)</example>', 
    r'<div class="numbered_example" COUNTER(EXAMPLE,+)><span class="example_text">Exemplo COUNTER(EXAMPLE,=). </span>\1</div>',
    flags=re.DOTALL
)

RULES.append(EXAMPLE)
