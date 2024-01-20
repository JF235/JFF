from default_rules.paragraph import P, P_IDENT
from default_rules.headers import H1, H2, H3
from default_rules.bold_italic import BOLD, ITALIC
from default_rules.math import DISPLAY_MATH, INLINE_MATH, NUMBERED_MATH
from default_rules.lists import (
    ORDERED_LIST,
    ORDERED_ITEM,
    UNORDERED_LIST,
    UNORDERED_ITEM,
)
from default_rules.figure import FIGURE
from default_rules.video import VIDEO
from default_rules.reference import REFERENCE

from custom_rules.question_answer import QUESTION, ANSWER
from custom_rules.example_enviroment import EXAMPLE_ENV

RULES = [
    QUESTION,
    ANSWER,
    P,
    P_IDENT,
    H1,
    H2,
    H3,
    BOLD,
    ITALIC,
    NUMBERED_MATH,
    DISPLAY_MATH,
    INLINE_MATH,
    ORDERED_LIST,
    ORDERED_ITEM,
    UNORDERED_LIST,
    UNORDERED_ITEM,
    FIGURE,
    VIDEO,
    REFERENCE,
    EXAMPLE_ENV,
]
