import re
from rule import Rule

# TODO: Ambientes que precisam de padding. Como tratar?
# Do jeito que está aqui, quem fica responsável pelo padding "\n\1\n" é quem define a regra, para garantir que os ambientes <p></p> funcionem

QUESTION = Rule(
    "Question",
    r"<question>(.+?)</question>",
    r'<div class="question">\n\1\n</div>',
    flags=re.DOTALL,
)

ANSWER = Rule(
    "Answer",
    r"<answer>(.+?)</answer>",
    r'<div class="answer">\n<div class="answer_title">Resposta</div>\n\1\n</div>',
    flags=re.DOTALL,
)
