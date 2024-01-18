# JF's Formatting

Formatando documentos.

## Uso

```bash
python jff.py filename.md
# Outputs: filename.html in current directory
```

## TODOS

- Numerar equação
- Permitir que as referências sejam feitas independente do que foi citado (vídeos, figuras, código)
- Incluir as legendas de ambientes separadamente.
- Organizar o diretório: disponibilizar os casos de teste, organizar os scripts .py
- Incluir arquivo css padrão nos metadados
- Melhorar a forma de incluir novas regras e separar css para cada uma
- Não permitir que código seja executado dentro de `counter_rule` e `question_rule`
- Adicionar uma documentação com todos os recursos disponíveis
- Repensar os padrões especiais de parágrafo
- Padrões que devem ser precedidos por um espaço vazio ou um começo de linha, como itálico e negrito. Desta forma, seria capaz de adicionar caracteres de escape e evitar ambiguidades, como no caso de negrito/itálico.