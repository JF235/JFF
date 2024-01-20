from rule import Rule
import re
from jff_globals import CODE_REF


def code_formatting(self: Rule, match) -> str:
    num_codes = len(CODE_REF)
    # Coloca no lugar
    replace = f"<CODEREF({num_codes})/>"
    CODE_REF[num_codes] = match.expand(self.repl)
    return replace


CODE = Rule(
    "Code",
    r"^\`\`\`(?!\n)(.+?)\n(.+?)\`\`\`(?=\n\n)",
    '<pre><code class="language-\\1">\\2</code></pre>',
    flags= re.DOTALL | re.MULTILINE,
    formatting=code_formatting,
)


def apply_code(string: str):
    return CODE.apply(string)


def resolve_code(string: str) -> str:
    new_string = string
    pattern = re.compile(r"<CODEREF\((.+?)\)/>")
    match = pattern.search(new_string)
    while match:
        pos, endpos = match.span()

        code_num = int(match.group(1))

        new_string = new_string[:pos] + f"{CODE_REF[code_num]}" + new_string[endpos:]

        match = pattern.search(new_string)
    return new_string
