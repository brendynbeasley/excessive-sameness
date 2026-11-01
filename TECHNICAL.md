# Technical notes

This is the technical companion to the [README](README.md). It covers the original model, the data, the rules fixed
before looking at results, every test statistic and how to reproduce the work. All tables are in
[results/FINDINGS.md](results/FINDINGS.md); a methods review of the 1929 paper is in
[METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

Harold Hotelling, "Stability in Competition," *Economic Journal* 39(153), March 1929, pp. 41–57. Two sellers with
zero cost sit on a line of length $`l`$ at distances $`a`$ and $`b`$ from its ends; each customer buys one unit and
pays travel cost $`c`$ per unit distance. The price equilibrium is

```math
p_1 = c\left(l + \frac{a-b}{3}\right),\quad p_2 = c\left(l - \frac{a-b}{3}\right),\quad
\pi_{1,2} = \frac{c}{2}\left(l \pm \frac{a-b}{3}\right)^{2}
```

His worked example ($`l = 35, a = 4, b = 1, c = 1`$) gives prices 36 and 34, quantities 18 and 17 and profits 648
and 578 (Fig. 2, p. 47); `results/hotelling_example.csv` reproduces all eight numbers. Because $`\pi_2`$ rises in
$`b`$, the second seller moves next to the first ("minimum differentiation", pp. 51–54). d'Aspremont, Gabszewicz
and Thisse (1979, Proposition 1) show that the price equilibrium exists only if
$`(l + \tfrac{a-b}{3})^2 \ge \tfrac{4}{3}l(a+2b)`$ and the mirror condition hold, which for symmetric locations
requires $`a = b \le l/4`$; with quadratic travel costs the sellers locate at the ends of the line.

## Headline results

| Test (half-mile radius) | Big box | Small box | Restaurant |
|---|---|---|---|
| Rival pairs (ordered) | 14 | 20 | 14 |
| Median ratio to random labeling, rivals | 0.53 | 2.48 | 1.52 |
| Median ratio to random labeling, same-format non-rivals | 1.19 | 1.45 | 1.30 |
| Rival pairs significantly below chance (p < 0.05) | 14 of 14 | 5 of 20 | 0 of 14 |
| PPML rival coefficient (cluster SE) | −0.619 (0.120) | 0.415 (0.127) | 0.001 (0.030) |
| exp(β), 95% CI | 0.54 [0.43, 0.68] | 1.51 [1.18, 1.94] | 1.00 [0.94, 1.06] |

The five small-box pairs below chance are all dollar-store pairs. The pooled rival coefficient is 0.185 (0.076),
p = 0.015; without banks it is 0.068 (0.068), p = 0.32.

## Data

- **Stores:** All the Places (CC0), per-chain GeoJSON from weekly runs between 2026-07-11 and 2026-10-24
  (`alltheplaces-data.openaddresses.io/runs/<run>/output/<spider>.geojson`). The run for each chain is listed in
  `src/fetch_stores.py` and `data/raw/chains.csv`. Cleaned extract: `data/raw/stores.csv` (174,674 rows). Raw files
  go to the ignored `data/raw/atp/`.
- **Population:** US Census Bureau, `CenPop2020_Mean_TR.txt`, 2020 centers of population for 85,395 tracts; 83,848
  populated tracts in the 50 states and DC are used.
- **Congress:** Voteview `HSall_members.csv` (DW-NOMINATE scores for every member, 1st to 119th Congress),
  downloaded 2026-11-01 from `voteview.com/static/data/out/members/` and committed unmodified as
  `data/raw/HSall_members.csv.gz`.
- **Travel cost:** IRS 2026 business standard mileage rate, 72.5 cents per mile (IR-2025-128, December 29, 2025).
  It counts the full cost of running a car, not the shopper's time.

## Method

Rules fixed before seeing results:

- **Store cleaning:** 50 states and DC only; drop ATMs, records with a `located_in` tag, CVS pharmacies inside
  Target, Walgreens specialty and partner pharmacies, licensed Starbucks counters, records named as distribution
  centers or temporarily closed, and repeat records of one chain within about 11 m.
- **Groups:** three formats (big box, small box, restaurant) and ten rival categories (home improvement, warehouse
  club, pet supplies, pharmacy, dollar store, auto parts, bank, burgers, chicken, coffee). Target, Kohl's, Best Buy,
  Taco Bell and Subway have no rival in the sample.
- **Distance:** great-circle miles via a k-d tree on unit-sphere coordinates. Main radius 0.5 mile, with 0.25 and
  1.0 as robustness checks.
- **Random labeling:** within each format pool, chain labels are permuted 999 times over the fixed set of sites,
  holding each chain's count fixed (seed 1929). The ratio is observed share over the mean shuffled share; the p-value
  is two-sided, $`p = (1 + \#\{|s^{(k)} - \bar s| \ge |s^{obs} - \bar s|\})/1000`$.
- **PPML:** on all 992 ordered pairs,

```math
\mathbb{E}[n_{AB}] = N_A \exp\Big(\alpha_A + \gamma_B + \sum_f \delta_f\,\text{SameFormat}_{AB,f}
+ \sum_f \beta_f\,\text{Rival}_{AB,f}\Big)
```

  with standard errors clustered by unordered pair (496 clusters).
- **Captive customers:** for each tract, distance to the nearest store of each chain in a pair; the
  population-weighted median of $`|d_A - d_B|`$, times $`2c`$ for a round trip.
- **Congress:** Democrats (code 100) and Republicans (200), 46th Congress (1879) on. The gap is
  $`G_t = \text{median}_R - \text{median}_D`$ of first-dimension scores. Trends are OLS on Congress number with
  Newey-West errors, four lags, reported per decade, for 1929–2027, 1929–1979 and 1979–2027.

## Full test statistics

| PPML term | Radius | β | SE | 95% CI | p |
|---|---|---|---|---|---|
| Rival, pooled | 0.25 | 0.209 | 0.085 | [0.042, 0.377] | 0.014 |
| Rival, pooled | 0.5 | 0.185 | 0.076 | [0.036, 0.335] | 0.015 |
| Rival, pooled | 1.0 | 0.142 | 0.066 | [0.012, 0.272] | 0.032 |
| Rival, big box | 0.25 | −1.132 | 0.189 | [−1.502, −0.762] | < 0.001 |
| Rival, big box | 1.0 | −0.410 | 0.072 | [−0.550, −0.270] | < 0.001 |
| Rival, small box | 0.25 | 0.485 | 0.136 | [0.220, 0.751] | < 0.001 |
| Rival, small box | 1.0 | 0.310 | 0.112 | [0.090, 0.530] | 0.006 |
| Rival, restaurant | 0.25 | −0.010 | 0.040 | [−0.089, 0.069] | 0.80 |
| Rival, restaurant | 1.0 | −0.006 | 0.024 | [−0.053, 0.041] | 0.80 |
| Same-format pairs only, big box | 0.5 | −0.447 | 0.212 | [−0.863, −0.031] | 0.035 |
| Same-format pairs only, small box | 0.5 | 0.383 | 0.129 | [0.130, 0.636] | 0.003 |

| Party gap trend, per decade | θ | SE (HAC) | 95% CI | p |
|---|---|---|---|---|
| House 1929–2027 | 0.040 | 0.006 | [0.028, 0.052] | < 0.001 |
| House 1929–1979 | 0.002 | 0.007 | [−0.012, 0.015] | 0.83 |
| House 1979–2027 | 0.069 | 0.003 | [0.062, 0.076] | < 0.001 |
| Senate 1929–2027 | 0.035 | 0.007 | [0.022, 0.048] | < 0.001 |
| Senate 1929–1979 | 0.016 | 0.014 | [−0.012, 0.044] | 0.27 |
| Senate 1979–2027 | 0.063 | 0.007 | [0.050, 0.076] | < 0.001 |

## Judgment calls

The format pools decide what "chance" means. A big-box rival is compared with other big-box sites, which already sit
in power centers, so a ratio below 1 says Home Depot is less likely to stand beside Lowe's than beside a typical big
box, not that it is far from retail. The PPML adds pairs across formats and absorbs each chain's taste for busy
sites with fixed effects, and it gives the same signs. Dollar Tree owned Family Dollar until July 2025, so that pair
partly reflects one owner spacing its own stores. Lowe's comes from a July 2026 run because its scraper failed in
later weeks.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/fetch_stores.py          # optional: refetches the raw GeoJSON and rebuilds data/raw/stores.csv
python src/hotelling_locations.py   # under a minute
python src/party_distance.py
```

## References

- d'Aspremont, C., Gabszewicz, J. J. & Thisse, J.-F. (1979). On Hotelling's "Stability in Competition."
  *Econometrica* 47(5), 1145–1150.
- Hotelling, H. (1929). Stability in competition. *Economic Journal* 39(153), 41–57.
- Lewis, J. B., Poole, K., Rosenthal, H., Boche, A., Rudkin, A. & Sonnet, L. Voteview: Congressional Roll-Call
  Votes Database. https://voteview.com/
- Salop, S. C. (1979). Monopolistic competition with outside goods. *Bell Journal of Economics* 10(1), 141–156.
- Silva, J. M. C. S. & Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics* 88(4),
  641–658.
