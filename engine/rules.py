"""
Forward chaining rules for the Rete engine (Levels 1, 2, and 3).
"""
from experta import Rule, MATCH, OR, AND
from facts.facts import Evidence, Origin, Classification, Recommendation

class RockRulesMixin:
    """
    Mixin class containing all forward chaining rules.
    It will be combined with KnowledgeEngine.
    """

    # ---------------------------------------------------------
    # LEVEL 1: Evidence -> Origin (Alpha Network Demonstration)
    # ---------------------------------------------------------
    @Rule(OR(
        Evidence(texture="crystalline"), 
        Evidence(texture="aphanitic"),
        Evidence(texture="vesicular"),
        Evidence(texture="glassy")
    ))
    def determine_igneous(self):
        print("\n[MATCH] Rule 'determine_igneous' activated")
        print("[ACT] R1 -> Origin(type='igneous')")
        self.declare(Origin(type="igneous"))

    @Rule(Evidence(texture="clastic"))
    def determine_sedimentary(self):
        print("\n[MATCH] Rule 'determine_sedimentary' activated")
        print("[ACT] R2 -> Origin(type='sedimentary')")
        self.declare(Origin(type="sedimentary"))

    @Rule(OR(Evidence(texture="foliated"), Evidence(texture="granoblastic")))
    def determine_metamorphic(self):
        print("\n[MATCH] Rule 'determine_metamorphic' activated")
        print("[ACT] R3 -> Origin(type='metamorphic')")
        self.declare(Origin(type="metamorphic"))

    # ---------------------------------------------------------
    # LEVEL 2: Origin + Evidence -> Classification (Beta Network Joins)
    # ---------------------------------------------------------
    @Rule(
        Origin(type="igneous"),
        Evidence(texture="crystalline"),
        Evidence(grain_size="coarse")
    )
    def classify_granite(self):
        print("\n[MATCH] Rule 'classify_granite' activated (JOIN beta network)")
        print("[ACT] R4 -> Classification(type='granite')")
        self.declare(Classification(type="granite"))

    @Rule(
        Origin(type="igneous"),
        Evidence(texture="aphanitic"),
        Evidence(grain_size="fine")
    )
    def classify_basalt(self):
        print("\n[MATCH] Rule 'classify_basalt' activated (JOIN beta network)")
        print("[ACT] R5 -> Classification(type='basalt')")
        self.declare(Classification(type="basalt"))

    @Rule(
        Origin(type="igneous"),
        Evidence(texture="vesicular")
    )
    def classify_pumice(self):
        print("\n[MATCH] Rule 'classify_pumice' activated (JOIN beta network)")
        print("[ACT] R6 -> Classification(type='pumice')")
        self.declare(Classification(type="pumice"))

    @Rule(
        Origin(type="igneous"),
        Evidence(texture="glassy")
    )
    def classify_obsidian(self):
        print("\n[MATCH] Rule 'classify_obsidian' activated (JOIN beta network)")
        print("[ACT] R7 -> Classification(type='obsidian')")
        self.declare(Classification(type="obsidian"))

    @Rule(
        Origin(type="sedimentary"),
        Evidence(texture="clastic"),
        Evidence(visible_layers="yes"),
        Evidence(acid_reaction="no")
    )
    def classify_sandstone(self):
        print("\n[MATCH] Rule 'classify_sandstone' activated (JOIN beta network)")
        print("[ACT] R8 -> Classification(type='sandstone')")
        self.declare(Classification(type="sandstone"))

    @Rule(
        Origin(type="sedimentary"),
        Evidence(texture="clastic"),
        Evidence(visible_layers="yes"),
        Evidence(acid_reaction="yes")
    )
    def classify_limestone(self):
        print("\n[MATCH] Rule 'classify_limestone' activated (JOIN beta network)")
        print("[ACT] R9 -> Classification(type='limestone')")
        self.declare(Classification(type="limestone"))

    @Rule(
        Origin(type="metamorphic"),
        Evidence(foliation="yes"),
        Evidence(texture="foliated")
    )
    def classify_slate(self):
        print("\n[MATCH] Rule 'classify_slate' activated (JOIN beta network)")
        print("[ACT] R10 -> Classification(type='slate')")
        self.declare(Classification(type="slate"))

    @Rule(
        Origin(type="metamorphic"),
        Evidence(foliation="banded"),
        Evidence(texture="foliated")
    )
    def classify_gneiss(self):
        print("\n[MATCH] Rule 'classify_gneiss' activated (JOIN beta network)")
        print("[ACT] R11 -> Classification(type='gneiss')")
        self.declare(Classification(type="gneiss"))

    @Rule(
        Origin(type="metamorphic"),
        Evidence(texture="granoblastic"),
        Evidence(acid_reaction="yes")
    )
    def classify_marble(self):
        print("\n[MATCH] Rule 'classify_marble' activated (JOIN beta network)")
        print("[ACT] R12 -> Classification(type='marble')")
        self.declare(Classification(type="marble"))

    @Rule(
        Origin(type="metamorphic"),
        Evidence(texture="granoblastic"),
        Evidence(acid_reaction="no")
    )
    def classify_quartzite(self):
        print("\n[MATCH] Rule 'classify_quartzite' activated (JOIN beta network)")
        print("[ACT] R13 -> Classification(type='quartzite')")
        self.declare(Classification(type="quartzite"))


    # ---------------------------------------------------------
    # LEVEL 3: Classification -> Recommendation (MATCH demonstration)
    # ---------------------------------------------------------
    @Rule(Classification(type=MATCH.rock_type))
    def recommend_use(self, rock_type):
        recommendations = {
            "granite": "construction/coating",
            "basalt": "construction aggregates",
            "pumice": "abrasives/exfoliants",
            "obsidian": "surgical blades/ornaments",
            "sandstone": "construction/coating",
            "limestone": "cement manufacturing/construction material",
            "slate": "coating/roofing",
            "gneiss": "paving/building stone",
            "marble": "coating/decoration",
            "quartzite": "railway ballast/countertops"
        }
        use = recommendations.get(rock_type, "general study")
        print(f"\n[MATCH] Rule 'recommend_use' activated for {rock_type}")
        print(f"[ACT] R14 -> Recommendation(use='{use}')")
        self.declare(Recommendation(use=use))
