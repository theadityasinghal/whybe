"""
TreeSHAP explainability engine initialized directly on the in-memory base model.
"""

import shap
import numpy as np

class ExplainerEngine:
    def __init__(self, base_model, feature_names):
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(base_model)

    def explain(self, X_proc, top_k=4) -> dict:
        shap_res = self.explainer(X_proc)
        values = shap_res.values[0]
        base_val = float(shap_res.base_values[0])
        
        contribs = []
        for name, val, raw_val in zip(self.feature_names, values, X_proc[0]):
            contribs.append({
                "feature": name,
                "label": name.replace("_", " ").title(),
                "shap_value": round(float(val), 3),
                "actual_value": round(float(raw_val), 2) if isinstance(raw_val, (int, float, np.number)) else str(raw_val),
            })
            
        positives = sorted([c for c in contribs if c["shap_value"] > 0], key=lambda x: x["shap_value"], reverse=True)[:top_k]
        negatives = sorted([c for c in contribs if c["shap_value"] < 0], key=lambda x: x["shap_value"])[:top_k]
        
        return {
            "base_expected_log_odds": round(base_val, 3),
            "top_positive": positives,
            "top_negative": negatives,
        }
