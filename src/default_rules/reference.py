from rule import Rule
from jff_globals import LABEL_DICT, METADATA

def reference_formattig(self: Rule, match) -> str:
    # Substitui a tag <a label="foo"> pelo formatador correto
    # (indicado no dicionario LABEL_DICT)
    #
    # Exemplo:
    #
    # <a label="figfoo">
    # 
    # <a href="#figfoo" class="reference">Figura COUNTER(FIG,=,fig-foo)</a>'
    label = match.group(1)
    reference_name = LABEL_DICT.get(label, "??")
    if reference_name == "??":
        print(f"Label não encontrada. '{label}'")
        ref_format = "??"
    else:
        ref_format = METADATA[reference_name + '_REF'].strip("'")
    replace = r'<a href="#\1" class="reference">' + ref_format + '</a>'
    replace = match.expand(replace)
    return replace


REFERENCE = Rule(
    "Reference",
    r'<a label="(.+?)">',
    "",
    formatting=reference_formattig,
)
