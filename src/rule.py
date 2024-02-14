import re

def rawString(string: str) -> str:
    return repr(string)[1:-1]

# TODO: Talvez eu não precise disso se eu fizer o meu próprio expand
# Pois estava tendo problemas com o uso de .expand em strings com caracteres escapados
def default_formatting(self, match):
    replace = match.expand(self.repl)
    return replace

class Rule:
    def __init__(
        self,
        name: str,
        pattern: str,
        repl: str,
        flags: re.RegexFlag = re.NOFLAG,
        formatting=default_formatting,
    ):
        self.name = name
        self.pattern = re.compile(pattern, flags)
        self.repl = repl
        self.formatting = formatting

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

        while match:
            pos, endpos = match.span()

            # Formata a string que será substituída no lugar do match
            replace = self.formatting(self, match)
            new_string = new_string[:pos] + replace + new_string[endpos:]

            # A soma de len(replace) garante que a nova busca só acontece após todo
            # texto já analisado, evitando reaplicações de regra.
            match = self.pattern.search(new_string, pos + len(replace))

        return new_string

    def get_pattern_string(self) -> str:
        return self.pattern.pattern
