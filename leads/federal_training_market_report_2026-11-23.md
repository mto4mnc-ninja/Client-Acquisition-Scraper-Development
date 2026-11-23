# US Government Training Market: HR, Soft Skills, AI (pulled 2026-11-23)

**Sources (official US government APIs, pulled live):**
- api.usaspending.gov: federal contract obligations
- api.grants.gov: open and forecasted grants

**Not pulled:** SAM.gov live notices (the API key was declined) and state/local portals (not reachable from this session).

## 1. Federal contract spend by training NAICS (contracts only, by fiscal year)

| NAICS | Meaning | FY2024 | FY2025 | FY2026 | Change FY24→26 |
|---|---|---|---|---|---|
| 611430 | Professional & management development training | $1,038.7M | $802.8M | $638.6M | **−38%** |
| 611420 | Computer training | $208.6M | $199.3M | $149.9M | −28% |
| 611710 | Educational support services | $560.6M | $407.2M | $366.4M | −35% |

FY = Oct–Sep. FY2026 ended Sep 30, 2026, but USAspending can still revise these figures.

## 2. Who buys (611430, FY2026)
| Agency | Spend |
|---|---|
| Defense (DoD) | $359.7M |
| Interior | $55.7M |
| Transportation | $41.9M |
| Homeland Security | $41.8M |
| GSA | $23.9M |
| HHS | $23.3M |
| Commerce | $16.7M |
| Veterans Affairs | $15.6M |
| Justice | $13.1M |
| State | $12.1M |

FY2026 had 1,545 contract awards in 611430 between $10k and $250k. This is the realistic size range for a small vendor or subcontractor.

## 3. Who wins (611430, FY2026 top recipients)
| Recipient | Amount |
|---|---|
| Amentum | $74.0M |
| Boeing | $61.5M |
| Deep Mile Networks | $52.0M |
| Leidos | $21.1M |
| Goldbelt Apex | $13.7M |
| HigherEchelon | $13.3M |
| Parker Tide | $12.7M |
| Guzman & Griffin | $12.5M |
| Aleut Mgmt | $12.5M |
| Team Carney | $11.7M |
| Avani | $11.6M |
| George Mason Univ | $8.4M |
| Management Concepts | $8.3M |
| CALIBRE | $8.2M |
| Pherson Associates | $8.2M |

## 4. Recent relevant awards (53 rows): see `federal_training_awards_2026-11-23.csv`
- Median award: **$80,000**.
- Vehicles: 33 standalone contracts, 13 GSA Schedule orders, 7 orders under agency IDVs.
- Mix: 30 soft-skills/leadership, 14 AI, 9 HR.
- Examples of AI-training buys:
  - DOL AI literacy training: $576k (Solutions3, GSA, Sep 2026)
  - DOL "BuyAI" training: $304.5k (ASI Government)
  - IRS data/AI training: $139.6k (Fearless)
  - NASA leadership + AI: $130k (Learning Tree)
  - Navy SES AI course: $140k (UNC)
  - State Dept AI curriculum: $28.7k (Management Concepts)
- **Foreign vendors have won:**
  - Simon Everett Ltd: $427k State Dept course facilitator (Sep 2026)
  - "Miscellaneous Foreign Awardees": $26k State Dept AI services
- **Seasonality:** a large share of awards are dated **Sep 15–30**, when agencies spend leftover fiscal-year money.

## 5. Grants.gov: mostly NOT usable by a non-US for-profit
- DOJ/NIC **27CS30 "Facilitating Behavior Change Training for Trainers"**: up to $150k, closes **Jan 19, 2027**.
  - Not eligible for a foreign firm.
  - No profit allowed.
  - 501(c)(3) proof required.
  - The only route is as an unpaid or partner role with a US nonprofit.
- The other hits are NSF/NIH research and education grants for US institutions. Not a fit.

## 6. Portals to work (state/local not verified live this session)
| Portal | Use |
|---|---|
| sam.gov | Federal RFQs and sources-sought notices. Foreign firms can register (UEI + NCAGE code) |
| usaspending.gov | Past winners and prices: use it to find teaming partners |
| gsa.gov MAS (SIN 611430 Training) | The main vehicle for federal training buys |
| State e-procurement portals (e.g. Cal eProcure, NYS Contract Reporter, Texas ESBD, eVA Virginia, eMMA Maryland) | State HR/leadership training RFPs. Many accept out-of-state and foreign bidders, but some require US registration |
