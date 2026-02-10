"""
Attack implementations for red teaming.

This module contains attack implementations across all tiers.
"""

from .agentic import (
    Hydra,
    IterativeJailbreak,
    MetaAgentJailbreak,
    SingleTurnComposite,
    TreeJailbreak,
)
from .base_attack import BaseAttack
from .multi_turn import (
    BadLikertJudge,
    Crescendo,
    GOAT,
    LinearJailbreak,
    MischievousUser,
    MultiTurnJailbreak,
    SequentialJailbreak,
    Simba,
    SocialEngineeringPromptExtraction,
)
from .single_turn import (
    ROT13,
    Base64,
    BaseSingleTurnAttack,
    BestOfN,
    ChainOfThoughtManipulation,
    Citation,
    ContextPoisoning,
    GCG,
    GoalRedirection,
    GrayBox,
    Hex,
    Homoglyph,
    InputBypass,
    Leetspeak,
    LikertJailbreak,
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
    # Single Turn
    "PromptInjection",
    "Base64",
    "ROT13",
    "Hex",
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
    "Citation",
    "GCG",
    "LikertJailbreak",
    "BestOfN",
    # Multi Turn
    "SocialEngineeringPromptExtraction",
    "MultiTurnJailbreak",
    "GOAT",
    "MischievousUser",
    "Simba",
    "Crescendo",
    "LinearJailbreak",
    "SequentialJailbreak",
    "BadLikertJudge",
    # Agentic
    "IterativeJailbreak",
    "MetaAgentJailbreak",
    "Hydra",
    "TreeJailbreak",
    "SingleTurnComposite",
]
