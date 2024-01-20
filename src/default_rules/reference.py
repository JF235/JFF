from rule import Rule
from jff_globals import LABEL_DICT, METADATA

def reference_formattig(self: Rule, match) -> str:
    label = match.group(1)
    reference_name = LABEL_DICT[label]
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
