METADATA
---
MEDIA_PATH: navigation_imgs
---


<div style="display: none">
\(
    \def\RF{\boldsymbol{\mathcal{F}}}
    \def\bvec#1{\mathbf{#1}}
\)
</div>

# Introduction

## Fundamental Concepts

TODO

# Coordinate Frames, Kinematics, and the Earth

## Coordinate Frames

<question>
O que é um *cordinate frame*? O que são os *reference frame* e *object frame*? O que é o *resolving frame*?

*Dica: p. 44*
</question>

<answer>
Para descrever o movimento de um **objeto** é necessário indicar: sua posição, a partir de um ponto chamado origem, e sua orientação, a partir de três eixos ortonormais.

No entanto, essas informações não tem sentido sozinhas. A posição e orientação do objeto devem ser baseadas em uma referência, que também é descirta por uma origem e três eixos.

O conjunto de uma origem e três eixos é chamado de *coordinate frame*. O *object frame* está associado ao objeto e o *reference frame* está associado à referência, como centro da terra, centro do sistema solar ou uma posição terrestre definida.

Dois *coordinate frames* podem apresentar uma orientação relativa entre si. Para ajustar isso, eu uso um *resolving frame* para descrever a orientação dos vetores de posição, velocidade, velocidade-angular no espaço.
</answer>


<question>
Qual o número mínimo de sistemas de coordenadas necessário em um problema de navegação?

*Dica: p. 24*
</question>

<answer>
Dois sistemas de coordenada são necessários: um do objeto e um de referência.
</answer>


### Earth-Centered Inertial Frame

<question>
O que é o referencial ECI? Por que ele não é estritamente inercial e por que não precisamos nos preocupar com isso?
</question>

<answer>
O *Earth-centered inertial frame* é um sistema com origem no centro da terra e com eixo $z$ orientado na direção do polo norte geográfico. Os eixos $xy$ estão no plano equatorial, mas não realizam o movimento de rotação com a terra.

Não é um sistema estritamente inercial uma vez que a terra realiza um movimento de revolução em torno do sol, mas esses efeitos podem ser ignorados, uma vez que são menores que o ruído das medidas. 

<figure src="ECI_FRAME" style="width: 35%">
</answer>

### Earth-Centered Earth-Fixed Frame

<question>
Quais as diferenças entre o ECEF e o ECI? Quais as semelhanças?
</question>

<answer>
Em contraste com o ECI, o sistema ECEF tem os eixos acoplados ao movimento de rotação da terra. Com eixo $z$ e origem iguais, mas com eixo $x$ indo da origem até o meridiano de Greenwich $0°$ L e o eixo $y$ completa o sistem destro.

<figure src="ECEF_FRAME">
</answer>

### Local Navigation Frame (NED)

<question>
Qual a origem e como são orientado os eixos?
</question>

<answer>
A origem está acoplada a um objeto e os eixos são definidos de forma que $z$ é a direção *Down*, aponta para o centro da terra, $x$ *North*, é a projeção no plano ortogonal a $z$ da linha que liga o objeto até o polo norte.

Esse sistema não serve de *reference frame*.

<figure src="NED_FRAME">
</answer>

### Local Tangent-Plane Frame

<question>
Como descrever esse sistema?
</question>

<answer> 
O sistema é descrito em aplicações locais, com um plano tangente a terra.
</answer>
 
### Body Frame

<question>
Qual a diferença entre o *body frame* e o *local navigation frame*?
</question>

<answer>
O *body frame* é formado pela origem e orientação do objeto descrito. A origem é a mesma do *NED (local) frame*, mas os eixos estão fixos com relação ao objeto.

<figure src="BODY_FRAME">
</answer>

## Attitude, Rotation, and Resolving Axes Transformations

<question>
O que é *attitude*?
</question>

<answer>
Attitude describes the orientation of the axes of one coordinate frame with respect to those of another.
</answer>

<question>
Considere dois sistemas de coordenadas, $\beta$ e $\gamma$, sendo que o segundo está rotacionado de um ângulo $+\psi$ do primeiro. Qual a coordenada de um ponto $\alpha$ com distância $r$ da origem de $\beta$ e ângulo $\phi$ **a)** para o sistema $\beta$, **b)** para o sistema $\gamma$ e **c)** qual a expressão que relaciona ambas as coordenadas? ($\mathbf{x}^{\gamma}_{\beta\alpha} = R\mathbf{x}^\beta_{\beta\alpha}$)

*Dica: O sentido positivo dos ângulos diz que a rotação acontece no sentido positivo da rotação trigonométrica (anti-horário)*

<fig src="rot2d">
</question>

<answer>
a)
$$\begin{bmatrix}
    x_{\beta\alpha}^{\beta} \\
    y_{\beta\alpha}^{\beta}
\end{bmatrix} = 
\begin{bmatrix}
    r_{\beta\alpha}\cos\phi \\
    r_{\beta\alpha}\sin\phi
\end{bmatrix}$$

b)
$$\begin{bmatrix}
    x_{\beta\alpha}^{\gamma} \\
    y_{\beta\alpha}^{\gamma}
\end{bmatrix} = 
\begin{bmatrix}
    r_{\beta\alpha}\cos(\phi - \psi) \\
    r_{\beta\alpha}\sin(\phi - \psi)
\end{bmatrix}$$

c)
$$\begin{bmatrix}
    x_{\beta\alpha}^{\gamma} \\
    y_{\beta\alpha}^{\gamma}
\end{bmatrix}
=
\begin{bmatrix}
    \cos\psi && \sin\psi \\
    -\sin\psi && \cos\psi
\end{bmatrix}
\begin{bmatrix}
    x_{\beta\alpha}^{\beta} \\
    y_{\beta\alpha}^{\beta}
\end{bmatrix}
$$

*Observação* - Quando usamos o sistema $\gamma$ como *resolving frame*, não é necessário indicar a origem desse sistema, pois a distância do ponto só é dependente do *reference frame* $\beta$.
</answer>

### Euler Attitude

<question>
Vimos como escrever uma relação entre as coordenadas de um ponto para dois sistemas de coordenadas, rotacionados entre si por um ângulo $\psi$. Considerando dois sistemas em três dimensões, quais seriam as três relações considerando a rotação em torno de cada um dos eixos?

*Dica: O sentido positivo de rotação para cada um dos eixos é mostrado na figura abaixo.*

*Dica 2: Reduza cada caso para uma rotação em 2D, com o eixo fixo orientado de forma a sair da página*

<fig src="positive_rotations" style="width: 90%">
</question>

<answer>
<fig src="solution">
</answer>

### Coordinate Transformation Matrix

<question>
Como transformar um vetor entre *resolving frames*?
</question>

<answer>
Vamos começar definindo o conceito de uma *vectrix* associado a um sistema de coordenada $\alpha$ como sendo um vetor, com cada componente sendo um vetor da base do sistema de coordenadas

$$\RF_\alpha = \begin{bmatrix}
    \bvec{i}_\alpha \\
    \bvec{j}_\alpha \\
    \bvec{k}_\alpha \\
\end{bmatrix}$$

Dessa forma, um vetor $\bvec{v}$ escrito na base canônica pode ser representado por

$$
\bvec{v} = v_{x\alpha}\bvec{i}_\alpha+
v_{y\alpha}\bvec{j}_\alpha+
v_{z\alpha}\bvec{k}_\alpha =
\RF_\alpha^T\bvec{v}_\alpha
$$

para qualquer outra base. O produto escalar envolvendo a entidade *vectrix*, como $\RF_\alpha^T\bvec{v}_\alpha$, deve ser interpretada como o produto entre o vetor e cada elemento da *vectrix*.

Um fato importante de uma base unitária é que o produto entre duas *vectrices* é

$$\RF_\alpha\RF_\alpha^T = \mathbb{I}$$

Dessa maneira, para duas bases diferentes, temos

$$
\bvec{v} =
\RF_\alpha^T\bvec{v}_\alpha =
\RF_\beta^T\bvec{v}_\beta
$$

Multiplicando ambos os lados por $\RF_\beta$

$$\bvec{v}_\beta = \RF_\beta\RF_\alpha ^T\bvec{v}_\alpha = \mathbf{C}_\alpha^\beta \bvec{v}_\alpha$$

Com a matriz de transformação de $\alpha$ para $\beta$ sendo

$$\mathbf{C}_\alpha^\beta 
= 
\begin{bmatrix}
    \bvec{i}_\beta\\
    \bvec{j}_\beta\\
    \bvec{k}_\beta
\end{bmatrix}
\begin{bmatrix}
    \bvec{i}_\alpha &
    \bvec{j}_\alpha &
    \bvec{k}_\alpha
\end{bmatrix}
=
\begin{bmatrix}
    \bvec{i}_\beta \cdot \bvec{i}_\alpha & \bvec{i}_\beta \cdot \bvec{j}_\alpha & \bvec{i}_\beta \cdot \bvec{k}_\alpha \\
    \bvec{j}_\beta \cdot \bvec{i}_\alpha & \bvec{j}_\beta \cdot \bvec{j}_\alpha & \bvec{j}_\beta \cdot \bvec{k}_\alpha \\
    \bvec{k}_\beta \cdot \bvec{i}_\alpha & \bvec{k}_\beta \cdot \bvec{j}_\alpha & \bvec{k}_\beta \cdot \bvec{k}_\alpha \\
\end{bmatrix}$$
</answer>

<question>
Qual a relação entre as matrizes $(\mathbf{C}_\alpha^\beta)^T$ e $(\mathbf{C}_\alpha^\beta)^{-1}$?
</question>

<answer>
Como o processo de inversão de uma matriz representa o retorno ao sistema original, então  $(\mathbf{C}_\alpha^\beta)^{-1} = \mathbf{C}_\beta^\alpha$. Dessa forma

$$(\mathbf{C}_\alpha^\beta)^T = (\RF_\beta \RF_\alpha^T)^T = \RF_\alpha\RF_\beta^T = \mathbf{C}_\beta^\alpha = (\mathbf{C}_\alpha^\beta)^{-1} $$

**IMPORTANTE**: Se eu tenho um sistema $\alpha$ e desejo aplicar uma rotação $R$ nele para obter um outro sistema $\beta$, então dado qualquer ponto em $\alpha$, para obter a coordenada resolvida em $\beta$ devo aplicar $R^{-1}$.

Por exemplo, tenho um sistema $\alpha$ e um ponto a $+60$ graus. Além disso, gostaria de criar um outro sistema $\beta$ girando $+30$ graus. Nesse caso, para obter a coordenada do ponto resolvido em $\beta$, em função de $\alpha$, aplico a rotação de $-30$ graus.
</answer>

<question>
Como escrever uma matriz de transformação $\mathbf{C}_\alpha^\beta$ em termos dos ângulos de Euler?
</question>

<answer> 
Vimos que para transformar de um sistema $\beta$ para um sistema $\alpha$ são necessários 3 valores, os *ângulos de Euler*

$$\boldsymbol{\Psi}_{\beta\alpha} = \begin{bmatrix}
    \phi_{\beta\alpha} \\
    \theta_{\beta\alpha} \\
    \psi_{\beta\alpha} \\
\end{bmatrix}$$

Sendo assim, rotacionar de $\beta$ para $\alpha$ consiste em aplicar sucessivamente as rotações de $\psi_{\beta\alpha}$ em torno do eixo $z$, $\theta_{\beta\alpha}$ em torno de $y$ e $\phi_{\beta\alpha}$ em torno de $x$.

<fig src="euler_coord_transf" style="width: 90%">
</answer>

<question>
Como transformar uma matriz entre *resolving frames*?
</question>

<answer> 
Dada uma matriz $\mathbf{M}_\alpha$ que transforma um vetor $\bvec{v}_\alpha$ em um vetor $\bvec{u}_\alpha$, gostaria de enontrar $\mathbf{M}_\beta$ que transformasse $\bvec{v}_\beta$ em $\bvec{u}_\beta$

$$\bvec{u}_\alpha = \mathbf{M}_\alpha\bvec{v}_\alpha$$

$$\mathbf{C}_\beta^\alpha\bvec{u}_\beta = \mathbf{M}_\alpha\mathbf{C}_\beta^\alpha\bvec{v}_\beta$$

$$\bvec{u}_\beta = \mathbf{C}_\alpha^\beta\mathbf{M}_\alpha\mathbf{C}_\beta^\alpha\bvec{v}_\beta \Leftrightarrow \mathbf{M}_\beta = \mathbf{C}_\alpha^\beta\mathbf{M}_\alpha\mathbf{C}_\beta^\alpha$$
</answer> 

### Quaternion Attitude

<question> 
Quais as singularidades em ângulos de Euler?
</question>

<answer>
A princípio, os ângulos de Euler são impecáveis, uma vez que dados os três ângulos $(\phi, \theta, \psi)$ é possível converter entre dois sistemas arbitrários. 

O problema ocorre em interpolações, por exemplo, quando uma determinada rotação intermediária acaba alinhando dois eixos de rotação. Isso é chamado de **Gimbal Lock**. 

Vamos demonstrar esses problemas com base em um exemplo, no qual desejo rotacionar a *Suzzane* em duas etapas.

1. Rotacionar -90 graus em torno de $z$ (global)
2. Rotacionar -90 graus em torno de $x$ (global)

O resultado esperado é mostrado no vídeo <a label="vid-rotate-yxz">, usando quaternions que não sofrem com Gimbal Lock

<vid src="rotate-yxz" caption="Rotação adequada sem Gimbal Lock" label="vid-rotate-yxz">

Na ordem de rotação XZY, ou seja, com matriz de rotação dada por

$$\mathbf{C} = R_x(\phi)R_z(\psi)R_y(\theta)$$

O resultado é mostrado no <a label="vid-rotate-xyz">

<vid src="rotate-xyz" caption="Rotação com Gimbal Lock" label="vid-rotate-xyz">

A diferença entre os resultados aparece por conta da ordem das multiplicações.

Quando $\psi = -\pi/2$, temos a matriz na forma

$$
\begin{pmatrix}
0 & 1 & 0\\
-\cos \left(\phi +\theta \right) & 0 & -\sin \left(\phi +\theta \right)\\
-\sin \left(\phi +\theta \right) & 0 & \cos \left(\phi +\theta \right)
\end{pmatrix}
$$

Indicando que as rotações em torno de $x$ e $y$ são redundantes (causam o mesmo efeito). Dizemos então que um dos graus de liberdade de rotação foi perdido.

Mais especificamente, o grau de rotação perdido é justamente aquele associado a rotação em torno do $x$ global. Dessa forma, não há mais como atingir o objetivo.

Para recuperar um dos graus de liberdade, o software *Blender* precisa desfazer parte da primeira rotação, desbloqueando a trava com relação a segunda rotação em torno de $x$ global, resultando no movimento estranho.

Podemos ver isso nas figuras abaixo

<fig src="interp-error">
<fig src="interp-certo">

</answer>

<question>
Qual a representação de um quaternion e quais os graus de liberdade?
</question>

### Rotation Vector

TODO

## Kinematics

<question>
Quais os três frames envolvidos nas representações cinemáticas?
</question>

### Angular rate

<question>
Deduza a equação para a derivada temporal da matriz de transformação de coordenadas, isto é, $\dot{\mathbf{C}}_\beta^\alpha$
</question>