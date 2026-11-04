# Certifying standalone-cost coverage from a finite sample

November 4, 2026. This note turns the population corollary in the
[publication assessment](publication_assessment.md) into a finite-data bound.
It estimates how much the fractional-coalition relaxation can overstate the
best real coalition's saving. It does **not**, on its own, give a tighter
upper confidence bound on that real saving.

## Setting and the population condition

Keep the offer q0, positive shares w summing to one, capacities R and positive
loss coefficients alpha and beta fixed independently of validation data.
Production is jointly observed and bounded, 0 <= Y_j <= R_j; validation vectors
are iid. Dependence between producers within a vector is unrestricted. In the
code, `over` is alpha and `under` is beta:

$$
\ell(q,t)=\alpha(t-q)_++\beta(q-t)_+,\quad
L=\mathbb E\ell(q_0,Y(N)),\quad a_j=w_jL.
$$

Let c_j be optimal standalone expected loss and let
rho=min({1} union {a_j/c_j : c_j>0}). Set rho=1 if all standalone costs vanish.
Let B be maximum positive excess of a proper integer coalition and D_k the
exclusion hierarchy. For s_k equal to the sum of the n-k largest shares,

$$
D_k-B\le (1-\rho)[s_kL-B]_+,\qquad 1\le k\le n-2.
$$

The terminal gap at k=n-1 is zero. The preceding proof assumes rho>0 when it
divides by rho; rho=0 follows directly from the share-only bound. When L=0,
nonnegative costs give B=D_k=0. These boundary cases require no division.

## A single global ratio bound

Use an independent pilot to fit offers q_j in [0,R_j]. Conditional on that
pilot, they are fixed. For a threshold t define paired validation variables

$$
X_{j,t}=w_j\ell(q_0,Y(N))-t\ell(q_j,Y_j).
$$

Writing b_j=E ell(q_j,Y_j), optimality gives c_j<=b_j. Thus all the inequalities
E X_{j,t}>0 imply rho>=t. More usefully, if t>rho, there is an index j with
c_j>0 and a_j<t c_j<=t b_j, so E X_{j,t}<0.

Let l_{j,t} be any scalar lower confidence bound with
Pr(l_{j,t}>E X_{j,t} | pilot)<=eta. The **intersection-union test** passes t only
when every l_{j,t}>0. If t>rho, passing implies an error on at least one
particular true-null producer j. Its probability is at most eta, with no
union bound over the number of producers. This does not assert simultaneous
coverage of all the individual l_{j,t}.

Use the predetermined increasing grid 0.05,0.10,...,1.00. Test in order,
**stop at the first failure**, and report the last passed threshold (zero if
none passed). If this result exceeds rho, the procedure necessarily passed
the first predetermined grid point greater than rho. The test at that one
point has error probability at most eta. Consequently

$$
\Pr(\widehat\rho_{\rm grid}>\rho\mid\text{pilot})\le\eta.
$$

There is no factor for the grid size either. Taking the largest passing
threshold after continuing beyond a failure would require a different proof.
The implementation and the matched Bonferroni comparison both stop at the
first failure. Bonferroni instead assigns eta/(20n) to each scalar bound.

This is an application of established statistical arguments. The IUT
level result is Theorem 1 in
[Berger and Hsu (1996)](https://doi.org/10.1214/ss/1032280304).
The indexed theorem and surrounding explanation were inspected in an
[archived copy](https://downloads.regulations.gov/FDA-2017-D-5525-0003/attachment_1.pdf);
the full PDF fetch was blocked in this cycle. The fixed-sequence principle is
explicit in the publisher abstract of
[Hsu and Berger (1999)](https://doi.org/10.1080/01621459.1999.10474141);
the full article was not inspected. The problem-specific validity argument
above is included in full and does not rely on an uninspected theorem.

## Scalar intervals and deterministic caps

Let A=max(beta*q0, alpha*(sum R-q0)) and
A_j=max(beta*q_j,alpha*(R_j-q_j)). Then
X_{j,t} is in [-t A_j,w_j A]. For M observations in a known interval of width
W, unbiased sample variance v and assigned one-sided tail eta, the code uses

$$
r=\min\left\{
W\sqrt{\frac{\log(2/\eta)}{2M}},\quad
\sqrt{\frac{2v\log(4/\eta)}{M}}
+\frac{7W\log(4/\eta)}{3(M-1)}\right\}.
$$

Clip mean +/- r to the known range. Hoeffding and the empirical Bernstein
inequality each receive eta/2, making their minimum valid by a union bound.
The empirical Bernstein formula is the scaled one-sided form of
[Maurer and Pontil (2009), Theorem 4](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf).
The reused implementation is `_mean_interval` in `face_residuals.py`.
For a two-sided interval, split the assigned tail again between directions.

There is also a distribution-free upper bound

$$
c_j\le C_j^{\max}=\frac{\alpha\beta R_j}{\alpha+\beta}.
$$

Indeed, the fixed offer alpha*R_j/(alpha+beta) equalizes the two endpoint
losses at this value. Given a lower confidence bound L_lo, this yields
rho_cap=min(1,min_{C_j^max>0} w_j L_lo/C_j^max), with the empty minimum set
to one. Combine it with the grid bound by taking their maximum, on the
intersection of their confidence events. Record both components: success
from the deterministic cap is not evidence for an improvement by paired tests.

## Feasible witness and simultaneous depth bounds

On the pilot, fit offers for the n leave-one-out coalitions and choose the one
with the largest positive empirical excess. If none is positive, choose the
empty coalition with excess zero. Freeze both the coalition S and its offer
q_S before validation. Its true feasible excess

$$
e_S=w(S)L-\mathbb E\ell(q_S,Y(S))\le B
$$

has a scalar paired estimator in [-A_S,w(S)A], where
A_S=max(beta*q_S,alpha*(R(S)-q_S)). A lower scalar confidence bound, clipped
below at zero, gives W_lo<=B; an empty witness gives W_lo=0 exactly.

Split the certificate budget delta into three equal parts: the global grid
test, the two-sided grand-cost interval [L_lo,L_hi], and the selected witness.
No independence between these three validation statistics is needed. The
pilot is independent of validation, and the frozen rule is independent of both.
With probability at least 1-delta, simultaneously at every nonterminal depth,

$$
\widehat\rho\le\rho,\qquad
D_k-B\le\widehat G_k
=(1-\widehat\rho)[s_k L_{\rm hi}-W_{\rm lo}]_+.
$$

The formula is monotone in each estimated argument in the required direction.
The terminal bound is exactly zero. If numerical intervals contradict the
deterministic relation W_lo<=s_1 L_hi, return the safe bounds rho=0, W_lo=0,
L_hi=A. These always bound the relevant gaps. Diagnostics preserve the flag.

Fitting n scalar quantiles and n face witnesses needs O(n M log M) work using
sorting. Totals minus individual coordinates avoid recomputing face sums.
After fitting, the fixed 20-point grid uses O(n M) arithmetic and no
coalition optimization. Absence of an explicit multiplicity factor does not
imply uniform statistical power in n: the minimum producer margin and the
chance that all tests pass can deteriorate with dimension. No minimax
sample-complexity or computational superiority claim is made here.

## Comparisons and their guarantees

All six methods and the development decision criteria were recorded in
[standalone_protocol.md](standalone_protocol.md) before the fresh draws.

**Marginal DKW.** Combine all 2M observations for the frozen grand loss and
individual empirical optimal costs. Uniform marginal CDF errors at most
epsilon=sqrt(log(2n/eta)/(2*2M)) hold together with probability 1-eta.
The Wasserstein/Lipschitz inequality then gives

$$
c_j\le\min\{C_j^{\max},\widehat c_j+
\max(\alpha,\beta)R_j\epsilon\}.
$$

Use these upper costs and L_lo for the ratio. The selected witness is still
evaluated only on the independent validation half. The capacity-only
comparison uses C_j^max directly, with the same full-budget grand interval.
Both use the same thirds allocation, leaving the ratio third unused for the
capacity-only method. Reusing pilot observations for these fixed-rule moments
is legitimate; reusing them for the selected witness would not be.

**Learned face prices.** Refit the preceding `face_residuals` method on exactly
the same pilot and evaluate on the same validation. Its gap bound addresses
the same D1-B estimand. The combined certificate is the minimum of the paired
standalone and face bounds; its validity uses their two assigned error budgets.

**Paired SAA blocks.** Split validation into independent blocks of 64. For each
block compute its empirical D1 and subtract the empirical excess of the frozen
feasible witness. Write the result Z. Optimization and expectation imply

$$
\mathbb E Z\ge D_1(P)-e_S(P)\ge D_1(P)-B(P).
$$

This is the standard paired sample-average optimality-gap construction from
[Mak, Morton and Wood (1999)](https://doi.org/10.1016/S0167-6377(98)00054-6),
Theorem 1 and section 3.2, already mapped in the publication assessment.
Here we calibrate it using a bounded scalar interval rather than their
asymptotic interval. Positive shares give

$$
0\le Z\le(s_1-w(S))A+A_S.
$$

Use half the method's delta for an upper confidence bound on E Z and half
for an upper bound on s_1 L, then take the minimum. The empirical face solver
recomputes a valid dual upper value with a drift correction; using that value
instead of the exact empirical optimum preserves the expectation inequality.
Capping the empirical value by s_1 times empirical grand loss preserves its
upper-bound direction. All LP solves and block values are saved. Larger
blocks reduce optimization bias but leave fewer independent observations for
concentration; the present experiment fixes 64 and does not settle that tradeoff.

The 18 method-size combinations each use delta=0.05/18. A union bound gives
95% simultaneous validity **within each instance** across this comparison.
It does not give 95% joint coverage across the 108 different instances.

## Evidence and scope

See the [generated comparison](../results/standalone/summary.md) and complete
[saved outcomes](../results/standalone/results.json). The input laws are known
development cases; the samples are fresh. Each law has one independent pilot
and validation stream, with prefixes at three sizes. Counts across these
different laws are descriptive, not estimates of repeated-sampling power.
Exchangeable controls have analytically known B=D1=0. Their finite standalone
bound can remain positive because rho need not explain exactness.

The sharp depth/share formula remains the theoretical candidate. The present
statistical conversion uses established IUT, fixed-sequence, concentration and
SAA ideas. A correct guarantee or a positive conditional screen alone does not
establish a publishable original method. Temporal dependence, forecasting
errors beyond the frozen-rule setup, and real-data precision remain open.
