"""Hotelling (1929) on 2026 store locations: do rival chains set up shop next to each other?

Hotelling's duopoly predicts that two sellers competing for customers spread along a line crowd
together ("minimum differentiation"). d'Aspremont, Gabszewicz and Thisse (1979) showed the result
needs fixing, and that with quadratic travel costs sellers move apart instead. This script:

  1. recomputes Hotelling's own numerical example and the 1979 existence condition,
  2. measures, for every ordered pair of 32 national chains, the share of chain A's US stores that
     have a chain B store within half a mile,
  3. compares rival pairs with a random-labeling null inside each store format (999 shuffles),
  4. estimates a Poisson (PPML) model on all 992 ordered pairs with chain fixed effects, and
  5. measures how much of a travel advantage the nearest store holds over its rival, using 2020
     Census tract population centers, which is Hotelling's source of local market power.

Usage (from the repository root, after src/fetch_stores.py or with the committed stores.csv):
    python src/hotelling_locations.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

EARTH_MILES = 3958.8
RADIUS = 0.5                 # main co-location radius in miles: same block or same shopping center
RADII = [0.25, 0.5, 1.0]     # robustness radii, fixed before looking at results
N_PERM = 999                 # random-labeling shuffles per format pool
SEED = 1929
COST_PER_MILE = 0.725        # IRS 2026 business standard mileage rate, IR-2025-128 (Dec 29, 2025)
FAR_GAP = 5.0                # miles: a household this much closer to one store than to its rival
# Rival pairs whose captive-customer split is reported (one per category with two big players).
CAPTIVE_PAIRS = [("Home Depot", "Lowe's"), ("CVS", "Walgreens"), ("PetSmart", "Petco"),
                 ("Costco", "Sam's Club"), ("McDonald's", "Burger King"), ("Starbucks", "Dunkin'"),
                 ("AutoZone", "O'Reilly"), ("Dollar General", "Family Dollar"),
                 ("Chase", "Bank of America")]


def hotelling_example():
    """Hotelling's Fig. 1 market: l = 35, a = 4, b = 1, c = 1, zero production cost."""
    l, a, b, c = 35.0, 4.0, 1.0, 1.0
    p1 = c * (l + (a - b) / 3)
    p2 = c * (l - (a - b) / 3)
    x = 0.5 * (l - a - b + (p2 - p1) / c)
    y = 0.5 * (l - a - b + (p1 - p2) / c)
    q1, q2 = a + x, b + y
    rows = [("price p1", p1), ("price p2", p2), ("x (A's inner customers)", x),
            ("y (B's inner customers)", y), ("quantity q1", q1), ("quantity q2", q2),
            ("profit pi1", p1 * q1), ("profit pi2", p2 * q2),
            # d'Aspremont-Gabszewicz-Thisse (1979) Proposition 1: equilibrium exists iff both hold
            ("dAGT condition (1): (l+(a-b)/3)^2", (l + (a - b) / 3) ** 2),
            ("dAGT condition (1): (4/3) l (a+2b)", 4 / 3 * l * (a + 2 * b)),
            ("dAGT condition (2): (l-(a-b)/3)^2", (l - (a - b) / 3) ** 2),
            ("dAGT condition (2): (4/3) l (b+2a)", 4 / 3 * l * (b + 2 * a)),
            ("symmetric equilibrium needs a = b <= l/4", l / 4)]
    df = pd.DataFrame(rows, columns=["quantity", "value"])
    df.to_csv(OUT / "hotelling_example.csv", index=False)
    print("Hotelling's example:", ", ".join(f"{q} = {v:g}" for q, v in rows[:8]))
    return df


def to_xyz(lat, lon):
    """Unit-sphere coordinates, so straight-line (chord) distance ranks like great-circle distance."""
    la, lo = np.radians(lat), np.radians(lon)
    return np.column_stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def chord(miles):
    return 2 * np.sin(miles / (2 * EARTH_MILES))


def miles(ch):
    return 2 * EARTH_MILES * np.arcsin(np.clip(ch / 2, 0, 1))


def pair_table(stores, chains, trees, xyz):
    """Observed nearest-rival distance statistics for every ordered pair (A, B)."""
    rows = []
    for a in chains.chain:
        pts = xyz[a]
        for b in chains.chain:
            if a == b:
                continue
            d = miles(trees[b].query(pts, k=1)[0])
            row = {"chain_a": a, "chain_b": b, "n_a": len(pts), "n_b": len(xyz[b]),
                   "median_miles_to_b": np.median(d)}
            for r in RADII:
                row[f"n_within_{r}"] = int((d <= r).sum())
                row[f"share_within_{r}"] = (d <= r).mean()
            rows.append(row)
    pairs = pd.DataFrame(rows)
    info = chains.set_index("chain")
    for side in ("a", "b"):
        pairs[f"category_{side}"] = pairs[f"chain_{side}"].map(info.category)
        pairs[f"format_{side}"] = pairs[f"chain_{side}"].map(info.format)
    pairs["same_format"] = pairs.format_a == pairs.format_b
    pairs["rival"] = (pairs.category_a == pairs.category_b) & (pairs.category_a != "none")
    pairs["pair_id"] = [" / ".join(sorted(t)) for t in zip(pairs.chain_a, pairs.chain_b)]
    return pairs


def random_labeling(stores, chains, radius, rng):
    """Shuffle chain labels among all sites of one store format and recount co-location.

    For each site the script lists every other site in the same format pool within `radius`.
    A shuffle keeps the sites and each chain's store count fixed and reassigns which chain sits
    where; the share of A's sites with at least one B site nearby is then recounted.
    """
    out = []
    for fmt, pool in stores.groupby("format"):
        pool = pool.reset_index(drop=True)
        names = sorted(pool.chain.unique())
        code = {c: i for i, c in enumerate(names)}
        labels = pool.chain.map(code).to_numpy()
        k = len(names)
        pairs = cKDTree(to_xyz(pool.lat.to_numpy(), pool.lon.to_numpy())).query_pairs(
            chord(radius), output_type="ndarray")
        i = np.concatenate([pairs[:, 0], pairs[:, 1]])   # both directions
        j = np.concatenate([pairs[:, 1], pairs[:, 0]])
        n_by_chain = np.bincount(labels, minlength=k)

        near = np.zeros((len(pool), k), dtype=np.float32)

        def shares(lab):
            near[:] = 0
            near[i, lab[j]] = 1                           # site i has a chain lab[j] site nearby
            onehot = np.zeros((len(pool), k), dtype=np.float32)
            onehot[np.arange(len(pool)), lab] = 1
            return (onehot.T @ near) / n_by_chain[:, None]

        obs = shares(labels)
        sims = np.empty((N_PERM, k, k))
        for s in range(N_PERM):
            sims[s] = shares(rng.permutation(labels))
        mean, sd = sims.mean(0), sims.std(0)
        dev = np.abs(sims - mean) >= np.abs(obs - mean) - 1e-12
        p = (1 + dev.sum(0)) / (N_PERM + 1)
        lo, hi = np.percentile(sims, 2.5, axis=0), np.percentile(sims, 97.5, axis=0)
        for a in names:
            for b in names:
                if a == b:
                    continue
                ia, ib = code[a], code[b]
                out.append({"format": fmt, "chain_a": a, "chain_b": b, "radius_miles": radius,
                            "observed_share": obs[ia, ib], "null_mean_share": mean[ia, ib],
                            "null_low_95": lo[ia, ib], "null_high_95": hi[ia, ib],
                            "ratio": obs[ia, ib] / mean[ia, ib] if mean[ia, ib] > 0 else np.nan,
                            "z": (obs[ia, ib] - mean[ia, ib]) / sd[ia, ib] if sd[ia, ib] > 0 else np.nan,
                            "p_two_sided": p[ia, ib]})
        print(f"  random labeling, {fmt:10s} r = {radius} mi: {len(pool):6d} sites, "
              f"{len(pairs):7d} site pairs within radius, {N_PERM} shuffles")
    return pd.DataFrame(out)


def ppml(pairs, radius, sample_note, keep=None, by_format=False):
    """Poisson pseudo-ML on ordered pairs: counts of A stores with a B store within radius.

    E[n_AB] = N_A exp(alpha_A + gamma_B + delta_f SameFormat + beta Rival); standard errors are
    clustered by unordered pair, since (A, B) and (B, A) share the same stores.
    """
    df = pairs if keep is None else pairs.loc[keep]
    df = df.reset_index(drop=True)
    X = pd.get_dummies(df[["chain_a"]], drop_first=True, dtype=float)
    X = X.join(pd.get_dummies(df[["chain_b"]], drop_first=True, dtype=float))
    for fmt in sorted(df.format_a.unique()):
        X[f"same_format_{fmt}"] = ((df.format_a == fmt) & df.same_format).astype(float)
    terms = []
    if by_format:
        for fmt in sorted(df.format_a.unique()):
            X[f"rival_{fmt}"] = ((df.format_a == fmt) & df.rival).astype(float)
            terms.append(f"rival_{fmt}")
    else:
        X["rival"] = df.rival.astype(float)
        terms.append("rival")
    X = sm.add_constant(X.loc[:, X.std() > 0])      # a subsample can leave a dummy with no variation
    # In a subsample (same-format pairs only) some format dummies are sums of chain dummies.
    # Drop any column that adds no rank, testing the constant and rival terms first so they stay.
    keep = []
    for col in ["const"] + terms + [c for c in X.columns if c not in terms and c != "const"]:
        if np.linalg.matrix_rank(X[keep + [col]].to_numpy()) > len(keep):
            keep.append(col)
    X = X[keep]
    groups = pd.factorize(df.pair_id)[0]
    fit = sm.GLM(df[f"n_within_{radius}"], X, family=sm.families.Poisson(),
                 offset=np.log(df.n_a)).fit(cov_type="cluster", cov_kwds={"groups": groups})
    rows = []
    for term in terms:
        b, se = fit.params[term], fit.bse[term]
        rows.append({"sample": sample_note, "term": term, "radius_miles": radius,
                     "ordered_pairs": len(df), "rival_pairs": int(X[term].sum()),
                     "beta": b, "se_cluster": se, "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
                     "p_value": fit.pvalues[term], "exp_beta": np.exp(b),
                     "exp_ci_low": np.exp(b - 1.96 * se), "exp_ci_high": np.exp(b + 1.96 * se),
                     "clusters": len(np.unique(groups))})
    return rows


def captive_customers(stores, trees):
    """Population-weighted travel advantage of the nearer store over its rival."""
    tr = pd.read_csv(RAW / "CenPop2020_Mean_TR.txt", encoding="utf-8-sig", dtype={"STATEFP": str})
    n0 = len(tr)
    tr = tr.loc[(tr.POPULATION > 0) & (tr.STATEFP.astype(int) <= 56)]   # 50 states + DC, no PR
    print(f"Census tracts: loaded {n0:,}, kept {len(tr):,} populated tracts in the 50 states and DC")
    pts = to_xyz(tr.LATITUDE.to_numpy(), tr.LONGITUDE.to_numpy())
    w = tr.POPULATION.to_numpy().astype(float)

    def wq(v, q):
        o = np.argsort(v)
        cw = np.cumsum(w[o]) / w.sum()
        return v[o][np.searchsorted(cw, q)]

    rows = []
    for a, b in CAPTIVE_PAIRS:
        da = miles(trees[a].query(pts, k=1)[0])
        db = miles(trees[b].query(pts, k=1)[0])
        gap = np.abs(da - db)
        rows.append({"chain_a": a, "chain_b": b, "tracts": len(w), "population": w.sum(),
                     "median_miles_to_a": wq(da, 0.5), "median_miles_to_b": wq(db, 0.5),
                     "share_closer_to_a": w[da < db].sum() / w.sum(),
                     "median_gap_miles": wq(gap, 0.5), "p75_gap_miles": wq(gap, 0.75),
                     "share_gap_over_5mi": w[gap > FAR_GAP].sum() / w.sum(),
                     "share_gap_under_1mi": w[gap < 1].sum() / w.sum(),
                     "median_round_trip_premium_usd": 2 * COST_PER_MILE * wq(gap, 0.5)})
    return pd.DataFrame(rows)


def own_spacing(chains, trees, xyz):
    """Distance from each store to the nearest other store of the same chain (miles)."""
    rows = []
    for c in chains.chain:
        d = miles(trees[c].query(xyz[c], k=2)[0][:, 1])
        rows.append({"chain": c, "stores": len(d), "median_miles_to_own": np.median(d),
                     "share_own_within_0.5": (d <= RADIUS).mean()})
    return pd.DataFrame(rows)


def figure(rl):
    """Observed vs expected co-location for every rival pair, against same-format non-rivals."""
    colors = {"big box": "#2a78d6", "small box": "#eb6834", "restaurant": "#1baf7a"}
    d = rl.loc[rl.radius_miles == RADIUS].copy()
    d["label"] = d.chain_a + " \u2192 " + d.chain_b
    riv = d.loc[d.rival].sort_values("ratio").reset_index(drop=True)
    non = d.loc[~d.rival]
    fig, ax = plt.subplots(figsize=(8, 12))
    for fmt, col in colors.items():
        sub = riv.loc[riv.format == fmt]
        lo = (sub.ratio - sub.null_low_95 / sub.null_mean_share).clip(lower=0)
        hi = (sub.null_high_95 / sub.null_mean_share - sub.ratio).clip(lower=0)
        ax.errorbar(sub.ratio, sub.index, fmt="o", ms=6, color=col, label=f"rival pair, {fmt}")
        ax.hlines(sub.index, sub.null_low_95 / sub.null_mean_share, sub.null_high_95 / sub.null_mean_share,
                  color="#bbbbbb", lw=3, zorder=0)
    jitter = np.random.default_rng(0).uniform(-0.3, 0.3, len(non))
    rows = {"big box": -2, "small box": -3, "restaurant": -4}
    for fmt, col in colors.items():
        m = (non.format == fmt).to_numpy()
        ax.scatter(non.ratio[m], rows[fmt] + jitter[m], s=9, color=col, alpha=0.45)
    ax.axvline(1, color="#444", lw=1, ls="--")
    ax.set_yticks(list(riv.index) + list(rows.values()))
    ax.set_yticklabels(list(riv.label) + [f"non-rival pairs, {f}" for f in rows], fontsize=8)
    ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1, 2, 4])
    ax.set_xticklabels(["0.25", "0.5", "1", "2", "4"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Share of A's stores with a B store within half a mile, divided by the share\n"
                  "expected if chains were assigned at random to sites of the same format (log scale)")
    ax.set_title("Small stores cluster with their rivals; big boxes keep their distance", fontsize=11)
    ax.legend(loc="center left", fontsize=8, frameon=False)
    ax.text(0.01, 0.995, "Grey bars: 95% range of 999 random shuffles", transform=ax.transAxes,
            fontsize=7, color="#555", va="top")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "colocation_ratios.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)
    hotelling_example()

    stores = pd.read_csv(RAW / "stores.csv")
    chains = pd.read_csv(RAW / "chains.csv")[["chain", "category", "format", "run", "kept"]]
    stores = stores.merge(chains[["chain", "category", "format"]], on="chain", how="left")
    print(f"Stores: loaded {len(stores):,} US locations for {stores.chain.nunique()} chains "
          f"(cleaning and drops are logged in data/raw/chains.csv)")
    counts = pd.read_csv(RAW / "chains.csv")
    total = {"chain": "All chains", "records": counts.records.sum(), "kept": counts.kept.sum()}
    pd.concat([counts, pd.DataFrame([total])]).to_csv(OUT / "store_counts.csv", index=False)
    xyz = {c: to_xyz(g.lat.to_numpy(), g.lon.to_numpy()) for c, g in stores.groupby("chain")}
    trees = {c: cKDTree(v) for c, v in xyz.items()}

    pairs = pair_table(stores, chains, trees, xyz)
    print(f"Ordered chain pairs: {len(pairs)} ({int(pairs.rival.sum())} rival, "
          f"{int((pairs.same_format & ~pairs.rival).sum())} same-format non-rival)")

    rl = pd.concat([random_labeling(stores, chains, r, rng) for r in RADII], ignore_index=True)
    rl = rl.merge(pairs[["chain_a", "chain_b", "rival", "category_a", "median_miles_to_b"]],
                  on=["chain_a", "chain_b"])
    rl.to_csv(OUT / "random_labeling_all_pairs.csv", index=False)

    main_rl = rl.loc[rl.radius_miles == RADIUS]
    rivals = main_rl.loc[main_rl.rival].merge(
        pairs[["chain_a", "chain_b", "n_a", "n_b"]], on=["chain_a", "chain_b"])
    rivals = rivals[["category_a", "chain_a", "chain_b", "n_a", "n_b", "observed_share",
                     "null_mean_share", "null_low_95", "null_high_95", "ratio", "z", "p_two_sided",
                     "median_miles_to_b"]].rename(columns={"category_a": "category"})
    rivals.sort_values(["category", "chain_a"]).to_csv(OUT / "rival_pairs.csv", index=False)

    rows = []
    for (fmt, riv), sub in rl.groupby(["format", "rival"]):
        for r, g in sub.groupby("radius_miles"):
            rows.append({"format": fmt, "group": "rival" if riv else "same format, not rival",
                         "radius_miles": r, "ordered_pairs": len(g), "median_ratio": g.ratio.median(),
                         "share_sig_above": ((g.p_two_sided < 0.05) & (g.ratio > 1)).mean(),
                         "share_sig_below": ((g.p_two_sided < 0.05) & (g.ratio < 1)).mean()})
    summary = pd.DataFrame(rows)
    summary.to_csv(OUT / "random_labeling_summary.csv", index=False)
    print(summary.loc[summary.radius_miles == RADIUS].to_string(index=False))

    reg = []
    for r in RADII:
        reg += ppml(pairs, r, "all 32 chains")
        reg += ppml(pairs, r, "all 32 chains", by_format=True)
    reg += ppml(pairs, RADIUS, "without banks", keep=(pairs.category_a != "bank") & (pairs.category_b != "bank"))
    reg += ppml(pairs, RADIUS, "same-format pairs only", keep=pairs.same_format, by_format=True)
    reg = pd.DataFrame(reg)
    reg.to_csv(OUT / "ppml_rival_effect.csv", index=False)
    print(reg[["sample", "term", "radius_miles", "ordered_pairs", "beta", "se_cluster", "p_value",
               "exp_beta"]].to_string(index=False))

    spacing = own_spacing(chains, trees, xyz)
    spacing.to_csv(OUT / "own_chain_spacing.csv", index=False)
    pairs.to_csv(OUT / "pair_distances.csv", index=False)
    cap = captive_customers(stores, trees)
    cap.to_csv(OUT / "captive_customers.csv", index=False)
    print(cap[["chain_a", "chain_b", "median_gap_miles", "share_gap_over_5mi", "median_round_trip_premium_usd"]].to_string(index=False))
    figure(rl)
    print("Wrote results/hotelling_example.csv, pair_distances.csv, random_labeling_all_pairs.csv, "
          "rival_pairs.csv, random_labeling_summary.csv, ppml_rival_effect.csv, own_chain_spacing.csv, "
          "store_counts.csv, captive_customers.csv, "
          "colocation_ratios.png")


if __name__ == "__main__":
    main()
