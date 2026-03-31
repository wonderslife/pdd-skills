---
name: expert-entropy-auditor
description: |
  Entropy audit skill that discovers the gap between "design intent" and "code implementation". Automatically triggered when users need technical debt audit, PRD and code consistency check, or AI residue detection. 支持中文触发：审计技术债务、检查PRD一致性、检测AI残渣、技术债务审计、熵增审计。
  
  Core responsibility: Identify "AI residue" scattered in the codebase and suggest consolidating them into shared utility packages.
  
  Trigger scenarios:
  - User requests "audit technical debt", "check PRD consistency", "detect AI residue"
  - pdd-entropy-reduction coordinator calls
  - Scheduled trigger (recommended weekly)
  
  支持中文触发：熵增审计、技术债务审计、PRD一致性检查、AI残渣检测、PDD熵审计。
author: neuqik@hotmail.com
license: MIT
---

# Entropy Audit (expert-entropy-auditor)

## Core Philosophy

> "Like a garbage collector, identify 'AI residue' scattered in the codebase and suggest consolidating them into shared utility packages." —— Harness Engineering

The entropy audit skill is specifically designed to discover the gap between "design intent" and "code implementation", identifying entropy increase points in the codebase.

## Audit Dimensions

### 1. PRD and Code Consistency

**Audit Method**:
- Parse feature points in PRD documents
- Scan code implementation
- Compare feature points with implementation

**Example**:
```
PRD Feature: Display welcome message after user login
Code Implementation: Redirect to homepage directly after user login
→ Audit Result: Implementation inconsistent with PRD
```

### 2. Spec Document and Code Consistency

**Audit Method**:
- Parse technical specifications in Spec documents
- Check if code conforms to specifications
- Mark deviations

**Example**:
```
Spec Specification: API returns { code, data, message }
Code Implementation: API returns { status, result }
→ Audit Result: Return format does not conform to specification
```

### 3. AI Residue Detection

**What is AI Residue**:
- Repeatedly generated similar code
- Guessed data structures
- Inconsistent naming patterns
- Scattered helper utilities

**Detection Method**:
- Code similarity analysis
- Naming pattern analysis
- Duplicate code detection

**Example**:
```
File A: function formatDate(date) { ... }
File B: function formatDateString(d) { ... }
File C: function dateFormat(dateVal) { ... }
→ Audit Result: AI residue, suggest extracting to shared utility package
```

### 4. Technical Debt Accumulation

**Detection Method**:
- Scan TODO/FIXME/HACK comments
- Check temporary solution markers
- Count technical debt items

**Example**:
```
Technical Debt Statistics:
- TODO: 15 items
- FIXME: 3 items
- HACK: 2 items
→ Audit Result: Technical debt accumulated, suggest handling
```

---

## Audit Process

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Collect   │ ──→ │   Analyze   │ ──→ │    Score    │ ──→ │   Report    │
│             │     │             │     │             │     │             │
│ • PRD Docs  │     │ • Consistency│    │ • Entropy   │     │ • Issues    │
│ • Spec Docs │     │ • Duplication│    │ • Debt Eval │     │ • Suggestions│
│ • Code Impl │     │ • Pattern    │     │ • Risk Rate │     │ • Prioritize │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Entropy Score System

### Scoring Dimensions

| Dimension | Weight | Scoring Criteria |
|-----------|--------|-----------------|
| PRD Consistency | 25% | Feature point and implementation match rate |
| Spec Consistency | 25% | Technical specification compliance rate |
| AI Residue | 25% | Duplicate code ratio |
| Technical Debt | 25% | Debt quantity and severity |

### Score Calculation

```
Entropy Score = 100 - (Inconsistencies × 5 + AI Residues × 3 + Tech Debts × 2)

Example:
- PRD Inconsistencies: 2 items → Deduct 10 points
- Spec Inconsistencies: 1 item → Deduct 5 points
- AI Residues: 5 items → Deduct 15 points
- Tech Debts: 10 items → Deduct 20 points

Entropy Score = 100 - (10 + 5 + 15 + 20) = 50
```

### Status Determination

| Score Range | Status | Recommended Action |
|------------|--------|-------------------|
| 90-100 | Excellent | Maintain current state |
| 70-89 | Good | Minor improvements |
| 50-69 | Fair | Planned cleanup |
| 30-49 | Warning | Priority handling |
| 0-29 | Critical | Emergency refactoring |

---

## Output Format

### Entropy Audit Report

```markdown
# Entropy Audit Report - YYYY-MM-DD

## Entropy Score: XX/100

## Audit Scope
- PRD Documents: X
- Spec Documents: X
- Code Files: X

## Consistency Audit

### PRD and Code Inconsistencies
| PRD Feature | Code Implementation | Deviation Description |
|-----------|---------|---------|
| FP-001 User login welcome message | Not implemented | Missing welcome message display |

### Spec and Code Inconsistencies
| Spec Specification | Code Implementation | Deviation Description |
|----------|---------|---------|
| API return format | Non-compliant | Missing message field |

## AI Residue Detection

### Duplicate Code
| File A | File B | Similarity | Suggestion |
|-------|-------|-------|------|
| utils/formatDate.js | utils/dateFormat.js | 85% | Extract to shared utility package |

### Guessed Data Structures
| File | Issue | Suggestion |
|------|------|------|
| service/UserService.ts | Hardcoded field names | Define type interfaces |

## Technical Debt Statistics

| Type | Count | Average Age |
|------|------|-------------|
| TODO | 15 | 14 days |
| FIXME | 3 | 7 days |
| HACK | 2 | 30 days |

## Improvement Suggestions

### High Priority
1. Fix PRD inconsistencies (2 items)
2. Extract duplicate code to shared utility package (5 items)

### Medium Priority
1. Handle FIXME comments (3 items)
2. Define missing type interfaces (3 items)

### Low Priority
1. Clean up outdated TODOs (12 items)
```

---

## Configuration Options

```yaml
# entropy-auditor-config.yaml
entropy_auditor:
  # Audit scope
  scope:
    prd_paths: ["docs/prd/", "docs/业务分析/"]
    spec_paths: ["docs/specs/", "docs/dev-specs/"]
    code_paths: ["src/"]
  
  # Detection thresholds
  thresholds:
    code_similarity: 0.8      # Code similarity threshold
    max_todo_age_days: 30     # Maximum TODO age
    max_fixme_age_days: 14    # Maximum FIXME age
  
  # Scoring weights
  weights:
    prd_consistency: 0.25
    spec_consistency: 0.25
    ai_residue: 0.25
    tech_debt: 0.25
```

---

## Usage Examples

### Example 1: Comprehensive Entropy Audit

```
User: Execute technical debt audit

AI:
1. Collect PRD, Spec, code
2. Analyze consistency
3. Detect AI residue
4. Calculate entropy score
5. Generate audit report
```

### Example 2: PRD Consistency Check

```
User: Check if PRD is consistent with code

AI:
1. Parse PRD feature points
2. Scan code implementation
3. Compare feature points with implementation
4. Generate deviation report
```

### Example 3: AI Residue Detection

```
User: Detect AI residue in code

AI:
1. Code similarity analysis
2. Naming pattern analysis
3. Identify duplicate code
4. Suggest extracting to shared utility package
```

---

## Collaboration with Other Skills

- **pdd-entropy-reduction**: Called as a sub-skill by the coordinator
- **pdd-doc-gardener**: Pass document inconsistency issues
- **expert-auto-refactor**: Pass refactoring suggestions
- **pdd-code-reviewer**: Integrate entropy checks into code review
