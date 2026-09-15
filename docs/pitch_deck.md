# EquiScore AI — Pitch Deck Outline & Evaluation Guide

---

### Slide 1: The Problem
* **The Bureau Blindspot**: Over 450 Million Indians (gig workers, rural SHG members, artisans, students) have zero formal bureau credit history (thin-file).
* **The Broken Paradox**: Traditional banks demand past loan history to grant a first loan. New-to-credit borrowers are forced toward informal money lenders with predatory 60%+ interest rates.

---

### Slide 2: The Solution — EquiScore AI
* **Alternative Behavioral Footprint Underwriting**: Assesses cash-flow health, utility bill timeliness, UPI transaction stability, Jan Dhan balance regularity, and community social collateral (SHG / Bachat Gat savings).
* **Transparent Scoring (300 to 850)**: Calibrated against industry scorecard standards ($650 \text{ Base} + 50 \text{ PDO}$).

---

### Slide 3: The Secret Sauce — TreeSHAP & Mathematical Governance
* **Explainable, Not a Black Box**: Decomposes every decision into exact game-theoretic feature attributions (TreeSHAP).
* **Monotonic Constraints**: Mathematically guarantees that positive discipline can never arbitrarily lower an applicant's score.
* **Asymmetric Risk Weighting**: 2.0x penalty on default loss to safeguard lender capital reserves.

---

### Slide 4: Real-World Model Benchmarks
* **ROC-AUC**: **96.4%** (5-Fold Stratified Cross-Validation) / **99.6%** Full Dataset.
* **Macro F1-Score**: **92.6%** (CV) / **98.0%** Full Dataset.
* **Precision-Recall AUC**: **98.4%** (CV) / **99.8%** Full Dataset.
* **Default Recall (Sensitivity)**: **94.8%** (captures 599 of 632 real defaults).

---

### Slide 5: Regulatory Compliance & Privacy (DPDP + RBI)
* **Account Aggregator (AA) Native**: 100% consent-driven, revocable electronic consent architecture.
* **Zero Mobile Scraping**: Complies fully with RBI Digital Lending Directives forbidding SMS, contact, or location scraping.
* **Adverse Action Ready**: Automatically provides lenders with compliant adverse notices stating the exact negative drivers.

---

### Slide 6: Live Product Demo Walkthrough
* **Persona 1: Urban Gig Delivery Partner** (High UPI transactions, strong ratings, zero prior loans $\rightarrow$ Approved with 850 score).
* **Persona 2: Rural Self-Help Group Member** (Bachat Gat savings, microfinance repayment track record $\rightarrow$ Approved with 785 score).
* **Persona 3: High Default Risk Applicant** (High UPI bounce rate, late utility and telecom payments $\rightarrow$ Needs Review with transparent adverse drivers).
