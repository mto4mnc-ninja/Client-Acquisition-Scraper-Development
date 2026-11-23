"""USAspending.gov: who actually won training contracts and for how much.

Official API, no key. Searches each category's keywords across FY2025-today
contracts, then re-scores locally to drop noise.
"""
import json, urllib.request, datetime as dt
from ..keywords import CATEGORIES, classify

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency", "Awarding Sub Agency",
          "Description", "Start Date", "End Date", "NAICS", "PSC", "generated_internal_id"]


def _post(body):
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def winners(start="2024-10-01", pages=2):
    end = dt.date.today().isoformat()
    seen = set()
    for cat, terms in CATEGORIES.items():
        for page in range(1, pages + 1):
            body = {"filters": {"time_period": [{"start_date": start, "end_date": end}],
                                "award_type_codes": ["A", "B", "C", "D"], "keywords": terms},
                    "fields": FIELDS, "sort": "Start Date", "order": "desc", "limit": 100, "page": page}
            try:
                res = _post(body)
            except Exception as e:  # keep going if one category fails
                print("usaspending error", cat, e)
                break
            for r in res.get("results", []):
                gid = r["generated_internal_id"]
                if gid in seen:
                    continue
                naics = (r.get("NAICS") or {}).get("code", "") if isinstance(r.get("NAICS"), dict) else ""
                psc = (r.get("PSC") or {}).get("code", "") if isinstance(r.get("PSC"), dict) else ""
                score, cats, _ = classify(r["Description"] or "", "", naics, psc)
                if score < 3:
                    continue
                seen.add(gid)
                yield {
                    "source": "USAspending", "award_date": r["Start Date"], "end_date": r["End Date"],
                    "agency": r["Awarding Agency"], "sub_agency": r["Awarding Sub Agency"],
                    "title": (r["Description"] or "")[:200], "winner": r["Recipient Name"],
                    "award_usd": round(r["Award Amount"] or 0), "award_number": r["Award ID"],
                    "naics": naics, "psc": psc,
                    "vehicle": "GSA Schedule order" if ("_GS" in gid or "_47Q" in gid) else
                               ("Order under agency IDV" if not gid.endswith("-NONE-_-NONE-") else "Standalone contract"),
                    "categories": "; ".join(cats), "score": score,
                    "url": "https://www.usaspending.gov/award/" + gid,
                }
            if not res.get("page_metadata", {}).get("hasNext"):
                break
