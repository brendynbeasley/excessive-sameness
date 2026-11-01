# Hotelling (1929) on 2026 store locations: findings

## In plain English

Harold Hotelling argued in 1929 that rival sellers crowd together, and that the distance between them gives each a
small local monopoly. This repository checks that claim against 174,674 US stores of 32 national chains, and checks
his political version against roll-call votes in Congress.

- **Small stores do sit next to their rivals.** A third of Chase branches have a Bank of America within half a mile
  (4.6 times chance), 38% of AutoZones have an O'Reilly that close (3.0 times), and CVS and Walgreens pair up 1.8
  times as often as chance. Fast-food chains (McDonald's, Wendy's, Burger King) cluster too, though no more with
  their rivals than with other restaurants.
- **Big boxes keep their distance.** Home Depot and Lowe's, PetSmart and Petco, and Costco, Sam's Club and BJ's all
  sit together less often than chance would put them, and so do the dollar stores (Dollar General and Dollar Tree),
  which the tests count as small stores. A Home Depot is more likely to have a Target within half a mile than a
  Lowe's. This spacing is the direction d'Aspremont, Gabszewicz and Thisse (1979) predicted.
- **Distance is worth something.** For the median American, the nearer of Home Depot and Lowe's is 1.5 miles closer
  than the other, worth $2.18 a round trip at the IRS mileage rate. For Costco and Sam's Club the gap is 4.7 miles,
  or $6.83, and for Chase and Bank of America, which cluster where both operate but cover different regions, 4.2
  miles, or $6.04.
- **Congress stopped converging.** The gap between the party medians in the House narrowed from 0.656 in 1927–29 to
  0.498 in 1947–49, was flat to 1979, and has widened since to 0.925. No House member has voted on the other party's
  side of the line since the 107th Congress (2001–03).

A fuller account is in the [README](../README.md); methods and all test statistics are in
[TECHNICAL.md](../TECHNICAL.md).

## Key to the labels

- *A → B* or *chain_a, chain_b*: the share of chain A's stores that have a chain B store nearby. The measure is not
  symmetric, because the chains have different numbers of stores.
- *observed_share*: share of A's stores with at least one B store within the radius (half a mile unless stated).
- *null_mean_share*, *null_low_95*, *null_high_95*: mean and 2.5th/97.5th percentiles of that share over 999 random
  shuffles of chain labels among all sites of the same format.
- *ratio*: observed share divided by the shuffled mean. Above 1 means more co-location than chance.
- *p_two_sided*: share of shuffles at least as far from the shuffled mean as the observed share (plus one, over 1,000).
- *format*: big box, small box or restaurant. *category*: the rival group; chains in the same category are rivals.
- *beta*: PPML coefficient on the rival indicator, with chain-A and chain-B fixed effects and same-format indicators;
  *exp_beta* is the multiplicative effect on the count of co-located stores. Standard errors are clustered by
  unordered pair.
- *median_gap_miles*: population-weighted median, over 2020 Census tracts, of the absolute difference between the
  distance to the nearest A store and to the nearest B store. *median_round_trip_premium_usd* is twice that times
  $0.725.
- *gap*: Republican median minus Democratic median of DW-NOMINATE first-dimension scores. *overlap_members*: Democrats
  scoring to the right of the most liberal Republican plus Republicans scoring to the left of the most conservative
  Democrat.

## Tables

### hotelling_example.csv

| quantity | value |
|---|---|
| price p1 | 36 |
| price p2 | 34 |
| x (A's inner customers) | 14 |
| y (B's inner customers) | 16 |
| quantity q1 | 18 |
| quantity q2 | 17 |
| profit pi1 | 648 |
| profit pi2 | 578 |
| dAGT condition (1): (l+(a-b)/3)^2 | 1296 |
| dAGT condition (1): (4/3) l (a+2b) | 280 |
| dAGT condition (2): (l-(a-b)/3)^2 | 1156 |
| dAGT condition (2): (4/3) l (b+2a) | 420 |
| symmetric equilibrium needs a = b <= l/4 | 8.75 |

### store_counts.csv

| chain | category | format | run | records | kept |
|---|---|---|---|---|---|
| Home Depot | home improvement | big box | 2026-10-24 | 2,031 | 2,013 |
| Lowe's | home improvement | big box | 2026-07-11 | 1,763 | 1,761 |
| Menards | home improvement | big box | 2026-10-17 | 341 | 341 |
| Costco | warehouse club | big box | 2026-10-24 | 808 | 655 |
| Sam's Club | warehouse club | big box | 2026-10-10 | 1,133 | 595 |
| BJ's Wholesale | warehouse club | big box | 2026-10-03 | 269 | 269 |
| PetSmart | pet supplies | big box | 2026-10-24 | 1,701 | 1,525 |
| Petco | pet supplies | big box | 2026-10-24 | 1,377 | 1,373 |
| Target | none | big box | 2026-10-24 | 2,026 | 2,026 |
| Kohl's | none | big box | 2026-10-24 | 1,150 | 1,150 |
| Best Buy | none | big box | 2026-10-24 | 1,020 | 1,010 |
| CVS | pharmacy | small box | 2026-08-29 | 8,993 | 7,103 |
| Walgreens | pharmacy | small box | 2026-10-10 | 7,986 | 7,680 |
| Dollar General | dollar store | small box | 2026-10-10 | 20,497 | 20,494 |
| Family Dollar | dollar store | small box | 2026-10-24 | 7,081 | 7,080 |
| Dollar Tree | dollar store | small box | 2026-10-17 | 9,180 | 9,103 |
| AutoZone | auto parts | small box | 2026-10-24 | 7,400 | 6,394 |
| O'Reilly | auto parts | small box | 2026-10-24 | 6,613 | 6,613 |
| Advance Auto Parts | auto parts | small box | 2026-10-24 | 4,089 | 4,049 |
| Chase | bank | small box | 2026-10-24 | 3,671 | 3,569 |
| Bank of America | bank | small box | 2026-10-24 | 5,694 | 3,531 |
| Wells Fargo | bank | small box | 2026-10-24 | 6,126 | 4,056 |
| McDonald's | burgers | restaurant | 2026-10-10 | 24,356 | 13,486 |
| Burger King | burgers | restaurant | 2026-10-17 | 9,582 | 6,168 |
| Wendy's | burgers | restaurant | 2026-10-10 | 16,172 | 5,867 |
| KFC | chicken | restaurant | 2026-10-24 | 3,704 | 3,661 |
| Popeyes | chicken | restaurant | 2026-10-24 | 3,594 | 3,124 |
| Chick-fil-A | chicken | restaurant | 2026-10-24 | 3,485 | 3,440 |
| Starbucks | coffee | restaurant | 2026-10-10 | 16,708 | 9,983 |
| Dunkin' | coffee | restaurant | 2026-10-24 | 10,488 | 10,482 |
| Taco Bell | none | restaurant | 2026-10-24 | 8,289 | 8,280 |
| Subway | none | restaurant | 2026-10-17 | 17,793 | 17,793 |
| All chains |  |  |  | 215,120 | 174,674 |

### rival_pairs.csv

| category | chain_a | chain_b | n_a | n_b | observed_share | null_mean_share | null_low_95 | null_high_95 | ratio | p_two_sided | median_miles_to_b |
|---|---|---|---|---|---|---|---|---|---|---|---|
| auto parts | Advance Auto Parts | AutoZone | 4049 | 6394 | 34.8% | 12.3% | 11.3% | 13.4% | 2.83 | 0.001 | 0.93 |
| auto parts | Advance Auto Parts | O'Reilly | 4049 | 6613 | 28.3% | 12.7% | 11.7% | 13.6% | 2.23 | 0.001 | 1.28 |
| auto parts | AutoZone | Advance Auto Parts | 6394 | 4049 | 22.0% | 8.1% | 7.4% | 8.8% | 2.73 | 0.001 | 2.17 |
| auto parts | AutoZone | O'Reilly | 6394 | 6613 | 38.4% | 12.7% | 11.8% | 13.5% | 3.03 | 0.001 | 0.83 |
| auto parts | O'Reilly | Advance Auto Parts | 6613 | 4049 | 17.3% | 8.1% | 7.4% | 8.7% | 2.14 | 0.001 | 3.82 |
| auto parts | O'Reilly | AutoZone | 6613 | 6394 | 37.0% | 12.3% | 11.5% | 13.1% | 3.02 | 0.001 | 0.88 |
| bank | Bank of America | Chase | 3531 | 3569 | 31.5% | 7.1% | 6.3% | 8.0% | 4.42 | 0.001 | 1.38 |
| bank | Bank of America | Wells Fargo | 3531 | 4056 | 35.5% | 8.1% | 7.2% | 9.0% | 4.38 | 0.001 | 1.03 |
| bank | Chase | Bank of America | 3569 | 3531 | 32.7% | 7.1% | 6.2% | 7.9% | 4.62 | 0.001 | 1.14 |
| bank | Chase | Wells Fargo | 3569 | 4056 | 30.1% | 8.1% | 7.2% | 9.0% | 3.74 | 0.001 | 1.38 |
| bank | Wells Fargo | Bank of America | 4056 | 3531 | 30.3% | 7.1% | 6.3% | 8.0% | 4.27 | 0.001 | 1.31 |
| bank | Wells Fargo | Chase | 4056 | 3569 | 24.8% | 7.2% | 6.3% | 8.0% | 3.47 | 0.001 | 2.16 |
| burgers | Burger King | McDonald's | 6168 | 13486 | 50.8% | 33.2% | 32.1% | 34.4% | 1.53 | 0.001 | 0.48 |
| burgers | Burger King | Wendy's | 6168 | 5867 | 25.6% | 16.9% | 15.9% | 17.9% | 1.52 | 0.001 | 1.45 |
| burgers | McDonald's | Burger King | 13486 | 6168 | 23.5% | 17.6% | 16.9% | 18.2% | 1.34 | 0.001 | 1.68 |
| burgers | McDonald's | Wendy's | 13486 | 5867 | 23.8% | 16.9% | 16.2% | 17.5% | 1.41 | 0.001 | 1.68 |
| burgers | Wendy's | Burger King | 5867 | 6168 | 26.9% | 17.6% | 16.6% | 18.6% | 1.53 | 0.001 | 1.37 |
| burgers | Wendy's | McDonald's | 5867 | 13486 | 53.8% | 33.3% | 32.0% | 34.4% | 1.62 | 0.001 | 0.43 |
| chicken | Chick-fil-A | KFC | 3440 | 3661 | 13.9% | 11.1% | 10.1% | 12.2% | 1.25 | 0.001 | 2.03 |
| chicken | Chick-fil-A | Popeyes | 3440 | 3124 | 18.0% | 9.6% | 8.6% | 10.7% | 1.88 | 0.001 | 1.92 |
| chicken | KFC | Chick-fil-A | 3661 | 3440 | 12.6% | 10.5% | 9.5% | 11.6% | 1.21 | 0.001 | 2.66 |
| chicken | KFC | Popeyes | 3661 | 3124 | 15.4% | 9.6% | 8.7% | 10.5% | 1.61 | 0.001 | 2.53 |
| chicken | Popeyes | Chick-fil-A | 3124 | 3440 | 19.0% | 10.5% | 9.4% | 11.6% | 1.82 | 0.001 | 1.88 |
| chicken | Popeyes | KFC | 3124 | 3661 | 18.2% | 11.1% | 10.0% | 12.2% | 1.64 | 0.001 | 1.82 |
| coffee | Dunkin' | Starbucks | 10482 | 9983 | 28.8% | 26.3% | 25.5% | 27.1% | 1.09 | 0.001 | 1.13 |
| coffee | Starbucks | Dunkin' | 9983 | 10482 | 27.2% | 27.4% | 26.5% | 28.3% | 0.99 | 0.751 | 1.49 |
| dollar store | Dollar General | Dollar Tree | 20494 | 9103 | 10.1% | 16.8% | 16.3% | 17.3% | 0.60 | 0.001 | 3.71 |
| dollar store | Dollar General | Family Dollar | 20494 | 7080 | 11.0% | 13.5% | 13.0% | 13.9% | 0.82 | 0.001 | 4.90 |
| dollar store | Dollar Tree | Dollar General | 9103 | 20494 | 22.6% | 32.4% | 31.5% | 33.4% | 0.70 | 0.001 | 1.37 |
| dollar store | Dollar Tree | Family Dollar | 9103 | 7080 | 9.7% | 13.5% | 12.8% | 14.1% | 0.72 | 0.001 | 2.88 |
| dollar store | Family Dollar | Dollar General | 7080 | 20494 | 31.7% | 32.4% | 31.4% | 33.5% | 0.98 | 0.224 | 0.88 |
| dollar store | Family Dollar | Dollar Tree | 7080 | 9103 | 12.4% | 16.8% | 16.0% | 17.7% | 0.74 | 0.001 | 1.78 |
| home improvement | Home Depot | Lowe's | 2013 | 1761 | 13.8% | 18.6% | 16.9% | 20.3% | 0.74 | 0.001 | 2.68 |
| home improvement | Home Depot | Menards | 2013 | 341 | 2.0% | 4.0% | 3.1% | 4.9% | 0.51 | 0.001 | 324.30 |
| home improvement | Lowe's | Home Depot | 1761 | 2013 | 15.7% | 20.9% | 19.1% | 22.7% | 0.75 | 0.001 | 2.24 |
| home improvement | Lowe's | Menards | 1761 | 341 | 1.6% | 4.0% | 3.1% | 4.9% | 0.41 | 0.001 | 264.49 |
| home improvement | Menards | Home Depot | 341 | 2013 | 12.0% | 20.9% | 16.7% | 25.5% | 0.57 | 0.001 | 3.97 |
| home improvement | Menards | Lowe's | 341 | 1761 | 8.5% | 18.6% | 14.7% | 22.6% | 0.46 | 0.001 | 4.53 |
| pet supplies | PetSmart | Petco | 1525 | 1373 | 10.5% | 15.0% | 13.1% | 16.9% | 0.70 | 0.001 | 3.21 |
| pet supplies | Petco | PetSmart | 1373 | 1525 | 11.7% | 16.4% | 14.3% | 18.4% | 0.71 | 0.001 | 2.76 |
| pharmacy | CVS | Walgreens | 7103 | 7680 | 26.1% | 14.5% | 13.7% | 15.3% | 1.80 | 0.001 | 1.25 |
| pharmacy | Walgreens | CVS | 7680 | 7103 | 24.1% | 13.5% | 12.7% | 14.3% | 1.79 | 0.001 | 1.40 |
| warehouse club | BJ's Wholesale | Costco | 269 | 655 | 1.9% | 7.5% | 4.5% | 10.8% | 0.25 | 0.001 | 5.86 |
| warehouse club | BJ's Wholesale | Sam's Club | 269 | 595 | 1.9% | 6.8% | 4.1% | 10.0% | 0.27 | 0.003 | 11.21 |
| warehouse club | Costco | BJ's Wholesale | 655 | 269 | 0.8% | 3.2% | 1.8% | 4.6% | 0.24 | 0.002 | 266.80 |
| warehouse club | Costco | Sam's Club | 655 | 595 | 3.8% | 6.9% | 4.9% | 8.9% | 0.56 | 0.005 | 6.37 |
| warehouse club | Sam's Club | BJ's Wholesale | 595 | 269 | 0.8% | 3.2% | 1.8% | 4.7% | 0.27 | 0.004 | 100.02 |
| warehouse club | Sam's Club | Costco | 595 | 655 | 4.2% | 7.5% | 5.4% | 9.8% | 0.56 | 0.006 | 6.09 |

### random_labeling_summary.csv

| format | group | radius_miles | ordered_pairs | median_ratio | share_sig_above | share_sig_below |
|---|---|---|---|---|---|---|
| big box | same format, not rival | 0.25 | 96 | 1.04 | 31.2% | 22.9% |
| big box | same format, not rival | 0.5 | 96 | 1.19 | 52.1% | 14.6% |
| big box | same format, not rival | 1 | 96 | 1.34 | 69.8% | 8.3% |
| big box | rival | 0.25 | 14 | 0.24 | 0.0% | 100.0% |
| big box | rival | 0.5 | 14 | 0.53 | 0.0% | 100.0% |
| big box | rival | 1 | 14 | 0.68 | 0.0% | 71.4% |
| restaurant | same format, not rival | 0.25 | 76 | 1.26 | 77.6% | 9.2% |
| restaurant | same format, not rival | 0.5 | 76 | 1.30 | 85.5% | 7.9% |
| restaurant | same format, not rival | 1 | 76 | 1.31 | 89.5% | 3.9% |
| restaurant | rival | 0.25 | 14 | 1.49 | 71.4% | 7.1% |
| restaurant | rival | 0.5 | 14 | 1.52 | 92.9% | 0.0% |
| restaurant | rival | 1 | 14 | 1.45 | 92.9% | 0.0% |
| small box | same format, not rival | 0.25 | 90 | 1.39 | 62.2% | 31.1% |
| small box | same format, not rival | 0.5 | 90 | 1.45 | 67.8% | 26.7% |
| small box | same format, not rival | 1 | 90 | 1.50 | 73.3% | 24.4% |
| small box | rival | 0.25 | 20 | 2.45 | 70.0% | 30.0% |
| small box | rival | 0.5 | 20 | 2.48 | 70.0% | 25.0% |
| small box | rival | 1 | 20 | 2.15 | 75.0% | 20.0% |

### ppml_rival_effect.csv

| sample | term | radius_miles | ordered_pairs | rival_pairs | beta | se_cluster | ci_low | ci_high | p_value | exp_beta | exp_ci_low | exp_ci_high | clusters |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all 32 chains | rival | 0.25 | 992 | 48 | 0.209 | 0.085 | 0.042 | 0.377 | 0.014 | 1.233 | 1.043 | 1.457 | 496 |
| all 32 chains | rival_big box | 0.25 | 992 | 14 | -1.132 | 0.189 | -1.502 | -0.762 | < 0.001 | 0.322 | 0.223 | 0.467 | 496 |
| all 32 chains | rival_restaurant | 0.25 | 992 | 14 | -0.010 | 0.040 | -0.089 | 0.069 | 0.801 | 0.990 | 0.915 | 1.071 | 496 |
| all 32 chains | rival_small box | 0.25 | 992 | 20 | 0.485 | 0.136 | 0.220 | 0.751 | < 0.001 | 1.624 | 1.246 | 2.119 | 496 |
| all 32 chains | rival | 0.5 | 992 | 48 | 0.185 | 0.076 | 0.036 | 0.335 | 0.015 | 1.204 | 1.037 | 1.398 | 496 |
| all 32 chains | rival_big box | 0.5 | 992 | 14 | -0.619 | 0.120 | -0.855 | -0.383 | < 0.001 | 0.539 | 0.425 | 0.682 | 496 |
| all 32 chains | rival_restaurant | 0.5 | 992 | 14 | 0.001 | 0.030 | -0.058 | 0.059 | 0.983 | 1.001 | 0.944 | 1.061 | 496 |
| all 32 chains | rival_small box | 0.5 | 992 | 20 | 0.415 | 0.127 | 0.165 | 0.665 | 0.001 | 1.514 | 1.180 | 1.944 | 496 |
| all 32 chains | rival | 1 | 992 | 48 | 0.142 | 0.066 | 0.012 | 0.272 | 0.032 | 1.152 | 1.012 | 1.312 | 496 |
| all 32 chains | rival_big box | 1 | 992 | 14 | -0.410 | 0.072 | -0.550 | -0.270 | < 0.001 | 0.664 | 0.577 | 0.764 | 496 |
| all 32 chains | rival_restaurant | 1 | 992 | 14 | -0.006 | 0.024 | -0.053 | 0.041 | 0.797 | 0.994 | 0.948 | 1.042 | 496 |
| all 32 chains | rival_small box | 1 | 992 | 20 | 0.310 | 0.112 | 0.090 | 0.530 | 0.006 | 1.363 | 1.094 | 1.699 | 496 |
| without banks | rival | 0.5 | 812 | 42 | 0.068 | 0.068 | -0.066 | 0.202 | 0.320 | 1.070 | 0.936 | 1.224 | 406 |
| same-format pairs only | rival_big box | 0.5 | 310 | 14 | -0.447 | 0.212 | -0.863 | -0.031 | 0.035 | 0.639 | 0.422 | 0.969 | 155 |
| same-format pairs only | rival_restaurant | 0.5 | 310 | 14 | -0.019 | 0.035 | -0.089 | 0.050 | 0.583 | 0.981 | 0.915 | 1.051 | 155 |
| same-format pairs only | rival_small box | 0.5 | 310 | 20 | 0.383 | 0.129 | 0.130 | 0.636 | 0.003 | 1.467 | 1.139 | 1.890 | 155 |

### own_chain_spacing.csv

| chain | stores | median_miles_to_own | share_own_within_0.5 |
|---|---|---|---|
| Home Depot | 2013 | 5.86 | 0.2% |
| Lowe's | 1761 | 8.11 | 0.0% |
| Menards | 341 | 13.63 | 0.0% |
| Costco | 655 | 8.69 | 0.9% |
| Sam's Club | 595 | 12.54 | 0.0% |
| BJ's Wholesale | 269 | 10.60 | 1.5% |
| PetSmart | 1525 | 6.67 | 0.1% |
| Petco | 1373 | 6.63 | 0.0% |
| Target | 2026 | 4.88 | 0.2% |
| Kohl's | 1150 | 9.45 | 0.0% |
| Best Buy | 1010 | 8.40 | 1.8% |
| CVS | 7103 | 2.45 | 3.1% |
| Walgreens | 7680 | 2.31 | 2.8% |
| Dollar General | 20494 | 3.11 | 0.3% |
| Family Dollar | 7080 | 2.89 | 1.0% |
| Dollar Tree | 9103 | 2.28 | 1.1% |
| AutoZone | 6394 | 3.17 | 0.2% |
| O'Reilly | 6613 | 3.83 | 0.1% |
| Advance Auto Parts | 4049 | 3.79 | 0.4% |
| Chase | 3569 | 2.16 | 5.4% |
| Bank of America | 3531 | 2.62 | 3.3% |
| Wells Fargo | 4056 | 2.54 | 1.9% |
| McDonald's | 13486 | 2.16 | 1.9% |
| Burger King | 6168 | 3.06 | 0.9% |
| Wendy's | 5867 | 3.19 | 0.8% |
| KFC | 3661 | 4.53 | 1.7% |
| Popeyes | 3124 | 3.47 | 1.3% |
| Chick-fil-A | 3440 | 2.94 | 6.0% |
| Starbucks | 9983 | 1.58 | 8.3% |
| Dunkin' | 10482 | 1.52 | 16.4% |
| Taco Bell | 8280 | 2.81 | 0.8% |
| Subway | 17793 | 1.89 | 6.5% |

### captive_customers.csv

| chain_a | chain_b | median_miles_to_a | median_miles_to_b | share_closer_to_a | median_gap_miles | p75_gap_miles | share_gap_over_5mi | share_gap_under_1mi | median_round_trip_premium_usd |
|---|---|---|---|---|---|---|---|---|---|
| Home Depot | Lowe's | 3.52 | 4.48 | 57.9% | 1.50 | 4.23 | 21.6% | 40.5% | $2.18 |
| CVS | Walgreens | 1.92 | 1.75 | 45.0% | 0.90 | 2.52 | 16.6% | 52.9% | $1.31 |
| PetSmart | Petco | 4.36 | 4.76 | 54.4% | 1.78 | 4.54 | 23.1% | 35.3% | $2.59 |
| Costco | Sam's Club | 7.39 | 9.26 | 51.6% | 4.71 | 17.80 | 48.5% | 18.3% | $6.83 |
| McDonald's | Burger King | 1.31 | 2.16 | 73.5% | 0.72 | 1.99 | 11.1% | 58.1% | $1.04 |
| Starbucks | Dunkin' | 1.68 | 2.35 | 57.0% | 1.10 | 3.41 | 19.8% | 47.6% | $1.60 |
| AutoZone | O'Reilly | 1.92 | 2.34 | 55.8% | 0.65 | 2.52 | 19.0% | 59.3% | $0.94 |
| Dollar General | Family Dollar | 2.29 | 4.14 | 65.9% | 1.99 | 6.84 | 31.0% | 34.2% | $2.89 |
| Chase | Bank of America | 5.94 | 2.92 | 42.3% | 4.16 | 72.47 | 49.0% | 35.1% | $6.04 |

### party_gap_key_congresses.csv

| chamber | congress | start_year | dem_median | rep_median | gap | overlap_members | most_conservative_dem | most_conservative_dem_score | most_liberal_rep | most_liberal_rep_score |
|---|---|---|---|---|---|---|---|---|---|---|
| House | 70 | 1927 | -0.266 | 0.390 | 0.656 | 45 | MOREHEAD, John Henry | 0.117 | WELCH, Richard Joseph | -0.174 |
| Senate | 70 | 1927 | -0.263 | 0.417 | 0.680 | 3 | WHEELER, Burton Kendall | 0.065 | BLAINE, John James | 0.022 |
| House | 95 | 1977 | -0.324 | 0.262 | 0.586 | 196 | McDONALD, Lawrence Patton | 0.884 | WHALEN, Charles William, Jr. | -0.139 |
| Senate | 95 | 1977 | -0.329 | 0.293 | 0.623 | 18 | ALLEN, Maryon Pittman | 0.128 | JAVITS, Jacob Koppel | -0.124 |
| House | 119 | 2025 | -0.395 | 0.530 | 0.925 | 0 | PEREZ, Marie Gluesenkamp | -0.099 | FITZPATRICK, Brian K. | 0.141 |
| Senate | 119 | 2025 | -0.356 | 0.558 | 0.914 | 0 | FETTERMAN, John Karl | -0.177 | COLLINS, Susan Margaret | 0.124 |
| House | 80 | 1947 | -0.220 | 0.278 | 0.498 | 106 | WILLIAMS, John Bell | 0.127 | WELCH, Richard Joseph | -0.174 |
| Senate | 78 | 1943 | -0.191 | 0.277 | 0.468 | 21 | O'DANIEL, Wilbert Lee (Pappy) | 0.231 | LANGER, William | 0.023 |

### party_gap_trends.csv

| chamber | from | to | congresses | slope_per_decade | se_hac | ci_low | ci_high | p_value |
|---|---|---|---|---|---|---|---|---|
| House | 1929 | 2027 | 49 | 0.040 | 0.006 | 0.028 | 0.052 | < 0.001 |
| House | 1929 | 1979 | 25 | 0.002 | 0.007 | -0.012 | 0.015 | 0.826 |
| House | 1979 | 2027 | 24 | 0.069 | 0.003 | 0.062 | 0.076 | < 0.001 |
| Senate | 1929 | 2027 | 49 | 0.035 | 0.007 | 0.022 | 0.048 | < 0.001 |
| Senate | 1929 | 1979 | 25 | 0.016 | 0.014 | -0.012 | 0.044 | 0.267 |
| Senate | 1979 | 2027 | 24 | 0.063 | 0.007 | 0.050 | 0.076 | < 0.001 |

### party_overlap_last.csv

| chamber | last_congress_with_overlap | start_year |
|---|---|---|
| House | 107 | 2001 |
| Senate | 108 | 2003 |

### party_gap_by_congress.csv (every fifth Congress)

| congress | chamber | start_year | dem_median | rep_median | gap | overlap_members |
|---|---|---|---|---|---|---|
| 50 | House | 1887 | -0.379 | 0.398 | 0.777 | 3 |
| 50 | Senate | 1887 | -0.457 | 0.287 | 0.744 | 0 |
| 55 | House | 1897 | -0.396 | 0.434 | 0.831 | 0 |
| 55 | Senate | 1897 | -0.424 | 0.374 | 0.798 | 0 |
| 60 | House | 1907 | -0.366 | 0.442 | 0.808 | 0 |
| 60 | Senate | 1907 | -0.391 | 0.426 | 0.817 | 2 |
| 65 | House | 1917 | -0.312 | 0.400 | 0.712 | 0 |
| 65 | Senate | 1917 | -0.269 | 0.403 | 0.672 | 0 |
| 70 | House | 1927 | -0.266 | 0.390 | 0.656 | 45 |
| 70 | Senate | 1927 | -0.263 | 0.417 | 0.680 | 3 |
| 75 | House | 1937 | -0.239 | 0.318 | 0.557 | 105 |
| 75 | Senate | 1937 | -0.228 | 0.255 | 0.482 | 14 |
| 80 | House | 1947 | -0.220 | 0.278 | 0.498 | 106 |
| 80 | Senate | 1947 | -0.195 | 0.287 | 0.482 | 42 |
| 85 | House | 1957 | -0.306 | 0.265 | 0.571 | 76 |
| 85 | Senate | 1957 | -0.242 | 0.280 | 0.522 | 41 |
| 90 | House | 1967 | -0.343 | 0.241 | 0.584 | 206 |
| 90 | Senate | 1967 | -0.312 | 0.275 | 0.587 | 27 |
| 95 | House | 1977 | -0.324 | 0.262 | 0.586 | 196 |
| 95 | Senate | 1977 | -0.329 | 0.293 | 0.623 | 18 |
| 100 | House | 1987 | -0.320 | 0.346 | 0.666 | 42 |
| 100 | Senate | 1987 | -0.313 | 0.302 | 0.615 | 0 |
| 105 | House | 1997 | -0.384 | 0.390 | 0.774 | 8 |
| 105 | Senate | 1997 | -0.308 | 0.381 | 0.689 | 0 |
| 110 | House | 2007 | -0.379 | 0.426 | 0.805 | 0 |
| 110 | Senate | 2007 | -0.314 | 0.395 | 0.709 | 0 |
| 115 | House | 2017 | -0.393 | 0.497 | 0.890 | 0 |
| 115 | Senate | 2017 | -0.339 | 0.461 | 0.800 | 0 |

Full files, including all 992 ordered pairs (`pair_distances.csv`, `random_labeling_all_pairs.csv`) and every Congress (`party_gap_by_congress.csv`), are in this folder.
