"""
Main entry point for the interactive console application.
Demonstrates the Rete inference cycle, working memory state, and Goal-Driven pattern.
"""
import sys

# Monkey patch for experta on Python 3.10+
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import Fact
from engine.engine import RockExpertEngine
from facts.facts import Goal, Request, Evidence, Classification, Recommendation

OPTIONS = {
    "texture": ["crystalline", "aphanitic", "clastic", "foliated", "granoblastic", "vesicular", "glassy"],
    "grain_size": ["fine", "medium", "coarse"],
    "foliation": ["yes", "no", "banded"],
    "visible_layers": ["yes", "no"],
    "acid_reaction": ["yes", "no"],
    "hardness": ["low", "medium", "high"]
}

def print_memory(engine):
    print("\n=== WORKING MEMORY ===")
    for fact_id, fact in engine.facts.items():
        print(f"Fact {fact_id}: {fact}")
    print("========================\n")

def ask_user(variable):
    print(f"\nPlease provide the evidence for: {variable.upper()}")
    options = OPTIONS.get(variable, [])
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    
    while True:
        try:
            choice = input("Select an option (number) or 'q' to quit: ")
            if choice.lower() == 'q':
                sys.exit(0)
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid option. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("=== EXPERT SYSTEM FOR ROCK CLASSIFICATION ===")
    engine = RockExpertEngine()
    engine.reset()
    
    print("\n[DECLARE] Injecting initial Goal(target='classify')...")
    engine.declare(Goal(target="classify"))
    
    # Initial run to trigger the first request
    engine.run()
    
    while True:
        # Check for pending requests
        pending_request = None
        for fact_id, fact in engine.facts.items():
            if isinstance(fact, Request):
                pending_request = (fact_id, fact)
                break
                
        if not pending_request:
            # No more requests, classification should be done
            break
            
        fact_id, req_fact = pending_request
        variable = req_fact["variable"]
        
        # 1. Ask user
        user_value = ask_user(variable)
        
        # 2. Retract the Request (demonstrating retract feature)
        print(f"\n[RETRACT] Removing fulfilled Request for '{variable}'")
        engine.retract(req_fact)
        
        # 3. Declare new Evidence
        print(f"[DECLARE] Evidence({variable}='{user_value}')")
        engine.declare(Evidence(**{variable: user_value}))
        
        # 4. Audit Working Memory
        print_memory(engine)
        
        # 5. Run the engine again (Rete continues)
        print("Running Rete inference engine...")
        engine.run()
        
    print("\n=== CLASSIFICATION COMPLETE ===")
    classification = None
    recommendation = None
    for fact in engine.facts.values():
        if isinstance(fact, Classification):
            classification = fact["type"]
        elif isinstance(fact, Recommendation):
            recommendation = fact["use"]
            
    if classification:
        print(f">> INFERRED ROCK: {classification.upper()}")
        print(f">> RECOMMENDED USE: {recommendation}")
    else:
        print(">> Could not classify the rock with the given evidence.")

if __name__ == "__main__":
    main()
