# EquiScore AI: Transparent Alternate Credit Underwriting

An AI-powered alternative credit underwriting engine built for individuals without traditional credit histories — gig workers, rural self-help group members, and new-to-credit youth.

---

## 🏗️ Architecture

```text
whybe/
├── source/                             # Raw dataset
│   └── alternative_credit_scoring.csv # 2,000-record alternative credit dataset
├── server/                             # FastAPI backend (in-memory ML + Gemini Copilot)
│   ├── config.py                       # Monotonic rules, scoring params, feature definitions & env loader
│   ├── features.py                     # Behavioral & liquidity feature engineering
│   ├── model.py                        # Monotonic HistGradientBooster with 2x default loss & calibration
│   ├── explain.py                      # TreeSHAP exact game-theoretic feature attribution
│   ├── copilot.py                      # Multilingual Gemini Copilot (explain + chat)
│   ├── simulate.py                     # Counterfactual simulation & goal-seek optimizer
│   ├── evaluate_model.py               # Offline 5-fold CV benchmarking script
│   └── app.py                          # FastAPI REST service (serves static frontend too)
├── client/                             # Static frontend (Vercel / Netlify ready)
│   ├── index.html                      # Underwriting console UI
│   ├── style.css                       # Responsive FinTech styling
│   └── main.js                         # Gauge animations, preset loaders, API fetch, copilot chat
├── docs/                               # Deliverables & presentation materials
│   ├── rbi_compliance.md               # RBI Digital Lending Guidelines feasibility note
│   ├── pitch_deck.md                   # Slide-by-slide storyline
│   └── demo_script.md                  # 10-minute demo flow
├── Dockerfile                          # Docker image for containerised deployment
├── render.yaml                         # One-click Render.com deployment config
├── vercel.json                         # Vercel static frontend config
├── Procfile                            # Heroku/Render process file
├── requirements.txt                    # Python dependencies
├── package.json                        # npm scripts for local dev
└── .env.example                        # Environment variable template
```

---

## ✨ Features

| Feature | Details |
|---|---|
| **Monotonic ML Scoring** | `HistGradientBoostingClassifier` with enforced monotonic constraints, 2× default penalty, and Platt Sigmoid calibration. Score range: 300–850. |
| **TreeSHAP Explainability** | Exact game-theoretic attribution — top positive and negative factors per applicant. |
| **Gemini AI Copilot** | Multilingual (English / Hindi) conversational advisor powered by Google Gemini. Explains scores and answers applicant questions in plain language. |
| **What-If Simulator** | Counterfactual simulation: modify any behavioral field and see the instant score delta. |
| **Goal-Seek Optimizer** | Algorithmic roadmap: given a target score, finds the lowest-friction behavioural improvements to get there. |
| **Unified Server** | FastAPI serves the static frontend directly — single process, no separate static host needed. |

---

## 🚀 Running Locally

### Prerequisites

- Python 3.11+
- Node.js (for `npm` scripts — optional)

### 1. Set Up the Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required for Copilot)* | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` | Gemini model to use |

> The Copilot features degrade gracefully if `GEMINI_API_KEY` is not set — all scoring and explainability still work.

### 3. Start the Application

**Using npm (recommended):**

```bash
npm run dev          # Starts server (port 8000) + client (port 3000) concurrently
npm run dev:server   # FastAPI only on port 8000
npm run dev:client   # Static file server only on port 3000
```

**Using Python directly:**

```bash
MPLCONFIGDIR=/tmp/mpl_cache uvicorn server.app:app --host 127.0.0.1 --port 8000 --reload
```

**Access points:**

| | URL |
|---|---|
| **Underwriting Console** | `http://localhost:8000` (served by FastAPI) or `http://localhost:3000` (standalone) |
| **Interactive API Docs** | `http://localhost:8000/docs` |

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service status, model info, Gemini config |
| `POST` | `/api/score` | Score an applicant — returns score, risk band, decision, SHAP factors |
| `POST` | `/api/copilot/explain` | Gemini plain-language assessment of the applicant's score |
| `POST` | `/api/copilot/chat` | Multi-turn Gemini chat for applicant Q&A |
| `POST` | `/api/simulate` | What-if simulation: compare original vs. modified profile |
| `POST` | `/api/simulate/goal-seek` | Algorithmic roadmap to reach a target score |
| `GET` | `/api/metrics` | Model evaluation metrics and 5-fold CV benchmarks |

---

## 🤖 ML Model

- **Algorithm**: `HistGradientBoostingClassifier` (scikit-learn ≥ 1.4)
- **Training data**: 2,000 records (`source/alternative_credit_scoring.csv`)
- **Monotonic constraints**: Enforced on 19 features (income, bill discipline, SHG savings, etc.)
- **Asymmetric loss**: 2× sample weight on defaults (`loan_approved = 0`)
- **Calibration**: Platt Sigmoid (3-fold CV)
- **Startup time**: ~0.5 s — trains fully in-memory on server start, no saved model artifacts

**Benchmark metrics:**

| Metric | Held-out Test | 5-Fold CV |
|---|---|---|
| Accuracy | 97.2% | 89.7% |
| F1 Score | 98.0% | 92.6% |
| ROC-AUC | 99.6% | 96.4% |
| PR-AUC | 99.8% | 98.4% |

Run offline evaluation:

```bash
npm run evaluate
# or: ./.venv/bin/python3 server/evaluate_model.py
```

---

## 📐 Scoring Tiers

| Score Range | Risk Band | Decision |
|---|---|---|
| 680 – 850 | Low Risk | ✅ Approved |
| 580 – 679 | Medium Risk | ⚠️ Conditional Approval |
| 300 – 579 | High Risk | ❌ Declined |

---

## 🌍 Deployment

### Docker

```bash
docker build -t equiscore-ai .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key equiscore-ai
```

### Render

Deploy using the included [`render.yaml`](render.yaml). Set `GEMINI_API_KEY` in the Render dashboard environment variables.

### Vercel (Frontend Only)

The `client/` directory is configured for static deployment via [`vercel.json`](vercel.json). Point it at your deployed backend URL.

---

## 📄 License

MIT
