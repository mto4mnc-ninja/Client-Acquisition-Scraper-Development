# Opportunity Finder: US government training bids

Finds **open bids** and **past winners with prices** for training that can be delivered or subcontracted:
AI literacy / AI teaching, leadership, soft skills, HR, Excel / Microsoft 365, Power BI / data analytics,
MATLAB / technical software, and online / e-learning / course development.

## Sources

| Source | What it gives | How | Key needed? | Status (tested 2026-11-23) |
|---|---|---|---|---|
| **SAM.gov** | All federal notices: DoD / Dept of War, VA, DOT, State, Labor, DHS... | Official daily public extract (`sam.gov/data-services`, ~225 MB CSV) | No | ✅ works |
| **SAM.gov award notices** | Who won, award $ | Same file, `Type = Award Notice` | No | ✅ works |
| **USAspending.gov** | Every federal training contract since FY2025: winner, $, agency, GSA vs open market | Official API | No | ✅ works |
| **Grants.gov** | Training grants (mostly US nonprofits only) | Official API | No | ✅ works |
| **Texas ESBD** | All state agencies, universities, cities, ISDs | Public JSON behind txsmartbuy.gov/esbd | No | ✅ works |
| **New York Contract Reporter** | NY state agencies, SUNY/CUNY, authorities | Public search list (details need free login) | No | ✅ works |
| **Washington DC OCP** | All open DC government solicitations | Public JSON API | No | ✅ works |
| **California Cal eProcure** | CA state bids | Blocks automated access (HTTP 403) | - | ❌ manual: free alerts |
| **Virginia eVA** | VA state and local bids | Blocks automated access | - | ❌ manual: free alerts |

California and Virginia are **not** scraped. Their sites refuse automated clients, and getting around that would break their terms of use. Instead, register free as a vendor and turn on email alerts for the codes below:

- **Cal eProcure:** caleprocure.ca.gov → Register → UNSPSC 86101700, 86111600, 86132000 (vocational, adult education, management training)
- **Virginia eVA:** eva.virginia.gov → Register → NIGP 924 (Educational & Training Services) and 918 (Consulting)
- **DC, NY and Texas** also offer free alerts, which are worth turning on in addition to this tool.

## Run

```bash
pip install -r opportunity_finder/requirements.txt   # standard library only; file kept for clarity
python -m opportunity_finder.run                    # all sources (~10-20 min; Texas is the slow one)
python -m opportunity_finder.run --skip texas        # quicker run
```

Outputs are written to `opportunity_finder/output/`:

- `opportunities_<date>.csv`: open bids, ranked. Columns include:
  - `core_fit`
  - `score`
  - `deadline`
  - `open_to_foreign_firm`
  - `contact_email`
  - `url`
- `winners_prices_<date>.csv`: who won training work, for how much, and through which vehicle (GSA Schedule order, standalone contract, or order under an agency IDV)
- `digest_<date>.md`: one-page summary

## Daily automation

`.github/workflows/training-opportunities.yml` runs Mon–Fri at 11:17 UTC and commits the outputs. GitHub only runs scheduled workflows that are on the **default branch**, so merge this file into `main` to switch it on. To run it by hand: Actions tab → "Run workflow".

## Columns to read first

- **`open_to_foreign_firm`**
  - `likely`: no small-business set-aside, so a non-US firm with a SAM registration (UEI + NCAGE code) can bid.
  - `no (set-aside)`: only US small businesses can be the prime contractor, so the route is **subcontracting to whoever wins**.
- **`notice_type`**
  - *Sources Sought* and *RFI* notices are the best time to get in. Answering them is free and shapes the later bid.
- **`core_fit`**
  - `yes`: the title or description names AI, leadership, soft skills, HR, Excel, Power BI or MATLAB.
  - `generic training`: still training, but needs a manual check.

## Tuning

Edit `keywords.py`. Add phrases to a category, or add words to `NEGATIVE` to suppress noise.
