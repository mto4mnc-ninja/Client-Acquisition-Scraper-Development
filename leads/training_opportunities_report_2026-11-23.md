# Training Opportunities: Federal + State (pulled 2026-11-23)

The data was pulled live from official sources by `opportunity_finder/`. The full ranked lists are in `opportunity_finder/output/`:
- `opportunities_2026-11-23.csv`
- `winners_prices_2026-11-23.csv`
- `digest_2026-11-23.md`

## A. Open opportunities that fit (act on these first)

| # | Opportunity | Buyer | Type | Due | Set-aside | Contact | Link |
|---|---|---|---|---|---|---|---|
| 1 | **AI Training for the Technology Acquisition Center (TAC)** | Veterans Affairs | Sources Sought | **2026-11-27** | None (open) | meryl.czaplinski@va.gov | [SAM](https://sam.gov/workspace/contract/opp/602a74b031b14846af4452133564601d/view) |
| 2 | **Leadership Culture and Soft Skills Development Program**, NAVSUP Fleet Logistics Center Sigonella | Navy (Dept of War) | Sources Sought | 2026-12-04 | None | dana.m.rains.ln@us.navy.mil | [SAM](https://sam.gov/workspace/contract/opp/c27607e2351d4cd4b7b19fc79768d545/view) |
| 3 | **USPTO PTA transformation** (leadership / change management) | Commerce / USPTO | RFI | 2026-12-04 | None | Roy.Pitman@uspto.gov | [SAM](https://sam.gov/workspace/contract/opp/907a73f90cc2453c88c105a7cb5c57b8/view) |
| 4 | **MATLAB Training** | Army | Presolicitation | not set yet | None | julian.m.dileo.civ@army.mil | [SAM](https://sam.gov/workspace/contract/opp/3678273dca3b4a1c8e9d64e8210290fb/view) |
| 5 | **Instructional Systems Design Services** | USDA | Sources Sought | 2026-12-01 | None | kathleen.melby@usda.gov | [SAM](https://sam.gov/workspace/contract/opp/1599eff1256d44d3aeb2e1d70e933f41/view) |
| 6 | **Leadership Development Program Services** | Army Corps of Engineers | Solicitation | 2026-12-04 | **SDVOSB only** | austin.anderson@usace.army.mil | [SAM](https://sam.gov/workspace/contract/opp/995de60dcb9f44e3a1eebfaf72bf4e21/view) |
| 7 | **AI Readiness MVP** (data/AI governance) | Air Force AFOTEC | Sources Sought | 2026-11-24 | None | rafaela.kovacs@us.af.mil | [SAM](https://sam.gov/workspace/contract/opp/d826907afb7247e091c636869b85245a/view) |
| 8 | **CSO: Human Capital**, 338 Enterprise Sourcing Squadron | Air Force | Commercial Solutions Opening | open until 2030 | None | sasha.stewart@us.af.mil | [SAM](https://sam.gov/workspace/contract/opp/73bf63702cdb4b80b1702fc3f6786837/view) |
| 9 | MilLife Learning Management System support | Navy | Solicitation | 2026-12-21 | None | kelly.l.cline7.naf@us.navy.mil | [SAM](https://sam.gov/workspace/contract/opp/1489759659dd478ab2af56447c6974ae/view) |
| 10 | Navy Alternative Dispute Resolution program support (conflict resolution) | Navy | Sources Sought | 2026-12-01 | None | alexsis.d.morgan.civ@us.navy.mil | [SAM](https://sam.gov/workspace/contract/opp/28ace8aaf4a945ed965ba72307f97d81/view) |
| 11 | Strategic Plan + **Executive Coaching** | SUNY (New York) | Solicitation | 2026-12-08 | - | free NYSCR login | [NYSCR CR# 2140571](https://www.nyscr.ny.gov/Ads/Search?Keyword=2140571) |
| 12 | Faith-Based **Leadership Training** RFI | NYS OASAS | RFI | 2026-12-15 | - | free NYSCR login | [NYSCR CR# 2140459](https://www.nyscr.ny.gov/Ads/Search?Keyword=2140459) |
| 13 | **Leadership Development Services** (open-ended vendor list) | NYC Dept of Education | Standing solicitation | open | - | free NYSCR login | [NYSCR CR# 2067869](https://www.nyscr.ny.gov/Ads/Search?Keyword=2067869) |
| 14 | Contracted Educational + **Professional Development** Services | Cypress-Fairbanks ISD (Texas) | Solicitation | 2027-06-30 | - | via ESBD | [ESBD](https://www.txsmartbuy.gov/esbd) |
| 15 | Ready Workforce Training Pipeline | Workforce Solutions Borderplex (Texas) | Solicitation | 2030-09-30 | - | via ESBD | [ESBD](https://www.txsmartbuy.gov/esbd) |

**DC check:** all 23 open DC OCP solicitations were reviewed. None are training today.

**California / Virginia:** these could not be checked automatically. Both portals block automated access, so set up their free vendor email alerts (codes are in `opportunity_finder/README.md`).

## B. Who wins and at what price (federal, FY2025 to today)

Sources: USAspending (863 awards) plus SAM.gov award notices (278).

| Category | # priced awards | Median | Middle 50% | Most frequent winners (partner targets) |
|---|---|---|---|---|
| AI literacy / AI teaching | 19 | **$140k** | $100k – $850k | Management Concepts, Solutions3, Fearless, K.L. Scott, Lantec, GAP Solutions |
| Leadership | 32 | $98k | $27k – $350k | Management Concepts, UVA Darden, Sensa Solutions, BMRA, LDSS |
| Online / e-learning / course dev | 117 | $98k | $37k – $486k | BMRA, Skillsoft, Harvard, UVA Darden |
| HR training | 133 | $57k | $18k – $301k | Management Concepts, BMRA, Stafford Consulting |
| Soft skills | 103 | **$28k** | $15k – $81k | TalentSmart, Graceland College CPD, Management Concepts |
| Excel / Microsoft 365 | 9 | $26k | $14k – $73k | Webucator, Lantec, New Horizons, Online Consulting |
| Power BI / data analytics | 49 | $67k* | $34k – $176k* | Minburn, Dell (*mostly licenses) |
| MATLAB / technical software | 198 | $41k* | $22k – $108k* | MathWorks, Lyme Computer, Sterling (*mostly licenses) |

How to read these numbers:
- **MATLAB and Power BI:** most of the dollars are software license purchases, not training. The winners CSV now has a `kind` column that separates "software license (not training)" from "training / service". The number of real MATLAB/Power BI *training* awards is small.
- **SAM award notices** sometimes show a contract ceiling rather than the amount actually spent, so treat the large values as upper bounds.
- **Contract vehicles:** 445 awards were orders under an agency IDV, 285 were standalone contracts and 133 were GSA Schedule orders. More than half of the work therefore flows through contract vehicles an outsider cannot use directly. That is why subcontracting is the route in.
