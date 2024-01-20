from rule import Rule
import re


def reference_formattig(self: Rule, metadata: dict[str, str], match) -> str:
    replace = self.repl
    pattern = re.compile("REF_FORMAT")
    refmatch = pattern.search(self.repl)
    if refmatch:
        reference_format = metadata[refmatch.group(0)].strip("'")
        replace = (
            replace[: refmatch.start()] + reference_format + replace[refmatch.end() :]
        )
    replace = match.expand(replace)
    return replace


REFERENCE = Rule(
    "Reference",
    r'<a label="(.+)">',
    r'<a href="#fig-\1" class="reference">REF_FORMAT</a>',
    formatting=reference_formattig,
)
