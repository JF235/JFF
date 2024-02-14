import os
from rule import Rule

CWD = os.getcwd()
APPDIR = os.path.realpath(os.path.dirname(__file__)) + "\\.."

RULES: list[Rule] = []

# Associa NOME DO CONTADOR -> LABEL
# Tem caráter dinâmico, já que os contadores tem valores
# atualizados ao longo da execução.
COUNTER_DICT: dict[str, int] = {}

# Associa LABEL -> NOME DO CONTADOR
LABEL_DICT: dict[str, str] = {}

# Associa LABEL -> NUMERO
REFERENCE_DICT: dict[str, int] = {}

METADATA: dict[str, str] = {
    "COUNTERS": "",
    "MEDIA_PATH": "",
    "STYLESHEET": APPDIR + "\\assets\\style.css"
}

# Dicionário que associa para cada número o código que foi aplicado
CODE_REF: dict[int, str] = {}

# Dicionário que associa para cada número o código inline que foi aplicado
INLINECODE_REF: dict[int, str] = {}
