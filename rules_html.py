H1_T = r"<h1>\1</h1>"
H2_T = r"<h2>\1</h2>"
H3_T = r"<h3>\1</h3>"

BOLD_T = r"<strong>\1</strong>"
ITALIC_T = r"<em>\1</em>"

INLINE_MATH_T = r'<span class="inline-math">\(\1\)</span>'
DISPLAY_MATH_T = r'<div class="display-math">\[\1\]</div>'

ORDERED_LIST_T = r"<ol>\n\1</ol>"
ORDERED_ITEM_T = r"<li>\1</li>"

UNORDERED_LIST_T = r"<ul>\n\1</ul>"  # Newline para evitar problema com o primeiro item
UNORDERED_ITEM_T = r"<li>\1</li>"

P_T = r"\1<p>\2</p>"

TARGET_RULES = [
    P_T,
    H1_T,
    H2_T,
    H3_T,
    BOLD_T,
    ITALIC_T,
    INLINE_MATH_T,
    DISPLAY_MATH_T,
    ORDERED_LIST_T,
    ORDERED_ITEM_T,
    UNORDERED_LIST_T,
    UNORDERED_ITEM_T,
]
