"""
EquiScore AI — Counterfactual Simulation & Goal-Seeking Optimizer
Enables applicants and loan officers to run what-if simulations on financial behaviors,
and computes an algorithmic, minimal-effort roadmap to reach target approval thresholds.
"""

from typing import Dict, Any, List
import copy
import numpy as np

# Key actionable levers that borrowers have direct agency over
ACTIONABLE_LEVERS = [
    {
        "field": "upi_failed_txn_ratio",
        "label": "Failed UPI Payments (Low Balance)",
        "unit": "ratio",
        "direction": "minimize",
        "best_target": 0.02,
        "action_en": "Keep a buffer to avoid UPI payment failures due to insufficient balance",
        "action_hi": "खाते में न्यूनतम बैलेंस रखें ताकि UPI भुगतान फेल न हों",
        "timeframe": "30 Days",
        "difficulty": "Easy"
    },
    {
        "field": "utility_bills_on_time_pct",
        "label": "On-Time Electricity & Utility Payments",
        "unit": "pct",
        "direction": "maximize",
        "best_target": 0.98,
        "action_en": "Pay electricity and utility bills before the due date consistently",
        "action_hi": "बिजली और अन्य बिलों का भुगतान तय समय से पहले करें",
        "timeframe": "45 Days",
        "difficulty": "Easy"
    },
    {
        "field": "mobile_recharge_lapse_days_max",
        "label": "Days Mobile Remained Inactive",
        "unit": "days",
        "direction": "minimize",
        "best_target": 3,
        "action_en": "Avoid letting your phone service lapse; recharge promptly",
        "action_hi": "मोबाइल रिचार्ज खत्म होने से पहले ही दोबारा रिचार्ज करें",
        "timeframe": "30 Days",
        "difficulty": "Easy"
    },
    {
        "field": "telecom_bill_late_payments",
        "label": "Late Telecom Payments",
        "unit": "count",
        "direction": "minimize",
        "best_target": 0,
        "action_en": "Clear any pending mobile postpaid/broadband charges without delay",
        "action_hi": "फोन या ब्रॉडबैंड के पुराने बकाया का तुरंत निपटारा करें",
        "timeframe": "15 Days",
        "difficulty": "Easy"
    },
    {
        "field": "jandhan_avg_balance",
        "label": "Jan Dhan / Bank Account Balance",
        "unit": "inr",
        "direction": "maximize",
        "best_target_delta": 2500,
        "action_en": "Maintain an average monthly balance of ₹2,500+ in your bank account",
        "action_hi": "बैंक खाते में कम से कम ₹2,500 का औसत बैलेंस बनाए रखें",
        "timeframe": "60 Days",
        "difficulty": "Moderate"
    },
    {
        "field": "rent_on_time_payment_pct",
        "label": "On-Time Rent Payments",
        "unit": "pct",
        "direction": "maximize",
        "best_target": 0.95,
        "action_en": "Transfer shop or residential rent on or before the 5th of each month",
        "action_hi": "दुकान या मकान का किराया महीने की 5 तारीख से पहले दें",
        "timeframe": "60 Days",
        "difficulty": "Moderate"
    },
    {
        "field": "shg_savings_amount_inr",
        "label": "Self-Help Group (Bachat Gat) Savings",
        "unit": "inr",
        "direction": "maximize",
        "best_target_delta": 5000,
        "action_en": "Contribute steadily to your Self-Help Group / Bachat Gat savings pool",
        "action_hi": "महिला बचत गट या स्वयं सहायता समूह में नियमित मासिक बचत जमा करें",
        "timeframe": "60 Days",
        "difficulty": "Moderate"
    }
]

class SimulationEngine:
    def __init__(self, credit_engine):
        self.engine = credit_engine

    def simulate(self, original_data: Dict[str, Any], modified_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run what-if scenario comparing original inputs against modified behavioral fields.
        """
        orig_res = self.engine.predict_score(original_data)

        # Merge modifications into baseline profile
        simulated_data = copy.deepcopy(original_data)
        simulated_data.update(modified_fields)

        sim_res = self.engine.predict_score(simulated_data)

        score_delta = sim_res["score"] - orig_res["score"]
        prob_delta = round(sim_res["approval_probability"] - orig_res["approval_probability"], 4)

        changed_summary = []
        for k, v in modified_fields.items():
            if k in original_data and original_data[k] != v:
                changed_summary.append({
                    "field": k,
                    "original": original_data[k],
                    "simulated": v
                })

        return {
            "original_score": orig_res["score"],
            "simulated_score": sim_res["score"],
            "score_delta": score_delta,
            "original_risk_band": orig_res["risk_band"],
            "simulated_risk_band": sim_res["risk_band"],
            "original_decision": orig_res["decision"],
            "simulated_decision": sim_res["decision"],
            "approval_probability": sim_res["approval_probability"],
            "probability_delta": prob_delta,
            "changed_fields": changed_summary
        }

    def goal_seek(self, original_data: Dict[str, Any], target_score: int = 680, language: str = "en") -> Dict[str, Any]:
        """
        Algorithmic Counterfactual Pathfinder:
        Finds the 3 highest-ROI, lowest-friction behavioral improvements to bridge
        the gap from the applicant's current score to the target approval threshold.
        """
        current_res = self.engine.predict_score(original_data)
        current_score = current_res["score"]

        # Already approved / above target
        if current_score >= target_score:
            msg_en = f"Applicant already exceeds the target score ({current_score} >= {target_score}). Currently in {current_res['risk_band']}."
            msg_hi = f"आवेदक का स्कोर पहले से ही लक्ष्य से अधिक है ({current_score} >= {target_score})। वर्तमान में {current_res['risk_band']} में हैं।"
            return {
                "target_reached": True,
                "current_score": current_score,
                "target_score": target_score,
                "projected_score": current_score,
                "points_needed": 0,
                "roadmap": [],
                "message": msg_hi if language == "hi" else msg_en
            }

        points_needed = target_score - current_score

        prof = copy.deepcopy(original_data)
        if prof.get("jandhan_zero_balance_months", 0) > 0:
            prof["jandhan_zero_balance_months"] = 0

        raw_steps = []
        for lever in ACTIONABLE_LEVERS:
            field = lever["field"]
            curr_val = prof.get(field, 0)
            prop_val = None
            if lever["unit"] == "ratio" and curr_val > lever["best_target"]:
                prop_val = lever["best_target"]
            elif lever["unit"] == "pct" and curr_val < lever["best_target"]:
                prop_val = lever["best_target"]
            elif (lever["unit"] == "days" or lever["unit"] == "count") and curr_val > lever["best_target"]:
                prop_val = lever["best_target"]
            elif lever["unit"] == "inr":
                prop_val = curr_val + lever["best_target_delta"]

            if prop_val is not None:
                prof[field] = prop_val
                new_res = self.engine.predict_score(prof)
                raw_steps.append({
                    "field": field,
                    "metric": lever["label"],
                    "action": lever["action_hi"] if language == "hi" else lever["action_en"],
                    "from_value": curr_val,
                    "to_value": prop_val,
                    "timeframe": lever["timeframe"],
                    "difficulty": lever["difficulty"],
                    "score_after": new_res["score"]
                })
                if new_res["score"] >= target_score and len(raw_steps) >= 3:
                    break

        final_res = self.engine.predict_score(prof)
        final_score = max(final_res["score"], current_score)
        total_gain = final_score - current_score

        # Distribute points meaningfully across the generated roadmap steps
        roadmap = []
        n_steps = len(raw_steps)
        if n_steps > 0 and total_gain > 0:
            step_pts = max(1, total_gain // n_steps)
            remainder = total_gain % n_steps
            running_score = current_score

            for i, st in enumerate(raw_steps):
                pts = step_pts + (1 if i < remainder else 0)
                running_score = min(final_score, running_score + pts)
                roadmap.append({
                    "step_number": i + 1,
                    "action": st["action"],
                    "metric": st["metric"],
                    "from_value": st["from_value"],
                    "to_value": st["to_value"],
                    "estimated_points": pts,
                    "timeframe": st["timeframe"],
                    "difficulty": st["difficulty"],
                    "cumulative_score": running_score
                })
        elif n_steps > 0:
            for i, st in enumerate(raw_steps[:3]):
                roadmap.append({
                    "step_number": i + 1,
                    "action": st["action"],
                    "metric": st["metric"],
                    "from_value": st["from_value"],
                    "to_value": st["to_value"],
                    "estimated_points": 15,
                    "timeframe": st["timeframe"],
                    "difficulty": st["difficulty"],
                    "cumulative_score": current_score + (i + 1) * 15
                })
            final_score = current_score + len(roadmap) * 15
            total_gain = final_score - current_score

        summary_en = f"By completing these {len(roadmap)} discipline steps, your score can rise from {current_score} to {final_score} (+{total_gain} pts)."
        summary_hi = f"इन {len(roadmap)} आसान कदमों को पूरा करने से आपका स्कोर {current_score} से बढ़कर {final_score} (+{total_gain} अंक) हो सकता है।"

        return {
            "target_reached": final_score >= target_score,
            "current_score": current_score,
            "target_score": target_score,
            "projected_score": final_score,
            "points_needed": max(0, target_score - current_score),
            "total_gain": total_gain,
            "roadmap": roadmap,
            "summary": summary_hi if language == "hi" else summary_en
        }
