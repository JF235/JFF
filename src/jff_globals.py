import os

COUNTER_DICT: dict[str, int] = {}

# Associa LABEL -> NOME DO CONTADOR
LABEL_DICT: dict[str, str] = {}

# Associa LABEL -> NUMERO
REFERENCE_DICT: dict[str, int] = {}

METADATA: dict[str, str] = {
    "COUNTERS": "",
    "MEDIA_PATH": "",
}

CWD = os.getcwd()
APPDIR = os.path.realpath(os.path.dirname(__file__)) + "\\.."

# Dicionário que associa para cada número o código que foi aplicado
CODE_REF: dict[int, str] = {}
INLINECODE_REF: dict[int, str] = {}
