"""Integration test for dual-model specialist architecture.

Runs a single case that is known to benefit from specialist consultation
(FND-P03: FND superimposed on MS — the case where MedGemma scored 3/3
and all Qwen models scored 0/3).

Usage:
    # 1. Start both models (in a separate terminal):
    ./agent-platform/scripts/serve_dual.sh qwen3.5-9b medgemma-4b

    # 2. Run this test:
    uv run python agent-platform/scripts/test_dual_model.py

    # 3. Or run with mock server (no GPU needed):
    uv run python agent-platform/scripts/test_dual_model.py --mock
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agent-platform" / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import NeuroBenchCase

from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
from neuroagent.evaluation.metrics import MetricsCalculator
from neuroagent.evaluation.runner import format_patient_info
from neuroagent.llm.client import LLMClient
from neuroagent.rules.rules_engine import RulesEngine
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry


def load_case(case_id: str) -> NeuroBenchCase:
    """Load a case from v4 or v3 dataset."""
    for dataset in ["neurobench_v4", "neurobench_v3", "neurobench_v1"]:
        path = REPO_ROOT / "data" / dataset / "cases" / f"{case_id}.json"
        if path.exists():
            data = json.loads(path.read_text())
            return NeuroBenchCase.model_validate(data)
    raise FileNotFoundError(f"Case {case_id} not found in any dataset")


def test_mock_mode():
    """Test with MockServer — no GPU needed. Verifies tool registration and mock specialist."""
    print("=" * 70)
    print("  TEST 1: Mock mode (no GPU)")
    print("=" * 70)

    case = load_case("FND-P03")
    print(f"  Case: {case.case_id} ({case.condition.value}, {case.difficulty.value})")
    print(f"  Ground truth: {case.ground_truth.primary_diagnosis}")

    # Create registry WITH specialist (mock_server provides specialist responses)
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)

    tool_names = sorted(registry.tools.keys())
    print(f"\n  Registered tools ({len(tool_names)}):")
    for t in tool_names:
        marker = " ★" if t == "consult_medical_specialist" else ""
        print(f"    - {t}{marker}")

    assert "consult_medical_specialist" in registry.tools, \
        "FAIL: specialist tool not registered with mock_server"
    print("\n  ✓ Specialist tool registered in mock mode")

    # Test specialist tool directly
    from neuroagent.tools.base import ToolCall
    result = registry.execute(ToolCall(
        tool_name="consult_medical_specialist",
        parameters={
            "clinical_summary": (
                "45F with known RRMS (on natalizumab, stable 3 years). "
                "Presents with 2-week bilateral leg weakness and numbness. "
                "MRI brain and spine show NO new lesions. Exam shows "
                "bilateral give-way weakness, positive Hoover sign, "
                "tubular visual fields, and midline sensory splitting."
            ),
            "current_differential": [
                "MS relapse",
                "Secondary progressive MS",
                "Functional neurological disorder",
            ],
            "specific_question": (
                "The MRI is completely stable with no new lesions, but the "
                "patient has clear weakness on exam. Could this be functional "
                "neurological disorder superimposed on her known MS?"
            ),
        },
    ))

    print(f"\n  Specialist tool result:")
    print(f"    Success: {result.success}")
    if result.success and result.output:
        opinion = result.output.get("specialist_opinion", "")
        print(f"    Opinion length: {len(opinion)} chars")
        # Show first 300 chars
        preview = opinion[:300].replace("\n", "\n    ")
        print(f"    Preview:\n    {preview}...")
    else:
        print(f"    Error: {result.error_message}")

    assert result.success, f"FAIL: specialist mock call failed: {result.error_message}"
    assert result.output, "FAIL: specialist returned empty output"
    assert len(result.output.get("specialist_opinion", "")) > 50, \
        "FAIL: specialist opinion too short"
    print("\n  ✓ Mock specialist returns synthesized opinion from ground truth")

    # Verify the opinion mentions red herrings or key reasoning
    opinion_text = result.output.get("specialist_opinion", "").lower()
    has_useful_content = any(
        keyword in opinion_text
        for keyword in ["fnd", "functional", "ms", "stable", "hoover", "red flag",
                       "dual", "pathology", "give-way", "critique", "recommendation"]
    )
    assert has_useful_content, "FAIL: specialist opinion doesn't contain relevant clinical content"
    print("  ✓ Mock specialist opinion contains relevant clinical content")


def test_without_specialist():
    """Test that single-model mode still works (12 tools, no specialist)."""
    print("\n" + "=" * 70)
    print("  TEST 2: Single-model mode (backward compatibility)")
    print("=" * 70)

    case = load_case("FND-P03")

    # No mock_server, no specialist_client → 12 tools
    registry = ToolRegistry.create_default_registry(mock_server=None, specialist_client=None)
    tool_names = sorted(registry.tools.keys())
    print(f"  Registered tools: {len(tool_names)}")

    assert "consult_medical_specialist" not in registry.tools, \
        "FAIL: specialist should NOT be registered without mock_server or specialist_client"
    assert len(tool_names) == 12, f"FAIL: expected 12 tools, got {len(tool_names)}"
    print("  ✓ 12 tools registered (no specialist) — backward compatible")


def test_live_dual_model():
    """Test with live vLLM servers — requires both models running."""
    print("\n" + "=" * 70)
    print("  TEST 3: Live dual-model (requires GPU + both servers)")
    print("=" * 70)

    # Check if servers are running
    import urllib.request
    for port, name in [(8000, "orchestrator"), (8001, "specialist")]:
        try:
            urllib.request.urlopen(f"http://localhost:{port}/health", timeout=3)
            print(f"  ✓ {name} (port {port}) is healthy")
        except Exception:
            print(f"  ✗ {name} (port {port}) not reachable — skipping live test")
            print("    Start both with: ./agent-platform/scripts/serve_dual.sh")
            return False

    case = load_case("FND-P03")
    print(f"\n  Case: {case.case_id}")
    print(f"  Ground truth: {case.ground_truth.primary_diagnosis}")

    # Create specialist client
    specialist_client = LLMClient(
        base_url="http://localhost:8001/v1",
        api_key="not-needed",
        model="google/medgemma-1.5-4b-it",
        temperature=0.3,
        max_tokens=4096,
        presence_penalty=0.0,
    )

    # Create registry with mock_server (for diagnostic tools) + specialist_client (live)
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(
        mock_server=mock,
        specialist_client=specialist_client,
    )

    tool_names = sorted(registry.tools.keys())
    print(f"  Tools: {len(tool_names)} (including specialist)")
    assert "consult_medical_specialist" in registry.tools

    # Create orchestrator
    rules = RulesEngine(
        str(REPO_ROOT / "agent-platform" / "config" / "hospital_rules"),
        hospital="de_charite",
    )
    config = AgentConfig(
        base_url="http://localhost:8000/v1",
        model="Qwen/Qwen3.5-9B",
        specialist_enabled=True,
    )
    agent = AgentOrchestrator(
        config=config,
        tool_registry=registry,
        rules_engine=rules,
    )

    patient_info = format_patient_info(case)
    print(f"\n  Running agent (dual-model)...")
    t0 = time.time()
    trace = agent.run(patient_info=patient_info, case_id=case.case_id)
    elapsed = time.time() - t0

    print(f"\n  Results:")
    print(f"    Turns: {len(trace.turns)}")
    print(f"    Tool calls: {trace.total_tool_calls}")
    print(f"    Tools called: {trace.tools_called}")
    print(f"    Tokens: {trace.total_tokens}")
    print(f"    Time: {elapsed:.1f}s")

    specialist_calls = trace.tools_called.count("consult_medical_specialist")
    print(f"    Specialist consultations: {specialist_calls}")

    # Check if specialist was called
    if specialist_calls > 0:
        print("  ✓ Agent called the specialist tool!")
        # Find the specialist result in the trace
        for turn in trace.turns:
            if turn.tool_results:
                for tr in turn.tool_results:
                    if isinstance(tr, dict) and tr.get("tool_name") == "consult_medical_specialist":
                        opinion = tr.get("output", {}).get("specialist_opinion", "")
                        print(f"    Specialist opinion ({len(opinion)} chars):")
                        print(f"      {opinion[:200]}...")
    else:
        print("  ⚠ Agent did NOT call the specialist (may need prompt tuning)")

    # Check diagnosis
    calculator = MetricsCalculator()
    metrics = calculator.compute_all(trace, case.ground_truth)
    dx_correct = metrics.diagnostic_accuracy_top1
    print(f"\n    Diagnosis correct (top-1): {'✓ YES' if dx_correct else '✗ NO'}")
    print(f"    Safety score: {metrics.safety_score:.2f}")
    print(f"    Critical actions hit: {metrics.critical_actions_hit:.2f}")
    print(f"    Specialist calls: {metrics.specialist_calls}")

    if trace.final_response:
        print(f"\n    Final response (first 500 chars):")
        print(f"      {trace.final_response[:500]}...")

    return True


def test_specialist_tool_directly():
    """Test the specialist LLM call directly (bypass orchestrator)."""
    print("\n" + "=" * 70)
    print("  TEST 4: Direct specialist LLM call")
    print("=" * 70)

    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:8001/health", timeout=3)
        print("  ✓ Specialist server is healthy")
    except Exception:
        print("  ✗ Specialist server not reachable — skipping")
        return False

    from neuroagent.tools.medical_specialist import MedicalSpecialistTool

    specialist_client = LLMClient(
        base_url="http://localhost:8001/v1",
        api_key="not-needed",
        model="google/medgemma-1.5-4b-it",
        temperature=0.3,
        max_tokens=4096,
        presence_penalty=0.0,
    )

    tool = MedicalSpecialistTool(specialist_client=specialist_client)

    print("  Calling specialist with FND-on-MS question...")
    t0 = time.time()
    result = tool.execute({
        "clinical_summary": (
            "45F with 12-year RRMS on natalizumab (stable 3 years, last relapse 4 years ago). "
            "Presents with 2-week progressive bilateral leg weakness. MRI brain and spine "
            "completely stable — no new or enhancing lesions. Exam shows bilateral give-way "
            "weakness, positive Hoover sign bilaterally, tubular visual fields, midline "
            "sensory splitting. Old findings (right eye pallor from prior ON, brisk reflexes "
            "from prior myelitis) are STABLE from last visit."
        ),
        "current_differential": [
            "MS relapse",
            "Secondary progressive MS",
            "Spinal cord compression",
            "Functional neurological disorder",
        ],
        "specific_question": (
            "MRI is completely stable with no new lesions, but the patient has dramatic "
            "bilateral weakness on exam with positive functional signs (Hoover, give-way, "
            "midline splitting). Could this be FND superimposed on her known MS rather "
            "than an MS relapse or progression?"
        ),
    })
    elapsed = time.time() - t0

    print(f"  Response time: {elapsed:.1f}s")
    print(f"  Success: {result.success}")

    if result.success and result.output:
        opinion = result.output.get("specialist_opinion", "")
        print(f"  Opinion ({len(opinion)} chars):")
        print(f"  ---")
        # Print full opinion with indent
        for line in opinion.split("\n"):
            print(f"    {line}")
        print(f"  ---")

        # Check if MedGemma correctly identifies FND
        opinion_lower = opinion.lower()
        mentions_fnd = any(k in opinion_lower for k in ["functional", "fnd", "psychogenic", "conversion"])
        mentions_dual = any(k in opinion_lower for k in ["dual", "both", "coexist", "superimposed", "comorbid"])
        mentions_stable_mri = any(k in opinion_lower for k in ["stable", "no new", "unchanged"])

        print(f"\n  Content checks:")
        print(f"    Mentions FND/functional: {'✓' if mentions_fnd else '✗'}")
        print(f"    Mentions dual pathology: {'✓' if mentions_dual else '✗'}")
        print(f"    References stable MRI: {'✓' if mentions_stable_mri else '✗'}")

        if mentions_fnd:
            print("\n  ✓ Specialist correctly identified functional component!")
        else:
            print("\n  ⚠ Specialist did not clearly identify FND")
    else:
        print(f"  Error: {result.error_message}")

    return True


if __name__ == "__main__":
    mock_only = "--mock" in sys.argv

    print("\n" + "=" * 70)
    print("  DUAL-MODEL SPECIALIST — INTEGRATION TEST")
    print("=" * 70)

    # Tests that don't need GPU
    test_mock_mode()
    test_without_specialist()

    if not mock_only:
        # Tests that need live servers
        test_specialist_tool_directly()
        test_live_dual_model()
    else:
        print("\n  [Skipping live tests — use without --mock to run them]")

    print("\n" + "=" * 70)
    print("  ALL TESTS PASSED" if mock_only else "  TESTS COMPLETE")
    print("=" * 70 + "\n")
