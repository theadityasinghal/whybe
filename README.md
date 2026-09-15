# EquiScore AI: Transparent Alternate Credit Underwriting

An explainable, AI-powered alternative credit underwriting engine purpose-built for individuals without traditional bureau histories — gig economy workers, rural Self-Help Group (SHG / *Bachat Gat*) members, and new-to-credit youth.

EquiScore replaces legacy collateral and bureau requirements with high-frequency behavioral data: daily gig app earnings, utility bill discipline, phone recharge regularity, UPI transaction consistency, and community savings.

---

## 🎨 Design Philosophy & Theme

EquiScore features a strict **Stark Dark Mode** design system inspired by the Geist aesthetic, combined with an intelligent **Eulerian Blue** signature accent system:

- **Canvas & Cards**: 100% solid, stark black canvas (`#000000`), elevated card surfaces (`#0e0e0e`), and crisp hairline borders (`#222222`). Zero distracting glassmorphism or blur effects.
- **Eulerian Blue Accent System**: High-contrast geometric cobalt/electric blue (`#0066FF`, hover `#1F75FF`, subtle tints `rgba(0, 102, 255, 0.09)`) applied to brand marks, active persona selectors, input focus rings, range slider controls, primary CTA buttons, and AI Copilot badges.
- **Semantic Risk Signals**: Restrained, non-neon semantic indicators for underwriting outcomes — Approved Green (`#22C55E`), Conditional Amber (`#F59E0B`), and Declined Red (`#EF4444`).
- **Responsive Layout**: Two-column responsive desktop console with progressive 4-step input forms and sticky real-time eligibility feedback.

---

## 🏗️ Architecture & Codebase Structure

```text
whybe/
├── source/                             # Raw dataset
│   └── alternative_credit_scoring.csv  # 2,000-record alternative credit dataset
├── server/                             # FastAPI backend (in-memory ML + Gemini Copilot)
│   ├── app.py                          # FastAPI REST service, CORS, API routes & static client hosting
│   ├── config.py                       # Monotonic rules, scoring params, feature definitions & env loader
│   ├── features.py                     # Domain feature engineering (liquidity buffers, discipline composite)
│   ├── model.py                        # Monotonic HistGradientBooster with 2x default loss & calibration
│   ├── explain.py                      # TreeSHAP exact game-theoretic feature attribution
│   ├── copilot.py                      # Multilingual Gemini Copilot (plain-language explain + interactive chat)
│   ├── simulate.py                     # Counterfactual what-if simulation & algorithmic goal-seek optimizer
│   └── evaluate_model.py               # 5-fold Stratified CV & in-sample validation benchmark script
├── client/                             # Static frontend console
│   ├── index.html                      # 4-step underwriting console, score meter, simulator & copilot UI
│   ├── style.css                       # Stark Dark Geist styling with signature Eulerian Blue accents
│   └── main.js                         # Debounced real-time scoring, presets, TreeSHAP rendering & chat
├── docs/                               # Deliverables & presentation materials
│   ├── rbi_compliance.md               # RBI Digital Lending Guidelines & Fair Lending compliance analysis
│   ├── pitch_deck.md                   # Slide-by-slide investor storyline
│   └── demo_script.md                  # 10-minute live demo and presentation script
├── Dockerfile                          # Production container image (FastAPI + static client)
├── render.yaml                         # One-click Render.com web service deployment config
├── vercel.json                         # Vercel static frontend routing configuration
├── Procfile                            # Heroku/Render process declaration
├── requirements.txt                    # Python dependencies (scikit-learn, shap, fastapi, uvicorn, etc.)
├── package.json                        # npm scripts for local development
└── .env.example                        # Environment variable template
```

---

## ✨ Key Features

| Feature | Details |
|---|---|
| **Monotonic ML Underwriting** | `HistGradientBoostingClassifier` with enforced monotonic directional constraints across 24 features, 2× asymmetric penalty on defaults, and Platt Sigmoid calibration. Score range: 300–850. |
| **TreeSHAP Explainability** | Exact game-theoretic feature attribution per applicant — highlights the top positive boosters and adverse risk factors in plain language. |
| **Bilingual Gemini AI Copilot** | Conversational credit advisor powered by Google Gemini (English & Hindi). Explains scores, demystifies risk factors, answers financial questions, and suggests improvement strategies. |
| **What-If Counterfactual Simulator** | Interactive slider sandbox: adjust bill habits, UPI failure rates, or mobile recharge frequency and observe instant score shifts. |
| **Algorithmic Goal-Seeker** | Automatic roadmap generator: set a target score (e.g., 680 for low-risk approval) and receive a prioritized 30-to-60 day action plan. |
| **Instant Cold-Start Training** | Trains in ~0.5 seconds fully in-memory upon server boot — zero saved model pickle files or stale artifact drift. |
| **Unified Single-Process Host** | FastAPI mounts and serves the static frontend UI directly — run both backend and client from a single port without complex tooling. |

---

## 🤖 ML Model & Validation Benchmarks

- **Algorithm**: `HistGradientBoostingClassifier` (scikit-learn ≥ 1.4)
- **Training Population**: 2,000 alternative credit records (`source/alternative_credit_scoring.csv`)
- **Monotonic Directionality**: Enforced on 24 domain features:
  - **17 Positive Incentives (+1)**: Monthly income, mobile recharge consistency, utility on-time rate, SHG savings, cooperative attendance, microfinance repayment count, gig earnings, gig platform rating, Jan Dhan balance, on-time rent, community referrals, insurance policies, total monthly inflow, total liquid savings, liquidity buffer months, discipline composite index, and microfinance net score.
  - **7 Derogatory Risk Penalties (-1)**: UPI failed transaction ratio, mobile recharge lapse days, microfinance default rate, Jan Dhan zero-balance months, telecom late payments, rent-to-income ratio, and telecom stress flag.
- **Asymmetric Risk Loss**: 2.0× sample weight penalty on default cases (`loan_approved = 0`) to protect lender capital.
- **Probability Calibration**: Platt Sigmoid calibration via 3-fold cross-validation.
- **Scoring Formula**: Transformed to credit bureau scale (300–850) using Base Score 650 with Points to Double the Odds (PDO) = 50:
  $$\text{Score} = \text{round}\left(650 + 50 \times \log_2\left(\frac{P(\text{Approved})}{1 - P(\text{Approved})}\right)\right)$$

### Benchmark Performance

| Metric | In-Sample (Calibrated) | 5-Fold Stratified CV (Out-of-Sample) |
|---|---|---|
| **ROC-AUC Score** | **99.61%** | **96.40% (±0.69%)** |
| **Precision-Recall AUC** | **99.83%** | **98.36% (±0.33%)** |
| **Overall Accuracy** | **97.20%** | **89.70% (±0.91%)** |
| **Macro F1-Score** | **97.96%** | **92.62% (±0.66%)** |
| **Default Recall (Sensitivity)** | **94.78%** | — |
| **Approval Precision** | **97.61%** | — |

To execute the offline model validation suite:

```bash
npm run evaluate
# or directly:
python3 server/evaluate_model.py
```

---

## 📐 Scoring Tiers & Risk Bands

| Score Range | Risk Band | Decision | Policy Action |
|---|---|---|---|
| **680 – 850** | Low Risk | ✅ **Approved** | Instant disbursement, lowest interest tier |
| **580 – 679** | Medium Risk | ⚠️ **Conditional Approval** | Smaller initial micro-credit line or manual KYC verification |
| **300 – 579** | High Risk | ❌ **Declined** | Transparent adverse action notice + Goal-Seeker roadmap |

---

## 🚀 Getting Started Locally

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** *(optional, for npm convenience scripts)*

### 1. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and enter your Gemini API key (optional, for Copilot features)
```

| Environment Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *None* | Google Gemini API key for the AI Underwriting Copilot |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` | Gemini model variant |
| `MPLCONFIGDIR` | `/tmp/mpl_cache` | Writable cache path for Matplotlib runtime |

> **Note**: If `GEMINI_API_KEY` is not provided, the underwriting engine, TreeSHAP explainability, and What-If simulator continue to function with local heuristic fallback explanations.

### 3. Launch Application

**Using npm scripts:**

```bash
npm run dev         # Starts backend (port 8000) and client (port 3000) concurrently
npm run server      # Starts FastAPI server on port 8000 (serves static UI too)
npm run client      # Starts standalone static file server on port 3000
npm run evaluate    # Runs in-sample and 5-fold cross-validation benchmarks
```

**Using Python directly:**

```bash
source .venv/bin/activate
uvicorn server.app:app --host 127.0.0.1 --port 8000 --reload
```

**Access Endpoints:**

| Service | URL |
|---|---|
| **Underwriting Console** | [http://localhost:8000](http://localhost:8000) |
| **Interactive API Documentation (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Alternative OpenAPI Schema (ReDoc)** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 📡 REST API Reference

All endpoints return JSON responses. Interactive exploration is available at `/docs`.

| Method | Endpoint | Request Body | Description |
|---|---|---|---|
| `GET` | `/api/health` | None | Service operational status, active model, and Gemini status. |
| `POST` | `/api/score` | `ApplicantInput` | Computes score (300–850), risk band, decision, recommendation, and TreeSHAP factors. |
| `POST` | `/api/copilot/explain` | `{ applicant, language }` | Generates bilingual (EN/HI) plain-language underwriting breakdown. |
| `POST` | `/api/copilot/chat` | `{ applicant, query, history, language }` | Multi-turn conversational Q&A with applicant financial context. |
| `POST` | `/api/simulate` | `{ original, modifications }` | Counterfactual what-if analysis showing projected score deltas. |
| `POST` | `/api/simulate/goal-seek` | `{ applicant, target_score, language }` | Generates step-by-step algorithmic roadmap to reach target score. |
| `GET` | `/api/metrics` | None | Returns verified model benchmark metrics and 5-fold cross-validation results. |

---

## 🏛️ Regulatory & Compliance Alignment

EquiScore AI was architected from the ground up to comply with Indian fintech regulations and central banking directives:

- **RBI Digital Lending Guidelines (2022)**: Complete transparency in automated decisioning; zero covert scraping of device SMS logs, contact books, or call history. All data inputs are consented financial and utility aggregates.
- **Fair Practices Code (FPC)**: Adverse action notices are automatically paired with plain-language TreeSHAP reason codes, ensuring applicants know exactly why an application was denied.
- **Explainability Over Black-Box Models**: Mathematical monotonicity guarantees that positive actions (e.g. paying bills on time, saving in Bachat Gat) can never decrease an applicant's score.
- **Detailed Compliance Dossier**: See [`docs/rbi_compliance.md`](docs/rbi_compliance.md) for full audit checklists and legal feasibility notes.

---

## 🌍 Deployment Options

### Docker Container

```bash
docker build -t equiscore-ai .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key equiscore-ai
```

### Render.com (One-Click)

The repository includes a ready-to-use [`render.yaml`](render.yaml) blueprint. Simply connect the repository to Render, configure `GEMINI_API_KEY` under Environment Variables, and deploy.

### Vercel (Frontend Console Only)

The `client/` directory contains a [`vercel.json`](vercel.json) configuration for static deployment on Vercel or Netlify. Set the backend API target in `client/main.js` or via environment rewrites.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
