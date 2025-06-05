# Paradigm Shift Feature Plan

The **Paradigm Shift** feature allows users to choose a programming paradigm when running GACCIA. The competing agent teams must refactor and implement the code in the selected paradigm, allowing direct comparison of different styles (e.g. object-oriented vs functional).

## Goals
- Provide a user-facing option to select a paradigm such as OOP, FP, Procedural, or Declarative.
- Modify architect and coder agents so their prompts focus on the requested paradigm.
- Track the chosen paradigm in the `GACCIASession` and `CodeImplementation` data structures.
- Enable easy extension with additional paradigms in the future.

## Implementation Tasks
1. **Define `ProgrammingParadigm` enum**
   - Add an enum in `gaccia_types.py` listing supported paradigms: `OOP`, `FP`, `PROCEDURAL`, `DECLARATIVE`.
   - Default to `OOP` if none is provided.
2. **Extend session data structures**
   - Add a `paradigm` field to `CodeImplementation` and `GACCIASession`.
3. **Update orchestrator**
   - Modify `GACCIAOrchestrator.run_competitive_session()` to accept a `paradigm` argument.
   - Propagate this value to `_run_language_conversion_flow`.
4. **Adjust agent prompts**
   - Update `PythonArchitect.plan_implementation` and `TypeScriptArchitect.plan_implementation` to include the selected paradigm in their instructions.
   - Update `PythonCoder.implement_code` and `TypeScriptCoder.implement_code` to implement according to the paradigm.
5. **CLI and example updates**
   - Update `main.py` or `gaccia_main.py` to accept a `--paradigm` option.
   - Provide example usage showing how to run a session with `--paradigm fp`.
6. **Testing**
   - Create small code samples in `data/` demonstrating each paradigm.
   - Add unit tests verifying that the paradigm field is stored and passed correctly.
7. **Documentation**
   - Document the feature in `README.md` with a short explanation and link to this file.
   - Keep `AGENTS.md` up to date with progress notes for coding agents.

## Notes for Intelligence-Constrained Agents
Break tasks into small commits and keep changes localized:
- Start by adding the enum and data structure fields before touching orchestrator logic.
- Verify each new parameter is passed through function signatures with simple tests.
- When modifying prompts, copy existing strings and add short clauses about the paradigm.
- Use the examples in `data/` to manually check that the output follows the requested paradigm.
