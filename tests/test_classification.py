"""
Test cases for the classification expert system.
Demonstrates pure Forward Chaining for the 6 target rocks,
and the Goal-Driven request generation for ambiguous data.
"""
import unittest
from engine.engine import RockExpertEngine
from facts.facts import Evidence, Classification, Recommendation, Goal, Request

class TestRockClassification(unittest.TestCase):
    def setUp(self):
        self.engine = RockExpertEngine()
        self.engine.reset()

    def get_classification(self):
        for fact in self.engine.facts.values():
            if isinstance(fact, Classification):
                return fact["type"]
        return None

    def test_granite(self):
        self.engine.declare(Evidence(texture="crystalline"))
        self.engine.declare(Evidence(grain_size="coarse"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "granite")

    def test_basalt(self):
        self.engine.declare(Evidence(texture="aphanitic"))
        self.engine.declare(Evidence(grain_size="fine"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "basalt")

    def test_sandstone(self):
        self.engine.declare(Evidence(texture="clastic"))
        self.engine.declare(Evidence(visible_layers="yes"))
        self.engine.declare(Evidence(acid_reaction="no"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "sandstone")

    def test_limestone(self):
        self.engine.declare(Evidence(texture="clastic"))
        self.engine.declare(Evidence(visible_layers="yes"))
        self.engine.declare(Evidence(acid_reaction="yes"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "limestone")

    def test_slate(self):
        self.engine.declare(Evidence(texture="foliated"))
        self.engine.declare(Evidence(foliation="yes"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "slate")

    def test_marble(self):
        self.engine.declare(Evidence(texture="granoblastic"))
        self.engine.declare(Evidence(acid_reaction="yes"))
        self.engine.run()
        self.assertEqual(self.get_classification(), "marble")

    def test_goal_driven_request_ambiguous(self):
        """Test that injecting a goal triggers a Request for missing information."""
        self.engine.declare(Goal(target="classify"))
        self.engine.run()
        
        # It should request 'texture' first to figure out Origin
        requests = [f["variable"] for f in self.engine.facts.values() if isinstance(f, Request)]
        self.assertIn("texture", requests)

if __name__ == '__main__':
    unittest.main()
