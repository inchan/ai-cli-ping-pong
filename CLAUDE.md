# Claude Project Context

## Project Overview

This project implements an automated documentation workflow that transforms natural language instructions into structured requirements.

## Basic Workflow

### Instruction-to-Requirements Pipeline

1. **User Input**: User adds natural language instructions to `docs/INSTRUCTIONS.md`
2. **Change Detection**: System detects changes in `INSTRUCTIONS.md`
3. **Requirements Update**: Based on the updated instructions, the system automatically rewrites/modifies/updates `docs/REQUIREMENTS.md`

### Process Flow

```
User writes natural language
        ↓
docs/INSTRUCTIONS.md (updated)
        ↓
Detect changes
        ↓
Analyze INSTRUCTIONS.md
        ↓
docs/REQUIREMENTS.md (rewritten/modified/updated)
```

## Project Structure

```
/
├── CLAUDE.md                  # This file - Project context for AI
└── docs/
    ├── INSTRUCTIONS.md        # Natural language instructions (user input)
    └── REQUIREMENTS.md        # Structured requirements (auto-generated)
```

## Development Guidelines

### When INSTRUCTIONS.md Changes

- Read the entire `docs/INSTRUCTIONS.md` file
- Analyze the natural language instructions
- Extract functional and non-functional requirements
- Update `docs/REQUIREMENTS.md` accordingly
- Preserve existing requirements that are still relevant
- Add new requirements based on new instructions
- Remove or update outdated requirements

### Requirements Extraction Rules

- Convert user instructions into formal requirements
- Categorize requirements appropriately (functional, non-functional, technical, etc.)
- Maintain clear acceptance criteria
- Ensure requirements are testable and measurable

## Key Concepts

- **INSTRUCTIONS.md**: Source of truth for what the user wants (natural language)
- **REQUIREMENTS.md**: Formal, structured representation of requirements (technical specification)
- **Automated Sync**: Changes in instructions trigger requirements updates

## Important Notes

- Always read the full context of `INSTRUCTIONS.md` before updating requirements
- Maintain traceability between instructions and requirements
- Keep requirements atomic and testable
- Update timestamps or version information when modifying requirements

## References

- `docs/INSTRUCTIONS.md` - User instructions
- `docs/REQUIREMENTS.md` - Generated requirements
