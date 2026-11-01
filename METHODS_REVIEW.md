# Methods review: Hotelling (1929)

- **Paper:** Harold Hotelling, "Stability in Competition," *Economic Journal* 39(153), March 1929, pp. 41–57.
- **Statistical focus:** the closed-form price equilibrium $`p_{1,2} = c(l \pm \frac{a-b}{3})`$ with its numerical
  example ($`l = 35, a = 4, b = 1, c = 1`$, giving prices 36 and 34 and profits 648 and 578), and the location claim
  that a second seller moves "as close to A as other conditions permit" (the principle of minimum differentiation),
  which the paper extends to products, churches and political parties.
- **Review standard:** internal consistency of the formal results, explicit statement of assumptions, and the
  testability of the predictions; for the 1979 critique, whether its objection is to the algebra or to the
  equilibrium concept.
- **What was read:** the full text of the 1929 article (a JSTOR-stamped scan of pp. 41–57), and the full text of
  d'Aspremont, Gabszewicz and Thisse, "On Hotelling's 'Stability in Competition'," *Econometrica* 47(5), 1979,
  pp. 1145–1150, from a copy hosted on a web page at the École normale supérieure. Later literature is cited only where those two texts
  support it.

## Methods summary

### Research design

A deductive model of duopoly with spatially differentiated customers, solved in closed form, followed by verbal
extensions. There is no empirical design. The core is a two-stage argument presented informally: prices are set as
a Nash equilibrium given locations (pp. 45–47), then one seller's location choice is analyzed given the other's
location and the induced prices (pp. 51–52). The paper treats the price stage formally and the location stage by
inspecting the profit expression.

### Sampling strategy

Not applicable. The paper uses no data. Its illustrations (Main Street, a transcontinental railroad, cider, churches,
the tariff positions of the two parties) are examples, not a sample.

### Sample size

Not applicable. The single numerical example (Fig. 1 and Fig. 2) plays the role a sample would play in an empirical
paper.

### Inclusion and exclusion criteria

Not applicable as sample rules. The model's scope conditions serve the same purpose and are stated: customers
uniformly distributed on a segment of length $`l`$, one unit demanded per unit of length per unit time (perfectly
inelastic demand), zero production cost (constant cost is said to add to prices without changing profits, p. 51),
linear transport cost $`c`$ per unit distance, mill pricing with no discrimination. Footnote 1 on p. 48 states that
the solution requires $`|p_1 - p_2| \le c(l - a - b)`$ and gives a counterexample ($`l = 20, a = 11, b = 8`$).

### Independent and dependent variables

Exogenous: $`l, a, b, c`$. Endogenous: prices $`p_1, p_2`$, market boundary $`x, y`$, quantities $`q_1, q_2`$,
profits $`\pi_1, \pi_2`$, and in the location section $`b`$.

### Statistical methods

None. The "statistics" are the comparative statics of the equilibrium: prices and profits proportional to $`c`$;
$`\pi_2`$ increasing in $`b`$; total transport cost minimized when the sellers sit at the quartiles; the observation
that the sum of profits $`\pi_1 + \pi_2`$ rises with $`(a-b)^2`$.

### Reported effect sizes

The numerical example: $`p_1 = 36`$, $`p_2 = 34`$, $`x = 14`$, $`y = 16`$, $`q_1 = 18`$, $`q_2 = 17`$,
$`\pi_1 = 648`$, $`\pi_2 = 578`$. Fig. 1 states $`x = 14, y = 16`$; Fig. 2 labels the iso-profit curves 648 and
578 and a third at 200. The paper prints the general formulas but not the numerical prices; they follow from
substitution and match the labeled profits.

### Confidence intervals

Not applicable; there is no estimation.

### P-values, if applicable

Not applicable.

### Missing data treatment

Not applicable.

### Stated limitations

The paper states several. The solution is valid only when the price difference is below the transport cost between
the sellers (footnote, p. 48). The tendency of B to move infinitesimally close to A "requires a slight modification
in the particular case" (footnote, pp. 51–52), where B's profit rises only until the distance is four-fifths of
A's distance from the center; Hotelling calls this an "adventitious feature" of a discontinuity. With elastic demand
the tendency to cluster "will be less marked" and B may locate at some distance from A (p. 56). Price discrimination
and delivered pricing are named as modifications that change the conclusions (p. 56). Extensions to a plane, to
non-uniform density and to many dimensions are asserted, not derived.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Equilibrium price, seller A | $`p_1 = c(l + (a-b)/3)`$; 36 in the example (money per unit) | p. 46, first-order conditions; Fig. 2 point E | A's best response to B's price when both serve the interior | That this price pair is an equilibrium against large deviations (undercutting to take the whole market) |
| Equilibrium price, seller B | $`p_2 = c(l - (a-b)/3)`$; 34 | p. 46 | B's best response | Same as above |
| Market split | $`x = 14`$, $`y = 16`$ (units of length) | Fig. 1 caption, p. 45; formulas p. 46 | Interior customers served by each seller | Welfare loss magnitude in any real market |
| Quantities | $`q_1 = 18`$, $`q_2 = 17`$ (units) | p. 47 formulas | Each seller's sales including hinterland | Behavior under elastic demand |
| Profits | $`\pi_1 = 648`$, $`\pi_2 = 578`$ (money per period) | Fig. 2 labels, p. 47; formula p. 50 | Equilibrium profit; shows profit proportional to $`c`$ | That profits of this type persist with entry |
| Location incentive | $`\partial \pi_2/\partial b > 0`$ for all admissible $`b`$ | p. 51 | B gains by moving toward A | An equilibrium in locations; the price stage may have no equilibrium once B is close (d'Aspremont et al. 1979) |
| Four-fifths qualification | B's profit rises toward A only while their distance exceeds 4/5 of A's distance from the center | footnote, pp. 51–52 | Limit within the paper's own example | Hotelling treats it as an artifact; he does not show the general case |
| Social optimum | Two sellers at the quartiles; three at 1/6, 1/2, 5/6 | p. 53 | Locations minimizing total transport cost | That planners or real markets would reach them |
| Existence condition (critique) | $`(l + \frac{a-b}{3})^2 \ge \frac{4}{3}l(a+2b)`$ and mirror; symmetric case $`a = b \le l/4`$ | d'Aspremont et al. 1979, Proposition 1 | When Hotelling's prices are a Nash equilibrium | Anything about locations outside the linear-cost model |

## Interpretation notes

- The price-stage algebra is internally consistent. Substituting the paper's own example reproduces the profits
  printed on Fig. 2, and the repository's script recovers all eight numbers. The example also satisfies the 1979
  existence conditions (1,296 ≥ 280 and 1,156 ≥ 420), so the specific equilibrium Hotelling draws is valid.
- The weakness is in the step from prices to locations. Hotelling checks local (first-order) optimality of prices
  and notes the boundary condition in a footnote, but he does not check whether a seller could gain by undercutting
  the rival's delivered price and capturing the whole market. d'Aspremont, Gabszewicz and Thisse show this deviation
  is profitable, for symmetric locations, whenever the sellers are inside the quartiles, so the clustering conclusion is not supported by the
  model as written. This is a documented analytical error in the published literature, not a reporting problem.
- Their quadratic-cost variant, which has a price equilibrium for every pair of locations, reverses the location
  result to maximum differentiation. The 1929 paper's own caveat on elastic demand (p. 56) already points in this
  direction.
- The political and product applications (pp. 54–57) are analogies. They carry no formal derivation and should be
  read as conjectures.
- Testability: the model yields two observable predictions, local price premia proportional to travel cost times
  distance advantage, and co-location of rivals. Neither is tested in the paper.

## Unanswered questions

- What determines whether real sellers cluster or spread out, once prices are allowed to respond to location in a
  way that has an equilibrium? The 1929 paper offers inelastic demand as the case for clustering and elastic demand
  as a reason for less of it, without a criterion.
- How do the results extend to many sellers and two dimensions, which the paper asserts without proof?
- How large are the "incomes not properly belonging to any of the categories" (p. 41) in any actual market?

## Items requiring expert verification

- Whether the four-fifths qualification in the footnote on pp. 51–52 is consistent with the existence region later
  derived by d'Aspremont et al.; the two are stated in different terms and I have not reconciled them formally.
- The scan used here has OCR noise in the equations on pp. 46–47 and 50–52; the formulas were checked against the
  1979 paper's restatement and by recomputation, not against a clean print copy.
- The attribution of later results (Salop's circle model, multi-store spatial competition) to this paper's lineage
  rests on standard accounts and the reading list entry, not on a reading of those works.

The modern rerun in this repository does not reproduce anything in the 1929 paper, which has no data. It takes the
co-location prediction to 2026 store locations and finds clustering among small-format rivals and spacing among
big-box rivals, the second being the pattern the 1979 critique predicts.
