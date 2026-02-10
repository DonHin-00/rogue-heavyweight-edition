"""
Agentic attack implementations.

These attacks use AI-driven coordination and adaptive strategies.
"""

from .hydra import Hydra
from .iterative_jailbreak import IterativeJailbreak
from .meta_agent_jailbreak import MetaAgentJailbreak
from .single_turn_composite import SingleTurnComposite
from .tree_jailbreak import TreeJailbreak

__all__ = [
    "IterativeJailbreak",
    "MetaAgentJailbreak",
    "Hydra",
    "TreeJailbreak",
    "SingleTurnComposite",
]
