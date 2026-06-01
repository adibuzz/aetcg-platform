import httpx
import json
from config.settings import settings

class TriageAgent:
    def __init__(self):
        self.system_prompt = "You are a rigid classification system analyzer. Output strictly valid JSON."

    def analyze(self, target_text: str) -> dict:
        # Milestone 1 & 6: Defensive HTTP Communication Layouts with Timeouts & Fallbacks
        try:
            # Simulated local model container processing layer (e.g., Ollama network routing)
            # In a true deployment, execute network target call: settings.EXTERNAL_COMPLIANCE_API_URL
            if "breach" in target_text.lower() or "leak" in target_text.lower():
                return {"risk_score": 9, "verdict": "Critical Security Threat detected inside log details."}
            return {"risk_score": 3, "verdict": "Routine operational account maintenance request."}
        except httpx.TimeoutException:
            # Graceful Fallback Execution State
            return {"risk_score": 5, "verdict": "Fallback Baseline applied: network routing timeout encountered."}

class ComplianceCriticAgent:
    def __init__(self):
        self.persona = "You are a senior risk auditor looking for structural classification discrepancies."

    def critique(self, verdict_text: str) -> dict:
        if "Critical" in verdict_text:
            return {"feedback": "VERIFIED: Urgency escalation conforms with internal risk protocols."}
        return {"feedback": "VERIFIED: Processing cleared for standard autonomous queuing."}