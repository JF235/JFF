from rule import Rule
import re


def header_formattig(self: Rule, metadata: dict[str, str], match) -> str:
    """
    Substituir HN_FORMAT pelo formato especificado nos metadados.
    """
    replace = self.repl
    pattern = re.compile("H._FORMAT")
    hformat_match = pattern.search(self.repl)
    if hformat_match:
        header_format = metadata[hformat_match.group(0)].strip("'")
        replace = (
            replace[: hformat_match.start()]
            + header_format
            + replace[hformat_match.end() :]
        )
    replace = match.expand(replace)
    return replace


H1 = Rule(
    "Header 1",
    r"^# (.+)$",
    r"<h1 COUNTER(H1,+) COUNTER(H2,0) COUNTER(H3,0)>H1_FORMAT\1</h1>",
    re.MULTILINE,
    formatting=header_formattig,
)

H2 = Rule(
    "Header 2",
    r"^## (.+)$",
    r"<h2 COUNTER(H2,+) COUNTER(H3,0)>H2_FORMAT\1</h2>",
    re.MULTILINE,
    formatting=header_formattig,
)

H3 = Rule(
    "Header 3",
    r"^### (.+)$",
    r"<h3 COUNTER(H3,+)>H3_FORMAT\1</h3>",
    re.MULTILINE,
    formatting=header_formattig,
)
