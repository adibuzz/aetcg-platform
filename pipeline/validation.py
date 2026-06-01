import re
import json
import os
from pydantic import BaseModel, Field, field_validator

class TicketIngestionSchema(BaseModel):
    ticket_id: str = Field(..., description="Unique alphanumeric tracking string.")
    reporter_email: str = Field(..., description="Corporate sender communication handle.")
    raw_text: str = Field(..., description="Unstructured description text payload.")

    @field_validator('reporter_email')
    @classmethod
    def validate_corporate_domain(cls, value: str) -> str:
        if not value.endswith("@enterprise.com"):
            raise ValueError("Ingestion restricted to internal corporate system users.")
        return value

class DataSanitizationPipeline:
    def __init__(self, dlq_path: str = "dead_letter_queue.log"):
        self.dlq_path = dlq_path
        # Milestone 2: Explicit Regex Patterns for Credit Card and SSN Scrubbing
        self.pii_patterns = {
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b')
        }

    def scrub_pii(self, text: str) -> str:
        sanitized = text
        for label, pattern in self.pii_patterns.items():
            sanitized = pattern.sub(f"[{label.upper()}_REDACTED]", sanitized)
        return sanitized

    def route_to_dlq(self, error_message: str, unvalidated_payload: dict):
        with open(self.dlq_path, "a") as dlq_file:
            entry = {
                "error": error_message,
                "payload": unvalidated_payload
            }
            dlq_file.write(json.dumps(entry) + "\n")