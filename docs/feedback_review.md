# Response to the informal manuscript critique

November 6, 2026. This records the critique supplied by the author, our checks,
and the resulting research decision. It is not an independent referee report.

## Assessment

The main criticism is justified: correctness, a matching example and careful
scope do not by themselves make the first note a substantial research
contribution. The share ceiling follows immediately from nonnegative cost.
C30 identifies its exact worst case, but the construction alone does not
establish practical importance or sufficient publication significance. The
previous assessment gave too much weight to proof verification and robustness
relative to this significance question.

C37 removes atomicity and singular covariance as necessary conditions. It is
an elementary regularization, not a new central contribution. C38 proves a
positive gap at a fixed scale L/A, with correct aggregate forecasting and
individual means. It remains an engineered example, not evidence from a
realistic operational model or a dataset.

## The standalone ratio and pooling

The objection to the interpretation of C31 is correct. Its definition implies
rho*c_j <= a_j for every producer, hence

$$
\rho\sum_j c_j\le L.
$$

When the grand offer is optimal and the sum of standalone costs is positive,
the fractional pooling gain is g=1-L/(sum_j c_j), so 1-rho >= g.
Thus a small multiplier 1-rho requires limited pooling gains. Limited pooling
alone does not guarantee a large rho: an unbalanced allocation can still make
one ratio small. C31 is valid but does not cure the near-perfect-pooling
limitation of the original extremal sequence.

We developed the proposed sharp-parameter question in the smallest nontrivial
case. For three producers, equal shares and symmetric unit absolute loss,
the [complete proof](three_player_rho.md) now gives

$$
\sup_{\rho\ge r}\frac{D_1-B}{L}=
\begin{cases}
\frac23(1-r),&0\le r\le1/3,\\[3pt]
\frac{1-r^2}{6r},&1/3\le r\le1.
\end{cases}
$$

Both regimes have matching four-scenario laws with actual rho=r for r>0.
For 0<r<1, the same supremum holds with strictly stable proper coalitions and
positive definite covariance. At fixed positive r the constructions do not
force L/A to zero. The second regime is strictly below C31 for 1/3<r<1,
and its attaining witness has positive optimized cost.

For example, at r=1/2 the exact normalized worst gap is 1/4, rather than
the old ceiling 1/3. This is a structural characterization, albeit limited to
three equal shares. It does not establish a general two-parameter theorem,
bibliographic priority, or that the eventual paper is sufficiently substantial.
The [saved checks](../results/exclusion/three_player_rho.md) verify the
derived values; they are not the proof or a performance benchmark.

## Forecast allocation error

The proposed weak-duality argument is correct, and its basic form was already
recorded as C16 in [the direction comparison](research_directions.md).
It also controls the fractional objectives, not only binary excess.
Let a* be a true-law optimal dual allocation and put d=a-a*. Then

$$
c(z)\ge (a^*)^\top z,
\qquad B\le D_k\le D_0\le\sum_j[d_j]_+.
$$

If the grand offer is truly optimal and the allocation is budget balanced,
sum_j d_j=0, giving D_k <= (1/2)||a-a*||_1 and consequently
D_k-B <= [(1/2)||a-a*||_1-B]_+.
For an arbitrary fixed grand offer the budget difference must be retained:

$$
\sum_j[d_j]_+
=\frac{\|d\|_1+L-c(N)}2.
$$

Thus the suggestion reconnects the error to forecasting, but merely restating
this inequality would repeat an elementary baseline. A substantive extension
would need a sharp attainable characterization, an estimable improvement over
the existing certificates, or a prespecified decision benefit. No such further
claim is made here.

## Exact optimization and complexity

An exact finite-support MILP already exists in
`src/censored_newsvendor/coalition_audit.py` (`coalition_program`, integral mode)
and `ExclusionEnvelope.binary_reference()`. It has one binary membership per
producer, a continuous offer and linearized scenario losses. The continuous
version gives D0. The exclusion hierarchy explicitly explores faces and the
remaining larger integer coalitions; it is not a new adaptive branch-and-bound
algorithm.

The implementation has used the MILP as a correctness reference, including in
the new structural-envelope checks. We have not conducted a fair runtime
comparison with branch-and-bound. Solver agreement is not performance evidence.
With uniform shares the nonterminal worst gap is (n-k)/n, so a fixed normalized
tolerance requires depth proportional to n; the face count remains exponential
for a fixed tolerance strictly between zero and one. This supports the critique
of any general efficiency claim. A worst-case relaxation-error theorem can
still be studied without asserting an algorithmic advantage.

## Missing references: verified records and reading depth

All four suggested references exist and belong in the related-work discussion.
They have been added to the root bibliography. The current PDF is still the
November 5 version and does not yet contain these additions.

| Work | Verified relevance | Material inspected on November 6 |
| --- | --- | --- |
| Hartman, Dror and Shaked (2000), *Cores of Inventory Centralization Games*, Games and Economic Behavior 31(1), 26–49. [DOI](https://doi.org/10.1006/game.1999.0732) | Core existence under specified symmetric and Gaussian demand assumptions. | Publisher abstract and institutional bibliographic record; full proofs not obtained. |
| Müller, Scarsini and Shaked (2002), *The Newsvendor Game Has a Nonempty Core*, Games and Economic Behavior 38(1), 118–126. [DOI](https://doi.org/10.1006/game.2001.0854) | Core existence without the earlier distributional restrictions, within their newsvendor model. | Publisher abstract and metadata; full proofs not obtained. |
| Deng, Ibaraki and Nagamochi (1999), *Algorithmic Aspects of the Core of Combinatorial Optimization Games*, Mathematics of Operations Research 24(3), 751–766. [DOI](https://doi.org/10.1287/moor.24.3.751) | Links core nonemptiness in their integer-programming game class to integrality of the associated relaxation. | Publisher abstract and metadata; full proofs not obtained. |
| Goemans and Skutella (2004), *Cooperative facility location games*, Journal of Algorithms 50(2), 194–214. [DOI](https://doi.org/10.1016/S0196-6774(03)00098-1) | Theorem 2.1 equates their cost-allocation problem with the associated LP dual and relates core existence to zero integrality gap. | Journal metadata and the institutional preprint's introduction, Section 2 formulation, Theorem 2.1 and its proof; Section 3 opening. [Preprint](https://depositonce.tu-berlin.de/bitstreams/839d0ece-1d62-4c98-a92c-b5aa03497aa3/download). |

These are relevant precedents, not evidence that core existence is our new
contribution. Nor does the integrality/core equivalence for an associated
allocation LP automatically identify the gap of our fixed-allocation physical
fractional-membership relaxation. C36 already distinguishes physical and
canonical extensions. Determining a hidden equivalence requires an explicit
reduction and comparison with the full results; the abstracts cannot rule it out.

## Research and editorial decision

Continue the structural-parameter question within the current problem. The next
bounded target is three producers with arbitrary positive shares: derive the
face envelope and either construct matching demand laws or identify a rigorous
obstruction to attainment. Only then assess an extension to larger faces.
Do not add another forecasting model, retune the failed statistical grid, or
restart an unrestricted topic search as a substitute for that mathematical step.

Before revising the paper, assess the strength and closest precedents of that
result. The next manuscript should move Section 6 and Appendix A's statistical
development to the existing companion notes, keeping the failed precision
screens visible there. Put Appendix B's workflow statements and submission
status in the repository README. Add the missing classical references and
state the MILP/branch-and-bound baseline explicitly. Select only the robustness
arguments needed for the central theorem instead of appending every result.

The current PDF and Overleaf archive are retained as the first draft; this
response and C39 are research notes for the revision. C7, a publishable original
contribution, remains unestablished.
