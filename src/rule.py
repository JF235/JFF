import re


def rawString(string: str) -> str:
    return repr(string)[1:-1]


class Rule:
    def __init__(
        self,
        name: str,
        pattern: str,
        repl: str,
        flags: re.RegexFlag = re.NOFLAG,
    ):
        self.name = name
        self.pattern = re.compile(pattern, flags)
        self.repl = repl

    def __repr__(self):
        return f"Rule({self.name}, {self.get_pattern_string()})"

    def apply(self, string: str) -> str:
        """Aplica a regra na `string`, consistindo em:
        - Encontrar o padrão com `self.pattern`
        - Executar a função `pre_func`
        - Substituir o padrão com `self.repl` e formatando o resultado
        - Executar a função `post_func`

        Args:
            string (str): Nova string após aplicação da regra
        """

        new_string = string
        match = self.pattern.search(new_string)
        span = (0, 0)

        while match:
            new_string, span = self.replace(match, new_string)
            match = self.pattern.search(new_string, span[1])

        return new_string

    def replace(self, match: re.Match[str], string: str) -> tuple[str, tuple[int, int]]:
        """Substitui na `string` o padrão `match` por `self.repl` com
        as substituições do grupo e formatação desejada.

        Args:
            match (re.Match[str]): Padrão encontrado
            string (str): String onde será feita a substituição

        Returns:
            tuple[str, tuple[int, int]]: Tupla com novo padrão substituído e tupla com a posição da substituição
        """
        pos, endpos = match.span()
        # Não sei se usar match.expand() é a melhor maneira...
        replace = match.expand(self.repl)
        replace = self.format_string(replace)
        new_string = string[:pos] + replace + string[endpos:]
        return new_string, (pos, pos + len(replace))

    def format_string(self, string: str) -> str:
        # TODO: Não gosto do jeito que está implementado...
        new_string = string
        if self.name == "Paragraph" or self.name == "Paragraph w Identation":
            match = re.search(r"(<p>)(.+?)(</p>)", string, re.DOTALL)
            if match:
                middle = match.group(2)
                middle = middle.strip()
                new_string = match.expand(r"\1" + rawString(middle) + r"\3")
                new_string = new_string + "\n"
                if self.name == "Paragraph w Identation":
                    new_string = (" " * 4) + new_string
        elif self.name == "Ordered Item" or self.name == "Unordered Item":
            match = re.search(r"(<li>)(.+?)(</li>)", string, re.DOTALL)
            if match:
                middle = match.group(2)
                middle = middle.rstrip("\n")
                new_string = match.expand(
                    r"\1" + rawString(middle) + "\n" + r"\3" + "\n\n"
                )
        elif self.name == "Ordered List" or self.name == "Unordered List":
            match = re.search(r"(<[ou]l>)(.+?)(</[ou]l>)", string, re.DOTALL)
            if match:
                new_string = match.expand(r"\1" + "\n\n" + r"\2" + r"\3" + "\n\n")

        return new_string

    def format_repl(self, metadata: dict):
        for arg_name in metadata:
            # TODO: Aqui não preciso percorrer todos os itens
            if "_FORMAT" in arg_name:
                formatted_string = rawString(metadata[arg_name].strip("'"))
                self.repl = re.sub(arg_name, formatted_string, self.repl)

    def get_pattern_string(self) -> str:
        return self.pattern.pattern
