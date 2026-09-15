# Real-World Feasibility & RBI Compliance Framework
## EquiScore AI: Regulatory Alignment, Data Privacy & Implementation Architecture

---

### 1. Executive Summary & Regulatory Context
Traditional credit scoring mechanisms (e.g., CIBIL, Experian, Equifax) evaluate borrowers through historical bureau trades, credit cards, and formal banking lines. In India, this systematically excludes over **450 million thin-file citizens**—including gig economy delivery partners, rural Self-Help Group (SHG) members, street vendors, and newly employed youth. 

**EquiScore AI** provides an explainable alternative credit underwriting architecture built directly in alignment with the **Reserve Bank of India (RBI) Digital Lending Guidelines (2022/2023)** and the **Digital Personal Data Protection (DPDP) Act, 2023**.

---

### 2. Alignment with RBI Digital Lending Guidelines

| RBI Mandate | Regulatory Requirement | EquiScore AI Implementation Architecture |
| :--- | :--- | :--- |
| **No Unrestricted Mobile Scraping** | Lenders cannot scrape contacts, SMS logs, media files, or call registers. | **Zero scraping.** EquiScore only uses permissioned, verified data flows (Account Aggregator bank inflows, utility bill API receipts, and opt-in telecom recharge metadata). |
| **Right to Explanation & Adverse Action** | Borrowers must be notified of the exact grounds for rejection or adverse rating. | **TreeSHAP Explainability.** The engine decomposes each score into exact local Shapley values, providing the top credit-boosting and risk factors with quantified impact points. |
| **Loan Flow through Regulated Entities (REs)** | All loan disbursements and repayments must flow directly between the borrower and RE bank accounts without synthetic pass-through wallets. | The platform functions purely as a decision-support Scoring Provider (Lending Service Provider / LSP partner) outputting standardized credit bands and calibrated odds for RE underwriters. |
| **Key Fact Statement (KFS) & APR Transparency** | Borrowers must receive a clear Key Fact Statement detailing annualized rates and limits. | Scorecard odds mapping translates creditworthiness into risk tiers (Low/Medium/High), enabling lenders to dynamically determine fair, non-usurious APRs based on risk-based pricing. |

---

### 3. Data Privacy & DPDP Act 2023 Compliance

1. **Purpose Limitation & Data Minimization**:
   - Features captured are strictly restricted to financial proxies (e.g., utility timeliness, UPI failure ratio, Jan Dhan balance stability).
   - Sensitive personal attributes (religion, caste, gender, browsing history) are completely excluded from the model feature store.

2. **Consent-Driven Architecture via Account Aggregator (AA)**:
   - Financial data (Jan Dhan savings, UPI transaction flows) is ingested exclusively through RBI-regulated **Account Aggregators (AAs)** via electronic, revocable, time-bound consent artifacts.
   - Borrowers retain the legal right to revoke consent and request data deletion.

3. **Stateless Scoring & Ephemeral Execution**:
   - The ML scoring engine runs in-memory. Feature vectors are evaluated dynamically without persisting raw customer credentials or private identifiers in secondary storage.

---

### 4. Mathematical Governance & Algorithmic Fairness

Black-box machine learning often creates unintended, non-linear penalties (e.g., earning more income slightly lowering a score due to spurious tree correlations). EquiScore enforces three layers of mathematical governance:

1. **Strict Monotonic Constraints**:
   - Mathematical constraints ensure that positive financial discipline (e.g., higher SHG savings, timely electricity bill payments) **can never decrease** a borrower's score.
   - Derogatory behavior (e.g., telecom delays, UPI bounce rates) **can never increase** a score.

2. **Asymmetric Default Loss (2.0x Penalty)**:
   - Institutional solvency requires prioritizing default prevention over marginal approval volume. Training with a $2.0\times$ penalty on defaults protects lender Tier-1 capital.

3. **Platt Sigmoid Calibration**:
   - Raw tree outputs are calibrated via 3-Fold cross-validated Platt Sigmoids, ensuring that an estimated 80% approval probability matches an empirical 80% repayment rate.

---

### 5. Deployment Roadmap for NBFCs & Microfinance Institutions

```
[Borrower Consent / AA App]
            │
            ▼ (Secure AA Data Flow)
┌────────────────────────────────────────────────────────┐
│               EquiScore Underwriting API              │
│                                                        │
│  1. In-Memory Domain Feature Engineering               │
│  2. Monotonic Calibrated Classifier (96.4% CV ROC-AUC) │
│  3. TreeSHAP Attribution Decomposition                 │
└────────────────────────────────────────────────────────┘
            │
            ▼ (Structured Risk Payload)
[Regulated Entity Core Banking System / Underwriter Console]
```

* **Phase 1 (Sandbox)**: Deploy alongside existing MFI credit operations to score thin-file applicants under an NBFC sandbox.
* **Phase 2 (Co-Lending Integration)**: Hook API into digital co-lending platforms for micro-credit disbursements (₹10,000 – ₹50,000).
