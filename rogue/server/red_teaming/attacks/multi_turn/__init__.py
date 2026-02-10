"""
Multi-turn adversarial attack strategies - Free tier only.

Premium multi-turn attacks (GOAT, Crescendo, Simba, etc.) are handled
by the Deckard premium service.
"""

"""
Multi-turn attack implementations.
"""

from .bad_likert_judge import BadLikertJudge
from .crescendo import Crescendo
from .goat import GOAT
from .linear_jailbreak import LinearJailbreak
from .mischievous_user import MischievousUser
from .multi_turn_jailbreak import MultiTurnJailbreak
from .sequential_jailbreak import SequentialJailbreak
from .simba import Simba
from .social_engineering_prompt_extraction import SocialEngineeringPromptExtraction

__all__ = [
    "SocialEngineeringPromptExtraction",
    "MultiTurnJailbreak",
    "GOAT",
    "MischievousUser",
    "Simba",
    "Crescendo",
    "LinearJailbreak",
    "SequentialJailbreak",
    "BadLikertJudge",
]
