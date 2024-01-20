from rule import Rule
from jff_globals import REFERENCE_DICT

def reference_formattig(self: Rule, metadata: dict[str, str], match) -> str:
    label = match.group(1)
    _, reference_name = REFERENCE_DICT[label]
    ref_format = metadata[reference_name + '_REF'].strip("'")
    replace = r'<a href="#\1" class="reference">' + ref_format + '</a>'
    replace = match.expand(replace)
    return replace


REFERENCE = Rule(
    "Reference",
    r'<a label="(.+)">',
    "",
    formatting=reference_formattig,
)
