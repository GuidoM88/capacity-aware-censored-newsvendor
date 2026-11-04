# Validation protocol for standalone-cost coverage

Fixed on 2026-11-04 before drawing the new pilot and validation samples.
The population inspection of the original laws is development analysis. Of
100 original cases, 96 have strictly positive frozen shares and 47 of these
belong to the previous heterogeneous subgroup. Four cases with nonpositive
shares are outside the present theorem. Exact rho is at least 0.5 in 40 of
96 cases and at least 0.6 in 35. In the heterogeneous subgroup these counts
are 12 and 9. With exact moments and exact B, the standalone-cost bound is
at most 5% of A in 8 of 47 heterogeneous cases. This places a population
limit on its broad precision performance before any sampling experiment.

## Candidate and fixed comparisons

Keep the implemented offer and shares frozen. Fit each producer's standalone
offer on an independent pilot. For thresholds 0.05, 0.10, ..., 1.00, test
whether every paired mean w_j times grand loss minus threshold times the
producer's pilot-offer loss is positive. Stop at the first failed threshold.
Use the intersection-union and fixed-sequence arguments to control false
certification at the assigned level. Compare an otherwise identical version
with a Bonferroni adjustment over producers and thresholds.

Also use the deterministic standalone-cost cap alpha*beta*R_j/(alpha+beta).
Record the lower rho bound obtained from that cap separately from the paired
test. A grand-loss confidence interval and a lower bound from one feasible
coalition selected on the pilot complete the gap certificate. Split each
method's error budget equally among the rho bound, grand-cost interval and
witness bound when all three are used. The feasible witness is the best
pilot-fitted leave-one-out coalition or the empty coalition. All observations
used to validate that selected witness come from the independent validation.

Compare six prespecified methods at M=256,1024,4096 pilot and equally many
validation observations, each using delta=0.05/18.

1. Paired fixed-sequence singleton certificate, combined with the capacity cap.
2. Matched Bonferroni singleton certificate, combined with the capacity cap.
3. Marginal DKW optimized-cost ratio using all 2M observations for fixed-rule
   costs, and validation alone for the selected witness.
4. Capacity-cap ratio using all 2M observations for grand cost, and validation
   alone for the selected witness.
5. The preceding learned face-price certificate using M pilot and M validation.
6. A Mak-Morton-Wood paired block baseline, using the same pilot-selected
   witness and independent validation blocks of 64. Each block computes its
   first exclusion relaxation. Use a bounded-mean upper interval and cap it
   by a grand-cost upper interval. This changes the original asymptotic
   calibration to bounded finite-sample concentration.

All bounded scalar intervals use the same minimum of Hoeffding and empirical
Bernstein radii, with the tail budget divided between those two inequalities.
Record normalized upper gap G/A, coverage against the true population gap,
rho error, detection of rho >= 0.5, and numerical fallback flags. Also report
the minimum of the paired singleton and face bounds. Their separate error
budgets are already covered by the overall per-instance union bound.

## Data, controls and interpretation

Use fresh SeedSequence entropy [20261104, instance_index, stream], with
stream 0 for the pilot and 1 for validation. Reuse the original 96 eligible
laws as a development benchmark. Add 12 exchangeable controls with n=6,12,24
and true rho=0.4,0.5,0.6,0.8. Each control mixes independent Bernoulli-half
coordinates with a common Bernoulli-half output. Choose the mixture weight
analytically to obtain the specified rho. The frozen forecast has equal mass
on all-zero and all-one output, giving equal shares and offer n/2. Binomial
expectations give population costs, and the exchangeable theorem gives B=D1=0.
The controls evaluate both sides of the threshold and dimension dependence.

The candidate passes the conditional detection screen if, at M=4096, it
certifies at least 80% of the original cases with rho >= 0.6 and makes no
observed false certifications on cases with rho < 0.5. The latter is a
diagnostic, while the probability guarantee comes from the proof. Report
boundary rho=0.5 cases separately.

The earlier broad precision target remains at least half the heterogeneous
cases with G <= 0.05 A. Its population obstruction is recorded above.
Any improvement from combining certificates must be reported with the same
samples and simultaneous confidence accounting. Do not infer a publication
claim from conditional detection alone.

The previously examined wind quarters are development data. This cycle uses
the known-law and fresh iid experiments to assess the finite-sample theorem.
Time-series validity remains a separate research requirement.
