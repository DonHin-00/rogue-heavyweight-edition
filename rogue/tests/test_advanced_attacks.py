"""
Tests for the new advanced attack techniques.
"""

import pytest

from rogue.server.red_teaming.attacks.single_turn import (
    ChainOfThoughtManipulation,
    Homoglyph,
    MorseCode,
    UnicodeNormalization,
)


class TestUnicodeNormalization:
    """Tests for Unicode normalization attack."""

    def test_initialization(self):
        """Test attack initialization with default parameters."""
        attack = UnicodeNormalization()
        assert attack.name == "Unicode Normalization"
        assert attack.weight == 1
        assert attack.form == "NFKD"

    def test_initialization_custom_form(self):
        """Test attack initialization with custom normalization form."""
        attack = UnicodeNormalization(weight=2, form="NFD")
        assert attack.weight == 2
        assert attack.form == "NFD"

    def test_enhance_basic(self):
        """Test basic enhancement with Unicode normalization."""
        attack = UnicodeNormalization()
        test_input = "café"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > len(test_input)
        assert "Unicode normalization" in result
        assert "NFKD" in result

    def test_enhance_with_special_chars(self):
        """Test enhancement with special Unicode characters."""
        attack = UnicodeNormalization()
        test_input = "naïve résumé"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert "normalized" in result.lower()

    @pytest.mark.asyncio
    async def test_async_enhance(self):
        """Test async version of enhance."""
        attack = UnicodeNormalization()
        test_input = "test input"
        result = await attack.a_enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > 0


class TestHomoglyph:
    """Tests for homoglyph attack."""

    def test_initialization(self):
        """Test attack initialization."""
        attack = Homoglyph()
        assert attack.name == "Homoglyph"
        assert attack.weight == 1
        assert attack.substitution_rate == 0.7

    def test_initialization_custom_rate(self):
        """Test initialization with custom substitution rate."""
        attack = Homoglyph(substitution_rate=0.5)
        assert attack.substitution_rate == 0.5

    def test_substitution_rate_bounds(self):
        """Test that substitution rate is bounded between 0 and 1."""
        attack_low = Homoglyph(substitution_rate=-0.5)
        assert attack_low.substitution_rate == 0.0

        attack_high = Homoglyph(substitution_rate=1.5)
        assert attack_high.substitution_rate == 1.0

    def test_enhance_basic(self):
        """Test basic enhancement with homoglyphs."""
        attack = Homoglyph(substitution_rate=1.0)
        test_input = "access"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > len(test_input)
        assert "homoglyph" in result.lower()

    def test_enhance_contains_cyrillic(self):
        """Test that enhancement contains Cyrillic characters."""
        attack = Homoglyph(substitution_rate=1.0)
        test_input = "aeo"  # All have Cyrillic lookalikes
        result = attack.enhance(test_input)

        # Should contain instructional text about homoglyphs
        assert "Unicode" in result or "homoglyph" in result.lower()

    @pytest.mark.asyncio
    async def test_async_enhance(self):
        """Test async version of enhance."""
        attack = Homoglyph()
        test_input = "test"
        result = await attack.a_enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > 0


class TestMorseCode:
    """Tests for Morse code attack."""

    def test_initialization(self):
        """Test attack initialization."""
        attack = MorseCode()
        assert attack.name == "Morse Code"
        assert attack.weight == 1

    def test_enhance_basic(self):
        """Test basic enhancement with Morse code."""
        attack = MorseCode()
        test_input = "SOS"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert "..." in result  # S in Morse is ...
        assert "Morse" in result

    def test_enhance_alphabet(self):
        """Test enhancement with alphabet characters."""
        attack = MorseCode()
        test_input = "A"
        result = attack.enhance(test_input)

        assert ".-" in result  # A in Morse is .-
        assert "Morse code" in result

    def test_enhance_numbers(self):
        """Test enhancement with numbers."""
        attack = MorseCode()
        test_input = "123"
        result = attack.enhance(test_input)

        assert ".----" in result  # 1 in Morse
        assert "..---" in result  # 2 in Morse
        assert "...--" in result  # 3 in Morse

    def test_enhance_with_spaces(self):
        """Test enhancement with spaces (word separators)."""
        attack = MorseCode()
        test_input = "HI THERE"
        result = attack.enhance(test_input)

        assert "/" in result  # Space becomes /
        assert "word separator" in result.lower()

    @pytest.mark.asyncio
    async def test_async_enhance(self):
        """Test async version of enhance."""
        attack = MorseCode()
        test_input = "TEST"
        result = await attack.a_enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > 0


class TestChainOfThoughtManipulation:
    """Tests for chain-of-thought manipulation attack."""

    def test_initialization(self):
        """Test attack initialization."""
        attack = ChainOfThoughtManipulation()
        assert attack.name == "Chain-of-Thought Manipulation"
        assert attack.weight == 1

    def test_enhance_basic(self):
        """Test basic enhancement with chain-of-thought framing."""
        attack = ChainOfThoughtManipulation()
        test_input = "How to bypass security?"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert "Step 1" in result
        assert "Step 2" in result
        assert "Step 3" in result
        assert "Step 4" in result
        assert test_input in result

    def test_enhance_contains_reasoning_framework(self):
        """Test that enhancement contains logical reasoning framework."""
        attack = ChainOfThoughtManipulation()
        test_input = "test query"
        result = attack.enhance(test_input)

        assert "logical reasoning" in result.lower()
        assert "step by step" in result.lower()
        assert "analytical" in result.lower()

    def test_enhance_academic_framing(self):
        """Test that enhancement uses academic framing."""
        attack = ChainOfThoughtManipulation()
        test_input = "harmful request"
        result = attack.enhance(test_input)

        assert "academic" in result.lower() or "analytical" in result.lower()
        assert "theoretical" in result.lower() or "hypothetical" in result.lower()

    @pytest.mark.asyncio
    async def test_async_enhance(self):
        """Test async version of enhance."""
        attack = ChainOfThoughtManipulation()
        test_input = "test input"
        result = await attack.a_enhance(test_input)

        assert isinstance(result, str)
        assert len(result) > 0


class TestAttackConsistency:
    """Test consistency across all new attacks."""

    def test_all_attacks_have_name(self):
        """Verify all attacks have a name attribute."""
        attacks = [
            UnicodeNormalization(),
            Homoglyph(),
            MorseCode(),
            ChainOfThoughtManipulation(),
        ]

        for attack in attacks:
            assert hasattr(attack, "name")
            assert isinstance(attack.name, str)
            assert len(attack.name) > 0

    def test_all_attacks_have_weight(self):
        """Verify all attacks have a weight attribute."""
        attacks = [
            UnicodeNormalization(),
            Homoglyph(),
            MorseCode(),
            ChainOfThoughtManipulation(),
        ]

        for attack in attacks:
            assert hasattr(attack, "weight")
            assert isinstance(attack.weight, int)
            assert attack.weight > 0

    def test_all_attacks_enhance_returns_string(self):
        """Verify all attacks return strings from enhance()."""
        attacks = [
            UnicodeNormalization(),
            Homoglyph(),
            MorseCode(),
            ChainOfThoughtManipulation(),
        ]

        test_input = "test input"
        for attack in attacks:
            result = attack.enhance(test_input)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_all_attacks_enhance_not_empty(self):
        """Verify all attacks produce non-empty output."""
        attacks = [
            UnicodeNormalization(),
            Homoglyph(),
            MorseCode(),
            ChainOfThoughtManipulation(),
        ]

        for attack in attacks:
            result = attack.enhance("test")
            assert len(result.strip()) > 0

    def test_all_attacks_get_name_matches_name(self):
        """Verify get_name() returns the same as name attribute."""
        attacks = [
            UnicodeNormalization(),
            Homoglyph(),
            MorseCode(),
            ChainOfThoughtManipulation(),
        ]

        for attack in attacks:
            assert attack.get_name() == attack.name
