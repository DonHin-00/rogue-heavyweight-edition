"""
Tests for the attack catalog to verify free vs premium classification.
"""

import pytest

from rogue.server.red_teaming.catalog.attacks import (
    FREE_MULTI_TURN_ATTACKS,
    FREE_SINGLE_TURN_ATTACKS,
    PREMIUM_SINGLE_TURN_ATTACKS,
    get_basic_scan_attacks,
    get_free_attacks,
    get_premium_attacks,
    is_premium_attack,
)


class TestAttackCatalog:
    """Tests for attack catalog classification."""

    def test_free_single_turn_attacks_not_marked_premium(self):
        """Verify that free single-turn attacks don't have premium flag."""
        for attack in FREE_SINGLE_TURN_ATTACKS:
            assert not attack.premium, f"Attack {attack.id} is in FREE list but marked premium"

    def test_premium_single_turn_attacks_marked_premium(self):
        """Verify that premium single-turn attacks have premium flag."""
        for attack in PREMIUM_SINGLE_TURN_ATTACKS:
            assert attack.premium, f"Attack {attack.id} is in PREMIUM list but not marked premium"

    def test_free_multi_turn_attacks_not_marked_premium(self):
        """Verify that free multi-turn attacks don't have premium flag."""
        for attack in FREE_MULTI_TURN_ATTACKS:
            assert not attack.premium, f"Attack {attack.id} is in FREE list but marked premium"

    def test_hex_is_free(self):
        """Verify that hex attack is now free."""
        assert not is_premium_attack("hex"), "hex attack should be free"

    def test_leetspeak_is_free(self):
        """Verify that leetspeak attack is now free."""
        assert not is_premium_attack("leetspeak"), "leetspeak attack should be free"

    def test_context_poisoning_is_free(self):
        """Verify that context-poisoning attack is now free."""
        assert not is_premium_attack("context-poisoning"), "context-poisoning attack should be free"

    def test_social_engineering_is_free(self):
        """Verify that social-engineering-prompt-extraction attack is now free."""
        assert not is_premium_attack(
            "social-engineering-prompt-extraction"
        ), "social-engineering-prompt-extraction attack should be free"

    def test_gcg_is_premium(self):
        """Verify that gcg attack is still premium."""
        assert is_premium_attack("gcg"), "gcg attack should be premium"

    def test_citation_is_premium(self):
        """Verify that citation attack is still premium."""
        assert is_premium_attack("citation"), "citation attack should be premium"

    def test_all_locally_implemented_attacks_in_free_list(self):
        """Verify that all locally implemented attacks are in the free list."""
        expected_free_single_turn = {
            "base64",
            "rot13",
            "hex",
            "leetspeak",
            "prompt-injection",
            "roleplay",
            "prompt-probing",
            "unicode-normalization",
            "homoglyph-free",
            "morse-code",
            "chain-of-thought-manipulation",
            "math-problem",
            "gray-box",
            "multilingual",
            "context-poisoning",
            "goal-redirection",
            "input-bypass",
            "permission-escalation",
            "system-override",
            "semantic-manipulation",
        }

        actual_free_single_turn = {attack.id for attack in FREE_SINGLE_TURN_ATTACKS}

        assert (
            expected_free_single_turn == actual_free_single_turn
        ), f"Mismatch in free single-turn attacks. Expected: {expected_free_single_turn}, Got: {actual_free_single_turn}"

    def test_basic_scan_includes_all_free_attacks(self):
        """Verify that basic scan includes all free attacks."""
        basic_scan = set(get_basic_scan_attacks())
        free_attacks = {attack.id for attack in get_free_attacks()}

        assert (
            basic_scan == free_attacks
        ), f"Basic scan should include all free attacks. Missing: {free_attacks - basic_scan}, Extra: {basic_scan - free_attacks}"

    def test_free_attacks_count(self):
        """Verify that we have the expected number of free attacks."""
        free_attacks = get_free_attacks()
        # We should have 20 single-turn + 1 multi-turn = 21 free attacks
        assert len(free_attacks) == 21, f"Expected 21 free attacks, got {len(free_attacks)}"

    def test_premium_attacks_count(self):
        """Verify that premium attacks are reduced to truly premium ones."""
        premium_attacks = get_premium_attacks()
        # We should have 5 single-turn + 8 multi-turn + 5 agentic = 18 premium attacks
        assert (
            len(premium_attacks) == 18
        ), f"Expected 18 premium attacks, got {len(premium_attacks)}"
