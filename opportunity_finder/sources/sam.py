"""SAM.gov contract opportunities.

Default: the official public daily extract (no API key) published by GSA at
sam.gov/data-services (Contract Opportunities > datagov). ~225 MB CSV of every
active notice. If SAM_API_KEY is set, nothing else changes: the extract is still
the source, because it covers all notice types in one file.

Two outputs:
  open_opportunities()  - solicitations / sources sought / presolicitations
  award_notices()       - Award Notice rows = who won and at what price
"""
import csv, datetime as dt, os, urllib.request
from ..keywords import classify

URL = ("https://sam.gov/api/prod/fileextractservices/v1/api/download/"
       "Contract%20Opportunities/datagov/ContractOpportunitiesFullCSV.csv?privacy=Public")

OPEN_TYPES = {"Solicitation", "Combined Synopsis/Solicitation", "Presolicitation",
              "Sources Sought", "Special Notice"}
OPEN_TO_ALL = {"", "NONE"}  # no small-business set-aside => foreign firms may bid
FOCUS_DEPTS = {
    "DEPT OF DEFENSE": "Defense / War", "VETERANS AFFAIRS, DEPARTMENT OF": "Veterans Affairs",
    "TRANSPORTATION, DEPARTMENT OF": "Transportation", "STATE, DEPARTMENT OF": "State (overseas posts)",
    "LABOR, DEPARTMENT OF": "Labor", "HOMELAND SECURITY, DEPARTMENT OF": "Homeland Security",
}


def download(path):
    if os.path.exists(path) and dt.datetime.now().timestamp() - os.path.getmtime(path) < 20 * 3600:
        return path
    req = urllib.request.Request(URL, headers={"User-Agent": "opportunity-finder/1.0"})
    with urllib.request.urlopen(req, timeout=900) as r, open(path, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    return path


def _rows(path):
    csv.field_size_limit(10 ** 9)
    with open(path, encoding="latin-1", newline="") as f:
        yield from csv.DictReader(f)


def _deadline(s):
    try:
        return dt.datetime.fromisoformat(s[:19]).date()
    except Exception:
        return None


def open_opportunities(path, min_score=3):
    today = dt.date.today()
    for r in _rows(path):
        if r["Type"] not in OPEN_TYPES:
            continue
        dl = _deadline(r["ResponseDeadLine"])
        if dl and dl < today:
            continue
        score, cats, terms = classify(r["Title"], r["Description"], r["NaicsCode"], r["ClassificationCode"])
        if score < min_score:
            continue
        sa = r["SetASideCode"].strip('[]"')
        yield {
            "source": "SAM.gov", "jurisdiction": "Federal",
            "agency": r["Department/Ind.Agency"], "sub_agency": r["Sub-Tier"], "office": r["Office"],
            "focus_dept": FOCUS_DEPTS.get(r["Department/Ind.Agency"], ""),
            "title": r["Title"], "solicitation_no": r["Sol#"], "notice_type": r["Type"],
            "posted": r["PostedDate"][:10], "deadline": str(dl or ""),
            "naics": r["NaicsCode"], "psc": r["ClassificationCode"],
            "set_aside": r["SetASide"] or "None",
            "open_to_foreign_firm": "likely" if sa in OPEN_TO_ALL else "no (set-aside) - subcontract only",
            "place": ", ".join(x for x in [r["PopCity"], r["PopState"], r["PopCountry"]] if x),
            "contact": r["PrimaryContactFullname"], "contact_email": r["PrimaryContactEmail"],
            "categories": "; ".join(cats), "matched_terms": "; ".join(terms), "score": score,
            "url": r["Link"],
        }


def award_notices(path, min_score=3):
    for r in _rows(path):
        if r["Type"] != "Award Notice":
            continue
        score, cats, terms = classify(r["Title"], r["Description"], r["NaicsCode"], r["ClassificationCode"])
        if score < min_score:
            continue
        yield {
            "source": "SAM.gov award notice", "award_date": r["AwardDate"][:10],
            "agency": r["Department/Ind.Agency"], "sub_agency": r["Sub-Tier"], "office": r["Office"],
            "title": r["Title"], "winner": r["Awardee"], "award_usd": r["Award$"],
            "award_number": r["AwardNumber"], "naics": r["NaicsCode"], "psc": r["ClassificationCode"],
            "set_aside": r["SetASide"] or "None", "categories": "; ".join(cats), "score": score,
            "url": r["Link"],
        }
