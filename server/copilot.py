"""
EquiScore AI — Multilingual Gemini Copilot Engine
Translates monotonic ML scores and TreeSHAP explainability into empathetic,
plain-spoken guidance in English and Hindi for Indian gig workers, SHG members,
and new-to-credit borrowers. Adheres strictly to RBI Fair Practices Code.
"""

import json
import logging
import requests
from typing import List, Dict, Any, Optional
from server.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger("equiscore.copilot")

SYSTEM_PROMPT = """You are the EquiScore AI Credit Copilot — a trustworthy, empathetic financial advisor built for everyday Indian borrowers (gig delivery workers, auto drivers, self-help group/Bachat Gat members, rural artisans, and youth with no traditional CIBIL history).

CRITICAL UNDERWRITING & RBI COMPLIANCE RULES:
1. Ground truth: The scoring engine produces the score (300-850) and decision based on verified alternative data (UPI, utility bills, Jan Dhan savings, microfinance). You EXPLAIN the score; you do not invent or alter numbers.
2. Empathy & Dignity: Never shame low-income or distressed borrowers. Acknowledge hard work and provide concrete, achievable steps to build creditworthiness.
3. No False Promises: Never guarantee loan approval. Always use phrases like "based on your current cashflow data" or "the underwriting engine estimates".
4. Language Adaptability:
   - If language is 'hi', respond in respectful, clear Hindi (using Devanagari script) or natural Hinglish where appropriate.
   - If language is 'en', respond in clear, accessible English (avoid confusing Wall-Street banking jargon; use terms like 'savings reserve', 'bill discipline', 'UPI payments').
5. Output Format: Always return valid, clean JSON with the required keys requested in the user prompt. Do NOT wrap in markdown backticks if possible, or provide valid JSON inside.
"""

class CopilotEngine:
    def __init__(self, api_key: str = GEMINI_API_KEY, model_name: str = GEMINI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def _call_gemini(self, prompt: str) -> str:
        """Execute request to Google Gemini API."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured in server environment.")

        url = f"{self.endpoint}?key={self.api_key}"
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2500,
                "responseMimeType": "application/json"
            }
        }

        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
        if response.status_code != 200:
            logger.error(f"Gemini API error ({response.status_code}): {response.text}")
            raise RuntimeError(f"Gemini API call failed with status {response.status_code}: {response.text}")

        res_json = response.json()
        candidates = res_json.get("candidates", [])
        if not candidates:
            raise RuntimeError("Gemini returned empty response candidates.")

        text_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return text_content

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        """Robust JSON extraction handling markdown blocks or whitespace."""
        clean = text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            clean = "\n".join(lines).strip()
        try:
            return json.loads(clean)
        except Exception:
            start = clean.find("{")
            end = clean.rfind("}")
            if start != -1 and end != -1 and end > start:
                return json.loads(clean[start:end+1])
            raise

    def explain_score(self, score_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        """
        Generate a comprehensive, plain-language assessment of the applicant's credit score,
        highlighting positive drivers, risk points, and concrete improvement paths.
        """
        lang_instruction = "Respond entirely in Hindi (हिंदी / Devanagari)." if language == "hi" else "Respond in clear English."

        prompt = f"""
Applicant Assessment Data:
- EquiScore: {score_data.get('score')} (Scale: 300 to 850)
- Decision: {score_data.get('decision')}
- Risk Tier: {score_data.get('risk_band')}
- Calibrated Approval Probability: {round(score_data.get('approval_probability', 0) * 100, 1)}%
- Top Positive Factors (Credit Builders): {json.dumps(score_data.get('top_positive_factors', []))}
- Top Negative Factors (Risk Flags): {json.dumps(score_data.get('top_negative_factors', []))}
- Recommendation: {score_data.get('recommendation')}

Task:
Generate a structured JSON assessment with:
1. "summary": A warm 2-3 sentence overview explaining why the applicant received this score and what it means for loan eligibility.
2. "key_strengths": List of 2 bullet points describing their strongest financial habits.
3. "actionable_steps": List of 3 specific, practical steps they can take in the next 30-60 days to boost their score (focusing directly on their negative factors).
4. "loan_guidance": 1 sentence giving realistic borrowing guidance (e.g. eligible for prime micro-loan up to ₹50,000 vs. start with a ₹10,000 credit line).

{lang_instruction}
Return pure JSON matching this exact schema:
{{
  "summary": "string",
  "key_strengths": ["string", "string"],
  "actionable_steps": ["string", "string", "string"],
  "loan_guidance": "string"
}}
"""
        raw_text = self._call_gemini(prompt)
        return self._parse_json(raw_text)

    def chat(self, score_data: Dict[str, Any], query: str, history: Optional[List[Dict[str, str]]] = None, language: str = "en") -> Dict[str, Any]:
        """
        Interactive multi-turn conversational Q&A answering the applicant's financial queries.
        """
        lang_instruction = "Respond in Hindi (हिंदी / Devanagari)." if language == "hi" else "Respond in clear English."
        history_str = json.dumps(history[-4:]) if history else "[]"

        prompt = f"""
Current Applicant Financial Profile:
- EquiScore: {score_data.get('score')}
- Decision: {score_data.get('decision')} ({score_data.get('risk_band')})
- Approval Chance: {round(score_data.get('approval_probability', 0) * 100, 1)}%
- Top Positive Factors: {json.dumps(score_data.get('top_positive_factors', []))}
- Top Negative Factors: {json.dumps(score_data.get('top_negative_factors', []))}

Recent Conversation History:
{history_str}

User's Question:
"{query}"

Instructions:
Answer the user's question directly, honestly, and encouragingly in 2-4 sentences.
If they ask about loan approval, remind them that lenders look for consistent payments.
Suggest 2 related quick follow-up questions they might want to ask next.
{lang_instruction}

Return pure JSON matching this exact schema:
{{
  "answer": "string",
  "suggested_followups": ["string", "string"]
}}
"""
        raw_text = self._call_gemini(prompt)
        return self._parse_json(raw_text)
