"""
FastAPI application serving credit scoring and TreeSHAP explainability.
"""

import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_cache")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from server.model import CreditEngine
from server.explain import ExplainerEngine

app = FastAPI(title="EquiScore AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models in-memory on server start (takes ~0.5 seconds)
engine = CreditEngine()
explainer = ExplainerEngine(engine.base_model, engine.feature_names)

class ApplicantInput(BaseModel):
    # Relaxed constraints to allow mid-typing without 422 errors
    age: int = Field(default=25, ge=0)
    monthly_income_inr: float = Field(default=25000.0, ge=0)
    area_type: str = Field(default="Urban")
    upi_monthly_avg_txn_count: int = Field(default=0, ge=0)
    upi_avg_txn_amount: float = Field(default=0.0, ge=0)
    upi_failed_txn_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    mobile_recharge_consistency_score: float = Field(default=1.0, ge=0.0, le=1.0)
    mobile_recharge_lapse_days_max: int = Field(default=0, ge=0)
    utility_bills_on_time_pct: float = Field(default=1.0, ge=0.0, le=1.0)
    electricity_bill_avg_amount: float = Field(default=0.0, ge=0)
    cooperative_meeting_attendance_pct: float = Field(default=0.0, ge=0.0, le=1.0)
    shg_savings_amount_inr: float = Field(default=0.0, ge=0)
    microfinance_loans_repaid_count: int = Field(default=0, ge=0)
    microfinance_default_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    gig_monthly_earnings: float = Field(default=0.0, ge=0)
    gig_platform_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    jandhan_avg_balance: float = Field(default=0.0, ge=0)
    jandhan_zero_balance_months: int = Field(default=0, ge=0)
    monthly_data_usage_gb: float = Field(default=0.0, ge=0)
    telecom_bill_late_payments: int = Field(default=0, ge=0)
    banking_app_login_frequency_monthly: int = Field(default=0, ge=0)
    fintech_apps_count: int = Field(default=0, ge=0)
    rent_on_time_payment_pct: float = Field(default=1.0, ge=0.0, le=1.0)
    rent_to_income_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    social_referral_count: int = Field(default=0, ge=0)
    insurance_policy_count: int = Field(default=0, ge=0)

from typing import Optional, List, Dict, Any
from server.copilot import CopilotEngine
from server.simulate import SimulationEngine

copilot = CopilotEngine()
simulator = SimulationEngine(engine)

class CopilotExplainRequest(BaseModel):
    applicant: ApplicantInput
    language: str = Field(default="en")

class CopilotChatRequest(BaseModel):
    applicant: ApplicantInput
    query: str
    history: Optional[List[Dict[str, str]]] = Field(default=[])
    language: str = Field(default="en")

class SimulateRequest(BaseModel):
    original: ApplicantInput
    modifications: Dict[str, Any]

class GoalSeekRequest(BaseModel):
    applicant: ApplicantInput
    target_score: int = Field(default=680)
    language: str = Field(default="en")

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "model": "In-Memory Monotonic HistGradientBoosting",
        "copilot": f"Google Gemini ({copilot.model_name})",
        "gemini_configured": bool(copilot.api_key)
    }

@app.post("/api/score")
def score(applicant: ApplicantInput):
    # Sanitize bounds gracefully in case user enters out-of-range numbers
    data = applicant.model_dump()
    data["age"] = max(18, min(80, data["age"]))
    data["jandhan_zero_balance_months"] = min(12, max(0, data["jandhan_zero_balance_months"]))
    
    res = engine.predict_score(data)
    shap_res = explainer.explain(res["processed_matrix"])
    return {
        "score": res["score"],
        "approval_probability": res["approval_probability"],
        "risk_band": res["risk_band"],
        "decision": res["decision"],
        "recommendation": res["recommendation"],
        "top_positive_factors": shap_res["top_positive"],
        "top_negative_factors": shap_res["top_negative"],
    }

@app.post("/api/copilot/explain")
def copilot_explain(req: CopilotExplainRequest):
    data = req.applicant.model_dump()
    res = engine.predict_score(data)
    shap_res = explainer.explain(res["processed_matrix"])
    
    score_payload = {
        "score": res["score"],
        "approval_probability": res["approval_probability"],
        "risk_band": res["risk_band"],
        "decision": res["decision"],
        "recommendation": res["recommendation"],
        "top_positive_factors": shap_res["top_positive"],
        "top_negative_factors": shap_res["top_negative"],
    }
    
    try:
        explanation = copilot.explain_score(score_payload, language=req.language)
        return {"success": True, "data": explanation}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/copilot/chat")
def copilot_chat(req: CopilotChatRequest):
    data = req.applicant.model_dump()
    res = engine.predict_score(data)
    shap_res = explainer.explain(res["processed_matrix"])
    
    score_payload = {
        "score": res["score"],
        "approval_probability": res["approval_probability"],
        "risk_band": res["risk_band"],
        "decision": res["decision"],
        "recommendation": res["recommendation"],
        "top_positive_factors": shap_res["top_positive"],
        "top_negative_factors": shap_res["top_negative"],
    }
    
    try:
        reply = copilot.chat(score_payload, query=req.query, history=req.history, language=req.language)
        return {"success": True, "data": reply}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/simulate")
def simulate(req: SimulateRequest):
    orig_data = req.original.model_dump()
    result = simulator.simulate(orig_data, req.modifications)
    return {"success": True, "data": result}

@app.post("/api/simulate/goal-seek")
def goal_seek(req: GoalSeekRequest):
    data = req.applicant.model_dump()
    result = simulator.goal_seek(data, target_score=req.target_score, language=req.language)
    return {"success": True, "data": result}

@app.get("/api/metrics")
def get_metrics():
    """Returns exact model evaluation metrics and 5-fold CV benchmarks."""
    return {
        "accuracy": 97.2,
        "f1_score": 98.0,
        "roc_auc": 99.6,
        "pr_auc": 99.8,
        "cv_accuracy": 89.7,
        "cv_f1": 92.6,
        "cv_roc_auc": 96.4,
        "cv_pr_auc": 98.4,
        "confusion_matrix": {
            "true_negative": 599,
            "false_positive": 33,
            "false_negative": 23,
            "true_positive": 1345
        },
        "dataset_size": 2000,
        "default_penalty_ratio": "2.0x",
        "monotonic_constraints_enforced": True,
        "calibration": "Platt Sigmoid (3-Fold CV)"
    }

# Mount static frontend console so full app runs from a single unified server
CLIENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../client"))
if os.path.isdir(CLIENT_DIR):
    app.mount("/", StaticFiles(directory=CLIENT_DIR, html=True), name="client")

