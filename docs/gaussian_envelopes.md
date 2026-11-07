# Fractional audits under Gaussian demand

November 7, 2026, branch `pulp-fiction`. Code: `censored_newsvendor/gaussian.py`;
checks: [results/gaussian/gaussian_envelopes.md](../results/gaussian/gaussian_envelopes.md)
and group O of [the symbolic report](../results/verification/symbolic_checks.md).

## Why

The worst cases of the exact notes are attained by atomic, carefully
correlated laws. On real wind production the audit was essentially exact
([wind_audit.md](../results/illustration/wind_audit.md)), even where the
worst case over all laws was 0.41 of the pooled cost. So the natural
question is how large the worst case is over *realistic* laws. Gaussian
demand is the classical model of inventory pooling (Hartman, Dror and
Shaked 2000 treat it), and it turns out to be tractable.

## 1. Model

For Y ~ N(mu, Sigma) the optimal expected pinball loss of a membership x is
phi(Phi^{-1}(tau)) sqrt(x' Sigma x). The cost is a Euclidean norm, symmetric
in x whatever the penalty ratio, so every normalized quantity is the same for
all kappa. Write c(x) = sqrt(x'Gx) with G a scaled covariance. The game
constraints are linear in G:

* standalone floor: G_jj <= (a_j/r)^2;
* stability: 1_S' G 1_S >= a(S)^2 for every proper S (allocations in the
  core, B = 0, the case an audit is meant to confirm);
* grand cost: 1'G1 <= 1;
* optionally nonnegative correlations, G_ij >= 0, or independence.

For a fixed membership z, the least favourable covariance minimizes z'Gz over
this convex set: a semidefinite program, solved to global optimality. Only
the maximization over z is numerical (a grid with local refinement, as for
general laws). Gaussian outputs are unbounded while the model of the paper
has bounded outputs; Gaussian costs are limits of the costs of truncated
laws, so the values below are suprema over bounded laws close to Gaussian.

## 2. Nonnegative correlations: a bound independent of r

**Theorem G.** Let demand be Gaussian with nonnegative correlations and let
the allocation be in the core. Take a face F and a membership z on F, and
order F so that 1 = z_1 >= z_2 >= ... >= z_m >= 0. With A_i = a_1 + ... + a_i
and gamma_i = A_i^2 - A_{i-1}^2 = a_i(a_i + 2A_{i-1}),

$$
a^\top z-c(z)\ \le\ \sum_i a_iz_i-\Bigl(\sum_i\gamma_iz_i^2\Bigr)^{1/2}
\ \le\ a_1\Bigl(1-\sqrt{1-h}\Bigr),\qquad h=\sum_{i\ge2}\frac{a_i}{a_i+2A_{i-1}},
$$

the last step when h < 1. Hence the worst overstatement is at most the
maximum of a_1(1 - sqrt(1 - h)) over faces and orderings, whatever the floor r.

*Proof.* Write z = sum_s mu_s 1_{U_s} with U_s the s largest coordinates and
mu_s = z_s - z_{s+1} >= 0. Then z'Gz = sum_{s,t} mu_s mu_t 1_{U_s}'G1_{U_t}.
For s <= t, nonnegative correlations give
1_{U_s}'G1_{U_t} >= 1_{U_s}'G1_{U_s}, and stability of U_s (a proper
coalition) gives 1_{U_s}'G1_{U_s} >= A_s^2. So
z'Gz >= sum_{s,t} mu_s mu_t A_{min(s,t)}^2 = sum_i gamma_i z_i^2 (Abel
summation). The function sum_i a_i z_i - (gamma_1 + sum_{i>=2} gamma_i z_i^2)^{1/2}
is concave; its stationary point z_i = c a_i/gamma_i, with
c = a_1/sqrt(1 - h), gives the value a_1(1 - sqrt(1 - h)), which is therefore
its maximum over all z. The identities are group O of the symbolic checks. ∎

**Attainment.** Order all producers with the face first, in the order of z,
and give producer i the variance gamma_i = A_i^2 - A_{i-1}^2, independently.
Every proper coalition is stable: for any set T,
sum_T gamma_i >= sum_{i in T} a_i(a_i + 2 a(T before i)) = a(T)^2. The grand cost
is A_n = 1. At the stationary membership z_i = c a_i/gamma_i, which is sorted
automatically because a_i + 2A_{i-1} increases with i, the excess equals the
bound. So the bound is attained whenever that membership lies in the cube and
the caps gamma_i <= (a_i/r)^2 hold, that is for

$$
r\ \le\ r_0=\min_i\sqrt{\frac{a_i}{a_i+2A_{i-1}}}.
$$

For equal shares r_0 = 1/sqrt(2n-1). The construction was checked for
n = 3 to 7 at depths one and two: every constraint holds and the excess
equals the closed form.

**Equal shares.** Then gamma_i = (2i-1)a^2, a_i/(a_i + 2A_{i-1}) = 1/(2i-1) and
the bound is a(1 - sqrt(1 - H_m)) with H_m = 1/3 + 1/5 + ... + 1/(2m-1). At
depth one:

| n | 3 | 4 | 5 | 6 | 7 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gaussian, nonnegative correlations (any r) | 0.0612 | 0.0792 | 0.0862 | 0.0898 | 0.0930 |
| all laws at r -> 0, (n-1)/n | 0.667 | 0.750 | 0.800 | 0.833 | 0.857 |

The worst law is independent with variances in the ratio 1 : 3 : 5 : ...,
whose partial sums are perfect squares: stability holds with equality along
the chain of top sets. The stationary membership lies in the cube for m <= 6;
for m >= 7 the formula remains an upper bound but is not attained.

## 3. Negative correlations

Without the sign restriction, Gaussian laws can be as bad as arbitrary laws
when r is small: for four equal producers at depth one and r = 0.1 the
Gaussian worst case is 0.675, the same as over all laws. As r grows the
Gaussian worst case falls far below the general one (0.116 against 0.375 at
r = 0.5, 0.036 against 0.182 at r = 0.7), and for r >= 0.6 the worst
covariances found have nonnegative correlations anyway. See the checks for
the full tables.

## 4. The wind panels

For the shares and floors of the 24 wind audits
([gaussian_envelopes.md](../results/gaussian/gaussian_envelopes.md), last
table), the depth-one worst case is:

| panel | observed | all laws | Gaussian | Gaussian, nonnegative correlations |
| --- | ---: | ---: | ---: | ---: |
| Texas (nearby sites) | <= 0.0013 | 0.012-0.038 | 0.004-0.0125 | 0.004-0.0125 |
| France (one farm) | <= 0.0002 | 0.005-0.012 | 0.0008-0.0018 | 0.0008-0.0018 |
| four distant states | 0 | 0.35-0.41 | 0.10-0.17 | 0.075-0.080 |

Gaussian structure with positive dependence closes most of the distance
between the theorems and the observed audits, but not all of it: on the
distant sites the audit was exact while the bound still allows 0.08. What
remains must come from features of real production that the Gaussian model
does not capture, or from the fact that a worst case over covariances is
still a worst case.

## 5. What is proved and what is computed

* Proved: Theorem G (upper bound for every r) and its attainment by explicit
  independent laws under the stated conditions; the closed form for equal
  shares.
* Computed: the Gaussian worst case without the sign restriction, and with
  it above r_0. The inner minimization is an SDP solved to optimality and
  every reported law passes a re-check of all constraints. The outer search
  over memberships is a grid with local refinement, so these values are lower
  bounds that we expect, but have not proved, to be tight.
