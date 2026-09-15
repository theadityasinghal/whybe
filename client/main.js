const API_URL = "http://127.0.0.1:8000";

const PRESETS = {
  urban_gig_worker: {
    age: 29, monthly_income_inr: 28500, area_type: "Urban",
    upi_monthly_avg_txn_count: 85, upi_avg_txn_amount: 340, upi_failed_txn_ratio: 0.02,
    mobile_recharge_consistency_score: 0.95, mobile_recharge_lapse_days_max: 5,
    utility_bills_on_time_pct: 0.94, electricity_bill_avg_amount: 1850,
    cooperative_meeting_attendance_pct: 0.0, shg_savings_amount_inr: 0,
    microfinance_loans_repaid_count: 2, microfinance_default_rate: 0.0,
    gig_monthly_earnings: 24000, gig_platform_rating: 4.8,
    jandhan_avg_balance: 2500, jandhan_zero_balance_months: 0,
    monthly_data_usage_gb: 18.5, telecom_bill_late_payments: 0,
    banking_app_login_frequency_monthly: 45, fintech_apps_count: 5,
    rent_on_time_payment_pct: 0.95, rent_to_income_ratio: 0.22,
    social_referral_count: 4, insurance_policy_count: 1
  },
  rural_shg_member: {
    age: 38, monthly_income_inr: 14500, area_type: "Rural",
    upi_monthly_avg_txn_count: 35, upi_avg_txn_amount: 210, upi_failed_txn_ratio: 0.03,
    mobile_recharge_consistency_score: 0.88, mobile_recharge_lapse_days_max: 12,
    utility_bills_on_time_pct: 0.85, electricity_bill_avg_amount: 850,
    cooperative_meeting_attendance_pct: 0.85, shg_savings_amount_inr: 32000,
    microfinance_loans_repaid_count: 6, microfinance_default_rate: 0.01,
    gig_monthly_earnings: 0, gig_platform_rating: 0,
    jandhan_avg_balance: 3800, jandhan_zero_balance_months: 1,
    monthly_data_usage_gb: 4.5, telecom_bill_late_payments: 1,
    banking_app_login_frequency_monthly: 15, fintech_apps_count: 2,
    rent_on_time_payment_pct: 0.80, rent_to_income_ratio: 0.12,
    social_referral_count: 8, insurance_policy_count: 2
  },
  distressed_high_risk: {
    age: 42, monthly_income_inr: 11000, area_type: "Semi-Urban",
    upi_monthly_avg_txn_count: 12, upi_avg_txn_amount: 120, upi_failed_txn_ratio: 0.32,
    mobile_recharge_consistency_score: 0.25, mobile_recharge_lapse_days_max: 65,
    utility_bills_on_time_pct: 0.35, electricity_bill_avg_amount: 2400,
    cooperative_meeting_attendance_pct: 0.1, shg_savings_amount_inr: 0,
    microfinance_loans_repaid_count: 0, microfinance_default_rate: 0.28,
    gig_monthly_earnings: 0, gig_platform_rating: 0,
    jandhan_avg_balance: 150, jandhan_zero_balance_months: 7,
    monthly_data_usage_gb: 3.0, telecom_bill_late_payments: 8,
    banking_app_login_frequency_monthly: 2, fintech_apps_count: 0,
    rent_on_time_payment_pct: 0.25, rent_to_income_ratio: 0.65,
    social_referral_count: 0, insurance_policy_count: 0
  }
};

// Plain-language dictionary for model features (Easy for everyday workers & laborers)
const FRIENDLY_LABELS = {
  mobile_recharge_consistency_score: "Timely phone recharges",
  mobile_recharge_lapse_days_max: "Days phone stayed inactive",
  utility_bills_on_time_pct: "On-time electricity & bill payments",
  electricity_bill_avg_amount: "Household electricity bills",
  telecom_bill_late_payments: "Late phone bill payments",
  telecom_stress_flag: "Frequent phone disconnection flag",
  upi_monthly_avg_txn_count: "Frequent QR / UPI payments",
  upi_avg_txn_amount: "Average UPI payment size",
  upi_failed_txn_ratio: "UPI payments failed (low balance)",
  est_monthly_upi_volume: "Total monthly UPI transactions",
  upi_to_income_ratio: "UPI payment to income share",
  banking_app_login_frequency_monthly: "Regular bank passbook checks",
  fintech_apps_count: "Financial apps on smartphone",
  monthly_data_usage_gb: "Active smartphone internet use",
  cooperative_meeting_attendance_pct: "Bachat Gat / Co-op attendance",
  shg_savings_amount_inr: "Accumulated group savings",
  microfinance_loans_repaid_count: "Past group loans repaid in full",
  microfinance_default_rate: "Missed past loan payments",
  microfinance_net_score: "Proven loan repayment track record",
  jandhan_avg_balance: "Jan Dhan account balance",
  jandhan_zero_balance_months: "Months with zero bank balance",
  total_liquid_savings: "Total cash & group savings",
  liquidity_buffer_months: "Emergency savings reserve",
  discipline_composite_index: "Overall bill payment discipline",
  total_monthly_inflow: "Combined monthly earnings",
  rent_on_time_payment_pct: "On-time rent payments",
  rent_to_income_ratio: "Share of income spent on rent",
  social_referral_count: "Peer & elder community references",
  insurance_policy_count: "Active insurance protection policies",
  monthly_income_inr: "Steady monthly income",
  gig_monthly_earnings: "Earnings from delivery/cab work",
  gig_platform_rating: "High gig app rating & discipline",
  age: "Applicant age factor"
};

function updateSliderPct(labelId, val) {
  const el = document.getElementById(labelId);
  if (el) el.innerText = `${Math.round(parseFloat(val) * 100)}%`;
}

function updateSlider(labelId, val) {
  const el = document.getElementById(labelId);
  if (el) el.innerText = parseFloat(val).toFixed(2);
}

function loadPersona(key) {
  const d = PRESETS[key];
  if (!d) return;

  for (const [k, v] of Object.entries(d)) {
    const el = document.getElementById(k);
    if (el) el.value = v;
  }

  updateSliderPct('recharge_cons_val', d.mobile_recharge_consistency_score);
  updateSliderPct('util_ontime_val', d.utility_bills_on_time_pct);
  updateSliderPct('upi_failed_val', d.upi_failed_txn_ratio);
  updateSliderPct('coop_att_val', d.cooperative_meeting_attendance_pct);
  updateSliderPct('mfi_def_val', d.microfinance_default_rate);
  updateSliderPct('rent_ontime_val', d.rent_on_time_payment_pct);
  updateSliderPct('rent_ratio_val', d.rent_to_income_ratio);

  evaluateApplicant();
}

function getPayload() {
  const parseVal = (id, defaultVal = 0, isFloat = false) => {
    const el = document.getElementById(id);
    if (!el || el.value === "" || isNaN(el.value)) return defaultVal;
    return isFloat ? parseFloat(el.value) : parseInt(el.value, 10);
  };

  return {
    age: parseVal('age', 29),
    monthly_income_inr: parseVal('monthly_income_inr', 25000, true),
    area_type: document.getElementById('area_type') ? document.getElementById('area_type').value : "Urban",
    upi_monthly_avg_txn_count: parseVal('upi_monthly_avg_txn_count', 0),
    upi_avg_txn_amount: parseVal('upi_avg_txn_amount', 0, true),
    upi_failed_txn_ratio: parseVal('upi_failed_txn_ratio', 0, true),
    mobile_recharge_consistency_score: parseVal('mobile_recharge_consistency_score', 1.0, true),
    mobile_recharge_lapse_days_max: parseVal('mobile_recharge_lapse_days_max', 0),
    utility_bills_on_time_pct: parseVal('utility_bills_on_time_pct', 1.0, true),
    electricity_bill_avg_amount: parseVal('electricity_bill_avg_amount', 0, true),
    cooperative_meeting_attendance_pct: parseVal('cooperative_meeting_attendance_pct', 0, true),
    shg_savings_amount_inr: parseVal('shg_savings_amount_inr', 0, true),
    microfinance_loans_repaid_count: parseVal('microfinance_loans_repaid_count', 0),
    microfinance_default_rate: parseVal('microfinance_default_rate', 0, true),
    gig_monthly_earnings: parseVal('gig_monthly_earnings', 0, true),
    gig_platform_rating: parseVal('gig_platform_rating', 0, true),
    jandhan_avg_balance: parseVal('jandhan_avg_balance', 0, true),
    jandhan_zero_balance_months: parseVal('jandhan_zero_balance_months', 0),
    monthly_data_usage_gb: parseVal('monthly_data_usage_gb', 0, true),
    telecom_bill_late_payments: parseVal('telecom_bill_late_payments', 0),
    banking_app_login_frequency_monthly: parseVal('banking_app_login_frequency_monthly', 0),
    fintech_apps_count: parseVal('fintech_apps_count', 0),
    rent_on_time_payment_pct: parseVal('rent_on_time_payment_pct', 1.0, true),
    rent_to_income_ratio: parseVal('rent_to_income_ratio', 0, true),
    social_referral_count: parseVal('social_referral_count', 0),
    insurance_policy_count: parseVal('insurance_policy_count', 0)
  };
}

let debounceTimer = null;
function debouncedEvaluate() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(evaluateApplicant, 100);
}

async function evaluateApplicant() {
  const payload = getPayload();
  const statusEl = document.getElementById('calcStatus');
  if (statusEl) statusEl.innerText = "Updating score...";

  try {
    const res = await fetch(`${API_URL}/api/score`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      if (statusEl) statusEl.innerText = "Score Range: 300 to 850";
      return;
    }

    const data = await res.json();
    renderScore(data);
    renderFactors(data);
    if (statusEl) statusEl.innerText = "Score Range: 300 to 850";
  } catch (err) {
    console.error("Backend connection failed:", err);
    showBackendError();
  }
}

function showBackendError() {
  const scoreEl = document.getElementById('scoreVal');
  const badgeEl = document.getElementById('decisionBadge');
  const rec = document.getElementById('scoreRecommendation');
  const statusEl = document.getElementById('calcStatus');

  if (statusEl) statusEl.innerText = "Service unavailable";
  if (scoreEl) scoreEl.innerText = "--";
  if (badgeEl) {
    badgeEl.className = "decision-pill declined";
    badgeEl.innerText = "SERVER OFFLINE";
  }
  if (rec) {
    rec.innerHTML = `Credit service is not currently running. To start it, run: <code style="color:#ffffff; font-family:var(--font-mono); background:#1a1a1a; padding:2px 6px; border-radius:4px;">npm run dev</code>`;
  }
}

function renderScore(data) {
  const scoreEl = document.getElementById('scoreVal');
  const badgeEl = document.getElementById('decisionBadge');
  const meter = document.getElementById('meterFill');
  const rec = document.getElementById('scoreRecommendation');

  scoreEl.innerText = data.score;

  // Convert recommendation text to friendly guidance if needed
  rec.innerText = data.recommendation;

  const pct = Math.min(100, Math.max(0, ((data.score - 300) / (850 - 300)) * 100));
  meter.style.width = `${pct}%`;

  if (data.score >= 680) {
    meter.style.backgroundColor = "var(--accent-green)";
    badgeEl.className = "decision-pill approved";
    badgeEl.innerText = `APPROVED · LOW RISK`;
  } else if (data.score >= 580) {
    meter.style.backgroundColor = "var(--accent-amber)";
    badgeEl.className = "decision-pill review";
    badgeEl.innerText = `CONDITIONAL · MODERATE RISK`;
  } else {
    meter.style.backgroundColor = "var(--accent-red)";
    badgeEl.className = "decision-pill declined";
    badgeEl.innerText = `NEEDS REVIEW · HIGH RISK`;
  }
}

function getFriendlyLabel(featureName, fallbackLabel) {
  if (FRIENDLY_LABELS[featureName]) {
    return FRIENDLY_LABELS[featureName];
  }
  return fallbackLabel || featureName.replace(/_/g, ' ');
}

function renderFactors(data) {
  const bList = document.getElementById('boostersList');
  const aList = document.getElementById('adverseList');

  if (data.top_positive_factors && data.top_positive_factors.length > 0) {
    bList.innerHTML = data.top_positive_factors.map(f => {
      const friendlyName = getFriendlyLabel(f.feature, f.label);
      const impactPts = Math.round(Math.abs(f.shap_value) * 100);
      return `
        <div class="factor-item factor-pos">
          <span class="factor-label">${friendlyName}</span>
          <span class="factor-value">+${impactPts} pts</span>
        </div>
      `;
    }).join('');
  } else {
    bList.innerHTML = `<div class="factor-empty">No positive factors detected yet</div>`;
  }

  if (data.top_negative_factors && data.top_negative_factors.length > 0) {
    aList.innerHTML = data.top_negative_factors.map(f => {
      const friendlyName = getFriendlyLabel(f.feature, f.label);
      const impactPts = Math.round(Math.abs(f.shap_value) * 100);
      return `
        <div class="factor-item factor-neg">
          <span class="factor-label">${friendlyName}</span>
          <span class="factor-value">-${impactPts} pts</span>
        </div>
      `;
    }).join('');
  } else {
    aList.innerHTML = `<div class="factor-empty">No negative factors identified</div>`;
  }
}

// Interactive Tooltip Engine (Accessible on hover, focus, and mobile click)
function initTooltips() {
  const tooltipEl = document.getElementById('globalTooltip');
  if (!tooltipEl) return;

  const infoButtons = document.querySelectorAll('.info-btn');

  const showTooltip = (btn) => {
    const text = btn.getAttribute('data-tooltip');
    if (!text) return;

    tooltipEl.textContent = text;
    tooltipEl.classList.add('show');
    tooltipEl.setAttribute('aria-hidden', 'false');

    const rect = btn.getBoundingClientRect();
    const tooltipWidth = 260;
    
    // Position calculation
    let top = rect.top + window.scrollY - tooltipEl.offsetHeight - 8;
    let left = rect.left + window.scrollX - (tooltipWidth / 2) + (rect.width / 2);

    // Keep within screen horizontally
    if (left < 16) left = 16;
    if (left + tooltipWidth > window.innerWidth - 16) {
      left = window.innerWidth - tooltipWidth - 16;
    }

    // If too close to top, show below the button
    if (rect.top < tooltipEl.offsetHeight + 16) {
      top = rect.bottom + window.scrollY + 8;
    }

    tooltipEl.style.top = `${top}px`;
    tooltipEl.style.left = `${left}px`;
  };

  const hideTooltip = () => {
    tooltipEl.classList.remove('show');
    tooltipEl.setAttribute('aria-hidden', 'true');
  };

  infoButtons.forEach(btn => {
    btn.addEventListener('mouseenter', () => showTooltip(btn));
    btn.addEventListener('mouseleave', hideTooltip);
    btn.addEventListener('focus', () => showTooltip(btn));
    btn.addEventListener('blur', hideTooltip);
    
    // Mobile tap support
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (tooltipEl.classList.contains('show')) {
        hideTooltip();
      } else {
        showTooltip(btn);
      }
    });
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.info-btn')) {
      hideTooltip();
    }
  });

  window.addEventListener('scroll', hideTooltip, { passive: true });
}

window.addEventListener('DOMContentLoaded', () => {
  const formElements = document.querySelectorAll('#scoringForm input, #scoringForm select');
  formElements.forEach(el => {
    el.addEventListener('input', debouncedEvaluate);
    el.addEventListener('change', debouncedEvaluate);
  });

  initTooltips();
  evaluateApplicant();
});
