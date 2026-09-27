"""
Base KnowledgeEngine setup.
"""
from experta import KnowledgeEngine
from engine.rules import RockRulesMixin
from backward.goal_engine import GoalEngineMixin

class RockExpertEngine(KnowledgeEngine, RockRulesMixin, GoalEngineMixin):
    """
    Main expert system engine.
    Combines the core KnowledgeEngine from experta with our custom rules
    and the backward-chaining (goal-driven) simulation rules.
    """
    pass
