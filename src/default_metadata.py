
def get_default_metadata() -> dict:
    return {
        "COUNTERS": "H1, H2, H3, FIG",
        "H1_FORMAT": "'COUNTER(H1,=). '",
        "H2_FORMAT": "'COUNTER(H1,=).COUNTER(H2,=). '",
        "H3_FORMAT": "'COUNTER(H1,=).COUNTER(H2,=).COUNTER(H3,=). '",
        "FIG_FORMAT": "'Figure COUNTER(FIG,=) - '",
        "REF_FORMAT": r"'Fig.&nbsp;COUNTER(FIG,=,\1)'"
    }