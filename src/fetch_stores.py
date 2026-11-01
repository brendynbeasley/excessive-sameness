"""Download US store locations for 32 national chains from All the Places and write one tidy file.

All the Places (alltheplaces.xyz, CC0) runs a scraper for each chain's own store locator every week
and publishes one GeoJSON file per chain. Some scrapers break in some weeks, so each chain is taken
from the most recent 2026 weekly run in which its count looked complete (CHAINS below). Raw GeoJSON
goes to data/raw/atp/ (ignored by git, about 200 MB); the cleaned extract, data/raw/stores.csv, is
committed so the analysis runs offline.

Usage (from the repository root):
    python src/fetch_stores.py
"""

import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ATP_DIR = ROOT / "data" / "raw" / "atp"
OUT = ROOT / "data" / "raw" / "stores.csv"
BASE = "https://alltheplaces-data.openaddresses.io/runs/{run}/output/{spider}.geojson"

# chain label: (spider, weekly run id, what it sells, store format)
# Run ids picked by reading each run's stats/_results.json and taking the latest run whose feature
# count matched the chain's stable count over 2026 (e.g. lowes_us returned 0 in most autumn runs).
CHAINS = {
    "Home Depot": ("home_depot", "2026-10-24-13-32-37", "home improvement", "big box"),
    "Lowe's": ("lowes_us", "2026-07-11-13-32-25", "home improvement", "big box"),
    "Menards": ("menards", "2026-10-17-13-32-31", "home improvement", "big box"),
    "Costco": ("costco_ca_gb_us", "2026-10-24-13-32-37", "warehouse club", "big box"),
    "Sam's Club": ("sams_club", "2026-10-10-13-32-41", "warehouse club", "big box"),
    "BJ's Wholesale": ("bjs_wholesale", "2026-10-03-13-32-35", "warehouse club", "big box"),
    "PetSmart": ("petsmart", "2026-10-24-13-32-37", "pet supplies", "big box"),
    "Petco": ("petco", "2026-10-24-13-32-37", "pet supplies", "big box"),
    "Target": ("target_us", "2026-10-24-13-32-37", "none", "big box"),
    "Kohl's": ("kohls_us", "2026-10-24-13-32-37", "none", "big box"),
    "Best Buy": ("best_buy", "2026-10-24-13-32-37", "none", "big box"),
    "CVS": ("cvs_us", "2026-08-29-13-32-18", "pharmacy", "small box"),
    "Walgreens": ("walgreens", "2026-10-10-13-32-41", "pharmacy", "small box"),
    "Dollar General": ("dollar_general", "2026-10-10-13-32-41", "dollar store", "small box"),
    "Family Dollar": ("family_dollar_us", "2026-10-24-13-32-37", "dollar store", "small box"),
    "Dollar Tree": ("dollar_tree_us", "2026-10-17-13-32-31", "dollar store", "small box"),
    "AutoZone": ("autozone", "2026-10-24-13-32-37", "auto parts", "small box"),
    "O'Reilly": ("oreilly_auto", "2026-10-24-13-32-37", "auto parts", "small box"),
    "Advance Auto Parts": ("advance_auto_parts_us", "2026-10-24-13-32-37", "auto parts", "small box"),
    "Chase": ("chase_us", "2026-10-24-13-32-37", "bank", "small box"),
    "Bank of America": ("bank_of_america", "2026-10-24-13-32-37", "bank", "small box"),
    "Wells Fargo": ("wells_fargo_us", "2026-10-24-13-32-37", "bank", "small box"),
    "McDonald's": ("mcdonalds", "2026-10-10-13-32-41", "burgers", "restaurant"),
    "Burger King": ("burger_king", "2026-10-17-13-32-31", "burgers", "restaurant"),
    "Wendy's": ("wendys", "2026-10-10-13-32-41", "burgers", "restaurant"),
    "KFC": ("kfc_us", "2026-10-24-13-32-37", "chicken", "restaurant"),
    "Popeyes": ("popeyes", "2026-10-24-13-32-37", "chicken", "restaurant"),
    "Chick-fil-A": ("chick_fil_a", "2026-10-24-13-32-37", "chicken", "restaurant"),
    "Starbucks": ("starbucks_us", "2026-10-10-13-32-41", "coffee", "restaurant"),
    "Dunkin'": ("dunkin_us", "2026-10-24-13-32-37", "coffee", "restaurant"),
    "Taco Bell": ("taco_bell_us", "2026-10-24-13-32-37", "none", "restaurant"),
    "Subway": ("subway_us", "2026-10-17-13-32-31", "none", "restaurant"),
}

# 50 states plus DC. Puerto Rico and the other territories are dropped.
STATES = set("""AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV
NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY""".split())
# Rough box around the 50 states, used only when a record has no state field.
LAT_RANGE, LON_RANGE = (18.5, 71.5), (-179.5, -66.5)
DEDUPE_DECIMALS = 4  # two records of one chain within ~11 m of each other are one store


def download(spider, run):
    """Fetch one chain's GeoJSON unless it is already on disk."""
    path = ATP_DIR / f"{spider}_{run[:10]}.geojson"
    if not path.exists():
        tmp = path.with_suffix(".part")
        req = urllib.request.Request(BASE.format(run=run, spider=spider),
                                     headers={"User-Agent": "Brendyn Beasley research"})
        with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
            f.write(r.read())
        tmp.rename(path)
        time.sleep(1)
    return json.loads(path.read_text())["features"]


def keep_reason(chain, props):
    """Return None to keep a record, or a short reason for dropping it."""
    country = props.get("addr:country")
    if country not in (None, "US"):
        return "outside US"
    if props.get("located_in"):
        return "store inside another store"
    if props.get("amenity") == "atm":
        return "ATM only"
    name = props.get("name") or ""
    if "Distribution Center" in name or "Temporarily Closed" in name:
        return "not an open store"
    if chain == "CVS" and "target" in (props.get("departments") or "").lower():
        return "store inside another store"
    if chain == "Walgreens" and props.get("brand") not in ("Walgreens", "Duane Reade"):
        return "specialty or partner pharmacy"
    if chain == "Starbucks" and props.get("ownership_type") != "CO":
        return "licensed counter (airport, grocery, Target)"
    return None


def main():
    ATP_DIR.mkdir(parents=True, exist_ok=True)
    rows, log = [], []
    for chain, (spider, run, category, fmt) in CHAINS.items():
        feats = download(spider, run)
        drops = {}
        kept = []
        for f in feats:
            props, geom = f.get("properties", {}), f.get("geometry")
            reason = keep_reason(chain, props)
            if reason is None and not geom:
                reason = "no coordinates"
            if reason is None:
                lon, lat = geom["coordinates"][:2]
                state = props.get("addr:state")
                state = state.upper().strip() if isinstance(state, str) else None
                if state not in STATES:
                    in_box = LAT_RANGE[0] < lat < LAT_RANGE[1] and LON_RANGE[0] < lon < LON_RANGE[1]
                    if state is not None or not in_box:
                        reason = "territory or bad state"
            if reason:
                drops[reason] = drops.get(reason, 0) + 1
                continue
            kept.append((chain, round(lat, 5), round(lon, 5), state or ""))
        df = pd.DataFrame(kept, columns=["chain", "lat", "lon", "state"])
        before = len(df)
        df = df.loc[~df[["lat", "lon"]].round(DEDUPE_DECIMALS).duplicated()]
        if before > len(df):
            drops["duplicate record"] = before - len(df)
        rows.append(df)
        log.append({"chain": chain, "spider": spider, "run": run[:10], "category": category,
                    "format": fmt, "records": len(feats), "kept": len(df),
                    **{f"dropped: {k}": v for k, v in drops.items()}})
        print(f"{chain:20s} {spider:22s} run {run[:10]}  records {len(feats):6d}  kept {len(df):6d}  "
              + ", ".join(f"{k} {v}" for k, v in drops.items()))
    stores = pd.concat(rows, ignore_index=True)
    stores.to_csv(OUT, index=False)
    chains = pd.DataFrame(log).fillna(0)
    chains.to_csv(ROOT / "data" / "raw" / "chains.csv", index=False)
    print(f"\nWrote {len(stores):,} stores for {stores.chain.nunique()} chains to data/raw/stores.csv")


if __name__ == "__main__":
    main()
