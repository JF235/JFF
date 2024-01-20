from rule import Rule

BOLD = Rule("Bold", r"\*\*(.*?)\*\*", r"<strong>\1</strong>")
ITALIC = Rule("Italic", r"\*(.*?)\*", r"<em>\1</em>")
