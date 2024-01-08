METADATA
---
FIGPATH: navigation_imgs
---

# Introduction

## Fundamental Concepts

TODO

## Coordinate Frames

❓ O que é um *cordinate frame*? O que é o *resolving frame*? O que são os *reference frame* e *object frame*?

*Dica: p. 44*

❓ Qual o número mínimo de sistemas de coordenadas necessário em um problema de navegação?

*Dica: p. 24*

### Earth-Centered Inertial Frame

❓ O que é o referencial ECI? Por que ele não é estritamente inercial e por que não precisamos nos preocupar com isso?

❓ Como são orientados os eixos? Qual a origem?

<figure src="ECI_FRAME" size="width: 35%">

### Earth-Centered Earth-Fixed Frame

❓ Quais as diferenças entre o ECEF e o ECI? Quais as semelhanças?

❓ Como são orientados os eixos?

<figure src="ECEF_FRAME">

### Local Navigation Frame (NED)

❓ Qual a origem e como são orientado os eixos?

<figure src="NED_FRAME">

### Local Tangent-Plane Frame

❓ Como descrever esse sistema?

### Body Frame

❓ Qual a diferença entre o *body frame* e o *local navigation frame*?

<figure src="BODY_FRAME">

## Attitude, Rotation, and Resolving Axes Transformations

❓ O que é *attitude*?

<div style="color: #8BE9FD; border-style: dotted; border-color: #8BE9FD; margin-bottom: 2em">
Attitude describes the orientation of the axes of one coordinate frame with respect to those of another.
</div>

❓ Considere dois sistemas de coordenadas, $\beta$ e $\gamma$ com mesma origem, sendo que o segundo está rotacionado de um ângulo $+\psi$ do primeiro. Qual a coordenada de um ponto $\alpha$ com distância $r$ da origem e ângulo $\phi$ **a)** para o sistema $\beta$, **b)** para o sistema $\gamma$ e **c)** qual a expressão que relaciona ambas as coordenadas? ($\mathbf{x}^{\gamma}_{\beta\alpha} = R\mathbf{x}^\beta_{\beta\alpha}$)

*Dica: O sentido positivo dos ângulos diz que a rotação acontece no sentido positivo da rotação trigonométrica (anti-horário)*

<fig src="rot2d">

### Euler Attitude

❓ Vimos como escrever uma relação entre as coordenadas de um ponto para dois sistemas de coordenadas, rotacionados entre si por um ângulo $\psi$. Considerando dois sistemas em três dimensões, quais seriam as três relações considerando a rotação em torno de cada um dos eixos?

*Dica: O sentido positivo de rotação para cada um dos eixos é mostrado na figura abaixo.*

*Dica 2: Reduza cada caso para uma rotação em 2D, com o eixo fixo orientado de forma a sair da página*

<fig src="positive_rotations" size="width: 90%">

Resolução:

<fig src="solution">

### Coordinate Transformation Matrix

❓ Qual a relação entre as matrizes $(\mathbf{C}_\alpha^\beta)^T$ e $(\mathbf{C}_\alpha^\beta)^{-1}$?

❓ Como transformar um vetor entre *resolving frames*? Como transformar uma matriz entre *resolving frames*?

❓ Como escrever uma matriz de transformação $\mathbf{C}_\alpha^\beta$ em termos dos ângulos de Euler?


### Quaternion Attitude

❓ Quais as singularidades em ângulos de Euler?

❓ Qual a representação de um quaternion e quais os graus de liberdade?

### Rotation Vector

TODO

## Kinematics

❓ Quais os três frames envolvidos nas representações cinemáticas?

### Angular rate

❓ Deduza a equação para a derivada temporal da matriz de transformação de coordenadas, isto é, $\dot{\mathbf{C}}_\beta^\alpha$