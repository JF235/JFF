from rule import Rule


def link_formatting(self: Rule, match) -> str:
    if match.group(1):
        self.repl = r'<a class="url" href="\2">\1</a>'
    else:
        self.repl = r'<a class="url" href="\2">\2</a>'
    return match.expand(self.repl)


_empty_space = r"(?<=[ ]|\n|[(])"
LINK = Rule("Link", _empty_space + r"\[(.+?)\]\((.+?)\)", "", formatting=link_formatting)
