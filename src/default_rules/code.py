from rule import Rule
import re
from jff_globals import CODE_REF, INLINECODE_REF, METADATA

METADATA["COUNTERS"] += ", CODE"
METADATA.update(
    {
        "CODE_FORMAT": "'Código COUNTER(CODE,=) - '",
        "CODE_REF": r"'Código&nbsp;COUNTER(CODE,=,\1)'",
    }
)


def code_formatting(self: Rule, match) -> str:
    num_codes = len(CODE_REF)
    # Coloca no lugar
    replace = f"<CODEREF({num_codes})/>"
    CODE_REF[num_codes] = match.expand(self.repl)
    if match.group(2):
        label = "," + match.group(1) if match.group(1) else ""
        code_id = f' id="{match.group(1)}"' if match.group(1) else ""
        replace = (
            f'<div class="caption"{code_id} COUNTER(CODE,+{label})><span class="codelabel">{METADATA["CODE_FORMAT"].strip("'")}</span>{match.group(2)}</div>\n'
            + replace
        )
    return replace

def inlinecode_formatting(self: Rule, match) -> str:
    num_codes = len(INLINECODE_REF)
    # Coloca no lugar
    replace = f"<INLINECODEREF({num_codes})/>"
    INLINECODE_REF[num_codes] = match.expand(self.repl)
    return replace

CODE = Rule(
    "Code",
    r'(?:<caption(?: label="(.+?)")?>(.+?)</caption>\n)?^\`\`\`(?!\n)(.+?)\n(.+?)\`\`\`(?=\n\n)',
    r'<pre><code class="language-\3">\4</code></pre>',
    flags=re.DOTALL | re.MULTILINE,
    formatting=code_formatting,
)

_empty_space = r"(?<=[ ]|\n)"
INLINE_CODE = Rule(
    "Inline code",
    _empty_space + r'`(.+?)`',
    r'<code>\1</code>',
    formatting=inlinecode_formatting
)


def apply_code(string: str):
    string = CODE.apply(string)
    string = INLINE_CODE.apply(string)
    return string


def resolve_code(string: str) -> str:
    dicts = [CODE_REF, INLINECODE_REF]
    strings = [r"<CODEREF\((.+?)\)/>", r"<INLINECODEREF\((.+?)\)/>"]
    new_string = string
    for d, s in zip(dicts, strings):
        pattern = re.compile(s)
        match = pattern.search(new_string)
        while match:
            pos, endpos = match.span()

            code_num = int(match.group(1))

            new_string = new_string[:pos] + f"{d[code_num]}" + new_string[endpos:]

            match = pattern.search(new_string)
    return new_string
