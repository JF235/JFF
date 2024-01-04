import re

COUNTER_DICT: dict[str, int] = {}
REFERENCE_DICT: dict[str, int] = {}


def set_counters(string: str, metadata: dict) -> str:
    for counter_name in metadata["COUNTERS"]:
        COUNTER_DICT[counter_name] = 0
    string = insert_counters(string)
    string = insert_references(string)
    return string


def insert_references(string: str) -> str:
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


def insert_counters(string: str) -> str:
    new_string = string
    pattern = re.compile(r"COUNTER[(](.+?),(.+?)(?:,(.+?))?[)]")
    match = pattern.search(string)
    while match:
        pos, endpos = match.span()

        counter_name = match.group(1)
        counter_operation = match.group(2)
        counter_label = match.group(3)

        if counter_operation == "+":
            COUNTER_DICT[counter_name] += 1
            if counter_label:
                REFERENCE_DICT[counter_label] = COUNTER_DICT[counter_name]
            new_string = new_string[: pos - 1] + new_string[endpos:]
            endpos = pos - 1
        elif counter_operation == "=":
            if counter_label is None:
                new_string = (
                    new_string[:pos]
                    + str(COUNTER_DICT[counter_name])
                    + new_string[endpos:]
                )
                endpos = pos + len(str(COUNTER_DICT[counter_name]))
        elif counter_operation == "0":
            COUNTER_DICT[counter_name] = 0
            new_string = new_string[:pos] + new_string[endpos:]
            endpos = pos

        match = pattern.search(new_string, endpos)
    return new_string
