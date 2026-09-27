"""
Goal-Driven pattern implementation simulating backward chaining.
This module strictly isolates the logic that "asks" for missing information,
so it doesn't get confused with the forward-chaining rules.
"""
from experta import Rule, NOT, W
from facts.facts import Goal, Evidence, Origin, Request

class GoalEngineMixin:
    """
    Mixin class that handles the Goal-Driven logic (Backward Chaining simulation).
    It detects missing information required to achieve a Goal and generates Requests.
    """

    # 1. To start classifying anything, we first need to know the texture to determine Origin.
    @Rule(
        Goal(target="classify"),
        NOT(Evidence(texture=W()))
    )
    def ask_texture(self):
        print("\n[BACKWARD] Goal 'classify' requires 'texture'.")
        print("[ACT] -> Request(variable='texture')")
        self.declare(Request(variable="texture"))

    # 2. If it's Igneous, we need grain_size to differentiate Granite vs Basalt
    @Rule(
        Goal(target="classify"),
        Origin(type="igneous"),
        NOT(Evidence(grain_size=W()))
    )
    def ask_grain_size(self):
        print("\n[BACKWARD] Origin is 'igneous', need 'grain_size' to classify.")
        print("[ACT] -> Request(variable='grain_size')")
        self.declare(Request(variable="grain_size"))

    # 3. If it's Sedimentary, we need visible_layers to continue
    @Rule(
        Goal(target="classify"),
        Origin(type="sedimentary"),
        NOT(Evidence(visible_layers=W()))
    )
    def ask_visible_layers(self):
        print("\n[BACKWARD] Origin is 'sedimentary', need 'visible_layers' to classify.")
        print("[ACT] -> Request(variable='visible_layers')")
        self.declare(Request(variable="visible_layers"))

    # 4. If it's Sedimentary, we also need acid_reaction
    @Rule(
        Goal(target="classify"),
        Origin(type="sedimentary"),
        NOT(Evidence(acid_reaction=W()))
    )
    def ask_acid_reaction_sed(self):
        print("\n[BACKWARD] Origin is 'sedimentary', need 'acid_reaction' to classify.")
        print("[ACT] -> Request(variable='acid_reaction')")
        self.declare(Request(variable="acid_reaction"))

    # 5. If it's Metamorphic and foliated, we need to confirm foliation presence (e.g. for Slate)
    @Rule(
        Goal(target="classify"),
        Origin(type="metamorphic"),
        Evidence(texture="foliated"),
        NOT(Evidence(foliation=W()))
    )
    def ask_foliation(self):
        print("\n[BACKWARD] Origin is 'metamorphic' (foliated texture), need 'foliation'.")
        print("[ACT] -> Request(variable='foliation')")
        self.declare(Request(variable="foliation"))

    # 6. If it's Metamorphic and granoblastic, we need to confirm acid_reaction (e.g. for Marble)
    @Rule(
        Goal(target="classify"),
        Origin(type="metamorphic"),
        Evidence(texture="granoblastic"),
        NOT(Evidence(acid_reaction=W()))
    )
    def ask_acid_reaction_meta(self):
        print("\n[BACKWARD] Origin is 'metamorphic' (granoblastic texture), need 'acid_reaction'.")
        print("[ACT] -> Request(variable='acid_reaction')")
        self.declare(Request(variable="acid_reaction"))
