import re
from rule import Rule
from rules import RULES

QUESTION = Rule(
    "Question", 
    r'<question>(.+?)</question>', 
    r'<div class="question">\1</div>',
    flags=re.DOTALL
)

ANSWER = Rule(
    "Answer", 
    r'<answer>(.+?)</answer>', 
    r'<div class="answer">\n<div class="answer_title">Resposta</div>\1</div>',
    flags=re.DOTALL
)

RULES.append(QUESTION)
RULES.append(ANSWER)
