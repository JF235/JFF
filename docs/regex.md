# Regex

Expressões regulares usadas no projeto.

## Títulos

```
^# (.+)$
flag = MULTILINE
```

- `^` no começo da linha,
- `# ` apresenta um hashtag seguid de espaço
- `(.+)` um grupo com vários caracteres (exceto `\n`)
- `$` até o fim da linha

As outras expressões regulares de títulos alteram o número de `#` na expressão

```
^## (.+)$
^### (.+)$
```

## Negrito e Itálico

```
BOLD   -> r"\*\*(.*?)\*\*"
ITALIC -> r"\*(.*?)\*"
```

Observe que o padrão `BOLD` deve ser aplicado primeiro, uma vez que `ITALIC` também iria encontrar qualquer padrão com dois asteriscos.

## Matemática

```
DISPLAY_MATH -> r"\$\$(.+?)\$\$", flag DOTALL
INLINE_MATH  -> r"\$(.+?)\$"
```

A mesma observação feita no caso de negrito e itálico também pode ser aplicada, de forma que a regra `DISPLAY_MATH` deve ser aplicada primeiro.

No entanto, existe uma diferença sendo que o ambiente `DISPLAY_MATH` permite digitar uma fórmula em mais de uma linha, por conta da flag `DOTALL`.

## Parágrafos

A expressão que representa os parágrafos, são quebradas em subexpressões:

### Padrões especiais de começo de linha 

```python
_padroes_especiais = r"#|\d\.|[-*][ ]|\$\$|```|<"
```

Esses padrões são usados para garantir que um parágrafo não será identificado em trechos que são começados com os padrões:
- `#`, título
- `\d\.` (dígito seguido de ponto), item de uma lista ordenada
- `-` ou `*` seguido de espaço, item de uma lista não ordenada
- `\$\$`, equação no modo display
- ` ``` ` código
- `<`, outra tag especial como `<figure>`, `<answer>`, `<question>`

### Conteúdo do parágrafo

```python
_conteudo = r"((.+\n)+)"
```

São os conteúdos dos parágrafos
- `(.+)\n` uma linha acabada em `\n`.
- `(?:(.+)\n)+` múltiplas linhas. O grupo com `(?:...)` não captura o conteúdo
- `((?:(.+)\n)+)` grupo que captura todas as linhas, inclusive a última quebra de linha

### Parágrafo sem identação

```
r"(?<=\n\n)" + f"(?!{_padroes_especiais + r"|[ ]{4}"})" + _conteudo + r"(?=\n)"
```

- `(?<=\n\n)`, lookbehind que garante que é precedido por uma linha vazia
- `(?!{_padroes_especiais + r"|[ ]{4}"})` não começa com caracteres especiais ou quatro espaços (elimina as identações)
- `_conteudo`, múltiplas linhas
- `(?=\n)`, lookahead que garante que é seguido de uma linha vazia (somente um `\n` é necessário, pois o último está contido em `_conteudo`)

### Parágrafo com identação

Em um parágrafo com identação, a única diferença é que após a linha vazia `(?<=\n\n)` deve haver uma identação de 4 espaços em branco `[ ]{4}`, que não pode ser seguida de um dos padroes especiais.

```
r"(?<=\n\n)" + r"(([ ]{4}" + f"(?!{_padroes_especiais})" + r".+\n)+)" + r"(?=\n)"
```

## Listas

### Linhas da Lista

```
(.+\n([ ]{4}.+\n|\n)*)
```

- `.+\n`, primeira linha não vazia
- `([ ]{4}.+\n|\n)*` linhas opcionais com 4 espaços iniciais e conteúdo (ou linha vazia)

### Itens de Lista e Lista Inteira

```
^\d+\.[ ]+" + _ordered_item_lines
```

- `^\d+\.[ ]+`, uma linha que começa com um digito+ponto e espacos vazios
- `_ordered_item_lines`, linhas da lista

No caso de uma lista não ordenada, os itens tem os caracteres inicias da linha trocados

```
r"^[-*][ ]+" + _unordered_item_lines
```

A lista inteira é representada por um conjunto de diversos itens seguidos

```
(({_ordered_item})+)
```

## Código

```
r"\`\`\`(.+?)\n(.+?)\`\`\`"
flag DOTALL
```

- Três acentos graves seguidos da linguagem que será usada.
- O conteúdo do código
- Três acentos graves finais

## Figura

### Parâmetros da figura 

```python
_figure_params = r'(?: (.+?)="(.+?)")*'
```

Expressões da forma `nome_param="param_value"` 

### Figura completa

```python
_figure = r'<fig(?:ure)? src="(.+?)"' + _figure_params + r">"
```

- `<fig(?:ure)? src="(.+?)"` uma tag autofechada que pode ser com o texto `fig` ou `figure` e apresenta o primeiro parâmetro `src` que indica o caminho da figura.
- Parâmetros opcionais
- Fechamento da tag

## Vídeo

Muito parecido com figura:

```
_video_params = r'(?: (.+?)="(.+?)")*'
r'<vid src="(.+?)"' + _video_params + r">"
```

## Condição de Contorno

Devida a necessidade de uma linha vazia antes e depois de alguns dos padrões, é adicionado um *padding* de linhas vazias no começo e no fim do conteúdo do arquivo `.md` processado.

```python
with open(filename, mode="r", encoding="utf8") as file:
        string = file.read()
        # Para garantir que as regras funcionem de forma apropriada...
        string += "\n\n"
```