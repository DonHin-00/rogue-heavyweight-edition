"""
Hex encoding attack technique.

Encodes the attack input in hexadecimal to bypass text-based filters.
"""

from .base_single_turn_attack import BaseSingleTurnAttack


class Hex(BaseSingleTurnAttack):
    """Hex encoding attack."""

    name = "Hex"

    def __init__(self, weight: int = 1):
        self.weight = weight

    def enhance(self, attack: str) -> str:
        """Enhance the attack using hex encoding."""
        return attack.encode().hex()

    async def a_enhance(self, attack: str) -> str:
        """Async version of enhance."""
        return self.enhance(attack)

    def get_name(self) -> str:
        return self.name
