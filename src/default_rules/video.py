from rule import Rule
import re
import os


def video_formatting(self: Rule, metadata: dict[str, str], match) -> str:
    replace = self.repl
    video_string = match.group(0)

    # Obter caminho/nome da figura
    vidname_match = re.search(r' src="(.+?)"', video_string)
    if vidname_match:
        vidpath = metadata["MEDIAPATH"]
        vidname, vidext = os.path.splitext(vidname_match.group(1))
        full_vidname = vidname + vidext

        for arquivo in os.listdir(vidpath):
            if vidext and os.path.splitext(arquivo) == (vidname, vidext):
                full_vidname = os.path.join(vidpath, arquivo)
                break
            elif vidext == "" and os.path.splitext(arquivo)[0] == vidname:
                full_vidname = os.path.join(vidpath, arquivo)
                break

        m = re.search("VIDNAME", replace)
        if m:
            replace = replace[: m.start()] + full_vidname + replace[m.end() :]
    else:
        raise (FileNotFoundError)

    # Trantando o estilo
    vidstyle_match = re.search(r' size="(.+?)"', video_string)
    vidstyle = (
        f' style="{vidstyle_match.group(1)}"'
        if vidstyle_match
        else f' style="{metadata['VIDSTYLE']}"'
    )
    replace = re.sub(" VIDSTYLE", vidstyle, replace)

    # Tratando a legenda
    vidcaption_match = re.search(r' caption="(.+?)"', video_string)
    full_vidcaption = ""
    if vidcaption_match:
        vidcaption = vidcaption_match.group(1)
        vidformat = metadata["VID_FORMAT"].strip("'")
        full_vidcaption = f'<figcaption><span class="videolabel">{vidformat}</span>{vidcaption}</figcaption>'
    replace = re.sub("VID_CAPTION", full_vidcaption, replace)

    # Tratando o label
    vidlabel_match = re.search(r' label="(.+?)"', video_string)
    vidlabel = vidlabel_match.group(1) if vidlabel_match else vidname
    replace = re.sub("VIDLABEL", vidlabel, replace)

    return replace


_video_params = r'(?: (.+?)="(.+?)")*'
_video = r'<vid src="(.+?)"' + _video_params + r">"
_video_repl = r'<video VIDSTYLE controls COUNTER(VID,+,VIDLABEL)><source src="VIDNAME" id="vid-VIDLABEL"></video>VID_CAPTION'

VIDEO = Rule("Video", _video, _video_repl, formatting=video_formatting)
