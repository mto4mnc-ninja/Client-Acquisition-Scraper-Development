"""State and local portals.

Automated (public, no login):
  - Texas ESBD          www.txsmartbuy.gov/esbd          (public JSON behind the search page)
  - New York Contract Reporter  www.nyscr.ny.gov/Ads/Search  (list is public; details need free login)
  - Washington DC OCP   contracts.ocp.dc.gov             (public JSON)

Not automated, on purpose: California Cal eProcure and Virginia eVA block
automated clients (HTTP 403 / empty 202). Use their free vendor e-mail alerts
instead (see README).
"""
import datetime as dt, html, json, re, urllib.parse, urllib.request
from ..keywords import classify

UA = {"User-Agent": "Mozilla/5.0 (opportunity-finder)"}
SEARCH_WORDS = ["training", "leadership", "artificial intelligence", "e-learning", "curriculum",
                "power bi", "excel", "matlab", "coaching", "professional development"]


def _get(url, data=None, headers=None):
    h = dict(UA, **(headers or {}))
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


def _row(jur, agency, title, sol, posted, deadline, url, contact="", email="", note=""):
    score, cats, terms = classify(title)
    return {"source": jur + " portal", "jurisdiction": jur, "agency": agency, "sub_agency": "", "office": "",
            "focus_dept": "", "title": title, "solicitation_no": sol, "notice_type": note or "Solicitation",
            "posted": posted, "deadline": deadline, "naics": "", "psc": "", "set_aside": "",
            "open_to_foreign_firm": "check solicitation", "place": jur, "contact": contact,
            "contact_email": email, "categories": "; ".join(cats), "matched_terms": "; ".join(terms),
            "score": score, "url": url}


# ---------------- Washington DC ----------------
def dc():
    body = {"FilterBy": [{"id": 0, "name": "Type", "value": 0}, {"id": 1, "name": "Status", "value": "Open"},
                         {"id": 2, "name": "DatesOption", "value": 2}], "OrderBy": []}
    raw = _get("https://contracts.ocp.dc.gov/api/solicitations/search", json.dumps(body).encode(),
               {"Content-Type": "application/json"})
    for s in json.loads(raw).get("results", []):
        sp = s.get("specialist") or {}
        yield _row("Washington DC", ", ".join(s.get("agencyNames") or []), s["title"], s["solicitationNumber"],
                   "", s.get("closingDate", ""), "https://contracts.ocp.dc.gov/solicitations/search",
                   sp.get("name", ""), sp.get("email", ""))


# ---------------- New York ----------------
_NY = re.compile(r"Title: (.+?) (?:Note: .+? )?CR#: (\d+) Agency: (.+?) (?:Division: .+? )?Issue date: (\S+) Due date: (\S+)")


def ny(max_pages=4):
    seen = set()
    for w in SEARCH_WORDS:
        for page in range(1, max_pages + 1):
            q = urllib.parse.urlencode({"Keyword": w, "DateFilter": "AllTime", "Page": page, "PageSize": 50})
            t = _get("https://www.nyscr.ny.gov/Ads/Search?" + q)
            s = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
            found = _NY.findall(s)
            for title, cr, agency, issued, due in found:
                if cr in seen:
                    continue
                seen.add(cr)
                yield _row("New York", agency, title, "CR# " + cr, issued, due,
                           "https://www.nyscr.ny.gov/Ads/Search?Keyword=" + cr)
            if len(found) < 10:
                break


# ---------------- Texas ESBD (public JSON used by the site) ----------------
TX_API = "https://www.txsmartbuy.gov/app/extensions/CPA/CPAMain/1.0.0/services/ESBD.Service.ss?c=852252&n=2"
TX_OPEN = {"Posted", "Addendum Posted"}


def texas(max_pages=None, lookback_days=150):
    """Walk the newest-first list of all Texas state/local solicitations; keep open training ones.
    NIGP class 924 = Educational & Training Services (counted as training by code)."""
    import os
    max_pages = max_pages or int(os.environ.get("TX_PAGES", "200"))  # ~24 rows/page, newest first
    cutoff = dt.date.today() - dt.timedelta(days=lookback_days)
    for page in range(1, max_pages + 1):
        body = json.dumps({"lines": [], "page": page, "urlRoot": "esbd"}).encode()
        lines = json.loads(_get(TX_API, body, {"Content-Type": "application/json"})).get("lines", [])
        if not lines:
            break
        oldest = None
        for l in lines:
            try:
                oldest = dt.datetime.strptime(l["postingDate"], "%m/%d/%Y").date()
            except ValueError:
                pass
            if l["statusName"] not in TX_OPEN:
                continue
            nigp = l.get("nigpCodes", "")
            r = _row("Texas", l["agencyName"], l["title"], l["solicitationId"], l["postingDate"],
                     l["responseDue"], f"https://www.txsmartbuy.gov/esbd/{l['solicitationId']}")
            if re.search(r"(^|\n)924\d\d-", nigp):
                r["score"] += 3
                r["categories"] = r["categories"] or "Training (by NIGP 924)"
            r["naics"] = "NIGP: " + "; ".join(x.split("-")[0] for x in nigp.split(";") if x.strip())
            yield r
