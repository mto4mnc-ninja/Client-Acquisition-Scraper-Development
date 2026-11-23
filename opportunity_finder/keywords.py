"""Training categories, search terms and scoring used by every source.

Phrases are matched case-insensitively against title (weight 3) and
description (weight 1). Bare words such as "training" are deliberately NOT
used: on their own they match ammunition, aircraft simulators and similar
noise.
"""
import re

CATEGORIES = {
    "AI literacy / AI teaching": [
        "artificial intelligence training", "ai training", "ai literacy", "ai education",
        "ai upskilling", "ai workforce", "ai fluency", "ai readiness", "ai course",
        "generative ai training", "genai training", "responsible ai training",
        "prompt engineering", "chatgpt training", "copilot training", "ai academy",
        "machine learning training", "ai curriculum", "ai skills",
    ],
    "Leadership": [
        "leadership training", "leadership development", "leadership program",
        "executive coaching", "executive development", "supervisory training",
        "supervisor training", "management training", "management development",
        "leadership course", "leadership academy", "leadership workshop",
    ],
    "Soft skills": [
        "soft skills", "communication training", "communication skills",
        "emotional intelligence", "conflict resolution training", "team building",
        "customer service training", "presentation skills", "writing training",
        "time management training", "professional development training",
        "interpersonal skills", "negotiation training",
    ],
    "HR training": [
        "human resources training", "hr training", "eeo training",
        "harassment prevention", "sexual harassment training", "onboarding training",
        "performance management training", "workplace training", "employee training",
        "staff training", "workforce training", "workforce development training",
    ],
    "Excel / Microsoft 365": [
        "excel training", "microsoft excel", "microsoft office training",
        "microsoft 365 training", "office 365 training", "m365 training",
        "sharepoint training", "microsoft teams training", "computer skills training",
    ],
    "Power BI / data analytics": [
        "power bi", "powerbi", "tableau training", "data analytics training",
        "data literacy", "data analysis training", "sql training", "python training",
        "data science training", "analytics training",
    ],
    "MATLAB / technical software": [
        "matlab", "simulink", "labview", "autocad training", "solidworks training",
        "arcgis training", "gis training", "software training", "it training",
        "cybersecurity training", "cyber awareness training",
    ],
    "Online / digital training": [
        "e-learning", "elearning", "online training", "virtual training",
        "web-based training", "computer-based training", "instructor-led",
        "learning management system", "course development", "curriculum development",
        "instructional design", "instructional systems design", "training development",
        "digital skills", "digital literacy", "training services", "training support services",
        "training program", "training course", "training courses",
    ],
}

# Federal codes that are training by definition.
TRAINING_NAICS = {"611430", "611420", "611710", "611699", "611519", "611310", "611691"}
TRAINING_PSC = {"U001", "U004", "U005", "U006", "U008", "U009", "U010", "U012", "U099", "U"}

# Words that indicate the notice is about buying a thing, not training services.
NEGATIVE = [
    "ammunition", "simulator", "flight training device", "aircraft", "vehicle",
    "construction", "repair", "roof", "hvac", "janitorial", "food service",
    "medical equipment", "spare parts", "uniform", "furniture", "firearm",
    # tactical / physical training: real training, but not this business's lane
    "tactics", "tactical", "weapons", "jump", "parachute", "aviation", "flight", "mariner",
    "confined space", "firefighting", "tccc", "combat", "diving", "range services", "athletic",
    "gulfstream", "proctoring", "tutoring",
]
CORE = [c for c in CATEGORIES if c != "Online / digital training"]

_COMPILED = {c: [re.compile(r"\b" + re.escape(t) + r"\b", re.I) for t in ts] for c, ts in CATEGORIES.items()}
_NEG = [re.compile(r"\b" + re.escape(t) + r"\b", re.I) for t in NEGATIVE]


def classify(title: str, description: str = "", naics: str = "", psc: str = ""):
    """Return (score, [categories], matched_terms). score 0 means not relevant."""
    title = title or ""
    description = (description or "")[:20000]
    score, cats, terms = 0, [], []
    for cat, pats in _COMPILED.items():
        hit = False
        for p in pats:
            if p.search(title):
                score += 3; hit = True; terms.append(p.pattern)
            elif description and p.search(description):
                score += 1; hit = True; terms.append(p.pattern)
        if hit:
            cats.append(cat)
    code_hit = (naics or "")[:6] in TRAINING_NAICS or (psc or "").upper() in TRAINING_PSC
    if code_hit:
        score += 3
    core_in_title = any(p.search(title) for c in CORE for p in _COMPILED[c])
    if any(p.search(title) for p in _NEG) and not core_in_title:
        score -= 4
    if not cats and code_hit:
        cats.append("Training (by NAICS/PSC code)")
    if core_in_title:
        score += 2  # boost: the title itself names AI/leadership/HR/Excel/Power BI/MATLAB etc.
    terms = sorted({re.sub(r"\\b|\\", "", t) for t in terms})
    return max(score, 0), cats, terms


# Rough subcontract/partner fit, highest first. AI literacy is ranked first on purpose.
CATEGORY_PRIORITY = list(CATEGORIES.keys())
