import re

from rule import Rule
from jff_globals import CODE_REF, INLINECODE_REF, METADATA
import metadata

metadata.set_counter("CODE")
metadata.update(
    {
        "CODE_FORMAT": "'Código COUNTER(CODE,=) - '",
        "CODE_REF": r"'Código&nbsp;COUNTER(CODE,=,\1)'",
    }
)

def apply_code(string: str) -> str:
    """Aplica as regras `CODE` e `INLINE_CODE`

    Dessa forma todos os trechos de código são substituídos por uma referência
    do tipo `<CODEREF(N)/>` ou `<INLINECODEREF(N)/>`, sendo `N` o identificador
    numérico do código.

    O identificador númerico é usado para resolver as referências, consultando
    os dicionários `CODE_REF` e `INLINECODE_REF`.

    Args:
        string (str): String jff

    Returns:
        str: String jff sem trechos de código
    """
    string = CODE.apply(string)
    string = INLINE_CODE.apply(string)
    return string


def resolve_code(string: str) -> str:
    """Busca todas as referências da forma

    -`<CODEREF(N)/>` e
    - `<INLINECODEREF(N)/>`

    na string e faz a substituição usando os dicionários `CODE_REF` e `INLINECODE_REF`.

    Args:
        string (str): String com códigos referenciados

    Returns:
        str: String com códigos resolvidos (referências substituídas)
    """
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


def subs_ltgt(full_string, code_string):
    # Substitui os símbolos < > por &lt; &gt;
    # Isso é necessário para interpretação correta do código HTML
    new_code_string = code_string.replace("<", "&lt;")
    new_code_string = new_code_string.replace(">", "&gt;")
    match = re.search(re.escape(code_string), full_string)
    if match:
        new_full_string = (
            full_string[: match.start()] + new_code_string + full_string[match.end() :]
        )
    else:
        new_full_string = full_string
    return new_full_string


def code_formatting(self: Rule, match) -> str:
    # Obtém o identificador numérico para o código
    num_codes = len(CODE_REF)

    # Guarda o texto do código
    code_string = match.expand(self.repl)
    CODE_REF[num_codes] = subs_ltgt(code_string, match.group(4))

    # Substitui o código pela referência e outras informações, como legenda.
    replace = f"<CODEREF({num_codes})/>"
    if match.group(2):
        # Se tem legenda, adiciona <div> antes
        label = "," + match.group(1) if match.group(1) else ""
        code_id = f' id="{match.group(1)}"' if match.group(1) else ""
        replace = (
            f'<div class="caption"{code_id} COUNTER(CODE,+{label})><span class="codelabel">{METADATA["CODE_FORMAT"].strip("'")}</span>{match.group(2)}</div>\n'
            + replace
        )
    return replace


def inlinecode_formatting(self: Rule, match) -> str:
    num_codes = len(INLINECODE_REF)

    code_string = match.expand(self.repl)
    INLINECODE_REF[num_codes] = subs_ltgt(code_string, match.group(1))

    replace = f"<INLINECODEREF({num_codes})/>"

    return replace


CODE = Rule(
    "Code",
    r'(?:<caption(?: label="(.+?)")?>((?:(?!</caption>).)+)</caption>\n)?^\`\`\`(?!\n)(.+?)\n(.+?)\`\`\`(?=\n\n)',
    r'<pre><code class="language-\3">\4</code></pre>',
    flags=re.DOTALL | re.MULTILINE,
    formatting=code_formatting,
)

_empty_space = r"(?<=[ ]|\n|[(])"
INLINE_CODE = Rule(
    "Inline code",
    _empty_space + r"`(.+?)`",
    r"<code>\1</code>",
    formatting=inlinecode_formatting,
)