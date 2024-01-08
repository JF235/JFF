# Adicionando regra com contador

## Definir o contador nos metadados

```
METADATA
---
COUNTER: EXAMPLE
...
---

...
```

## Definir a regra em um outro arquivo

```python
# Em `counter_rule.py`
import re
from rule import Rule
from rules import RULES

EXAMPLE = Rule(
    "Numbered Example", 
    r'<example>(.+?)</example>', 
    r'<div class="numbered_example" COUNTER(EXAMPLE,+)><span class="example_text">Exemplo COUNTER(EXAMPLE,=). </span>\1</div>',
    flags=re.DOTALL
)

RULES.append(EXAMPLE)
```

## Incluir o arquivo com nova regra

```python
# No `jf.py`
import counter_rule
```

## Adicionar os estilos no style.css

```css
.example_text {
    font-weight: bold;
}
```