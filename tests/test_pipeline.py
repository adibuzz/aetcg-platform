import pytest
from pipeline.validation import TicketIngestionSchema, DataSanitizationPipeline

def test_pydantic_corporate_domain_enforcement():
    valid_data = {
        "ticket_id": "TCK-101",
        "reporter_email": "engineer@enterprise.com",
        "raw_text": "System logs show standard disk allocations exceeding 85% thresholds."
    }
    schema = TicketIngestionSchema(**valid_data)
    assert schema.reporter_email == "engineer@enterprise.com"

    invalid_data = {
        "ticket_id": "TCK-102",
        "reporter_email": "adversary@gmail.com",
        "raw_text": "Attempted arbitrary cross-domain payload pipeline inject."
    }
    with pytest.raises(ValueError, match="Ingestion restricted to internal corporate system users."):
        TicketIngestionSchema(**invalid_data)

def test_regex_pii_scrubbing_pipeline():
    pipeline = DataSanitizationPipeline(dlq_path="tests/mock_dlq.log")
    dirty_text = "Urgent: Customer identity verification details matched SSN: 000-12-3456 profile."
    
    clean_text = pipeline.scrub_pii(dirty_text)
    assert "000-12-3456" not in clean_text
    assert "[SSN_REDACTED]" in clean_text

    if os.path.exists("tests/mock_dlq.log"):
        os.remove("tests/mock_dlq.log")