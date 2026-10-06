# Claude Code Rules — Enterprise-Level Guide

## 1. Introduction

In Claude Code, **Rules are persistent Markdown instructions that shape how Claude works with a codebase**.

At an enterprise level, Claude Rules can be treated as an **AI engineering standards layer** that continuously provides Claude with organizational guidance such as:

- Coding conventions
- Architecture principles
- Testing expectations
- Documentation standards
- Security handling guidance
- Technology-specific development practices
- Database standards
- Frontend and backend conventions
- Git and DevOps practices

Unlike instructions that developers repeatedly type into a prompt, Rules are stored in files that Claude can automatically load into its working context.

The main purpose is to make Claude work more consistently across projects, teams, repositories, and technologies.

---

# 2. What Is a Claude Rule?

A Claude Rule is usually a Markdown instruction stored inside:

```text
.claude/rules/
```

For example:

```text
.claude/rules/backend/laravel.md
```

A Laravel development rule could contain:

```markdown
# Laravel Development Rules

- Use Laravel Form Requests for API request validation.
- Controllers must remain thin.
- Business logic belongs in the service layer.
- Use the project's standard API response structure.
- Use Eloquent relationships where appropriate.
- Schema changes must be implemented using migrations.
```

When Claude works inside the project, these instructions become part of the working context.

Conceptually:

```text
Developer Request
       ↓
Claude Task
       ↓
Project Rules
       ↓
Architecture Rules
       ↓
Technology Rules
       ↓
Coding Rules
       ↓
Claude Produces Code
```

Rules provide Claude with organizational knowledge that it cannot reliably infer only from source code.

---

# 3. CLAUDE.md vs .claude/rules/

Claude Code commonly uses two important instruction mechanisms:

```text
CLAUDE.md
```

and:

```text
.claude/rules/
```

They should serve different purposes.

## CLAUDE.md

`CLAUDE.md` is best used as the **high-level project constitution**.

It can explain:

- What the application is
- Main technologies
- Overall architecture
- Important project conventions
- Key development principles
- Important commands
- High-level constraints

Example:

```markdown
# Project Overview

This is an enterprise ERP platform.

Backend:
- Laravel
- PHP
- MySQL

Frontend:
- Vue 3
- TypeScript

# Architecture

The system follows:

Controller
    ↓
Service
    ↓
Repository
    ↓
Model

# General Principles

- Preserve existing architecture.
- Prefer reusable components.
- Avoid unnecessary dependencies.
- Keep changes scoped to the requested requirement.
```

## .claude/rules/

`.claude/rules/` should contain **modular and focused instructions**.

Example:

```text
.claude/
│
├── CLAUDE.md
│
└── rules/
    │
    ├── architecture.md
    ├── coding-standards.md
    ├── security.md
    ├── testing.md
    ├── documentation.md
    │
    ├── backend/
    │   ├── laravel.md
    │   ├── api.md
    │   └── database.md
    │
    └── frontend/
        ├── vue.md
        ├── typescript.md
        └── ui-ux.md
```

This modular approach is better for larger projects because it prevents a single `CLAUDE.md` file from becoming too large.

---

# 4. Global Rules and Conditional Rules

Claude Rules can be either:

1. **Always-active rules**
2. **Path-specific rules**

---

## 4.1 Always-Active Rules

A normal rule without path conditions applies generally to the project.

Example:

```text
.claude/rules/security.md
```

```markdown
# Security Rules

- Never hardcode credentials.
- Never expose secrets in logs.
- Validate external input.
- Follow least-privilege principles.
```

This type of rule is appropriate for standards that apply across the entire repository.

---

## 4.2 Path-Specific Rules

Path-specific Rules are useful when an instruction should apply only to a particular part of the repository.

Example:

```markdown
---
paths:
  - "frontend/**/*.vue"
  - "frontend/**/*.ts"
---

# Vue Rules

- Use Vue 3 Composition API.
- Use TypeScript.
- Prefer reusable components.
- Follow existing Vuetify conventions.
- Keep API access in the service layer.
```

Conceptually:

```text
Claude Reads:

frontend/src/User.vue
        │
        ▼
Does it match frontend/**/*.vue?
        │
       YES
        │
        ▼
Apply Vue Rules
```

But if Claude reads:

```text
backend/app/UserService.php
```

then the Vue-specific rule is irrelevant.

Path-specific rules are especially valuable in enterprise monorepositories.

---

# 5. Example Enterprise Monorepo

Consider the following repository:

```text
enterprise-platform/
│
├── frontend/
│     └── Vue
│
├── backend/
│     └── Laravel
│
├── mobile/
│     └── Flutter
│
├── services/
│     └── Spring Boot
│
├── infrastructure/
│     └── Terraform
│
└── database/
      └── migrations
```

An enterprise rules structure could be:

```text
.claude/rules/
│
├── common/
│   ├── engineering.md
│   ├── security.md
│   └── documentation.md
│
├── frontend/
│   ├── vue.md
│   └── ui-standards.md
│
├── backend/
│   ├── laravel.md
│   └── api.md
│
├── java/
│   └── springboot.md
│
├── mobile/
│   └── flutter.md
│
├── database/
│   └── database.md
│
└── infrastructure/
    └── terraform.md
```

A Spring Boot rule could be:

```markdown
---
paths:
  - "services/**/*.java"
---

# Spring Boot Rules

- Use constructor injection.
- Follow controller-service-repository architecture.
- Use DTOs at API boundaries.
- Controllers must not access repositories directly.
- Use Bean Validation for request validation.
- Centralize exception handling.
```

A database rule could be:

```markdown
---
paths:
  - "database/**/*"
  - "**/migrations/**/*"
---

# Database Rules

- All database changes require migrations.
- Never modify an existing production migration.
- Create a new migration for changes.
- Use indexes for frequently filtered columns.
- Foreign keys must follow the existing naming convention.
```

This approach helps Claude receive only the most relevant instructions for the code currently being modified.

---

# 6. How Claude Loads Rules

At a conceptual level, Claude can receive instructions from multiple locations.

A practical enterprise model is:

```text
Organization Instructions
        ↓
User Instructions
        ↓
Project CLAUDE.md
        ↓
.claude/rules/
        ↓
Subdirectory Instructions
        ↓
Task Context
```

It is important to avoid contradictory Rules.

For example:

```text
User Rule:
Use tabs.

Project Rule:
Use 2 spaces.
```

Conflicting instructions can reduce consistency.

An enterprise rule system should therefore be designed like this:

```text
Broad Principles
       ↓
Project Standards
       ↓
Technology Standards
       ↓
Directory-Specific Standards
```

Instead of:

```text
Rule A
   ↓
Contradicts
   ↓
Rule B
   ↓
Contradicts
   ↓
Rule C
```

---

# 7. Enterprise-Level Rules

Large organizations can define common engineering expectations that should apply across projects.

A shared enterprise rule may cover:

- Engineering principles
- Architecture consistency
- Security expectations
- Dependency management
- Testing expectations
- Documentation standards
- Code quality requirements

Example:

```markdown
# Enterprise Engineering Principles

All software created by Claude must comply with company
engineering standards.

## Architecture

Prefer the architecture already established by the application.

Do not introduce a new architectural pattern unless required
by the task.

## Dependencies

Before adding a new library:

1. Check whether the existing codebase already provides the functionality.
2. Prefer framework-native capabilities.
3. Avoid unnecessary third-party dependencies.

## Code Quality

Generated code must:

- Be readable.
- Be maintainable.
- Avoid unnecessary abstraction.
- Follow existing naming conventions.
- Remain within the requested scope.

## Security

Never place secrets, credentials, passwords, or API tokens
inside source code.

## Documentation

Document architectural decisions that are not obvious from
the implementation.
```

Project-specific rules can then extend these enterprise-wide principles.

---

# 8. Recommended Enterprise Rule Hierarchy

A scalable enterprise Claude Rules architecture can look like this:

```text
                 ORGANIZATION
                     │
                     ▼
          Enterprise CLAUDE.md
                     │
       ┌─────────────┼─────────────┐
       │             │             │
 Engineering     Security       Quality
 Standards       Principles     Principles
                     │
                     ▼
                  PROJECT
                     │
                 CLAUDE.md
                     │
              Architecture
                     │
                     ▼
             .claude/rules/
                     │
       ┌─────────────┼──────────────┐
       │             │              │
    Backend       Frontend       Database
       │             │              │
   Laravel         Vue          MySQL
   Spring Boot     React        Oracle
       │             │              │
       └─────────────┼──────────────┘
                     │
                     ▼
               Claude Code
```

The organizational level answers:

> How do we engineer software?

The project level answers:

> How does this application work?

The technology level answers:

> How should Claude write this particular type of code?

This separation helps standardize Claude usage across many repositories.

---

# 9. Shared Rules Across Multiple Projects

Organizations often have common standards that should be reused across many repositories.

For example:

```text
company-claude-rules/
│
├── security.md
├── git.md
├── api.md
└── documentation.md
```

These common Rules can then be shared across projects using repository automation, templates, package mechanisms, or supported filesystem linking approaches.

Conceptually:

```text
company-claude-rules/
        │
        │ Shared Standards
        ▼

Project A/.claude/rules/
Project B/.claude/rules/
Project C/.claude/rules/
Project D/.claude/rules/
```

This allows a company to maintain a controlled ruleset such as:

```text
Enterprise Claude Rules v1.4
```

instead of allowing each team to invent completely different standards.

---

# 10. Personal Rules

Claude also supports user-specific rule locations such as:

```text
~/.claude/rules/
```

These can contain personal development preferences.

Example:

```text
~/.claude/rules/
├── preferences.md
└── workflow.md
```

Example content:

```markdown
# Personal Preferences

- Explain architectural decisions before major refactoring.
- Keep responses concise unless detailed explanation is requested.
- Prefer PowerShell examples on Windows.
```

Personal rules should normally contain workflow preferences rather than competing architecture or security policies.

Enterprise standards should remain consistent across developers.

---

# 11. What Should Go Into Rules?

One of the most important principles is:

> Rules should be specific, practical, and verifiable.

Avoid vague instructions.

Bad:

```text
Write good code.
```

Better:

```text
Controllers may call services but must not access repositories directly.
```

Bad:

```text
Follow security best practices.
```

Better:

```text
API requests must use Laravel Form Requests for validation.
Do not expose exception stack traces through API responses.
```

Bad:

```text
Test your work.
```

Better:

```text
For backend changes, run:

php artisan test

before considering the implementation complete.
```

Good Rules tell Claude exactly what is expected.

---

# 12. Enterprise Rule Categories

A mature enterprise Rules library will usually include several categories.

## 12.1 Engineering Rules

Examples:

- Architecture conventions
- Naming conventions
- Dependency management
- Code scope control
- Reusability
- Maintainability
- Refactoring expectations

Example:

```markdown
# Engineering Rules

- Follow the existing project architecture.
- Reuse existing functionality before creating new abstractions.
- Avoid unnecessary dependencies.
- Keep changes within the requested scope.
- Do not refactor unrelated code unless required.
```

---

## 12.2 Backend Rules

Examples:

- Controller responsibilities
- Service layer conventions
- Repository conventions
- DTO usage
- API design
- Error handling
- Validation

Example:

```markdown
# Backend Rules

- Keep controllers thin.
- Business logic belongs in services.
- Repositories handle persistence concerns.
- Validate all external input.
- Use consistent API response formats.
```

---

## 12.3 Frontend Rules

Examples:

- Component structure
- State management
- TypeScript expectations
- Accessibility
- Design system usage
- API interaction

Example:

```markdown
# Frontend Rules

- Reuse shared components before creating new ones.
- Follow the project's state management conventions.
- Use TypeScript where configured.
- Preserve accessibility standards.
- Use the established UI design system.
```

---

## 12.4 Database Rules

Examples:

- Migration standards
- Indexing
- Naming
- Relationships
- Constraints
- Query optimization

Example:

```markdown
# Database Rules

- All schema changes must use migrations.
- Never modify an already-deployed production migration.
- Add indexes for frequently queried fields.
- Follow existing naming conventions.
- Use foreign keys where appropriate.
```

---

## 12.5 Security Rules

Examples:

- Secrets management
- Authentication
- Authorization
- Validation
- Logging
- Sensitive information

Example:

```markdown
# Security Rules

- Never hardcode secrets.
- Never commit credentials.
- Validate external input.
- Do not bypass authentication or authorization.
- Do not expose sensitive data in logs or error messages.
```

---

## 12.6 Testing Rules

Examples:

- Unit tests
- Integration tests
- Required commands
- Regression testing
- Coverage expectations

Example:

```markdown
# Testing Rules

- Update tests when behavior changes.
- Add regression tests for fixed defects where practical.
- Run the relevant project test suite before completion.
- Do not disable failing tests simply to make a build pass.
```

---

## 12.7 Documentation Rules

Examples:

- README updates
- API documentation
- Comments
- Architecture decisions
- Deployment documentation

Example:

```markdown
# Documentation Rules

- Update documentation when public behavior changes.
- Document important architecture decisions.
- Avoid unnecessary comments that merely repeat the code.
- Update API documentation when endpoints change.
```

---

## 12.8 DevOps Rules

Examples:

- Configuration structure
- Docker conventions
- Environment separation
- CI/CD expectations
- Deployment scripts

Example:

```markdown
# DevOps Rules

- Keep environment-specific values outside source code.
- Reuse existing deployment automation.
- Do not introduce infrastructure changes outside the requested scope.
- Keep DEV, UAT, and PROD configurations clearly separated.
```

---

## 12.9 Git Rules

Examples:

- Branch naming
- Commit conventions
- Pull request practices
- Change scope

Example:

```markdown
# Git Rules

- Keep commits focused.
- Follow the project's branch naming convention.
- Do not include unrelated changes.
- Write meaningful commit messages.
```

---

## 12.10 AI Development Rules

These are particularly useful for AI-assisted development.

Example:

```markdown
# AI Development Rules

- Inspect existing implementations before creating new functionality.
- Do not invent internal APIs without checking the codebase.
- Do not assume database columns exist without verifying models or migrations.
- Do not introduce unnecessary architectural changes.
- Ask for or inspect relevant context before making major assumptions.
```

These Rules reduce common AI coding problems such as hallucinated APIs or unnecessary rewrites.

---

# 13. Keep Rules Small and Focused

Claude Rules consume working context.

Therefore, avoid creating a single massive file such as:

```text
CLAUDE.md
3000 lines
```

covering everything:

```text
Laravel
Vue
React
Java
Flutter
AWS
Azure
Docker
Oracle
MySQL
Security
Testing
UI
DevOps
...
```

Instead, use smaller modular files.

Example:

```text
CLAUDE.md                ~80 lines

.claude/rules/
├── architecture.md      ~60 lines
├── security.md          ~50 lines
├── backend/
│   ├── laravel.md       ~80 lines
│   └── java.md          ~70 lines
├── frontend/
│   ├── vue.md           ~60 lines
│   └── react.md         ~60 lines
└── database/
    ├── mysql.md         ~40 lines
    └── oracle.md        ~40 lines
```

Path-specific rules can help reduce unnecessary context loading.

---

# 14. Recommended Rule Writing Principles

Enterprise Rules should follow several principles.

## Rule 1 — Be Specific

Bad:

```text
Use good architecture.
```

Better:

```text
Controllers must not directly access repositories.
```

## Rule 2 — Be Actionable

Bad:

```text
Improve security.
```

Better:

```text
Never log authentication tokens, passwords, or API secrets.
```

## Rule 3 — Match Existing Architecture

Claude should not redesign a working system unnecessarily.

Example:

```markdown
- Before introducing a new pattern, inspect the existing architecture.
- Prefer consistency with the existing codebase.
```

## Rule 4 — Avoid Contradictions

Do not maintain different Rules that give opposing instructions.

## Rule 5 — Keep Rules Modular

Prefer:

```text
security.md
database.md
testing.md
```

instead of one very large Rules file.

## Rule 6 — Use Path-Specific Rules

Apply frontend instructions only to frontend code and backend instructions only to backend code.

## Rule 7 — Keep Rules Verifiable

Prefer rules Claude can actually check.

Example:

```markdown
- Run `php artisan test` after backend changes.
```

instead of:

```markdown
- Make sure everything works.
```

---

# 15. Enterprise Governance Model

Claude Rules can become part of the organization's development governance.

Conceptually:

```text
Company Engineering Standards
              │
              ▼
      Enterprise Claude Rules
              │
              ▼
        Project Rules
              │
              ▼
      Technology Rules
              │
              ▼
        Claude Code
              │
              ▼
        Generated Code
```

This creates better consistency between human and AI-assisted development.

---

# 16. Traditional Development vs AI-Native Development

Traditional development often works like this:

```text
Human Developer
       +
Coding Standards Document
       +
Architecture Document
       +
Security Guidelines
       ↓
      Code
```

The problem is that standards may exist in:

- PDFs
- Wiki pages
- Confluence
- SharePoint
- Email
- Team knowledge
- Senior developers' experience

Developers must remember to consult them.

With Claude Rules:

```text
Claude
       +
CLAUDE.md
       +
.claude/rules/
       ↓
      Code
```

The engineering standards are placed directly into Claude's working context.

This helps convert organizational knowledge into persistent AI instructions.

---

# 17. Why Rules Matter at Enterprise Scale

Without enterprise Rules:

```text
Developer A
    ↓
Claude behaves one way

Developer B
    ↓
Claude behaves differently

Developer C
    ↓
Claude introduces another pattern
```

Over time, this can create:

- Architectural inconsistency
- Different naming conventions
- Different validation approaches
- Different testing standards
- Unnecessary dependencies
- Duplicate solutions
- Different security practices

With shared enterprise Rules:

```text
Enterprise Standards
        │
        ▼
   Shared Rules
        │
   ┌────┼────┐
   ▼    ▼    ▼
Team A Team B Team C
   │    │    │
   ▼    ▼    ▼
Claude Claude Claude
```

Claude receives a consistent engineering baseline across teams.

---

# 18. Recommended Enterprise Folder Structure

A practical enterprise repository could use:

```text
project-root/
│
├── CLAUDE.md
│
└── .claude/
    └── rules/
        │
        ├── common/
        │   ├── engineering.md
        │   ├── security.md
        │   ├── documentation.md
        │   └── git.md
        │
        ├── architecture/
        │   ├── application.md
        │   └── integration.md
        │
        ├── backend/
        │   ├── laravel.md
        │   ├── springboot.md
        │   └── api.md
        │
        ├── frontend/
        │   ├── vue.md
        │   ├── react.md
        │   └── ui-ux.md
        │
        ├── database/
        │   ├── mysql.md
        │   └── oracle.md
        │
        ├── testing/
        │   ├── backend-testing.md
        │   └── frontend-testing.md
        │
        └── devops/
            ├── deployment.md
            ├── docker.md
            └── infrastructure.md
```

This is scalable, understandable, and maintainable.

---

# 19. Example Complete Enterprise Rule

Example:

```markdown
---
paths:
  - "backend/**/*.php"
---

# Laravel Backend Engineering Rules

## Architecture

- Follow Controller → Service → Repository → Model architecture.
- Controllers must not directly access repositories.
- Business logic must remain outside controllers.
- Reuse existing services before creating new ones.

## Validation

- Use Laravel Form Requests for API validation.
- Never trust client-provided identifiers without validation.

## Database

- Use Eloquent where practical.
- All schema changes must use migrations.
- Never modify an already-deployed production migration.

## API

- Follow the project's standard response structure.
- Use appropriate HTTP status codes.
- Do not expose stack traces in production-facing responses.

## Security

- Do not hardcode credentials.
- Do not log tokens or passwords.
- Preserve authentication and authorization checks.

## Testing

- Update relevant tests when behavior changes.
- Run:

  php artisan test

  before considering backend changes complete.

## Scope

- Do not refactor unrelated modules.
- Do not introduce new dependencies unless required.
- Prefer existing project utilities and patterns.
```

This is far more useful than vague instructions such as:

```text
Follow best practices.
```

---

# 20. Final Mental Model

The simplest way to understand Claude Rules is:

```text
CLAUDE.md
      =
Project Constitution


.claude/rules/
      =
Detailed Engineering Standards


Path-Specific Rules
      =
Technology / Module-Specific Standards


Enterprise Shared Rules
      =
Company-Wide AI Engineering Standards
```

At enterprise scale, Claude Rules help turn development standards from passive documentation into **active context that accompanies the AI while it works**.

The main value is not simply better code generation.

The larger value is:

> **Consistency, standardization, maintainability, and preservation of organizational engineering knowledge across AI-assisted development.**


---

# 21. Project Example: Handle an Unknown Component

## 21.1 The Scenario in Our Project

Our Board Defect Inspection landing page renders only nine approved components through `apps/ui/src/registry.ts`:

```text
Hero, Heading, Text, FeatureCard, FeatureGrid,
CTA, Alert, InfoPanel, ProgressIndicator
```

Suppose a specification contains this unsupported block:

```json
{
  "component": "run_query",
  "props": {}
}
```

`run_query` is not an approved component. Even if the other blocks are valid, the renderer must reject the whole rendering. It must not skip this block, replace it with Text, or attempt to execute a query.

In the normal Task 4 workflow, the Python validator rejects such a fixture before it reaches the browser. The renderer also checks registry membership as a defensive boundary. Malformed renderer inputs belong only in tests; this scenario does not authorize passing raw JSON into the demonstration.

## 21.2 Write a Focused Rule

We could place the following rule in:

```text
.claude/rules/frontend/unknown-components.md
```

```markdown
---
paths:
  - "apps/ui/src/registry.ts"
  - "apps/ui/src/render.tsx"
  - "apps/ui/tests/**/*.tsx"
---

# Unknown Component Handling

- Read the existing registry, renderer and renderer tests before making changes.
- Resolve component names only through the fixed nine-component registry.
- Use an own-property membership check; inherited keys such as constructor,
  toString and __proto__ must not resolve as components.
- If any block has an unsupported component, reject the whole rendering
  before producing page elements.
- Never silently skip, rename, replace or dynamically load an unknown component.
- Do not expand the registry or change the schema to make a malformed input pass.
- Preserve the ApprovedUISpec handle boundary. Do not add a raw-JSON entry point.
- Keep malformed renderer probes test-only and reuse existing error behaviour.
- Do not invent a new Python validator rejection code.
- Test an unknown block mixed with valid blocks, and test inherited object keys.
- Confirm approved fixtures still render and inputs remain unchanged.
- From apps/ui, run npm test, npm run typecheck, npm run lint and npm run build.
- From the repository root, run .venv/Scripts/python.exe -m pytest -q.
- Report actual results and any failures.
```

This is an illustrative rule, not an installed file. This documentation update does not create anything under `.claude/rules/`. To adopt the example later, save the fenced Markdown content in the proposed file, keeping the YAML frontmatter at the top. The path patterns scope it to the registry, renderer and their TypeScript tests.

## 21.3 Use the Rule with a Developer Request

After installing the rule, a developer could ask Claude:

> Review unknown-component handling in our controlled UISpec renderer. Verify that a page containing valid blocks and a `run_query` block is rejected completely. Cover inherited names such as `constructor` as well. Reuse existing checks and tests; fix only missing behaviour without changing the approved-input boundary.

When Claude reads matching files, the rule supplies the project's expected handling. The developer does not need to restate every constraint in each request.

| Step | Expected use of the rule |
| --- | --- |
| Inspect existing behaviour | Read `registry.ts`, `render.tsx` and `tests/renderer.test.tsx`. Our implementation already has an own-key registry check and whole-page preflight. |
| Check an unknown name | Verify `run_query` cannot resolve. Do not create a new component or execute anything to satisfy the input. |
| Check mixed blocks | Use the existing test-only malformed-input mechanism to combine valid blocks with an unknown block. Expect the whole rendering to throw, not a partial page. |
| Check inherited names | Verify `constructor`, `toString` and `__proto__` are rejected even though ordinary JavaScript objects can inherit properties. |
| Preserve valid behaviour | Confirm existing Python-verified fixtures still render through issued handles and the registry. |
| Verify and report | Run the stated checks and report actual outcomes. If existing coverage already proves the requirement, explain that without duplicating implementation or tests. |

## 21.4 Expected Result

```text
Normal fixture preparation:
UISpec + complete context -> Python validator
Unknown component -> Fixture rejected before browser use

Defensive renderer test:
Valid block + unknown block -> Whole-page registry preflight
Unknown component -> Entire rendering rejected
```

For example, `requireComponent('run_query')` currently throws `Rendering rejected: unsupported component`. This is a renderer boundary error, not a board-quality rejection or a newly defined Python validation result.

The rule tells the coding assistant which behaviour to preserve. The registry check, renderer preflight, approved-input boundary and tests enforce it. These instructions are an example of how to use rules; this documentation change does not modify application code or claim a fresh test run.
