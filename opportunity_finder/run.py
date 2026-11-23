"""Run every source and write dated CSVs + a markdown digest.

    python -m opportunity_finder.run                 # all sources
    python -m opportunity_finder.run --skip texas    # skip a source

Outputs (in opportunity_finder/output/):
    opportunities_<date>.csv   open bids, ranked
    winners_prices_<date>.csv  who won training work and for how much
    digest_<date>.md           short human summary
"""
import argparse, csv, datetime as dt, os, re, statistics, traceback
from collections import Counter
from .sources import sam, usaspending, states, grants
from .keywords import CORE

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "output")
CACHE = os.environ.get("OF_CACHE", os.path.join(HERE, ".cache"))


def write(path, rows):
    if not rows:
        return
    keys = list(rows[0].keys())
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip", nargs="*", default=[])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    today = dt.date.today().isoformat()
    opps, wins, status = [], [], {}

    def run(name, fn, bucket):
        if name in a.skip:
            status[name] = "skipped"
            return
        try:
            rows = list(fn())
            bucket.extend(rows)
            status[name] = f"ok ({len(rows)} rows)"
        except Exception as e:
            traceback.print_exc()
            status[name] = f"FAILED: {e}"

    sam_path = None
    if "sam" not in a.skip:
        try:
            sam_path = sam.download(os.path.join(CACHE, "sam_full.csv"))
        except Exception as e:
            status["sam"] = f"FAILED download: {e}"
    if sam_path:
        run("sam", lambda: sam.open_opportunities(sam_path), opps)
        run("sam_awards", lambda: sam.award_notices(sam_path), wins)
    run("usaspending", usaspending.winners, wins)
    run("grants", grants.grants, opps)
    run("dc", states.dc, opps)
    run("ny", states.ny, opps)
    run("texas", states.texas, opps)

    # state portals return everything for a broad word; keep only relevant
    opps = [o for o in opps if o["score"] >= 3]
    # one row per solicitation: SAM repeats a notice for every amendment
    best = {}
    for o in sorted(opps, key=lambda o: o["posted"] or "", reverse=True):
        key = (o["source"], (o["solicitation_no"] or o["title"]).strip().upper())
        best.setdefault(key, o)
    opps = list(best.values())
    for o in opps:
        o["core_fit"] = "yes" if any(c in CORE for c in o["categories"].split("; ")) else "generic training"
    opps.sort(key=lambda o: (o["core_fit"] != "yes", -o["score"], o["deadline"] or "9999"))
    wins.sort(key=lambda w: w.get("award_date") or "", reverse=True)
    lic = re.compile(r"licen[sc]|subscription|renewal|maintenance|software|seats", re.I)
    trn = re.compile(r"train|course|class|instruct|coach|workshop|curriculum|learning", re.I)
    for w in wins:
        t = w.get("title") or ""
        w["kind"] = "software license (not training)" if lic.search(t) and not trn.search(t) else "training / service"
    write(os.path.join(OUT, f"opportunities_{today}.csv"), opps)
    write(os.path.join(OUT, f"winners_prices_{today}.csv"), wins)

    # digest
    L = [f"# Training opportunities digest - {today}", "", "## Source status", ""]
    L += [f"- **{k}**: {v}" for k, v in status.items()]
    L += ["", "## Open opportunities by category", ""]
    cc = Counter(c for o in opps for c in o["categories"].split("; ") if c)
    L += [f"- {c}: {n}" for c, n in cc.most_common()]
    L += ["", "## Top 40 open opportunities (core fit first)", "", "| Fit | Score | Source | Agency | Title | Type | Deadline | Foreign firm? |", "|---|---|---|---|---|---|---|---|"]
    for o in opps[:40]:
        L.append(f"| {o['core_fit']} | {o['score']} | {o['source']} | {o['agency'][:35]} | [{o['title'][:80]}]({o['url']}) | {o['notice_type'][:20]} | {o['deadline']} | {o['open_to_foreign_firm']} |")
    amts = []
    for w in [w for w in wins if w["kind"] == "training / service"]:
        try:
            v = float(str(w["award_usd"]).replace("$", "").replace(",", ""))
            if v > 0:
                amts.append(v)
        except ValueError:
            pass
    L += ["", "## Who wins and at what price", ""]
    if amts:
        L.append(f"- {len(amts)} priced training/service awards (software licenses excluded); median ${statistics.median(amts):,.0f}; "
                 f"25th pct ${statistics.quantiles(amts, n=4)[0]:,.0f}; 75th pct ${statistics.quantiles(amts, n=4)[2]:,.0f}")
    top = Counter(w["winner"] for w in wins if w.get("winner") and w["kind"] == "training / service").most_common(20)
    L += ["", "| Vendor (partner target) | # training awards |", "|---|---|"] + [f"| {v} | {n} |" for v, n in top]
    with open(os.path.join(OUT, f"digest_{today}.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
