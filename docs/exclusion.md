# Certifying the largest incentive to leave a coalition

Date 2026-10-31. The October 28 certificate allowed every producer to take a fractional position. This note uses a restriction satisfied by every proper coalition. At least one producer must have position zero. On the original four-producer example this changes the population upper bound from \(3/16\) to zero, the exact answer.

## What is being bounded

Keep the one-period loss, forecast-derived offer and fixed signed shares from the first certificate. Write \(L\) for the true expected cost of the implemented grand offer, \(a_i=w_iL\), and \(c_P(z)=\min_q E_P\ell(q,z^TY)\) for the balancing cost of a membership vector. This cost is convex and positively homogeneous in \(z\), by scalar newsvendor duality. The quantity of interest is the largest positive saving \(B\) of an actual nonempty proper coalition. An empty coalition supplies the zero lower bound. [Model and baseline proof](coalition_certificate.md)

At population level the objective is \(f(z)=a^Tz-c_P(z)\). For validation data use the original simultaneous DKW bounds on *integer* coalition costs and the two-sided interval \([L_-,L_+]\) on the grand cost. Set \(r_i=\max(\alpha,\beta)R_i e_c\), where \(e_c\) is the original DKW radius. The statistical envelope is

$$
f_M(z)=\max_{\ell\in\{L_-,L_+\}}\ell\,w^Tz-
              [\widehat c(z)-r^Tz]_+ .
$$

The two endpoints handle signed shares and the positive part enforces nonnegative standalone cost. On the simultaneous confidence event, \(B\) is at most the maximum of this envelope over binary proper memberships. Fractional values only extend the optimization problem. The proof needs confidence bounds for integer coalitions alone. All levels below share this one event for the frozen rule and fixed validation size.

## The hierarchy and the stopping rule

Level zero maximizes the relevant objective on \(Z_0=\{0\le z\le1,\ \sum z_i\le n-1\}\). At level \(k\ge1\), compute the maximum over two sets of candidates.

1. Evaluate exactly every proper coalition that omits fewer than \(k\) producers.
2. For every \(J\) of size \(k\), maximize the objective on the face \(z_J=0\), with all other entries in \([0,1]\).

Call the maximum \(D_k\), including zero. Use \(B_{\rm bin}\) for the largest binary objective, either population excess or the exhaustive statistical envelope as appropriate.

**Proposition 1.** \(D_0\ge D_1\ge\cdots\ge D_{n-1}=B_{\rm bin}\). In particular every validation level is an upper confidence bound for \(B\) with the same coverage as the exhaustive envelope.

**Proof.** Every proper binary membership either omits fewer than \(k\) players or belongs to a face in the second set. Every face at level \(k+1\) lies inside a face at level \(k\). The extra binary candidates evaluated at \(k+1\) also belonged to a face at \(k\). This proves coverage and monotonicity. At \(k=n-1\), a face has one free coordinate. Both objectives are positively homogeneous. Their maximum on the resulting line segment is attained at an endpoint. All other proper binary memberships have already been evaluated. QED.

A rounded binary membership gives a feasible value \(W\) of the *same objective*. Hence \(W\le B_{\rm bin}\le D_k\). If \(D_k-W\le\tau\), additional optimization could improve the upper bound by at most \(\tau\). For validation data, \(W\) brackets the exhaustive confidence **bound**, not the unknown true excess. Sampling uncertainty remains even when \(W=D_k\). The single simultaneous event permits choosing a level in response to the observed computational gap.

At fixed \(k\) the work is \(\binom nk\) face problems and \(\sum_{j=1}^{k-1}\binom nj\) direct coalition evaluations, plus rounding checks. A face needs one population LP or up to two validation LPs. Each LP is polynomial in \(n\) and the number of supplied scenarios. Deeper levels have an increasing combinatorial cost.

### Computing a face upper bound

At one loss endpoint let \(h=\ell w\). For a finite law, let \(V\) consist of scenario scores in \([-\beta,\alpha]\) with mean zero. The scalar balancing problem has \(c(z)=\max_{\nu\in V}E[(z^TY)\nu]\). Introduce \(0\le t\le1\) and a discounted score \(\theta\in t V\). For a feasible face \(F\), finite-dimensional LP duality gives

$$
\max_{z\in F}\{h^Tz-[c(z)-r^Tz]_+\}
=\min_{0\le t\le1,\ \theta\in tV}
     \max_{z\in F}z^T\{h+t r-E[Y\theta]\}.
$$

Indeed, for fixed \(z\) the maximization over discounted scores recovers the positive part. Bilinear minimax then exchanges the two optimizations. On a face the inner support function sums positive coordinates of the free producers. At the root it uses the proper-coalition support from the previous note.

The implementation clips the returned score to its discounted bounds and recomputes the upper bound, including \(R_i[E\theta]_+\) for any floating-point mean residual. Quantile enumeration and a separate primal binary MILP check the objective. Numerical comparisons use tolerance \(10^{-8}\). [Implementation](../src/censored_newsvendor/exclusion.py)

## When one exclusion is exact

**Proposition 2.** If the joint production law is exchangeable and actual expected charges are all equal to \(a_0\), then for any \(i\),
$$
B=D_1=[(n-1)a_0-c_P(N\setminus\{i\})]_+ .
$$

**Proof.** On the face \(z_i=0\) let \(s=\sum z_j\). Averaging \(z\) over permutations of the other \(n-1\) labels gives \(s/(n-1)\) times the indicator of \(N\setminus\{i\}\). Exchangeability makes the cost invariant under each permutation. Convexity and homogeneity therefore give
$$
c_P(z)\ \ge\ {s\over n-1}c_P(N\setminus\{i\}).
$$
Charges on the face sum to \(s a_0\). Maximizing over \(0\le s\le n-1\) gives either the empty membership or the whole face. Both are integer coalitions. Exchangeability makes the value the same on every face. QED.

The result allows dependent production. Equal one-dimensional marginal laws alone do not imply exchangeability. A finite sample from an exchangeable law can also be asymmetric. When the population symmetry is a justified model assumption, one can apply the cost and grand-loss confidence bounds to a single *prespecified* leave-one-out coalition. Without that assumption use the simultaneous hierarchy above. Under exchangeability with unequal charges, the integer check still reduces to one coalition per size, taking the largest \(k\) charges at size \(k\).

A sufficient condition extends beyond exchangeability. On each face \(F=N\setminus\{i\}\), take a mean-zero optimal dual score \(\nu_F\) for that face's full coalition. Put \(d_j=a_j-E[Y_j\nu_F]\) for \(j\in F\). Weak duality gives a face upper bound \(\sum_{j\in F}(d_j)_+\). The actual face coalition and the empty coalition achieve at least \([\sum_{j\in F}d_j]_+\), by optimality of \(\nu_F\). Subtracting gives the population estimate
$$
0\le D_1-B\le\max_F \min\left\{\sum_{j\in F}(d_j)_+,\ \sum_{j\in F}(-d_j)_+\right\}.
$$
In particular a same-sign residual vector on every face is sufficient for exactness. This is a bound on structural error using population quantities. Estimating those quantities from validation data introduces a separate statistical problem.

## Two boundaries

With four independent Bernoulli-half producers, the previous study's equal-share offer had \(B=0\) and \(D_0=3/16\). Proposition 2 proves \(D_1=0\). This removes the positive relaxation value even though the implemented aggregate offer remains suboptimal under the true law.

For an asymmetric example, the true law gives equal masses to \((1,0,0)\) and \((0,3/5,2/5)\). The fixed offer is \(3/4\), the shares are \((3/5,1/5,1/5)\), and the expected charges are \((3/20,1/20,1/20)\). The protocol specifies a forecast giving exactly this rule. Every actual coalition has nonpositive excess. On the face excluding player 3 the cost is \(|z_1-3z_2/5|/2\). For each fixed \(z_2\) the best \(z_1\) is \(3z_2/5\). At \(z_2=1\) the excess is \(7/50\). The face excluding player 2 has maximum \(11/100\) by the same calculation, and the face excluding player 1 has maximum zero. Thus \(D_1=7/50\), \(D_2=B=0\).

**Proposition 3.** For every \(k\ge1\), a bounded instance with \(n=k+2\) producers has \(B=0\) and \(D_k=7/50\). Every producer has positive variance and the forecast has the correct aggregate distribution. The construction allows signed shares.

**Proof.** Start with three producers. The equally likely true states are \((1,0,0)\) and \((0,3/5,1/10)\). The forecast's equally likely low and high states are \((1/4,1/10,7/20)\) and \((11/20,1/5,1/4)\). In both laws aggregate production takes values \(7/10,1\). With unit penalties and offer \(17/20\), expected aggregate cost is \(3/20\). The forecast dual with scores \(-1,+1\) gives actual expected charges \((3/20,1/20,-1/20)\). True singleton costs are \(1/2,3/10,1/20\). Pair costs for 12, 13, 23 are \(1/5,9/20,7/20\). All are at least their assigned charges, and the grand coalition also attains equality.

Append \(k-1\) independent producers to both laws, each equal to \(1/2\pm1/(20k)\) with equal probabilities, independent of the original vector. Shift the offer by \((k-1)/2\). Total noise stays below \(1/20\), so it cannot change which side of the offer the original total falls on. The same aggregate score remains optimal under the forecast. Every appended producer has zero expected dual charge, since it is independent of the mean-zero score. Total expected cost stays \(3/20\). Conditional Jensen shows that adding these producers to any original subset can only increase its optimized cost after subtracting their deterministic mean from the offer. Hence all integer coalitions are stable.

At level \(k=n-2\), a face has only two free producers. Freeing original players 1 and 2 attains \(7/50\), by the preceding two-coordinate calculation. Freeing players 1 and 3 gives zero maximum: the objective is \(3z_1/20-z_3/20-|z_1-z_3/10|/2\), with maximum zero. Freeing players 2 and 3 also gives zero by their same-direction fluctuations and their charges. A face containing an appended producer gains no charge from it and its independent noise can only increase optimized cost. The directly evaluated integer coalitions have zero positive excess. This gives the matching upper bound. QED.

This last family was derived after the fixed comparison and is reported separately. Numerical checks for \(k=1,\ldots,5\) reproduce the constant gap. [Additional checks](../results/exclusion/obstruction.json)

## Evidence and next decision

On the original 100 population cases, levels zero, one and two attained the exact answer on 95, 99 and 100 cases within tolerance. Across the 300 validation comparisons the corresponding counts against the exhaustive **confidence envelope** were 196, 299 and 300. The largest original structural gap fell from 0.1875 to approximately 0.02415 at level one. At 4,096 observations the mean level-two bound still exceeded the true excess by about 0.326, essentially the same slack as exhaustive statistical evaluation. The twelve additional exchangeable population laws all agreed with Proposition 2. Standard binary MILP agreed with the independent references in five population and twelve validation comparisons. [Protocol](exclusion_protocol.md) · [Generated results](../results/exclusion/summary.md)

The time spent on each LP and each quantile calculation can differ substantially. The experiment supports agreement on this small grid. Runtime superiority and performance on real energy observations remain open. The coverage proof assumes bounded iid validation observations independent of the rule.

The next contribution to evaluate is a **finite-sample bound based on the sign and size of the leave-one-out residuals**. Use dual scores fixed on separate training data, then estimate the face moments on validation data. Compare the statistical slack and the cost of this approach with the moment baseline and exhaustive confidence bound. Proposition 3 gives a reason to focus on measurable heterogeneity rather than assume a fixed depth always succeeds.

## Prior work

Balas gives general disjunctive hierarchies for discrete optimization. Montrucchio and Scarsini's proposition 2.4 treats a symmetric allocation and exchangeability in newsvendor games. These provide precedents for disjunctions and symmetrization. The specific objects derived here are upper bounds on the maximum excess of an already implemented offer, their finite-data interpretation and the fixed-depth construction. Their originality as a package still requires a theorem-level comparison. The available Wang et al. publisher material describes coalition constraint generation for robust resource allocation. An algorithmic novelty claim would require its full formulation and proofs. [Balas](https://doi.org/10.1137/0606047) · [Montrucchio and Scarsini, §2.4](https://www.carloalberto.org/wp-content/uploads/2018/11/no.15.pdf) · [Wang et al.](https://doi.org/10.1016/j.tre.2025.104633)

