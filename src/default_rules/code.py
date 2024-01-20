from rule import Rule
import re

# Dicionário que associa para cada número o código que foi aplicado
CODE_REF: dict[int, str] = {}


def code_formatting(self: Rule, metadata: dict[str, str], match) -> str:
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


def apply_code(string: str, metadata: dict):
    return CODE.apply(string, metadata)


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