import re
from default_rules.reference import REFERENCE
from jff_globals import REFERENCE_DICT, LABEL_DICT, COUNTER_DICT, METADATA


def resolve_numbering(string: str) -> str:
    """Após a primeira substituição realizada com os métodos,

    ```python
    rule.apply(string)
    ```

    haverão marcadores da forma `COUNTER(countername,operation,label)` que serão tratados nessa função com **substituição direta** e **resolução de referências**.

    Args:
        string (str): Conteúdo do HTML após a primeira aplicação de regras.
        metadata (dict): Metadados contendo o nome dos contadores

    Returns:
        str: String final após resolução dos contadores
    """
    for counter_name in METADATA["COUNTERS"].split(","):
        # Inicia os contadores
        counter_name = counter_name.strip()
        COUNTER_DICT[counter_name] = 0

    # (1)
    identify_labels(string)
    string = REFERENCE.apply(string)

    # (2)
    string = resolve_counters(string)

    # (3)
    string = resolve_references(string)

    # A necessidade de tantos processamentos tem origem:
    # - (1) substituicao da regra <a label="foo"> pelos formatadores
    # - (2) resolve os contadores que não apresentam rótulo
    # - (3) resolve os contadores que apresentam rótulo

    return string


def identify_labels(string: str):
    """Busca todos os contadores que possuem label.

    Adiciona no dicionário `LABEL_DICT` o par:
    - label: contador associado a essa label

    Esse pré-processamento é fundamental para substituir as referências
    `<a label="foo">` pelos formatadores apropriados (como H1_FORMAT, FIG_FORMAT, CODE_FORMAT), uma vez que na aplicação dessa regra os contadores não foram resolvidos.

    Args:
        string (str): String com contadores não resolvidos
    """
    pattern = re.compile(r"COUNTER[(]([^)]+?),[^)]+?,([^)]+?)[)]")
    match = pattern.search(string)
    while match:
        counter_name = match.group(1)
        counter_label = match.group(2)

        if counter_name not in LABEL_DICT:
            LABEL_DICT[counter_label] = counter_name
        match = pattern.search(string, pos=match.end())


def resolve_references(string: str) -> str:
    """Resolve os padrões `COUNTER(countername,=,label)` substituindo a referência ao item com 'label' pelo contador correto. Para isso, o dicionário de referências `REFERENCE_DICT` é consultado.

    Args:
        string (str): String com, possivelmente, referências não resolvidas

    Returns:
        str: String com refererências resolvidas
    """
    new_string = string
    pattern = re.compile(r"COUNTER[(](.+?),(.+?),(.+?)[)]")
    match = pattern.search(string)
    while match:
        pos, endpos = match.span()

        counter_label = match.group(3)

        new_string = (
            new_string[:pos] + f"{REFERENCE_DICT[counter_label]}" + new_string[endpos:]
        )

        match = pattern.search(new_string)
    return new_string


def resolve_counters(string: str) -> str:
    """Resolve os contadores com substituiçao direta e atualiza os contadores dinamicamente baseando-se nos incrementadores `COUNTER(countername,+)`

    Args:
        string (str): String com, possivelmente, padrões `COUNTER(countername,=)`

    Returns:
        str: String com padrões substituídos pelos seus contadores
    """
    new_string = string
    pattern = re.compile(r"COUNTER[(](.+?),(.+?)(?:,(.+?))?[)]")
    match = pattern.search(string)
    while match:
        pos, endpos = match.span()

        counter_name = match.group(1)
        counter_operation = match.group(2)
        counter_label = match.group(3)

        # Operação de incremento
        if counter_operation == "+":
            COUNTER_DICT[counter_name] += 1
            if counter_label:
                # Se existir label, armazena no dicionário de referências
                REFERENCE_DICT[counter_label] = COUNTER_DICT[counter_name]
            new_string = new_string[: pos - 1] + new_string[endpos:]
            endpos = pos - 1

        elif counter_operation == "=":
            # Substituição direta pelo contador
            if counter_label is None:
                # Se não existir label, faz substituição direta
                new_string = (
                    new_string[:pos]
                    + str(COUNTER_DICT[counter_name])
                    + new_string[endpos:]
                )
                endpos = pos + len(str(COUNTER_DICT[counter_name]))
            # Se existir label, então espera para resolver depois.

        elif counter_operation.isdecimal():
            # Seta o contador
            COUNTER_DICT[counter_name] = int(counter_operation)
            if new_string[pos - 1] == " " and pos - 1 >= 0:
                new_string = new_string[: pos - 1] + new_string[endpos:]
            else:
                new_string = new_string[:pos] + new_string[endpos:]
            endpos = pos

        match = pattern.search(new_string, endpos)
    return new_string
