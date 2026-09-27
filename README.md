# Rock Classification Expert System

An academic implementation of a Knowledge-Based Expert System that classifies minerals/rocks using the **Rete Algorithm**. This project was built to demonstrate the practical application of Forward Chaining, Goal-Driven (simulated Backward Chaining) reasoning, and Knowledge Representation.

## 🚀 Features

- **Forward Chaining (Data-Driven)**: 14 strict logical rules divided into 3 inference levels (Evidence -> Origin -> Classification -> Recommendation).
- **Goal-Driven Interaction**: Simulated backward chaining. When the engine has a `Goal(target="classify")` but lacks required data, it generates a `Request` fact, prompting the user interactively.
- **Rete Engine Tracing**: The internal `run()` execution loop is overridden to visually print the Rete cycle (Match-Resolve-Act) at each step. You can see the real-time state of the Working Memory (Base de Hechos) and the Agenda (Conflict Set) resolving in the terminal.
- **Python 3.10+ Compatible**: Includes a runtime monkey-patch to maintain compatibility with `experta` (which relies on deprecated `collections.Mapping`).

## 🛠️ Installation

1. Clone or download this repository.
2. Navigate to the project root directory (`rock-expert-rete`).
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - **Windows:** `.\.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`
5. Install the required libraries:
   ```bash
   pip install experta schema frozendict
   ```

## 💻 Execution

To run the interactive CLI application:
```bash
python main.py
```
Follow the on-screen prompts. Provide evidence regarding the rock's physical properties (texture, grain size, acid reaction, etc.) to watch the Rete engine dynamically construct the Alpha/Beta networks and yield a classification.

## 🧪 Testing

The project includes a robust suite of unit tests verifying all 10 rock classes and the backward-chaining mechanisms.
To execute the tests:
```bash
python -m unittest tests/test_classification.py
```

## 📚 Academic Explanation

This expert system employs the **Rete algorithm** for efficient pattern matching over a set of rules and facts:

- **Facts (Working Memory)**: Immutable units of knowledge represented as subclasses of `Fact` (e.g., `Evidence`, `Origin`, `Classification`). When a fact is declared (`declare()`), it is pushed into the Working Memory.
- **Rules (Knowledge Base)**: Declarative IF-THEN constructs represented as class methods decorated with `@Rule()`. 
- **Alpha & Beta Networks**: 
  - Single-condition checks (e.g., *Is the texture glassy?*) are evaluated once in the Alpha Network.
  - Multi-condition joins (e.g., *Origin=Igneous AND Texture=Glassy*) are handled in the Beta Network, eliminating the need for redundant recalculations.
- **The Inference Cycle**: 
  1. **Match**: The engine evaluates changes in the Working Memory against the Rete network.
  2. **Resolve**: Satisfied rules are placed into the Agenda (Conflict Set). The engine picks the highest priority rule.
  3. **Act**: The RHS (Right-Hand Side) of the rule executes, often declaring new facts, triggering a new cycle until the Agenda is empty.
