METADATA
---
COUNTERS: H1, H2, H3, FIG
---

# Espaços Topológicos

Espaços topológicos são estruturas matemáticas que permitem a formalização dos conceitos de convergência, conexidade e continuidade. 
Eles aparecem em praticamente todos os ramos da matemática moderna e são uma noção unificadora central.

O ramo da matemática que estuda os espaços topológicos é denominado topologia.

## Definição

Uma **topologia** em um conjunto $X$ é uma coleção $\tau$ em partes de $X$, chamados os **abertos** da topologia, com as seguintes propriedades:

1. *O conjunto vazio e o próprio conjunto $X$ são abertos.* 

    $\emptyset, X\in \tau$

2. *A intersecção de dois conjuntos abertos é um aberto.*

    Se $A_1, A_2 \in \tau$, 
    então $A_1\cap A_2 \in \tau$

3. *A união de uma família arbitrária de abertos é um aberto.*

    Dada uma família arbitrária $(A_\lambda)_{\lambda \in L}$, com $A_\lambda \in \tau, \forall \lambda \in L$, tem-se $\left(\bigcup\limits_{\lambda\in L}A_\lambda\right) \in \tau$

Um **espaço topológico** é um par $(X, \tau)$ onde $X$ é um conjunto e $\tau$ é uma topologia em $X$.

## Exemplo

Dado o conjunto $X=\{1,2,3\}$, possíveis topologias $\tau$ são:

- $\{\emptyset, X\}$
- $\{\emptyset, X, \{1\}\}$
- $\{\emptyset, X, \{1\}, \{2\}, \{1, 2\}\}$
- $\{\emptyset, X, \{2\}, \{1, 2\}, \{2, 3\}\}$
- $\wp\{X\}$, conjunto potência (família de todos os subconjuntos de $X$)

Exemplos de conjuntos que não formam uma topologia

- $\{\emptyset, X, \{1, 2\}, \{2, 3\}\}$, viola a propriedade 2, uma vez que a intesecção dos abertos $\{1, 2\} \cap \{2, 3\}$ não é um aberto (não está em $\tau$).
- $\{\emptyset, X, \{1\}, \{2\}\}$, viola propriedade 3, uma vez que a união dos abertos $\{1\}\cup \{2\}$ não é um aberto.

# Grupos

Em matemática, um grupo é um conjunto de elementos associados a uma operação que combina dois elementos quaisquer para formar um terceiro. Para se qualificar como grupo o conjunto e a operação devem satisfazer algumas condições chamadas axiomas de grupo: associatividade, elemento neutro e elementos inversos. Apesar destes serem comuns a muitas estruturas matemáticas familiares - e.g. os números inteiros munidos da adição formam um grupo - a formulação dos axiomas é independente da natureza concreta do grupo e sua operação. Isso permite lidar-se com entidade de origens matemáticas completamente diferentes de uma maneira flexível, mas retendo os aspectos estruturais essenciais de muitos objetos da álgebra abstrata e além. A ubiquidade dos grupos em inúmeras áreas - dentro e fora da matemática - os tornam um princípio organizador central da matemática contemporânea. 

## Definição

Seja $G$ um conjunto e $\ast$ uma **operação binária** definida sobre $G$. O par ordenado $(G,\ast)$ é um grupo se são satisfeitos os seguintes axiomas:

Sendo $a, b, c \in G$

- **Fecho**: $a\ast b \in G$
- **Associatividade**: $(a\ast b)\ast c =  a\ast (b\ast c)$
- **Elemento neutro**: Existe $1_G \in G$  tal que $a\ast 1_G = 1_G\ast a = a$
- **Elemento simétrico**: Para qualquer elemento $g\in G$ existe $g' \in G$  tal que $g\ast g' = g'\ast g = 1_G$
