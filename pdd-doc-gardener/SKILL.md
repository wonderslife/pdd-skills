---
name: pdd-doc-gardener
description: |
  Document Gardener skill that periodically scans document directories in the codebase to identify outdated or deprecated documents. Automatically triggered when users need document consistency checks, document updates, or document cleanup.
  
  Core responsibility: Maintain knowledge base freshness, ensure documents are synchronized with code implementation.
  
  Trigger scenarios:
  - User requests "check document consistency", "update documents", "clean up outdated documents"
  - pdd-entropy-reduction coordinator invocation
  - Scheduled trigger (recommended daily)
  
  支持中文触发：文档园丁、文档一致性检查、文档更新、文档清理、过时文档、PDD文档园丁。
author: neuqik@hotmail.com
license: MIT
---

# Document Gardener (pdd-doc-gardener)

## Core Philosophy

> "Documentation as code, keep synchronized. Outdated documentation is technical debt." —— PDD Golden Principle

Document Gardener is a key skill for implementing garbage collection, responsible for periodically scanning the `docs/` directory in the codebase to identify outdated or deprecated documents that no longer reflect actual code behavior.

## Detection Items

### 1. Code-Document Inconsistency

**Detection Method**:
- Parse code references in documents (e.g., file paths, function names, API endpoints)
- Check if referenced code exists
- Check if code behavior matches document description

**Example**:
```
Document description: API /api/users returns user list
Actual code: API /api/users returns user details (including orders)
→ Detection result: Document outdated
```

### 2. Outdated Comments

**Detection Method**:
- Scan TODO, FIXME, HACK comments in code
- Check comment age
- Mark comments older than N days as outdated

**Example**:
```
Code comment: // TODO: implement this later (created 30 days ago)
→ Detection result: Comment outdated, needs handling or deletion
```

### 3. Document References Deleted Code

**Detection Method**:
- Parse file path references in documents
- Check if files exist
- Mark documents referencing deleted files

**Example**:
```
Document reference: See src/utils/helper.js
Actual status: File deleted
→ Detection result: Document reference invalid
```

### 4. API Documentation Mismatch with Implementation

**Detection Method**:
- Parse endpoint definitions in API documentation
- Scan actual API implementations in code
- Compare parameters, return values, error codes

**Example**:
```
API documentation: POST /api/users, parameters { name, email }
Actual code: POST /api/users, parameters { name, email, phone }
→ Detection result: API documentation missing parameter description
```

---

## Execution Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Scan      │ ──→ │   Compare   │ ──→ │   Classify  │ ──→ │   Execute   │
│             │     │             │     │             │     │             │
│ • Doc dirs  │     │ • Code refs │     │ • Issue type│     │ • Update    │
│ • Code      │     │ • API defs  │     │ • Severity  │     │   docs      │
│   comments  │     │ • Behavior  │     │ • Priority  │     │ • Create PR │
│ • API docs  │     │   desc      │     │             │     │ • Delete    │
│             │     │             │     │             │     │   deprecated│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Output Format

### Document Gardener Report

```markdown
# Document Gardener Report - YYYY-MM-DD

## Scan Scope
- Document directory: docs/
- Code directory: src/
- Files scanned: XX

## Issues Found

### Critical (Must Fix)
| File | Issue | Suggestion |
|------|-------|------------|
| docs/api/users.md | API parameter missing | Add phone parameter description |

### Warning (Recommended Fix)
| File | Issue | Suggestion |
|------|-------|------------|
| docs/architecture.md | References deleted file | Update reference path |

### Info (Optional Fix)
| File | Issue | Suggestion |
|------|-------|------------|
| src/utils/helper.js | TODO exists for 30 days | Handle or delete |

## Execution Results
- Documents updated: X items
- PRs created: X items
- Skipped: X items
```

---

## Usage Examples

### Example 1: Comprehensive Document Check

```
User: Check all document consistency

AI:
1. Scan docs/ directory
2. Parse all code references in documents
3. Compare with code implementation
4. Generate report and create fix PR
```

### Example 2: API Documentation Check

```
User: Check if API documentation matches code

AI:
1. Scan docs/api/ directory
2. Parse API endpoint definitions
3. Compare with API implementations in code
4. Generate difference report
```

### Example 3: Clean Up Outdated Comments

```
User: Clean up outdated TODOs in code

AI:
1. Scan TODO/FIXME comments in code
2. Check comment age
3. Mark comments older than 30 days
4. Generate cleanup suggestions
```

---

## Configuration Options

```yaml
# doc-gardener-config.yaml
doc_gardener:
  # Scan configuration
  scan:
    docs_paths: ["docs/", "*.md"]
    code_paths: ["src/"]
    exclude: ["node_modules/", "dist/"]
  
  # Staleness detection
  staleness:
    todo_max_age_days: 30
    doc_max_age_days: 90
  
  # Execution configuration
  execution:
    auto_update: true      # Auto-update simple documents
    create_pr: true        # Create PR
    max_pr_per_run: 3      # Max PRs per run
```

---

## Collaboration with Other Skills

- **pdd-entropy-reduction**: Invoked as a sub-skill by the coordinator
- **pdd-doc-change**: Calls this skill to create document change PRs
- **expert-entropy-auditor**: Receives audit results, executes document fixes
