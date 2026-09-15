"""
FastAPI application serving credit scoring and TreeSHAP explainability.
"""

from fastapi import FastAPI
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

@app.get("/")
def health():
    return {"status": "online", "model": "In-Memory Monotonic HistGradientBoosting"}

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
