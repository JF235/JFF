from rule import Rule
from jff_globals import METADATA
import re
import os

METADATA["COUNTERS"] += ", VID"
METADATA.update(
    {
        "VID_FORMAT": "'Vídeo COUNTER(VID,=) - '",
        "VID_STYLE": "width: 50%",
        "VID_REF": r"'Vídeo&nbsp;COUNTER(VID,=,\1)'"
    }
)


def video_formatting(self: Rule, match) -> str:
    video_string = match.group(0)
    vidpath = METADATA["MEDIA_PATH"]

    vidname = match.group(1)
    name, ext = os.path.splitext(vidname)

    full_vidname = os.path.join(vidpath, vidname)

    if ext == "":
        arquivo = next(
            arquivo
            for arquivo in os.listdir(vidpath)
            if os.path.splitext(arquivo)[0] == name
        )
        full_vidname = os.path.join(vidpath, arquivo)

    # Trantando o estilo
    vidstyle_match = re.search(r' style="(.+?)"', video_string)
    vidstyle = (
        f'style="{vidstyle_match.group(1)}"'
        if vidstyle_match
        else f'style="{METADATA['VID_STYLE']}"'
    )

    # Tratando a legenda
    vidcaption_match = re.search(r' caption="(.+?)"', video_string)
    full_vidcaption = ""
    if vidcaption_match:
        vidcaption = vidcaption_match.group(1)
        vidformat = METADATA["VID_FORMAT"].strip("'")
        full_vidcaption = f'<figcaption><span class="videolabel">{vidformat}</span>{vidcaption}</figcaption>'

    vidlabel_match = re.search(r' label="(.+?)"', video_string)
    vidlabel = vidlabel_match.group(1) if vidlabel_match else vidname

    replace = f'<video {vidstyle} id="{vidlabel}" controls COUNTER(VID,+,{vidlabel})><source src="{full_vidname}"></video>{full_vidcaption}'

    return replace


_video_params = r'(?: (.+?)="(.+?)")*'
_video = r'<vid src="(.+?)"' + _video_params + r">"
_video_repl = ""

VIDEO = Rule("Video", _video, _video_repl, formatting=video_formatting)
