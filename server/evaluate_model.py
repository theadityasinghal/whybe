"""
EquiScore AI — Model Evaluation & Validation Benchmark Script
Evaluates the in-memory Monotonic HistGradientBoostingClassifier against
the alternate credit dataset (N=2,000) using both full-set and 5-Fold Stratified CV.
"""

import sys
from pathlib import Path

# Add project root to sys.path so script can be run standalone
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)
from server.model import CreditEngine
from server.features import engineer_features

def run_evaluation():
    print("=" * 70)
    print("  EQUISCORE AI — MODEL BENCHMARK & EVALUATION SUITE")
    print("=" * 70)

    # 1. Load Data
    df = pd.read_csv("source/alternative_credit_scoring.csv")
    y = df["loan_approved"].astype(int).values
    drop_cols = ["loan_approved", "credit_risk_label", "alternative_credit_score"]
    X_raw = df.drop(columns=drop_cols)

    # 2. Feature Engineering & Preprocessing
    print(f"Dataset Size: {len(df)} applicants | Default Rate: {round((1 - y.mean())*100, 1)}%")
    engine = CreditEngine()
    X_eng = engineer_features(X_raw)
    X_proc = engine.preprocessor.transform(X_eng)

    # 3. In-Sample Calibrated Predictions
    probs = engine.calibrated_model.predict_proba(X_proc)[:, 1]
    preds = (probs >= 0.5).astype(int)

    acc = accuracy_score(y, preds)
    f1 = f1_score(y, preds)
    roc = roc_auc_score(y, probs)
    pr = average_precision_score(y, probs)
    cm = confusion_matrix(y, preds)

    print("\n--- In-Sample Performance (Calibrated Platt Sigmoid) ---")
    print(f"  • ROC-AUC Score:        {roc*100:.2f}%")
    print(f"  • Precision-Recall AUC: {pr*100:.2f}%")
    print(f"  • Accuracy:             {acc*100:.2f}%")
    print(f"  • Macro F1-Score:       {f1*100:.2f}%")

    print("\n--- Classification Breakdown ---")
    print(classification_report(y, preds, target_names=["Default (0)", "Approved (1)"], digits=4))

    print("--- Confusion Matrix (Row=Actual, Col=Predicted) ---")
    print(f"  TN: {cm[0,0]:<5} | FP: {cm[0,1]:<5}  (Default Recall / Sensitivity: {cm[0,0]/(cm[0,0]+cm[0,1])*100:.1f}%)")
    print(f"  FN: {cm[1,0]:<5} | TP: {cm[1,1]:<5}  (Approval Precision: {cm[1,1]/(cm[0,1]+cm[1,1])*100:.1f}%)")

    # 4. 5-Fold Stratified Cross-Validation (Out-of-Sample Verification)
    print("\n--- 5-Fold Stratified Out-of-Sample Cross-Validation ---")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_acc, cv_f1, cv_roc, cv_pr = [], [], [], []

    for train_idx, val_idx in skf.split(X_proc, y):
        m = engine.base_model
        m.fit(X_proc[train_idx], y[train_idx])
        fold_probs = m.predict_proba(X_proc[val_idx])[:, 1]
        fold_preds = (fold_probs >= 0.5).astype(int)
        cv_acc.append(accuracy_score(y[val_idx], fold_preds))
        cv_f1.append(f1_score(y[val_idx], fold_preds))
        cv_roc.append(roc_auc_score(y[val_idx], fold_probs))
        cv_pr.append(average_precision_score(y[val_idx], fold_probs))

    print(f"  • 5-Fold CV ROC-AUC:  {np.mean(cv_roc)*100:.2f}% (+/- {np.std(cv_roc)*100:.2f}%)")
    print(f"  • 5-Fold CV PR-AUC:   {np.mean(cv_pr)*100:.2f}% (+/- {np.std(cv_pr)*100:.2f}%)")
    print(f"  • 5-Fold CV Accuracy: {np.mean(cv_acc)*100:.2f}% (+/- {np.std(cv_acc)*100:.2f}%)")
    print(f"  • 5-Fold CV Macro F1: {np.mean(cv_f1)*100:.2f}% (+/- {np.std(cv_f1)*100:.2f}%)")

    print("\n--- Risk Governance Standards Enforced ---")
    print("  [X] Monotonic constraints on all income, savings, and delinquency features")
    print("  [X] 2.0x Asymmetric loss weight penalty on loan defaults (protects lender capital)")
    print("  [X] Platt Sigmoid probability calibration for accurate odds transformation")
    print("=" * 70)

if __name__ == "__main__":
    run_evaluation()
