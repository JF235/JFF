def get_default_metadata() -> dict:
    return {
        "COUNTERS": "H1, H2, H3, FIG, VID, EQ",
        "H1_FORMAT": "'COUNTER(H1,=). '",
        "H2_FORMAT": "'COUNTER(H1,=).COUNTER(H2,=). '",
        "H3_FORMAT": "'COUNTER(H1,=).COUNTER(H2,=).COUNTER(H3,=). '",
        "FIG_FORMAT": "'Figure COUNTER(FIG,=) - '",
        "FIG_REF": r"'Fig.&nbsp;COUNTER(FIG,=,\1)'",
        "EQ_REF": r"'Eq.&nbsp;COUNTER(EQ,=,\1)'",
        "EQ_FORMAT": r"'COUNTER(EQ,=)'",
        "FIGSTYLE": "width: 50%",
        "VID_FORMAT": "'Vídeo COUNTER(VID,=) - '",
        "VIDSTYLE": "width: 50%",
        "MEDIAPATH": ".\\",
    }
