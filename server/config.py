"""
Central configuration for features, monotonic constraints, and scoring thresholds.
"""

NUMERICAL_FEATURES = [
    "age", "monthly_income_inr", "upi_monthly_avg_txn_count", "upi_avg_txn_amount",
    "upi_failed_txn_ratio", "mobile_recharge_consistency_score", "mobile_recharge_lapse_days_max",
    "utility_bills_on_time_pct", "electricity_bill_avg_amount", "cooperative_meeting_attendance_pct",
    "shg_savings_amount_inr", "microfinance_loans_repaid_count", "microfinance_default_rate",
    "gig_monthly_earnings", "gig_platform_rating", "jandhan_avg_balance", "jandhan_zero_balance_months",
    "monthly_data_usage_gb", "telecom_bill_late_payments", "banking_app_login_frequency_monthly",
    "fintech_apps_count", "rent_on_time_payment_pct", "rent_to_income_ratio", "social_referral_count",
    "insurance_policy_count"
]

CATEGORICAL_FEATURES = ["area_type"]

# Monotonic constraints: +1 for positive indicators, -1 for derogatory risk
MONOTONIC_RULES = {
    "monthly_income_inr": 1, "mobile_recharge_consistency_score": 1, "utility_bills_on_time_pct": 1,
    "cooperative_meeting_attendance_pct": 1, "shg_savings_amount_inr": 1, "microfinance_loans_repaid_count": 1,
    "gig_monthly_earnings": 1, "gig_platform_rating": 1, "jandhan_avg_balance": 1, "rent_on_time_payment_pct": 1,
    "social_referral_count": 1, "insurance_policy_count": 1, "total_monthly_inflow": 1,
    "total_liquid_savings": 1, "liquidity_buffer_months": 1, "discipline_composite_index": 1,
    "microfinance_net_score": 1,
    
    "upi_failed_txn_ratio": -1, "mobile_recharge_lapse_days_max": -1, "microfinance_default_rate": -1,
    "jandhan_zero_balance_months": -1, "telecom_bill_late_payments": -1, "rent_to_income_ratio": -1,
    "telecom_stress_flag": -1,
}

SCORE_BASE = 650
SCORE_PDO = 50
