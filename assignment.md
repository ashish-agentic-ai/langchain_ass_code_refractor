Ashish — Code Refactoring Advisor Agent
Use Case: A user pastes a working but messy block of code. The agent detects code smells and then suggests a cleaner, refactored version.

Tool 1 — detect_code_smells

Input: a block of working code
Task: Identify code smells — duplication, long functions, poor naming, deep nesting, magic numbers, missing error handling — without changing functionality
Output: A prioritised list of code smells, each with the line/area affected and why it matters
Tool 2 — suggest_refactor

Input: the original code + the detected smells from Tool 1
Task: Produce a refactored version that addresses the smells while preserving behaviour, with a short note on each change
Output: The refactored code plus a summary of improvements made
System Prompt: The agent acts as a senior software engineer focused on clean, readable, maintainable code — it improves structure without altering behaviour.