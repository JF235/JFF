METADATA
---
COUNTERS: EXAMPLE
FIG_FORMAT: 'Figura COUNTER(H1,=).COUNTER(FIG,=) - '
REF_FORMAT: 'Figura COUNTER(H1,=).COUNTER(FIG,=,\1)'
---

# Manifolds

The idea of a differentiable manifold had its genesis in the nineteenth century
with the work of Carl Friedrich Gauss and of Georg Friedrich Bernhard Riemann.
Gauss was interested in surveying and cartography, which led him to develop the
tools of calculus on curved surfaces. His famous *theorema egregium*, or remarkable theorem, revealed that one could consider the intrinsic properties of a surface
independently of the way in which it was embedded in three-dimensional space,
and this led him, Riemann, and others, to abstract these concepts even further.
Their ideas have had far reaching applications in many areas of mathematics and
the natural sciences.

Roughly, an $n$-dimensional manifold (or $n$-manifold) can be thought of as a kind
of patchwork quilt built from pieces of $\mathbb{R}^n$ . Classic examples of 2-manifolds are
the 2-sphere $S^2$ and the 2-torus $T^2$ (see <a label="manifolds">). Usually one pictures these as
living in $\mathbb{R}^3$ , but one can consider them in their own right just as bits of $\mathbb{R}^2$ sewn
together in certain ways. The technical definition of a manifold requires considerable background, which we will try to keep to a minimum. First, we need the idea
of a topology.

<figure src="manifolds.png" size="width:70%" caption="The 2-sphere and the 2-torus" label="manifolds">

## Basic Topology

Consider a basketball. When it is inflated, its surface is a sphere. But when it is
deflated its surface *is still a topological sphere*. In fact, we could deform the sphere
in any way we like and, as long as we do not tear it anywhere, it is still topologically a sphere. We say that all these shapes have the same *topology* but, since
the distance between the points on the surface has changed, they have different
*geometries* (see <a label="manifolds2">).

<figure src="manifolds2.png" size="width:70%" caption="Topological 2-spheres." label="manifolds2">

At first sight the actual definition of a topology appears to have nothing to do
with these notions. Only after much study does one begin to see why the following
definition is reasonable. A **topology** $\tau$ on a set $X$ is a family of subsets of $X$, called
*open* sets, satisfying the following.

1. Arbitrary unions of open sets are open.
2. Finite intersections of open sets are open.
3. The empty set $∅$ and $X$ are both open.

A topological space (or, simply, a space) is a set X endowed with a topology.

<example>
Let $X$ be a finite set, and let $τ$ be the set of all subsets of $X$. This is
called the **discrete topology** on $X$.
</example>

A **neighborhood** of $p ∈ X$ is any open set containing $p$. If q lies in a neighborhood of $p$ we say that $q$ is **near** $p$. Topology is therefore sometimes called the
study of nearness relations. A topology on $X$ is called **Hausdorff** if the points
in every pair lie in disjoint neighborhoods or, more technically, if for every two
points $p, q ∈ X$, there exist two disjoint open sets $U$ and $V$ such that $p ∈ U$
and $q ∈ V$. We will primarily be interested in Hausdorff topologies, because these
coincide with our intuition that points are isolated objects; other sorts of topologies
are generally considered to be pathological (at least by non-topologists).