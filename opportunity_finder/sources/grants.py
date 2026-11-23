"""Grants.gov (official API, no key). Mostly for US nonprofits/schools; kept for partner leads."""
import json, urllib.request
from ..keywords import classify

API = "https://api.grants.gov/v1/api/search2"
QUERIES = ["artificial intelligence training", "AI literacy", "leadership training", "workforce training",
           "digital skills", "data literacy", "professional development training"]


def grants():
    seen = set()
    for q in QUERIES:
        body = json.dumps({"keyword": q, "oppStatuses": "forecasted|posted", "rows": 50}).encode()
        req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            hits = json.load(r)["data"].get("oppHits", [])
        for h in hits:
            if h["id"] in seen:
                continue
            seen.add(h["id"])
            score, cats, terms = classify(h["title"])
            if score < 3:
                continue
            yield {"source": "Grants.gov", "jurisdiction": "Federal grant", "agency": h.get("agency", h["agencyCode"]),
                   "sub_agency": "", "office": "", "focus_dept": "", "title": h["title"], "solicitation_no": h["number"],
                   "notice_type": "Grant (" + h["oppStatus"] + ")", "posted": h.get("openDate", ""),
                   "deadline": h.get("closeDate", ""), "naics": "", "psc": "", "set_aside": "",
                   "open_to_foreign_firm": "usually no - partner with US nonprofit", "place": "",
                   "contact": "", "contact_email": "", "categories": "; ".join(cats),
                   "matched_terms": "; ".join(terms), "score": score,
                   "url": f"https://www.grants.gov/search-results-detail/{h['id']}"}
