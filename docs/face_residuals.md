# Learned face prices and the statistical precision bottleneck

Completed 2026-11-01 under the [protocol fixed on 2026-10-31](residual_protocol.md).
The method has a finite-sample guarantee, including the population drift of a
pilot-fitted price. It fails the prespecified precision gate. The error
decomposition supports investigating joint statistical estimation of the gap
within the existing coalition-stability question.

The results below establish a baseline and a diagnosis. Scientific originality,
runtime superiority and publication readiness remain unestablished.

## Model and quantities being certified

Let \(0\le Y_i\le R_i\), \(n\ge2\), and
\(\ell(q,t)=\alpha(t-q)_++\beta(q-t)_+\), with positive common penalties.
Fix an implemented offer \(q_0\in[0,R(N)]\) and possibly signed shares
\(\sum_i w_i=1\), independently of validation data. Write

$$
L=E_P\ell(q_0,Y(N)),\quad a_i=w_iL,\quad
c_P(z)=\min_{0\le q\le R^\top z}E_P\ell(q,z^\top Y).
$$

For an actual coalition \(S\), use \(c_P(S)=c_P(1_S)\). The target saving and
the first exclusion relaxation from the [preceding note](exclusion.md) are

$$
B=\max\{0,\max_{\varnothing\ne S\subsetneq N}[a(S)-c_P(S)]\},
\qquad
D_1=\max_{i\in N}\max_{\substack{0\le z\le1\\z_i=0}}
             [a^\top z-c_P(z)].
$$

Every proper coalition belongs to a face, so \(0\le B\le D_1\).
We seek both an interval for \(B\) and an upper bound on \(D_1-B\).
Small structural error alone does not imply a narrow statistical interval.

## Frozen prices with nonzero population mean

For each face \(F=N\setminus\{i\}\), use an independent pilot to choose
\(q_F\in[0,R(F)]\). Set \(\nu_F(Y)\) to \(\alpha\) above this offer and
\(-\beta\) below it, with any frozen value in \([-\beta,\alpha]\) at equality.
The implementation fits a pilot quantile and chooses its tie value to balance
the pilot score. The argument only requires the stated bounds and threshold
identity. It does not require population optimality of the fitted offer.

For this fixed score define

$$
\mu_F=E\nu_F,\qquad
x_{Fj}=E[w_j\ell(q_0,Y(N))-Y_j\nu_F],\qquad
v_{Fj}=x_{Fj}+R_j(\mu_F)_+,\quad j\in F.
$$

The drift correction and face upper bound are

$$
b_F=R(F)(\mu_F)_+-q_F\mu_F
   =(R(F)-q_F)(\mu_F)_++q_F(-\mu_F)_+,\qquad
H_F=\sum_{j\in F}(v_{Fj})_+.
$$

Pilot balancing does not justify setting \(\mu_F=0\). If a pilot contains only
zero production but true production is always \((1,1,1)\), the rule
\(q_0=0,w_i=1/3\) has \(B=2\). Fitted face offers are zero. Ignoring drift
gives zero residuals and an invalid zero upper bound. The correction recovers
two. This case is a regression test.

**Proposition 1.** Put

$$
e_F=w(F)L-E\ell(q_F,Y(F)),\quad W_F=(e_F)_+,\quad
g_F=\min\left\{H_F,\sum_{j\in F}(-v_{Fj})_++b_F\right\}.
$$

Then

$$
\max_F W_F\le B\le D_1\le\max_F H_F,\qquad
0\le D_1-B\le\max_F g_F.
$$

**Proof.** For any fractional membership on face \(F\) and its optimal offer
\(q_z\), bounded scores give

$$
c_P(z)\ge E[(z^\top Y-q_z)\nu_F]
       \ge E[z^\top Y\nu_F]-(R^\top z)(\mu_F)_+.
$$

The last inequality uses \(0\le q_z\le R^\top z\), including both signs of
\(\mu_F\). Consequently \(a^\top z-c_P(z)\le z^\top v_F\le H_F\).

The full face coalition can use \(q_F\), which gives \(e_F\le B\).
The threshold score has the exact pointwise identity
\(\ell(q_F,Y(F))=\nu_F(Y)(Y(F)-q_F)\). Thus
\(e_F=\sum_{j\in F}v_{Fj}-b_F\).
Writing \(P_F=\sum(v_{Fj})_+\) and \(N_F=\sum(-v_{Fj})_+\),

$$
H_F-W_F=P_F-[P_F-N_F-b_F]_+
       =\min(P_F,N_F+b_F)=g_F.
$$

Finally \(D_1-B\le\max_F(H_F-B)\le\max_F(H_F-W_F)\). QED.

This extends the preceding population residual observation to fixed, possibly
suboptimal pilot prices. It uses ordinary weak duality and a positive-part
identity. It is not claimed as a novel general duality theorem.

## Simultaneous finite-sample certificate

Conditional on the frozen rule and pilot, let the \(M\ge2\) validation vectors
be iid from \(P\). They need not have independent producer coordinates.
Use simultaneous intervals for every \(\mu_F\) and \(x_{Fj}\), lower bounds
for the paired witnesses \(e_F\), and an upper bound \(L_+\) for \(L\).

For a bounded scalar with known range width \(d\), sample mean \(\bar X\) and
unbiased sample variance \(s^2\), the implementation uses radius

$$
r=\min\left\{
d\sqrt{\frac{\log(2/\eta)}{2M}},
\sqrt{\frac{2s^2\log(4/\eta)}M}
 +\frac{7d\log(4/\eta)}{3(M-1)}
\right\}.
$$

Each expression has one-sided failure budget \(\eta/2\). A union bound therefore
justifies their minimum with budget \(\eta\). The second expression is the scaled
empirical Bernstein inequality in Maurer and Pontil, Theorem 4. Lower tails use
the reflected random variable. Clip intervals to the known scalar range.
[Primary theorem](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf)

There are \(K=2n^2+n+1\) one-sided events. These comprise \(2n\) score tails,
\(2n(n-1)\) residual tails, \(n\) witness lower tails and one grand-loss upper
tail. Set \(\eta=\delta/K\).

Let \(A=\max\{\beta q_0,\alpha(R(N)-q_0)\}\) and
\(A_F=\max\{\beta q_F,\alpha(R(F)-q_F)\}\).
The deterministic intervals used for the observed scalars are

| Scalar | Minimum | Maximum |
| --- | --- | --- |
| \(\nu_F\) | \(-\beta\) | \(\alpha\) |
| \(w_j\ell_0-Y_j\nu_F\) | \(\min(0,w_jA)-\alpha R_j\) | \(\max(0,w_jA)+\beta R_j\) |
| \(w(F)\ell_0-\ell_F\) | \(\min(0,w(F)A)-A_F\) | \(\max(0,w(F)A)\) |
| \(\ell_0\) | \(0\) | \(A\) |

Here \(\ell_0=\ell(q_0,Y(N))\) and \(\ell_F=\ell(q_F,Y(F))\).
These paired observations retain covariance within each scalar. The final
bound still combines separate scalar confidence intervals across producers.

Write the score interval as \([\mu_F^-,\mu_F^+]\) and the residual intervals
as \([x_{Fj}^-,x_{Fj}^+]\). Define

$$
v_{Fj}^- =x_{Fj}^-+R_j(\mu_F^-)_+,\qquad
v_{Fj}^+ =x_{Fj}^++R_j(\mu_F^+)_+,
$$
$$
b_F^+=\max\{(R(F)-q_F)(\mu_F^+)_+,\ q_F(-\mu_F^-)_+\},
\quad H_F^+=\sum_j(v_{Fj}^+)_+,
$$
$$
g_F^+=\min\{H_F^+,\ \sum_j(-v_{Fj}^-)_++b_F^+\}.
$$

Let \(W_-=\max(0,\max_F e_F^-)\). For any vector \(u\), write
\(h_{\rm proper}(u)=\sum_j(u_j)_+-\min_j(u_j)_+\).
Nonnegative standalone costs also imply \(D_1\le h_{\rm proper}(w)L\).
The final reported values are

$$
U=\min\{\max_F H_F^+,\ h_{\rm proper}(w)L_+\},
\qquad
G=\min\{\max_F g_F^+,\ U-W_-\}.
$$

**Proposition 2.** With probability at least \(1-\delta\),

$$
W_-\le B\le D_1\le U,\qquad D_1-B\le G.
$$

**Proof.** Condition on the pilot and frozen rule. The union bound gives all
scalar bounds simultaneously. Positive parts are monotone, and \(b_F\) reaches
its largest value over the mean interval at an endpoint. Therefore
\(H_F\le H_F^+\), \(g_F\le g_F^+\) and \(e_F^-\le e_F\). Apply Proposition 1
and the nonnegative-cost cap. The two upper bounds on \(D_1-B\) hold on the
same event, so taking their minimum is valid. Integrating over the independent
pilot preserves the probability statement. QED.

If the computed interval is empty beyond numerical tolerance, the implementation
returns the deterministic interval \([0,h_{\rm proper}(w)A]\), with the same
upper bound for the gap and an explicit fallback flag. There were no fallbacks
in the reported synthetic primary runs.

Fitting all face quantiles takes \(O(nM_{\rm pilot}\log M_{\rm pilot})\) sorting
work, in addition to the current array calculations. Validation takes
\(O(Mn^2)\) arithmetic and performs neither coalition enumeration nor a linear
program. This is an operation-count statement. Runtime superiority has not
been benchmarked. The matched single-grand-price control uses
\(2(n+1)+1\) scalar tails and the proper-subset support function.

## Fair-budget experiment and failed precision gate

The [saved comparison](../results/residuals/summary.md) uses 104 known laws and
fresh, separate pilot and validation streams. The original 100 laws retain
their previously frozen offers and shares. Four six-producer mixture cases
were added in the protocol. The heterogeneous subgroup has 48 prespecified
cases. Pilot-fitted methods receive \(M\) pilot plus \(M\) validation observations.
Fixed-forecast methods use all \(2M\) observations for validation. Exhaustive
references use both the validation-only and the full \(2M\) budgets.

Each of six methods at each of three sizes receives
\(\delta=0.05/18\). This provides a 95% simultaneous statement for the
prespecified methods and sizes of one instance under their iid assumptions.
It is not a 95% simultaneous claim across all 104 different instances.

At \(M=4096\), the heterogeneous subgroup gives the following mean slack
\((U-B)/A\). This measures conservative certification, not operating-cost savings.

| Method | Mean normalized upper slack |
| --- | ---: |
| Pilot-fitted face prices | 0.149625 |
| Pilot-fitted single grand price, matched concentration | 0.164731 |
| Forecast face prices, full validation budget | 0.191648 |
| Original forecast moment certificate, full budget | 0.205850 |
| Exhaustive certificate on validation only | 0.082388 |
| Exhaustive certificate, full budget | 0.056600 |

The face method reduces mean slack by about 27.3% against the original
full-budget moment bound. Exhaustive checking remains more precise.
Only **1 of 48** heterogeneous instances certifies \(G\le0.05A\), against
the prespecified requirement of at least half. The main-candidate gate fails.

All 1,872 evaluated upper bounds covered the known \(B\). All 312 primary
checks satisfied the joint inequalities against the population oracles.
These finite observations check implementation and can expose violations.
They do not establish the theorem or estimate its coverage accurately.

### Diagnosis using the same learned prices

The [post-run decomposition](../results/residuals/diagnosis.md) keeps every
pilot-fitted price unchanged and substitutes exact population moments for
validation estimates. In the heterogeneous group, 41 of 48 population-moment
gap bounds satisfy the 5% threshold. The finite-data count is 1 of 48.
Mean normalized values are

| Quantity | Mean |
| --- | ---: |
| Actual structural gap \(D_1-B\) | 0.000168 |
| Gap bound using learned prices and exact moments | 0.026120 |
| Certified finite-data gap bound | 0.149803 |
| Population upper-bound slack \(U_{\rm pop}-B\) | 0.021398 |
| Statistical expansion \(U-U_{\rm pop}\) | 0.128226 |

The statistical expansion is the dominant contributor within this estimator.
It includes the score-mean correction and simultaneous residual intervals.
This is evidence about the implemented construction. It is not a lower bound
on the information needed by every possible estimator.

All 48 actual structural gaps satisfy the chosen threshold. The grid therefore
tests successful certification of small gaps. It does not establish balanced
classification performance for large and small gaps. The earlier signed-share
construction with gap \(7/50\) remains an explicit regression control.

## Chronological wind check

The [source configuration](../configs/residual_wind_sources.json) pins archive
identities and upstream versions. Raw archives stay outside the repository.

* The Texas panel has 17,544 complete joint hours in 2007–2008 at sites
  19612, 18831, 20178 and 20329. These are modeled WIND Toolkit outputs.
  Site IDs and archive hashes match the original reconciliation repository's
  pinned manifest. Capacities are 2, 16, 10 and 16 MW, each with the specified
  0.001 MW rounding allowance. All twelve five-minute readings are required
  to construct an hour.
* The French panel has 17,262 retained joint hours in 2014–2015 for the four
  ENGIE La Haute Borne turbines distributed with OpenOA. These are measured
  SCADA active-power readings, transformed to bounded export. Each available
  ten-minute reading is clipped to \([0,2050]\) kW before averaging.
  Of 420,480 raw rows, 48 are duplicate keys, 2,569 unique readings are
  nonfinite, 77,431 finite readings are negative and 68 exceed rated power.
  There are also 48 absent turbine slots. Requiring six valid readings for
  each turbine discards 258 joint hours. The substantial negative-power
  clipping changes the target to exported production and is part of the model.

ENGIE is the source of the measured data. The pinned OpenOA data readme states
Open Licence 2.0 (Etalab) for this dataset. The repository stores derived
summaries and a verified downloader, not a copy of the raw archive.
[OpenOA source and attribution](https://github.com/NatLabRockies/OpenOA/blob/bf2dacd44e0a54ad818b1a7691988d0b004f4496/examples/data/readme.md)

For each year, January–March determines one frozen historical-scenario offer and
shares. April–June fits audit prices, July–September computes the certificate,
and October–December supplies the untouched empirical reference. Each quarter's
joint timestamps, counts, offers, shares and data hashes are saved.
The future benchmark optimizes each of the 14 proper coalitions within its own
quarter. It is an empirical benchmark, not its unknown population optimum.

This test reuses the Texas sites, not the original project's hourly forecast
reconciler. The new rule is unconditional and held fixed within the year.
The [generated table](../results/residuals/wind.md) shows the new face upper
bound improves on the original moment upper bound only for France 2014.
It is looser in the other three panel-years. Full-budget exhaustive checking
has the smallest upper bound in all four comparisons.

All four future empirical excesses lie within the reported primary intervals.
Hourly dependence and seasonal change invalidate the iid coverage interpretation
for this exercise. These are descriptive transfer outcomes, with no demonstrated
operational advantage or time-series confidence guarantee.

## Closest statistical precedents and reading limits

| Source | Relevant result and inspected scope | Relationship to this investigation |
| --- | --- | --- |
| [Maurer and Pontil (2009)](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf) | Theorem 4 statement and finite-class discussion | Supplies the implemented variance-sensitive concentration. This statistical ingredient is established prior work. |
| [Pantazis et al. (2024)](https://proceedings.mlr.press/v242/pantazis24a.html) | Model, instability definition and theorem statements in the proceedings PDF, including Theorem 5. Full algorithm proofs were not audited. | PAC stability with private uncertainty samples is already studied. Their probability of realized coalition instability differs from the magnitude of our maximum expected excess with optimizing coalition offers. The distinction needs a full reduction comparison before any originality claim. |
| [Balkanski, Syed and Vassilvitskii (2017)](https://arxiv.org/abs/1703.03111) | Abstract and stated sampling model | Statistical cost sharing uses observed coalition-cost tuples. Our joint production samples give a different observation model. Abstract-level inspection does not rule out a theorem implication. |
| [Mak, Morton and Wood (1999)](https://doi.org/10.1016/S0167-6377(98)00054-6) | Publisher abstract and accessible institutional manuscript excerpts. Full proof audit remains pending. | Sample-average optimization bounds and common-random-number gap estimates are established tools. A paired aggregate-gap estimator must be compared against this work, rather than claimed new by construction. |

The original newsvendor-game and expected-core sources remain in
[research_directions.md](research_directions.md). None of the current reading
establishes global absence of an equivalent result.

## Decision and next bounded question

Retain the proof, counterexamples, fresh-sample comparison and measured-data
stress test. Do not scale this componentwise confidence construction as the
main precision result. The failed gate concerns this estimator.

The next question is whether a **paired aggregate gap estimate** can preserve
the useful covariance without accumulating a separate error margin for every
producer. One valid starting inequality follows from ordinary sample-average
optimization.

Choose a proper coalition \(S_*\) and feasible offer \(q_*\) using a separate
pilot and then freeze them. For a fresh iid block with empirical law
\(\widehat P_b\), define

$$
e_*(P)=w(S_*)E_P\ell_0-E_P\ell(q_*,Y(S_*)),\qquad
Z_b=D_1(\widehat P_b)-e_*(\widehat P_b).
$$

The witness is feasible in the face relaxation, so \(Z_b\ge0\) pointwise.
For fixed rule and feasible set, \(D_1(P)\) is a supremum of functionals linear
in \(P\), hence \(E D_1(\widehat P_b)\ge D_1(P)\). The frozen witness is
unbiased and satisfies \(e_*(P)\le B(P)\). It follows that

$$
E Z_b\ge D_1(P)-e_*(P)\ge D_1(P)-B(P).
$$

Independent blocks permit scalar concentration for their mean with known
bounds. The price is sample-average optimization bias, witness suboptimality
and the cost of solving each block. Subtracting two separately optimized
empirical values \(D_1(\widehat P)-B(\widehat P)\) has no such justification.

This inequality is a standard starting point, not a new contribution. Before
another empirical run, complete the closest-proof comparison, specify a
fixed-budget block design and fresh random streams, and prespecify a precision
gate. The existing synthetic outcomes are now development data. A successful
extension must improve an explicit finite-sample or computational tradeoff
beyond the standard paired-gap construction. Temporal dependence is a separate
unresolved assumption.

## Reproduction

From an installed checkout, run

    python -m unittest discover -s tests -v
    python scripts/check_face_residuals.py
    python scripts/analyze_residuals.py
    python scripts/check_wind_residuals.py --cache /path/outside/repository/wind-cache

The wind script verifies archive hashes before parsing and downloads missing
files from the configured sources. Synthetic results record generator entropy,
sample counts, dependency versions and source hashes. The diagnosis script
reads saved outcomes and records their hash. The completed suite has 33 passing
tests. Wind processing was also executed against the verified archives.
