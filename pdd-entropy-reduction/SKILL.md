---
name: pdd-entropy-reduction
description: |
  PDD Entropy Reduction Agent, continuously monitors and repays technical debt to prevent system decay. Automatically triggered when users need code cleanup, documentation updates, technical debt management, architecture alignment, entropy reduction, or garbage collection.
  
  Core Objective: Combat system "entropy increase" and "decay" by periodically running agents to discover documentation inconsistencies or architecture constraint violations.
  
  Trigger Scenarios:
  - User requests "entropy reduction", "clean up technical debt", "code cleanup", "garbage collection"
  - User requests checking documentation and code consistency
  - User requests architecture constraint checking
  - User requests technical debt audit
  - Scheduled trigger (recommended weekly)
  - Automatic trigger after code commit (optional)
  - Automatic trigger after PR merge (optional)
  
  支持中文触发：熵减、清理技术债务、代码清理、文档更新、技术债务管理、架构对齐、垃圾回收、PDD熵减。
author: neuqik@hotmail.com
license: MIT
---

# PDD Entropy Reduction Agent

## Core Philosophy

> "Technical debt is like a high-interest loan: it's better to continuously repay the debt in small amounts than to let it accumulate and then painfully resolve it all at once." —— OpenAI Harness Engineering

In the PDD (PRD-Driven Development) methodology, the core objective of the entropy reduction mechanism is to **combat system "entropy increase" and "decay"** by periodically running agents to discover documentation inconsistencies or architecture constraint violations.

### Natural Trend of Entropy Increase

```
Entropy Increase (Natural Trend):
- Code decay: Duplicate code, overly long functions, inconsistent naming
- Documentation obsolescence: Code and documentation out of sync, outdated comments
- Technical debt accumulation: Unhandled TODOs, unoptimized temporary solutions
- Architecture drift: Violating dependency directions, blurred boundaries
- Test deficiency: Decreasing coverage, outdated tests

Entropy Reduction (Requires Energy Input):
- Refactoring: Eliminate duplication, simplify complexity
- Documentation updates: Synchronize documentation with code
- Technical debt repayment: Handle TODOs, optimize temporary solutions
- Architecture alignment: Fix violations, strengthen boundaries
- Test supplementation: Increase coverage, update tests
```

## Four Professional Sub-Skills

The entropy reduction agent coordinates four professional sub-skills to form a complete entropy reduction closed loop:

```
┌─────────────────────────────────────────────────────────────┐
│                  pdd-entropy-reduction                       │
│                      (Main Coordinator)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │ pdd-doc-    │  │ expert-arch │  │ expert-     │  │ expert-auto ││
│  │ gardener    │  │ -enforcer   │  │ entropy-    │  │ -refactor   ││
│  │             │  │             │  │ auditor     │  │             ││
│  │ Document    │  │ Architecture│  │ Entropy     │  │ Auto        ││
│  │ Gardener    │  │ Enforcer    │  │ Auditor     │  │ Refactor    ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1. pdd-doc-gardener (Document Gardener)

**Responsibility**: Periodically scans the `docs/` directory in the code repository to identify outdated or deprecated documentation that no longer reflects actual code behavior.

**Detection Items**:
- Code and documentation inconsistency
- Outdated comments (TODOs existing for more than N days)
- Code referenced in documentation has been deleted
- API documentation doesn't match implementation

**Action**: When documentation is found to be out of sync with implementation, automatically initiate a Pull Request for fixes.

### 2. expert-arch-enforcer (Architecture Constraint Enforcer)

**Responsibility**: Monitors whether code violates preset invariants and architecture boundaries.

**Detection Items**:
- Module dependency direction violations (e.g., Types → Config → Repo → Service → Runtime → UI)
- Missing boundary data validation
- File size exceeding limits
- Naming convention violations

**Tool Integration**: Utilizes custom Linters or structural tests (like ArchUnit), running periodically in the background to scan for deviations.

### 3. expert-entropy-auditor (Entropy Increase Auditor)

**Responsibility**: Discovers gaps between "design intent" and "code implementation".

**Detection Items**:
- PRD and code implementation inconsistency
- Spec documentation and code inconsistency
- Duplicate code (AI residue)
- Guessed data structures
- Scattered utility tools

**Function**: Like a garbage collector, identifies "AI residue" scattered in the codebase and recommends consolidating them into shared utility packages.

### 4. expert-auto-refactor (Automated Refactoring)

**Responsibility**: Transforms collected quality improvement tasks into concrete code operations.

**Strategy**: Periodically initiates targeted refactoring PRs using a "small loan repayment" approach to prevent technical debt accumulation.

**Refactoring Types**:
- Extract common methods
- Eliminate duplicate code
- Simplify complex logic
- Optimize naming

---

## Workflow

### Entropy Reduction Execution Process

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Trigger   │ ──→ │   Scan      │ ──→ │   Analyze   │ ──→ │   Execute   │
│             │     │             │     │             │     │             │
│ • Manual    │     │ • Doc scan  │     │ • Entropy   │     │ • Auto fix  │
│ • Scheduled │     │ • Code scan │     │   score     │     │ • Create PR │
│ • Event     │     │ • Arch scan │     │ • Classify  │     │ • Update    │
│             │     │             │     │ • Prioritize│     │   docs      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Entropy Score System

Entropy score range: 0-100 (100 = most orderly)

| Score Range | Status | Recommended Action |
|---------|------|---------|
| 90-100 | Excellent | Maintain current state |
| 70-89 | Good | Small improvements |
| 50-69 | Fair | Planned cleanup |
| 30-49 | Warning | Priority handling |
| 0-29 | Critical | Emergency refactoring |

---

## Execution Guide

### Step 1: Entropy Detection

Based on user request or trigger condition, select appropriate detection scope:

1. **Full Detection**: Scan all entropy increase points
2. **Documentation Detection**: Only scan documentation-related issues
3. **Architecture Detection**: Only scan architecture constraint violations
4. **Code Detection**: Only scan code quality issues

### Step 2: Generate Entropy Report

Use `references/entropy-report-template.md` to generate entropy report, including:

- Entropy score
- Issue list (sorted by priority)
- Fix recommendations
- Estimated workload

### Step 3: Entropy Reduction Execution

Select execution strategy based on issue type:

| Issue Type | Execution Method | Manual Confirmation |
|---------|---------|---------|
| Simple fixes (naming, formatting) | Auto fix and commit | No |
| Medium fixes (documentation updates) | Create PR | Yes |
| Complex fixes (refactoring) | Create Issue + PR | Yes |

---

## Integration with PDD Framework

```
PDD Forward Process                      PDD Entropy Reduction Process
    │                                     │
    ▼                                     ▼
┌─────────────┐                    ┌─────────────┐
│ PRD Document │                    │ Entropy     │
├─────────────┤                    │ Detection   │
│ Feature     │                    ├─────────────┤
│ Extraction  │                    │ Entropy     │
├─────────────┤                    │ Report      │
│ Spec Design │                    ├─────────────┤
├─────────────┤                    │ Entropy     │
│ Code        │  ←───────────────  │ Reduction   │
│ Implementation│                   │ Execution   │
├─────────────┤                    ├─────────────┤
│ Acceptance  │                    │ Auto Fix    │
│ Testing     │                    ├─────────────┤
└─────────────┘                    │ PR Creation │
                                   └─────────────┘
```

---

## Golden Principles

Based on Harness Engineering best practices, define the following golden principles:

1. **Use Shared Toolkits, Avoid Handwritten Helper Functions**
   - Centralize invariant management
   - Reduce duplicate code

2. **Validate Boundary Data, Don't Guess Data Structures**
   - All API entry points must have Schema validation
   - Don't rely on implicit type inference

3. **Keep Code Concise, Prioritize Readability**
   - Single file no more than 300 lines
   - Single function no more than 50 lines

4. **Documentation as Code, Keep Synchronized**
   - Code changes must synchronize documentation
   - Outdated documentation is considered technical debt

5. **Small Loan Repayment, Continuous Improvement**
   - Every commit is an improvement opportunity
   - Don't let technical debt accumulate

---

## Configuration File

Entropy reduction behavior can be configured via `entropy-config.yaml`:

```yaml
# entropy-config.yaml
entropy_reduction:
  # Trigger configuration
  triggers:
    schedule: "0 2 * * *"  # Daily at 2 AM
    on_commit: false       # Trigger on commit
    on_pr_merge: true      # Trigger on PR merge
  
  # Detection configuration
  detection:
    docs:
      enabled: true
      paths: ["docs/", "*.md"]
      max_age_days: 30     # Maximum documentation age in days
    architecture:
      enabled: true
      layers: ["types", "config", "repo", "service", "runtime", "ui"]
    code:
      enabled: true
      max_file_lines: 300
      max_function_lines: 50
    tests:
      enabled: true
      min_coverage: 80
  
  # Execution configuration
  execution:
    auto_fix: true         # Auto fix simple issues
    create_pr: true        # Create PR
    max_pr_per_run: 5      # Maximum PRs per run
  
  # Scoring configuration
  scoring:
    weights:
      docs: 0.25
      architecture: 0.25
      code: 0.25
      tests: 0.25
```

---

## Output Format

### Entropy Report Format

After each entropy reduction execution, generate an entropy report saved to the `docs/entropy-reports/` directory:

```markdown
# Entropy Reduction Report - YYYY-MM-DD

## Entropy Score: XX/100

## Issue List

### Critical (Must Fix)
- [ ] Issue description

### Warning (Recommended Fix)
- [ ] Issue description

### Info (Optional Fix)
- [ ] Issue description

## Fix Recommendations

### Critical Fixes
1. Fix recommendation details

## Execution Results
- Auto fixed: X items
- Created PR: X items
- Skipped: X items
```

---

## Usage Examples

### Example 1: Full Entropy Reduction

```
User: Execute full entropy reduction

AI:
1. Trigger all detectors
2. Generate entropy report
3. Execute fixes by priority
4. Report results
```

### Example 2: Documentation Entropy Reduction

```
User: Check documentation consistency

AI:
1. Trigger pdd-doc-gardener
2. Scan docs/ directory
3. Compare code with documentation
4. Generate fix PR
```

### Example 3: Architecture Entropy Reduction

```
User: Check architecture constraints

AI:
1. Trigger expert-arch-enforcer
2. Run custom Linter
3. Detect dependency violations
4. Generate fix recommendations
```

---

## References

- [Harness Engineering - Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [Harness Engineering - OpenAI](https://openai.com/zh-Hans-CN/index/harness-engineering/)
- `references/entropy-report-template.md` - Entropy report template
- `references/golden-principles.md` - Golden principles detailed explanation
