"""
Attack implementations for red teaming.

This module contains free-tier attack implementations.
Premium attacks (multi-turn, agentic) are handled by the Deckard service.
"""

from .base_attack import BaseAttack
from .multi_turn import SocialEngineeringPromptExtraction
from .single_turn import (
    ROT13,
    Base64,
    BaseSingleTurnAttack,
    ChainOfThoughtManipulation,
    ContextPoisoning,
    GoalRedirection,
    GrayBox,
    Homoglyph,
    InputBypass,
    Leetspeak,
    MathProblem,
    MorseCode,
    Multilingual,
    PermissionEscalation,
    PromptInjection,
    PromptProbing,
    Roleplay,
    SemanticManipulation,
    SystemOverride,
    UnicodeNormalization,
)

__all__ = [
    "BaseAttack",
    "BaseSingleTurnAttack",
    # Single Turn (Free)
    "PromptInjection",
    "Base64",
    "ROT13",
    "Leetspeak",
    "Roleplay",
    "PromptProbing",
    "GrayBox",
    "MathProblem",
    "Multilingual",
    "ContextPoisoning",
    "GoalRedirection",
    "InputBypass",
    "PermissionEscalation",
    "SemanticManipulation",
    "SystemOverride",
    "UnicodeNormalization",
    "Homoglyph",
    "MorseCode",
    "ChainOfThoughtManipulation",
    # Multi Turn (Free)
    "SocialEngineeringPromptExtraction",
]
