"""
Base KnowledgeEngine setup.
"""
from experta import KnowledgeEngine
from engine.rules import RockRulesMixin

class RockExpertEngine(KnowledgeEngine, RockRulesMixin):
    """
    Main expert system engine.
    Combines the core KnowledgeEngine from experta with our custom rules.
    """
    pass
