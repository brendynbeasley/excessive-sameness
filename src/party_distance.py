"""Hotelling's political example on roll-call data: did the two parties keep converging after 1929?

Hotelling (1929, p. 54) wrote that Republicans and Democrats each strive "to make its platform as
much like the other's as possible" and that real differences "fade gradually with time." This
script measures the distance between the parties in Congress with DW-NOMINATE first-dimension
scores from Voteview (Lewis, Poole, Rosenthal et al.), for every House and Senate from the 46th
Congress (1879) to the 119th (2025-27), and tests for the convergence Hotelling predicted.

Usage (from the repository root):
    python src/party_distance.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

FIRST_CONGRESS = 46      # 1879: first Congress after Reconstruction, two-party Democrat/Republican era
HOTELLING = 70           # 70th Congress, 1927-29, sitting when the paper appeared in March 1929
TURN = 95                # last Congress of the first half of the post-1929 sample (1977-79)
PARTIES = {100: "Democrat", 200: "Republican"}
HAC_LAGS = 4             # Newey-West lags (eight years) for the trend regressions


def start_year(congress):
    return 1789 + 2 * (congress - 1)


def trend(df, lo, hi):
    """OLS of the median gap on Congress number, Newey-West errors; slope reported per decade."""
    d = df.loc[(df.congress >= lo) & (df.congress <= hi)]
    X = sm.add_constant(d.congress.astype(float))
    fit = sm.OLS(d.gap.to_numpy(), X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    b, se = fit.params.iloc[1] * 5, fit.bse.iloc[1] * 5    # five Congresses = ten years
    return {"from": start_year(lo), "to": start_year(hi) + 2, "congresses": len(d),
            "slope_per_decade": b, "se_hac": se, "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se,
            "p_value": fit.pvalues.iloc[1]}


def main():
    OUT.mkdir(exist_ok=True)
    m = pd.read_csv(RAW / "HSall_members.csv.gz")
    n0 = len(m)
    m = m.loc[m.chamber.isin(["House", "Senate"]) & (m.congress >= FIRST_CONGRESS)]
    n1 = len(m)
    m = m.loc[m.party_code.isin(PARTIES)]
    n2 = len(m)
    m = m.dropna(subset=["nominate_dim1"])
    print(f"Voteview members: loaded {n0:,} rows; {n1:,} House/Senate rows from Congress "
          f"{FIRST_CONGRESS} on; {n2:,} Democrats or Republicans; {len(m):,} with a DW-NOMINATE score "
          f"(dropped {n0 - n1:,} earlier or presidential rows, {n1 - n2:,} third-party, {n2 - len(m):,} unscored)")
    m["party"] = m.party_code.map(PARTIES)

    rows = []
    for (cong, ch), g in m.groupby(["congress", "chamber"]):
        d, r = g.loc[g.party == "Democrat"], g.loc[g.party == "Republican"]
        right_dem = d.loc[d.nominate_dim1.idxmax()]
        left_rep = r.loc[r.nominate_dim1.idxmin()]
        rows.append({"congress": cong, "chamber": ch, "start_year": start_year(cong),
                     "n_dem": len(d), "n_rep": len(r),
                     "dem_median": d.nominate_dim1.median(), "rep_median": r.nominate_dim1.median(),
                     "gap": r.nominate_dim1.median() - d.nominate_dim1.median(),
                     "dems_right_of_most_liberal_rep": int((d.nominate_dim1 > left_rep.nominate_dim1).sum()),
                     "reps_left_of_most_conservative_dem": int((r.nominate_dim1 < right_dem.nominate_dim1).sum()),
                     "most_conservative_dem": right_dem.bioname, "most_conservative_dem_score": right_dem.nominate_dim1,
                     "most_liberal_rep": left_rep.bioname, "most_liberal_rep_score": left_rep.nominate_dim1})
    gaps = pd.DataFrame(rows)
    gaps["overlap_members"] = gaps.dems_right_of_most_liberal_rep + gaps.reps_left_of_most_conservative_dem
    gaps.to_csv(OUT / "party_gap_by_congress.csv", index=False)

    tests = []
    last = int(gaps.congress.max())
    for ch in ["House", "Senate"]:
        g = gaps.loc[gaps.chamber == ch]
        for lo, hi in [(HOTELLING + 1, last), (HOTELLING + 1, TURN), (TURN + 1, last)]:
            tests.append({"chamber": ch, **trend(g, lo, hi)})
    tests = pd.DataFrame(tests)
    tests.to_csv(OUT / "party_gap_trends.csv", index=False)

    key = gaps.loc[gaps.congress.isin([HOTELLING, TURN, last])]
    key = key.assign(min_gap_year=np.nan)
    for ch in ["House", "Senate"]:
        g = gaps.loc[(gaps.chamber == ch) & (gaps.congress > HOTELLING)]
        low = g.loc[g.gap.idxmin()]
        key = pd.concat([key, low.to_frame().T.assign(min_gap_year=low.start_year)])
    key.to_csv(OUT / "party_gap_key_congresses.csv", index=False)
    last_overlap = (gaps.loc[gaps.overlap_members > 0].groupby("chamber")
                    .agg(last_congress_with_overlap=("congress", "max"), start_year=("start_year", "max")))
    last_overlap.reset_index().to_csv(OUT / "party_overlap_last.csv", index=False)
    print(last_overlap.to_string())
    print(key[["chamber", "congress", "start_year", "dem_median", "rep_median", "gap", "overlap_members",
               "most_conservative_dem", "most_liberal_rep"]].to_string(index=False))
    print(tests.to_string(index=False))

    fig, ax = plt.subplots(figsize=(9, 4.8))
    for ch, ls in [("House", "-"), ("Senate", ":")]:
        g = gaps.loc[gaps.chamber == ch]
        ax.plot(g.start_year, g.rep_median, ls, color="#b22222", label=f"Republican median, {ch}")
        ax.plot(g.start_year, g.dem_median, ls, color="#1f4e8c", label=f"Democratic median, {ch}")
    ax.axvline(1929, color="#444", lw=1, ls="--")
    ax.text(1930, 0.62, "Hotelling writes,\n1929", fontsize=8, va="top")
    ax.axhline(0, color="#999", lw=0.6)
    ax.set_ylabel("DW-NOMINATE first dimension\n(liberal ← 0 → conservative)")
    ax.set_title("Party medians in Congress, 1879–2027")
    ax.legend(fontsize=7, ncol=2, frameon=False, loc="center right")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "party_medians.png", dpi=150)
    plt.close(fig)
    print("Wrote results/party_gap_by_congress.csv, party_gap_trends.csv, party_gap_key_congresses.csv, "
          "party_overlap_last.csv, party_medians.png")


if __name__ == "__main__":
    main()
