# Focused comparison of the sharp exclusion gap

2026-11-05. This closes the bounded priority check requested after the
standalone-certificate experiment. The candidate is C30, the exact worst-case
gap at a fixed positive allocation. C31 is an elementary supporting condition.
This is an assessment of inspected results, not an exhaustive novelty certificate.

**Decision:** retain C30 as the center of a short theoretical note about the
limitations of an established relaxation. The exact depth/share formula was
not found in the results inspected below. The closest new match is the
fixed-allocation subproblem in **Burer and Dror's 2005 manuscript**, equation 19.
The relaxation itself must therefore be credited. Whether the sharp extremal
calculation is substantial enough for publication remains a separate judgment.
Do not continue tuning the failed general precision claim to justify the note.

## The statement being compared

Fix positive shares $w$, $\sum_jw_j=1$, and expected grand-offer cost $L>0$.
Write $a=Lw$, $c(z)=\min_q E\ell(q,z^\top Y)$, and

$$
B=\max\{0,\max_{\emptyset\ne S\subsetneq N}[a(S)-c(1_S)]\}.
$$

The physical cost $c$ is nonnegative, convex and positively homogeneous.
The root domain is $P_0=\{0\le z\le1:\sum_jz_j\le n-1\}$;
$D_0=\max_{z\in P_0}(a^\top z-c(z))$.
At depth $k\ge1$, $D_k$ maximizes over faces with $k$ coordinates fixed
to zero, and separately checks actual proper coalitions omitting fewer than
$k$ members. Zero is included. Hence $D_k\ge B$.

For each $n\ge3$, prescribed $w>0$, and $1\le k\le n-2$, C30 says

$$
0\le D_k-B\le[Ls_k(w)-B]_+,\qquad
\sup\frac{D_k-B}{L}=s_k(w),
\quad s_k(w)=\text{sum of the largest }n-k\text{ shares}.
$$

The supremum persists with two equiprobable bounded states, unit capacities,
nonzero individual variances, a correct aggregate forecast, and strictly
negative excess for every actual proper coalition. It is a supremum over laws
with the same $w$, not an instance-wise equality. The complete proof and
finite-member formula are in [publication_assessment.md](publication_assessment.md).

## Closest sources and actual reading depth

| Source | Result inspected | Relation to the proposed statement |
| --- | --- | --- |
| [Burer and Dror, 2005 manuscript](https://optimization-online.org/wp-content/uploads/2005/01/1042.pdf), §§5.2–5.3, Eqs. 16–21 | For norm-valued newsvendor costs, replace binary proper coalitions by their convex hull in the fixed-allocation separation problem, then optimize the allocation. Section 5 describes the resulting allocation procedure as heuristic without a quality guarantee. | Exact predecessor of the root subproblem. No depth/share gap formula appears in the inspected section. |
| [Burer and Dror, TOP 2012](https://doi.org/10.1007/s11750-010-0160-x), author-uploaded full text, §§2, 4–5 and Appendix | Fair allocations under optimized Gaussian correlations; Theorem 4.1 gives a nucleolus in that setting. Section 5 is a summary. | The 2005 manuscript's Section 5 relaxation is absent from this version. Cite the manuscript for Eq. 19, not the journal article. Online publication was in 2010. |
| [Bonnans and André, 2008](https://www.numdam.org/article/RO_2008__42_3_299_0.pdf), §§4–6 | Convex production costs, dual cutting planes, disaggregated players and partial continuous memberships. Eq. 6.12 separates a fixed allocation over a domain with selected continuous coordinates. | Fractional and partially integral coalition searches are established. Their selected continuous classes differ from our union of zero-coordinate faces; the inspected sections do not give the stated sharp error. |
| [Samet and Zemel, 1984](https://www.tau.ac.il/~samet/papers/lp%20games.pdf), Theorems 2–3 and associated proofs/corollaries | Conditions for replicated cores to equal the LP dual set; a canonical concave cover characterizes equality near the grand coalition. | This is structural core/dual comparison. Replication resolution is not our exclusion depth. We do not claim that a core/dual discrepancy is new. |
| [Aubin, 1981](https://doi.org/10.1287/moor.6.1.1), publisher abstract only | Fractional participation and the canonical extension of an ordinary game. | Establishes the concept. Full original proofs were not obtained; the cover formula is inspected in the next source and Samet–Zemel. |
| [Shellshear, 2009 working paper](https://noah.nrw/ubbihs/download/pdf/5123288), Definitions 1.1–1.14, Proposition 1.12, Theorem 1.27 statement and proof portion | Explicit concavification via fractional combinations of actual coalitions; core stability concerns external domination of sets. | Canonical and physical extensions are different objects. The cost-sign translation and a separating example are proved below. The 2011 journal version was not inspected. |
| [Denault, January 2001 manuscript](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/e0678cad2d06cd0bc1257bd20041fcd1/%24FILE/CoherentAllocation.pdf), Definition 10, Eq. 7, Theorems 6–7 | Full-box fractional cost inequalities and the subdifferential description for homogeneous costs. | A direct conceptual predecessor. Optimized imbalance cost satisfies convex homogeneity but need not satisfy the monetary coherence axioms. No identification with a coherent monetary risk measure is claimed. |
| [Chen and Zhang, 2009](https://publish.illinois.edu/xinchen/files/2012/12/SPinventorygame.pdf), Example 1 and §5, Theorem 7 and proof | Ordinary core versus dual allocations; hardness via a two-state absolute-sum newsvendor cost. | Supplies the known construction device. The candidate addition is the sharp value for every prescribed positive split and exclusion depth, not the two-state device or hardness. |
| [Montrucchio and Scarsini, 2006](https://www.carloalberto.org/wp-content/uploads/2018/11/no.15.pdf), §2 and Theorem 3.2 statement | Newsvendor cores, normal-demand norm costs, and a nonatomic limit. | Additional context. A limit in the number/size of players does not identify the fixed-$n$, depth-dependent supremum. |

Additional screening covered approximate-core results for matching games,
q-partitioning valuations, and excess-based risk-capital allocation. Their
objectives or admissible cost classes differ; they are not used to assert
non-duplication. Two search engines and citation follow-ups were used.
Representative search terms included “newsvendor fractional integrality gap”,
“cooperative games fractional additive gap relaxation”, and
“Burer Dror 2005 approximation nucleolus”.
An unsuccessful search is not evidence of a universal absence.

## Exact root correspondence: our reduction

Put $f(z)=a^\top z-c(z)$ and
$P_1=\{0\le z\le1:1\le\sum_jz_j\le n-1\}$. Positive homogeneity gives

$$
D_0=\max\{0,\max_{z\in P_1}f(z)\}.
\tag{1}
$$

Indeed, a positive value at a point of mass $s<1$ can be increased by replacing
$z$ with $z/s$. Its coordinates remain at most one because $z_j\le s$.
Points with nonpositive value cannot improve on zero. The other inclusion
is immediate.

For $c(z)=\|Mz\|_2$, the fixed-allocation minimum in the 2005 Eq. 19 is
$\min_{z\in P_1}[-f(z)]$. Thus (1) identifies $D_0$ with its sign-reversed,
positive-part value. Similarly, $B$ is the sign-reversed, positive-part
binary minimum. With a budget-balanced optimal grand allocation,
$a(N)=c(1)$, the fractional minimum is already nonpositive: a scaled
all-ones vector has value zero.

The comparison fixes $a$. It does **not** bound the quality of the allocation
obtained by their outer maximization, the complete nucleolus calculation, or
the difference between two allocation vectors.

### Root corollary and transfer of the example

The root also has the sharp ceiling

$$
0\le D_0-B\le[L(1-\min_jw_j)-B]_+,\qquad
\sup\frac{D_0-B}{L}=1-\min_jw_j,\quad n\ge3.
\tag{2}
$$

**Proof.** Nonnegative cost gives
$D_0\le\max_{P_0}a^\top z=L(1-\min_jw_j)$.
Every one-exclusion face lies in $P_0$, so $D_0\ge D_1$.
The C30 family approaches the right-hand side with $B=0$ at depth one.
This proves the matching supremum. All restrictions in that construction
are retained. This is an immediate corollary of C30, not a second independent
novelty claim.

The same functional obstruction also lies in the norm-cost class. In unscaled
units the construction has state difference $d$ and
$c(z)=|d^\top z|/2=\|Mz\|_2$ for the one-row matrix $M=d^\top/2$.
For an actual Gaussian realization, let $Z\sim N(0,1)$,
$\eta=E|Z|=\sqrt{2/\pi}$, and

$$
X=\mu+\frac{d}{2\eta}Z.
$$

Under unit absolute loss the optimal aggregate offer is $\mu^\top z$ and
the optimized cost is again $|d^\top z|/2$. This transfers the cost,
coalition excess and gap calculations. Gaussian outputs themselves are not
bounded or almost surely nonnegative. The bounded two-state realization
provides those physical properties separately. The covariance is singular;
we are not asserting the same construction under an imposed positive
lower eigenvalue or restricted correlations.

## Why the canonical extension is not the physical extension

Translate the inspected concave-cover formula to cost signs:

$$
\bar c(z)=\min_{\lambda_S\ge0}
\left\{\sum_{\emptyset\ne S\subseteq N}\lambda_Sc(1_S):
\sum_S\lambda_S1_S=z\right\}.
\tag{3}
$$

The following specialization is our explicit comparison, using only
subadditivity and positive homogeneity:

1. $c(z)\le\bar c(z)$, by applying these properties to every feasible
   decomposition of $z$.
2. At every integer coalition $z=1_S$, using that coalition alone proves
   $\bar c(1_S)=c(1_S)$.
3. If $a(N)=c(1)$ and $a$ is in the ordinary core, multiplying the integer
   inequalities by $\lambda_S$ and summing proves $a^\top z\le\bar c(z)$.

Consequently an ordinary-core allocation has no positive violation under (3),
but can have one under the smaller physical cost.
This is consistent with the prior core/dual distinction.

For a concrete illustration take unscaled outputs $(2,2,0)$ and $(0,0,3)$,
unit absolute loss, and equal charges $a_j=1/6$. At
$z=(1,0,2/3)$, the physical cost is zero and $a^\top z=5/18$.
The canonical cost is $2/3$: decompose $z$ as
$\frac13 1_{\{1\}}+\frac23 1_{\{1,3\}}$.
This is optimal because the only usable coalitions are $\{1\},\{3\},\{1,3\}$.
Writing their pair coefficient as $t\le2/3$, the cost is $2-2t$,
minimized at $t=2/3$. All actual proper coalitions have strictly negative
excess. The discrepancy concerns the choice of extension, not a contradiction
of canonical-extension core equivalence.

## What remains a contribution candidate

| Item | Classification after this comparison |
| --- | --- |
| Fractional memberships, ordinary versus fractional core, dual certificates | Established background. |
| Continuous root separation for norm newsvendor costs | Direct prior formulation, Burer–Dror 2005. |
| Tightening by fixing coordinates or considering partial memberships | Standard optimization idea; no new general hierarchy claimed. |
| Exact worst-case error $s_k(w)$, with the specified positive split, every nonterminal depth and strictly stable calibrated bounded instances | C30 survives this focused comparison as a narrow candidate. Its upper bound is elementary; the matching family is the substantive calculation being assessed. |
| Root formula (2), norm-cost transfer and canonical-extension comparison | Supporting corollaries/reductions, not separate claims of priority. |
| Standalone ratio factor $1-\rho$ | Elementary sufficient condition from subadditivity and comparison with the whole face; retain C31 as support without an independent originality claim. |
| IUT, fixed-sequence inference and paired SAA blocks | Established methods. The saved experiments measure applicability, not statistical novelty. |

The [observed checks](../results/exclusion/prior_art_checks.md) compare two
independent primal programs with the existing dual code and solve (3) separately.
The earlier [84 level checks](../results/exclusion/sharp_gap.json) remain
unchanged. None of these executions establishes priority. The check record
also states the interruption and recovery limits.

**Publication scope:** proceed with the [theoretical-note outline](theory_note_outline.md).
The case for interest is that a familiar relaxation can report almost the
entire retained share of expected cost as a saving while no actual coalition
benefits. The case against a standalone paper is that the derivation is short,
the worst-case family is specialized, and $L/A\to0$ along the unit-capacity
limit. The broad finite-data precision failure remains visible.
The next assessment should examine the complete short argument for significance
and hidden equivalence, not restart an unrestricted search for a different topic.
