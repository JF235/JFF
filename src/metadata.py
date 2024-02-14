import re
from jff_globals import METADATA


def read_metadata(string: str) -> str:
    """Lê os metadados presentes no arquivo e armazena no dicionário `METADATA`.

    Args:
        string (str): conteúdo do arquivo

    Returns:
        str: conteúdo do arquivo sem os metadados
    """
    pattern = re.compile(r"METADATA\n---\n(.+?)\n---\n\n", re.DOTALL)
    match = pattern.search(string)

    if match:
        new_metadata = parse_metadata(match.group(1))

        counter = new_metadata.pop("COUNTERS", None)
        if counter:
            set_counter(counter)
        update(new_metadata)

        # Remove os metadados do arquivo
        string = string[: match.start()] + string[match.end() :]

    return string


def parse_metadata(metadata_str: str) -> dict:
    """Realiza o parse da string contendo linhas na forma
    `ARG_NAME: ARG_VALUE` e devolve um dicionário correspondente.

    Args:
        metadata_str (str): String com metadados

    Returns:
        dict: Dicionário com metadados
    """
    new_metadata = {}
    metadata_list = metadata_str.split("\n")
    for metadata in metadata_list:
        # Lê cada linha no formato NOME: VALOR
        arg_name, arg_value = metadata.split(":")
        arg_value = arg_value.strip()
        new_metadata[arg_name] = arg_value
    return new_metadata


def update(new_metadata: dict):
    # TODO: Ordem de precedência não considerada.
    METADATA.update(new_metadata)


def set_counter(counter: str | list[str]):
    if isinstance(counter, list):
        counter = ', '.join(counter)
    METADATA["COUNTERS"] += f", {counter}"
