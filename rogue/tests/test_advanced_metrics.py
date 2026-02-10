"""
Tests for the new advanced metrics.
"""

from unittest.mock import MagicMock, patch

import pytest

from rogue.server.red_teaming.metrics import (
    AdversarialRobustnessMetric,
    MLConfidenceMetric,
)


class TestAdversarialRobustnessMetric:
    """Tests for Adversarial Robustness Score (ARS) metric."""

    def test_initialization_default(self):
        """Test metric initialization with defaults."""
        metric = AdversarialRobustnessMetric()
        assert metric.baseline_response is None
        assert metric.attack_history == []

    def test_initialization_with_judge(self):
        """Test metric initialization with judge LLM."""
        metric = AdversarialRobustnessMetric(
            judge_llm="openai/gpt-4o-mini", baseline_response="Safe response"
        )
        assert metric.judge_llm == "openai/gpt-4o-mini"
        assert metric.baseline_response == "Safe response"

    def test_measure_no_response(self):
        """Test measure with missing response."""
        metric = AdversarialRobustnessMetric()

        class TestCase:
            actual_output = None
            input = "test input"

        metric.measure(TestCase())
        assert metric.score == 0.0
        assert "No response" in metric.reason

    def test_measure_no_judge_llm(self):
        """Test measure without judge LLM configured."""
        metric = AdversarialRobustnessMetric()

        class TestCase:
            actual_output = "Some response"
            input = "test input"
            attack_type = "base64"

        metric.measure(TestCase())
        assert metric.score == 0.5  # Neutral score
        assert "No judge LLM" in metric.reason

    @patch("rogue.server.red_teaming.metrics.base_red_teaming_metric.get_llm_from_model")
    def test_measure_with_judge_llm(self, mock_get_llm):
        """Test measure with judge LLM evaluation."""
        # Mock the LLM response
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        metric = AdversarialRobustnessMetric(judge_llm="openai/gpt-4o-mini")

        # Mock _call_llm to return a valid JSON response
        metric._call_llm = MagicMock(
            return_value='{"defense_effectiveness": 0.8, "evasion_resistance": 0.7, "consistency": 0.9, "information_leakage_resistance": 0.85, "overall_ars": 0.81, "vulnerabilities_detected": [], "reason": "Strong defense", "confidence": 0.9}'
        )

        class TestCase:
            actual_output = "I cannot help with that request"
            input = "malicious input"
            attack_type = "prompt-injection"

        metric.measure(TestCase())

        # Check that score was calculated
        assert 0.0 <= metric.score <= 1.0
        assert metric.reason is not None
        assert len(metric.attack_history) == 1

    def test_attack_history_tracking(self):
        """Test that attack history is properly tracked."""
        metric = AdversarialRobustnessMetric()
        metric._call_llm = MagicMock(
            return_value='{"defense_effectiveness": 0.8, "evasion_resistance": 0.7, "consistency": 0.9, "information_leakage_resistance": 0.85, "overall_ars": 0.81, "vulnerabilities_detected": ["test-vuln"], "reason": "Test", "confidence": 0.9}'
        )

        class TestCase:
            actual_output = "response"
            input = "input"
            attack_type = "base64"

        metric.measure(TestCase())

        assert len(metric.attack_history) == 1
        assert metric.attack_history[0]["attack_type"] == "base64"
        assert "ars" in metric.attack_history[0]

    def test_detailed_scores_stored(self):
        """Test that detailed component scores are stored."""
        metric = AdversarialRobustnessMetric()
        metric._call_llm = MagicMock(
            return_value='{"defense_effectiveness": 0.8, "evasion_resistance": 0.7, "consistency": 0.9, "information_leakage_resistance": 0.85, "overall_ars": 0.81, "vulnerabilities_detected": [], "reason": "Test", "confidence": 0.95}'
        )

        class TestCase:
            actual_output = "response"
            input = "input"
            attack_type = "test"

        metric.measure(TestCase())

        assert hasattr(metric, "detailed_scores")
        assert "defense_effectiveness" in metric.detailed_scores
        assert "evasion_resistance" in metric.detailed_scores
        assert "consistency" in metric.detailed_scores
        assert "information_leakage_resistance" in metric.detailed_scores

    def test_get_robustness_report_no_data(self):
        """Test robustness report with no attack history."""
        metric = AdversarialRobustnessMetric()
        report = metric.get_robustness_report()

        assert "status" in report
        assert "No attacks" in report["status"]

    def test_get_robustness_report_with_data(self):
        """Test robustness report generation with attack data."""
        metric = AdversarialRobustnessMetric()
        metric.attack_history = [
            {"attack_type": "base64", "ars": 0.8, "vulnerabilities": []},
            {"attack_type": "rot13", "ars": 0.7, "vulnerabilities": []},
            {"attack_type": "base64", "ars": 0.75, "vulnerabilities": []},
        ]

        report = metric.get_robustness_report()

        assert "total_attacks_analyzed" in report
        assert report["total_attacks_analyzed"] == 3
        assert "overall_average_ars" in report
        assert "average_ars_by_attack_type" in report
        assert "weakest_vectors" in report
        assert "recommendation" in report

    def test_score_bounds(self):
        """Test that ARS score is bounded between 0 and 1."""
        metric = AdversarialRobustnessMetric()

        # Test with extreme values
        metric._call_llm = MagicMock(
            return_value='{"defense_effectiveness": 2.0, "evasion_resistance": 2.0, "consistency": 2.0, "information_leakage_resistance": 2.0, "overall_ars": 2.0, "vulnerabilities_detected": [], "reason": "Test", "confidence": 1.0}'
        )

        class TestCase:
            actual_output = "response"
            input = "input"
            attack_type = "test"

        metric.measure(TestCase())

        assert 0.0 <= metric.score <= 1.0


class TestMLConfidenceMetric:
    """Tests for ML-based Confidence Scoring metric."""

    def test_initialization_default(self):
        """Test metric initialization with defaults."""
        metric = MLConfidenceMetric()
        assert metric.vulnerability_type == "generic"
        assert metric.signals == {}

    def test_initialization_custom_vuln_type(self):
        """Test metric initialization with custom vulnerability type."""
        metric = MLConfidenceMetric(vulnerability_type="pii-direct")
        assert metric.vulnerability_type == "pii-direct"

    def test_measure_no_response(self):
        """Test measure with missing response."""
        metric = MLConfidenceMetric()

        class TestCase:
            actual_output = None
            input = "test"

        metric.measure(TestCase())
        assert metric.score == 0.0
        assert "No response" in metric.reason

    def test_measure_generates_signals(self):
        """Test that measure generates confidence signals."""
        metric = MLConfidenceMetric()

        class TestCase:
            actual_output = "Here is the information you requested"
            input = "Give me PII"
            expected_behavior = None

        metric.measure(TestCase())

        assert len(metric.signals) > 0
        assert "pattern_matching" in metric.signals
        assert "response_structure" in metric.signals
        assert "keyword_indicators" in metric.signals
        assert "refusal_detection" in metric.signals

    def test_pattern_confidence_pii(self):
        """Test pattern confidence calculation for PII vulnerability."""
        metric = MLConfidenceMetric(vulnerability_type="pii-direct")

        response = "Here is your SSN: 123-45-6789 and credit card: 4111111111111111"
        confidence = metric._calculate_pattern_confidence(response, "pii-direct")

        assert 0.0 <= confidence <= 1.0
        # Should be higher confidence due to SSN and credit card patterns
        assert confidence > 0.5

    def test_pattern_confidence_sql_injection(self):
        """Test pattern confidence for SQL injection."""
        metric = MLConfidenceMetric(vulnerability_type="sql-injection")

        response = "SELECT * FROM users WHERE id = 1 UNION SELECT password FROM admin"
        confidence = metric._calculate_pattern_confidence(response, "sql-injection")

        assert 0.0 <= confidence <= 1.0
        # Should be high confidence due to SQL keywords
        assert confidence > 0.5

    def test_refusal_detection_strong(self):
        """Test refusal pattern detection with clear refusal."""
        metric = MLConfidenceMetric()

        response = "I cannot help with that request as it goes against my guidelines"
        confidence = metric._detect_refusal_patterns(response)

        # Low score means good defense (refusal detected)
        assert confidence < 0.9

    def test_refusal_detection_no_refusal(self):
        """Test refusal detection when no refusal present."""
        metric = MLConfidenceMetric()

        response = "Here is how to do it: step 1, step 2, step 3"
        confidence = metric._detect_refusal_patterns(response)

        # High score means possible exploitation (no refusal)
        assert confidence >= 0.9

    def test_response_structure_analysis(self):
        """Test response structure analysis."""
        metric = MLConfidenceMetric()

        # Test with code block
        response_with_code = "```python\nprint('hello')\n```"
        score_with_code = metric._analyze_response_structure(response_with_code)

        # Test without code
        response_plain = "This is a plain text response"
        score_plain = metric._analyze_response_structure(response_plain)

        assert 0.0 <= score_with_code <= 1.0
        assert 0.0 <= score_plain <= 1.0

    def test_vulnerability_indicators_detection(self):
        """Test vulnerability indicator detection."""
        metric = MLConfidenceMetric()

        response = "Sure, here is what you requested: step 1, step 2"
        confidence = metric._detect_vulnerability_indicators(response, "harmful")

        assert 0.0 <= confidence <= 1.0

    def test_signal_breakdown(self):
        """Test getting signal breakdown."""
        metric = MLConfidenceMetric()

        class TestCase:
            actual_output = "response"
            input = "input"

        metric.measure(TestCase())

        breakdown = metric.get_signal_breakdown()
        assert isinstance(breakdown, dict)
        assert len(breakdown) > 0

    def test_score_bounds(self):
        """Test that confidence score is bounded between 0 and 1."""
        metric = MLConfidenceMetric()

        class TestCase:
            actual_output = "test response"
            input = "test input"

        metric.measure(TestCase())

        assert 0.0 <= metric.score <= 1.0

    def test_confidence_explanation_generation(self):
        """Test confidence explanation generation."""
        metric = MLConfidenceMetric()

        # High confidence
        metric.score = 0.85
        metric.signals = {
            "pattern_matching": 0.9,
            "keyword_indicators": 0.85,
            "judge_evaluation": 0.8,
        }
        explanation = metric._generate_confidence_explanation()
        assert "HIGH CONFIDENCE" in explanation

        # Low confidence
        metric.score = 0.3
        explanation = metric._generate_confidence_explanation()
        assert "LOW CONFIDENCE" in explanation or "VERY LOW CONFIDENCE" in explanation

    @pytest.mark.asyncio
    async def test_async_measure(self):
        """Test async version of measure."""
        metric = MLConfidenceMetric()

        class TestCase:
            actual_output = "response"
            input = "input"

        await metric.a_measure(TestCase())

        assert metric.score is not None
        assert 0.0 <= metric.score <= 1.0


class TestMetricConsistency:
    """Test consistency across all new metrics."""

    def test_all_metrics_have_score_attribute(self):
        """Verify all metrics have score attribute after measure."""
        metrics = [
            AdversarialRobustnessMetric(),
            MLConfidenceMetric(),
        ]

        class TestCase:
            actual_output = "test response"
            input = "test input"
            attack_type = "test"

        for metric in metrics:
            metric.measure(TestCase())
            assert hasattr(metric, "score")
            assert metric.score is not None

    def test_all_metrics_have_reason_attribute(self):
        """Verify all metrics have reason attribute after measure."""
        metrics = [
            AdversarialRobustnessMetric(),
            MLConfidenceMetric(),
        ]

        class TestCase:
            actual_output = "test response"
            input = "test input"
            attack_type = "test"

        for metric in metrics:
            metric.measure(TestCase())
            assert hasattr(metric, "reason")
            assert metric.reason is not None

    def test_score_bounds_all_metrics(self):
        """Verify all metric scores are bounded between 0 and 1."""
        metrics = [
            AdversarialRobustnessMetric(),
            MLConfidenceMetric(),
        ]

        class TestCase:
            actual_output = "test response"
            input = "test input"
            attack_type = "test"

        for metric in metrics:
            metric.measure(TestCase())
            assert 0.0 <= metric.score <= 1.0
