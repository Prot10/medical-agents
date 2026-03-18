"""Tests for the CostTracker — parameter-dependent cost computation."""

import pytest

from neuroagent.tools.cost_tracker import CostTracker, ToolCostEntry


@pytest.fixture
def tracker() -> CostTracker:
    return CostTracker()


class TestCostTrackerBasicCosts:
    """Test flat-rate tools."""

    def test_ecg_base_cost(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_ecg", {"clinical_context": "syncope"})
        assert entry.cost_usd == 20.0
        assert entry.cost_breakdown == {"base": 20.0}

    def test_literature_search_free(self, tracker: CostTracker):
        entry = tracker.compute_cost("search_medical_literature", {"query": "epilepsy"})
        assert entry.cost_usd == 0.0

    def test_drug_interactions_free(self, tracker: CostTracker):
        entry = tracker.compute_cost("check_drug_interactions", {"drug": "levetiracetam"})
        assert entry.cost_usd == 0.0

    def test_unknown_tool_zero_cost(self, tracker: CostTracker):
        entry = tracker.compute_cost("nonexistent_tool", {})
        assert entry.cost_usd == 0.0


class TestCostTrackerMRI:
    """Test MRI cost with contrast modifier."""

    def test_mri_no_contrast(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_brain_mri", {"protocol": "standard"})
        assert entry.cost_usd == 320.0
        assert "base" in entry.cost_breakdown
        assert "contrast" not in entry.cost_breakdown

    def test_mri_with_contrast(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_brain_mri", {"contrast": True, "protocol": "ms"})
        assert entry.cost_usd == 446.0
        assert entry.cost_breakdown["base"] == 320.0
        assert entry.cost_breakdown["contrast"] == 126.0

    def test_mri_protocol_doesnt_change_cost(self, tracker: CostTracker):
        e1 = tracker.compute_cost("analyze_brain_mri", {"protocol": "standard"})
        tracker.reset()
        e2 = tracker.compute_cost("analyze_brain_mri", {"protocol": "epilepsy"})
        assert e1.cost_usd == e2.cost_usd


class TestCostTrackerEEG:
    """Test EEG cost by type."""

    def test_routine_eeg(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_eeg", {"eeg_type": "routine"})
        assert entry.cost_usd == 250.0

    def test_video_eeg(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_eeg", {"eeg_type": "video"})
        assert entry.cost_usd == 1200.0

    def test_ambulatory_eeg(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_eeg", {"eeg_type": "ambulatory"})
        assert entry.cost_usd == 700.0

    def test_continuous_icu_eeg(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_eeg", {"eeg_type": "continuous_icu"})
        assert entry.cost_usd == 900.0

    def test_default_eeg_type_is_routine(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_eeg", {})
        assert entry.cost_usd == 250.0


class TestCostTrackerLabs:
    """Test labs with per-panel costs."""

    def test_basic_panels(self, tracker: CostTracker):
        entry = tracker.compute_cost("interpret_labs", {"panels": ["CBC", "BMP"]})
        assert entry.cost_usd == 35.0  # 15 + 20
        assert entry.cost_breakdown["CBC"] == 15.0
        assert entry.cost_breakdown["BMP"] == 20.0

    def test_specialized_panel_expensive(self, tracker: CostTracker):
        entry = tracker.compute_cost("interpret_labs", {
            "panels": ["CBC", "autoimmune_encephalitis"],
        })
        assert entry.cost_usd == 2015.0  # 15 + 2000

    def test_empty_panels_default_cost(self, tracker: CostTracker):
        entry = tracker.compute_cost("interpret_labs", {})
        assert entry.cost_usd == 25.0  # default_panel
        assert "unspecified" in entry.cost_breakdown

    def test_unknown_panel_uses_default(self, tracker: CostTracker):
        entry = tracker.compute_cost("interpret_labs", {"panels": ["custom_panel"]})
        assert entry.cost_usd == 25.0  # default_panel cost


class TestCostTrackerCSF:
    """Test CSF with base + special test costs."""

    def test_csf_base_only(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_csf", {"clinical_context": "meningitis"})
        assert entry.cost_usd == 250.0
        assert entry.cost_breakdown["base"] == 250.0

    def test_csf_with_special_tests(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_csf", {
            "special_tests": ["oligoclonal_bands", "HSV_PCR"],
        })
        assert entry.cost_usd == 475.0  # 250 + 25 + 200
        assert entry.cost_breakdown["base"] == 250.0
        assert entry.cost_breakdown["oligoclonal_bands"] == 25.0
        assert entry.cost_breakdown["HSV_PCR"] == 200.0

    def test_csf_autoimmune_panel(self, tracker: CostTracker):
        entry = tracker.compute_cost("analyze_csf", {
            "special_tests": ["autoimmune_panel"],
        })
        assert entry.cost_usd == 2250.0  # 250 + 2000


class TestCostTrackerCT:
    """Test CT scan with modifiers."""

    def test_ct_plain(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_ct_scan", {})
        assert entry.cost_usd == 200.0

    def test_ct_with_contrast(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_ct_scan", {"contrast": True})
        assert entry.cost_usd == 300.0

    def test_cta(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_ct_scan", {"angiography": True})
        assert entry.cost_usd == 400.0

    def test_cta_with_contrast(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_ct_scan", {"contrast": True, "angiography": True})
        assert entry.cost_usd == 500.0


class TestCostTrackerNewTools:
    """Test new tool types (echo, cardiac monitoring, advanced, specialized)."""

    def test_echo_tte(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_echocardiogram", {"echo_type": "TTE"})
        assert entry.cost_usd == 300.0

    def test_echo_tee(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_echocardiogram", {"echo_type": "TEE"})
        assert entry.cost_usd == 600.0

    def test_echo_default_tte(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_echocardiogram", {})
        assert entry.cost_usd == 300.0

    def test_holter(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_cardiac_monitoring", {"monitor_type": "holter_24h"})
        assert entry.cost_usd == 150.0

    def test_event_monitor(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_cardiac_monitoring", {"monitor_type": "event_monitor_30d"})
        assert entry.cost_usd == 300.0

    def test_amyloid_pet(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_advanced_imaging", {"imaging_type": "amyloid_PET"})
        assert entry.cost_usd == 4000.0

    def test_datscan(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_advanced_imaging", {"imaging_type": "DaTscan"})
        assert entry.cost_usd == 5000.0

    def test_neuropsych(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_specialized_test", {"test_type": "neuropsych_battery"})
        assert entry.cost_usd == 1200.0

    def test_emg(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_specialized_test", {"test_type": "emg_ncs"})
        assert entry.cost_usd == 600.0

    def test_vep(self, tracker: CostTracker):
        entry = tracker.compute_cost("order_specialized_test", {"test_type": "vep"})
        assert entry.cost_usd == 200.0


class TestCostTrackerAccumulation:
    """Test total cost accumulation and reset."""

    def test_accumulates_multiple_calls(self, tracker: CostTracker):
        tracker.compute_cost("analyze_ecg", {})
        tracker.compute_cost("analyze_brain_mri", {"contrast": True})
        tracker.compute_cost("interpret_labs", {"panels": ["CBC", "BMP"]})
        assert tracker.total_cost_usd == 20.0 + 446.0 + 35.0
        assert len(tracker.entries) == 3

    def test_reset_clears(self, tracker: CostTracker):
        tracker.compute_cost("analyze_ecg", {})
        tracker.compute_cost("analyze_brain_mri", {})
        assert len(tracker.entries) == 2
        tracker.reset()
        assert len(tracker.entries) == 0
        assert tracker.total_cost_usd == 0.0

    def test_get_summary(self, tracker: CostTracker):
        tracker.compute_cost("analyze_ecg", {})
        tracker.compute_cost("analyze_brain_mri", {})
        tracker.compute_cost("analyze_brain_mri", {"contrast": True})
        summary = tracker.get_summary()
        assert summary["total_cost_usd"] == 20.0 + 320.0 + 446.0
        assert summary["num_tool_calls"] == 3
        assert summary["cost_by_tool"]["analyze_ecg"] == 20.0
        assert summary["cost_by_tool"]["analyze_brain_mri"] == 320.0 + 446.0


class TestCostTrackerRealisticWorkups:
    """Test realistic clinical workup scenarios."""

    def test_stroke_workup_cost(self, tracker: CostTracker):
        """Typical acute ischemic stroke: CT→MRI→ECG→labs→echo→Holter."""
        tracker.compute_cost("order_ct_scan", {"angiography": True})
        tracker.compute_cost("analyze_brain_mri", {"protocol": "stroke", "contrast": False})
        tracker.compute_cost("analyze_ecg", {})
        tracker.compute_cost("interpret_labs", {"panels": ["CBC", "BMP", "coagulation", "troponin", "lipid", "HbA1c"]})
        tracker.compute_cost("order_echocardiogram", {"echo_type": "TTE"})
        tracker.compute_cost("order_cardiac_monitoring", {"monitor_type": "holter_24h"})
        # Expected: 400 + 320 + 20 + 125 + 300 + 150 = 1315
        assert tracker.total_cost_usd == 1315.0

    def test_dementia_workup_cost(self, tracker: CostTracker):
        """Early Alzheimer's: labs→MRI→neuropsych→amyloid PET."""
        tracker.compute_cost("interpret_labs", {"panels": ["CBC", "BMP", "thyroid", "B12", "folate", "RPR", "HIV"]})
        tracker.compute_cost("analyze_brain_mri", {"protocol": "dementia", "contrast": False})
        tracker.compute_cost("order_specialized_test", {"test_type": "neuropsych_battery"})
        tracker.compute_cost("order_advanced_imaging", {"imaging_type": "amyloid_PET"})
        # Expected: 140 + 320 + 1200 + 4000 = 5660
        assert tracker.total_cost_usd == 5660.0

    def test_epilepsy_workup_cost(self, tracker: CostTracker):
        """First seizure: labs→ECG→EEG→MRI→drug check."""
        tracker.compute_cost("interpret_labs", {"panels": ["CBC", "BMP", "drug_screen", "prolactin"]})
        tracker.compute_cost("analyze_ecg", {})
        tracker.compute_cost("analyze_eeg", {"eeg_type": "routine"})
        tracker.compute_cost("analyze_brain_mri", {"protocol": "epilepsy", "contrast": True})
        tracker.compute_cost("check_drug_interactions", {"drug": "levetiracetam"})
        # Expected: 90 + 20 + 250 + 446 + 0 = 806
        assert tracker.total_cost_usd == 806.0
