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
    
    def __init__(self):
        super().__init__()
        self.step = 0

    def run(self, steps=float('inf')):
        """
        Overrides the default experta run loop to trace the Rete execution.
        We print the Agenda (Conjunto conflicto) and Working Memory (BH)
        before executing each rule.
        """
        self.running = True
        execution = 0
        while steps > 0 and self.running:
            # Update activations first
            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

            activations = self.agenda.activations
            if activations:
                # Print Base de Hechos (BH)
                fact_keys = [f"h{k}" for k in self.facts.keys()]
                print(f"\nBH{self.step} -> {', '.join(fact_keys)}")
                
                # Print Conjunto Conflicto
                conflict_set = [act.rule.__name__ for act in activations]
                print(f"Conjunto conflicto: {', '.join(conflict_set)}")
                
                # Print which one executes next
                print(f"Ejecutar {activations[0].rule.__name__}: Regla de mayor prioridad/orden")

            activation = self.agenda.get_next()

            if activation is None:
                break
            else:
                steps -= 1
                execution += 1
                self.step += 1

                activation.rule(
                    self,
                    **{k: v
                       for k, v in activation.context.items()
                       if not k.startswith('__')})

        self.running = False
