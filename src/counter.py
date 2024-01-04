import re

COUNTER_DICT: dict[str, int] = {}
REFERENCE_DICT: dict[str, int] = {}


def resolve_numbering(string: str, metadata: dict) -> str:
    """Após essa primeira substituição realizada com os métodos, 
    
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
    for counter_name in metadata["COUNTERS"].split(','):
        # Inicia os contadores
        counter_name = counter_name.strip()
        COUNTER_DICT[counter_name] = 0
    string = resolve_counters(string)
    string = resolve_references(string)
    return string


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
    """Resolve os contadores com substituiçao direta

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
        elif counter_operation == "0":
            # Reseta o contador
            COUNTER_DICT[counter_name] = 0
            new_string = new_string[:pos-1] + new_string[endpos:]
            endpos = pos

        match = pattern.search(new_string, endpos)
    return new_string
