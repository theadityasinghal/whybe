"""
Dynamic feature engineering and transformation pipeline.
Processes raw inputs directly in-memory without saving intermediate CSVs.
"""

import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes high-signal domain features for thin-file / gig workers."""
    out = df.copy()
    out["total_monthly_inflow"] = out["monthly_income_inr"] + out["gig_monthly_earnings"]
    out["total_liquid_savings"] = out["jandhan_avg_balance"] + out["shg_savings_amount_inr"]
    
    out["liquidity_buffer_months"] = np.where(
        out["monthly_income_inr"] > 0,
        out["total_liquid_savings"] / out["monthly_income_inr"],
        0.0
    ).round(2)
    
    out["discipline_composite_index"] = (
        0.45 * out["utility_bills_on_time_pct"] +
        0.35 * out["mobile_recharge_consistency_score"] +
        0.20 * out["cooperative_meeting_attendance_pct"]
    ).round(4)
    
    out["telecom_stress_flag"] = (
        (out["telecom_bill_late_payments"] >= 3) |
        (out["mobile_recharge_lapse_days_max"] >= 30)
    ).astype(int)
    
    out["est_monthly_upi_volume"] = (out["upi_monthly_avg_txn_count"] * out["upi_avg_txn_amount"]).round(2)
    
    out["upi_to_income_ratio"] = np.where(
        out["total_monthly_inflow"] > 0,
        out["est_monthly_upi_volume"] / out["total_monthly_inflow"],
        0.0
    ).clip(0.0, 5.0).round(4)
    
    out["microfinance_net_score"] = (
        out["microfinance_loans_repaid_count"] * (1.0 - out["microfinance_default_rate"])
    ).round(2)
    
    return out
