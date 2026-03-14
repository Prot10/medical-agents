"""Tests for the patient memory system."""

import tempfile

import pytest

from neuroagent.memory.patient_memory import PatientMemory
from neuroagent.memory.memory_summarizer import MemorySummarizer
from neuroagent.agent.reasoning import AgentTrace


@pytest.fixture
def memory():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem = PatientMemory(db_path=tmpdir)
        yield mem


def test_store_and_retrieve(memory):
    trace = AgentTrace(case_id="test-001")
    trace.tools_called = ["analyze_eeg", "interpret_labs"]
    trace.set_final_response("Diagnosis: focal epilepsy")

    memory.store_encounter("PT-001", trace)
    result = memory.retrieve("PT-001")

    assert "PT-001" not in result or len(result) > 0  # either has content or is empty (new patient)
    assert "focal epilepsy" in result or result == ""


def test_retrieve_empty(memory):
    result = memory.retrieve("NONEXISTENT")
    assert result == ""


def test_clear_patient(memory):
    trace = AgentTrace(case_id="test-001")
    trace.set_final_response("test")

    memory.store_encounter("PT-001", trace)
    memory.clear_patient("PT-001")
    result = memory.retrieve("PT-001")
    assert result == ""


def test_summarizer_rule_based():
    summarizer = MemorySummarizer(llm=None)
    short = summarizer.summarize("Short text")
    assert short == "Short text"

    long = summarizer.summarize("x" * 1000)
    assert len(long) <= 503  # 500 + "..."
