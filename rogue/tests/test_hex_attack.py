"""
Test for the Hex encoding attack.
"""

import pytest

from rogue.server.red_teaming.attacks.single_turn import Hex


class TestHex:
    """Tests for hex encoding attack."""

    def test_initialization(self):
        """Test attack initialization with default parameters."""
        attack = Hex()
        assert attack.name == "Hex"
        assert attack.weight == 1

    def test_initialization_custom_weight(self):
        """Test attack initialization with custom weight."""
        attack = Hex(weight=2)
        assert attack.weight == 2

    def test_enhance_basic(self):
        """Test basic enhancement with hex encoding."""
        attack = Hex()
        test_input = "test"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        # "test" in hex is "74657374"
        assert result == "74657374"

    def test_enhance_empty_string(self):
        """Test enhancement with empty string."""
        attack = Hex()
        test_input = ""
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        assert result == ""

    def test_enhance_special_chars(self):
        """Test enhancement with special characters."""
        attack = Hex()
        test_input = "Hello, World!"
        result = attack.enhance(test_input)

        assert isinstance(result, str)
        # Verify it's valid hex
        assert all(c in "0123456789abcdef" for c in result)
        # Verify we can decode it back
        assert bytes.fromhex(result).decode() == test_input

    @pytest.mark.asyncio
    async def test_async_enhance(self):
        """Test async version of enhance."""
        attack = Hex()
        test_input = "async test"
        result = await attack.a_enhance(test_input)

        assert isinstance(result, str)
        assert bytes.fromhex(result).decode() == test_input

    def test_get_name(self):
        """Test get_name method."""
        attack = Hex()
        assert attack.get_name() == "Hex"
