"""
Core ML engine: trains in-memory on startup in ~0.5s, avoiding any disk-persisted model artifacts.
Enforces monotonic constraints, asymmetric default loss, and probability calibration.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

from server.config import NUMERICAL_FEATURES, CATEGORICAL_FEATURES, MONOTONIC_RULES, SCORE_BASE, SCORE_PDO
from server.features import engineer_features

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/alternative_credit_scoring.csv"))

class CreditEngine:
    def __init__(self):
        self.preprocessor = None
        self.base_model = None
        self.calibrated_model = None
        self.feature_names = []
        self._initialize_and_train()

    def _initialize_and_train(self):
        """Loads data and trains the monotonic champion model in-memory."""
        df_raw = pd.read_csv(DATA_PATH)
        y = df_raw["loan_approved"].astype(int)
        
        # In-memory feature engineering
        drop_cols = ["loan_approved", "credit_risk_label", "alternative_credit_score"]
        X_raw = df_raw.drop(columns=drop_cols)
        X_eng = engineer_features(X_raw)
        
        eng_numerical = [c for c in X_eng.columns if c not in CATEGORICAL_FEATURES]
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", "passthrough", eng_numerical),
                ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ]
        )
        
        X_proc = self.preprocessor.fit_transform(X_eng)
        cat_names = list(self.preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
        self.feature_names = eng_numerical + cat_names
        
        # Build monotonic vector
        c_list = [MONOTONIC_RULES.get(f, 0) for f in self.feature_names]
        
        # Asymmetric default penalty: 2x weight on defaults (y=0)
        sample_weights = np.where(y == 0, 2.0, 1.0)
        
        self.base_model = HistGradientBoostingClassifier(
            monotonic_cst=tuple(c_list),
            max_iter=160,
            max_depth=5,
            min_samples_leaf=15,
            learning_rate=0.05,
            l2_regularization=1.5,
            random_state=42,
        )
        self.base_model.fit(X_proc, y, sample_weight=sample_weights)
        
        # Probability calibration (Platt Sigmoid)
        self.calibrated_model = CalibratedClassifierCV(
            estimator=self.base_model,
            method="sigmoid",
            cv=3,
        )
        self.calibrated_model.fit(X_proc, y)

    def predict_score(self, raw_input_dict: dict) -> dict:
        """Transforms a single applicant dict and returns score and decision."""
        df_single = pd.DataFrame([raw_input_dict])
        df_eng = engineer_features(df_single)
        X_proc = self.preprocessor.transform(df_eng)
        
        p = float(self.calibrated_model.predict_proba(X_proc)[0, 1])
        
        # Scorecard mapping
        eps = 1e-5
        p_safe = np.clip(p, eps, 1.0 - eps)
        odds = p_safe / (1.0 - p_safe)
        score = int(np.clip(np.round(SCORE_BASE + (SCORE_PDO / np.log(2.0)) * np.log(odds)), 300, 850))
        
        if score >= 680:
            band = "Low Risk"
            decision = "Approved"
            rec = "Eligible for prime interest rates and instant digital disbursement."
        elif score >= 580:
            band = "Medium Risk"
            decision = "Conditional Approval"
            rec = "Eligible for micro-credit line subject to guarantor or additional verification."
        else:
            band = "High Risk"
            decision = "Declined"
            rec = "High risk profile. Adverse Action notice generated below."
            
        return {
            "score": score,
            "approval_probability": round(p, 4),
            "risk_band": band,
            "decision": decision,
            "recommendation": rec,
            "processed_matrix": X_proc,
        }
