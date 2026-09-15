# EquiScore AI: Transparent Alternate Credit Underwriting

An AI-powered alternative credit underwriting engine built for individuals without traditional credit histories (gig workers, rural self-help group members, and new-to-credit youth).

---

## 🏗️ Architecture

```text
whybe/
├── data/                               # Raw source dataset (alternative_credit_scoring.csv)
├── server/                             # Pure Python backend (FastAPI + In-memory ML)
│   ├── config.py                       # Monotonic rules, scoring parameters, and feature definitions
│   ├── features.py                     # High-signal behavioral & liquidity feature engineering
│   ├── model.py                        # Monotonic Gradient Booster with 2x default loss & calibration
│   ├── explain.py                      # TreeSHAP exact game-theoretic feature attribution
│   └── app.py                          # Clean FastAPI REST microservice
├── client/                             # Pure static frontend (ready for Vercel / Netlify)
│   ├── index.html                      # Modern underwriting console UI
│   ├── style.css                       # Clean, responsive FinTech styling
│   └── main.js                         # Dynamic gauge animations, preset loaders, and API fetch
├── docs/                               # Deliverables & presentation materials
│   ├── rbi_compliance.md               # 1-pager feasibility under RBI Digital Lending Guidelines
│   ├── pitch_deck.md                   # Slide-by-slide storyline for evaluators
│   └── demo_script.md                  # Verbatim 10-minute presentation & demo flow
├── package.json                        # Single npm run dev entrypoint
└── README.md
```

---

## 🚀 Running the Web Application

To run both the backend server and frontend dashboard concurrently:

```bash
npm run dev
```

* **Frontend Console**: `http://localhost:3000`
* **Backend API Docs**: `http://localhost:8000/docs`

Alternatively, you can run them individually:
```bash
npm run dev:server   # Starts FastAPI on port 8000
npm run dev:client   # Starts web server on port 3000
```
