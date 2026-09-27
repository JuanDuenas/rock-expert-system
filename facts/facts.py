"""
Fact definitions for the Rock Expert System.
This module contains the structured facts used by the Rete engine.
All facts use a key-value schema to maintain immutability and referential integrity.
"""

from experta import Fact

class Evidence(Fact):
    """
    Represents an observable physical property of the rock sample.
    Expected keys:
        texture (str): crystalline, aphanitic, clastic, foliated, granoblastic
        grain_size (str): fine, medium, coarse
        foliation (str): yes, no
        visible_layers (str): yes, no
        acid_reaction (str): yes, no
        hardness (str): low, medium, high
    """
    pass

class Origin(Fact):
    """
    Represents the inferred geological origin of the rock.
    Expected keys:
        type (str): igneous, sedimentary, metamorphic
    """
    pass

class Classification(Fact):
    """
    Represents the final inferred rock type.
    Expected keys:
        type (str): granite, basalt, sandstone, limestone, slate, marble
    """
    pass

class Recommendation(Fact):
    """
    Represents the recommended use for the classified rock.
    Expected keys:
        use (str): construction, aggregates, coating, decoration, etc.
    """
    pass

class Goal(Fact):
    """
    Represents the current objective for the goal-driven (backward chaining) layer.
    Expected keys:
        target (str): e.g., 'classify'
    """
    pass

class Request(Fact):
    """
    Represents a request to ask the user for missing evidence.
    Expected keys:
        variable (str): e.g., 'texture', 'hardness'
    """
    pass
