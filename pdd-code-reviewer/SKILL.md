---
name: pdd-code-reviewer
description: Code review Skill under PDD framework, verifying whether feature implementation meets development specifications and acceptance criteria. Automatically triggered after feature implementation or manually invoked. 支持中文触发：代码审查、代码评审、审查代码、检查代码、PDD代码审查。
license: MIT
compatibility: Requires code implementation to be completed first
metadata:
  author: neuqik@hotmail.com
  version: "2.0"
  parent: pdd-main
---

Code Review - Verify whether feature implementation meets development specifications

**Input**:
- Code files
- Development specifications (spec.md)
- Acceptance criteria (checklist.md)

**Output**:
- Review report (docs/reviews/review-{timestamp}.md)
- Issue list (issues)

---

## Version History

| Version | Date | Changes |
|-----|------|---------|
| 2.1 | 2026-03-22 | Added collaboration with expert-code-quality: review first then analyze, quality issues do not block |
| 2.0 | 2026-03-21 | Added architect review invocation, integrated software-architect / system-architect |
| 1.0 | Early | Initial version |

---

## 1. Skill Integration

### 1.1 Architect Review

When architecture issues are discovered during code review, invoke architect skills as needed:

| Architect Skill | Trigger Condition | Service Content |
|-----------|---------|---------|
| **software-architect** | Architecture deviation, interface design issues discovered | Architecture recommendations, design patterns |
| **system-architect** | System architecture issues discovered | System architecture review |

### 1.2 Expert Consultation

When technical issues are discovered during code review, invoke expert-xxx as needed:

| Expert Skill | Trigger Condition | Service Content |
|-----------|---------|---------|
| **expert-code-quality** | Code smells, refactoring needs discovered | Refactoring solutions, design patterns |
| **expert-ruoyi** | RuoYi framework usage issues discovered | Framework best practices |
| **expert-mysql** | SQL issues discovered | Optimization recommendations |

### 1.3 Invocation Conditions

**Must perform basic review**:
- All code files must undergo basic review
- Verify implementation completeness against specifications

**Invoke architects as needed**:
- Module boundaries unclear discovered
- Interface design deviation discovered
- Architecture pattern issues discovered

**Invoke experts as needed**:
- Code quality issues discovered
- Framework usage issues discovered
- Database design issues discovered

---

## 2. Review Dimensions

### 2.1 Design Consistency

- [ ] Whether code implementation is consistent with specification description
- [ ] Whether interface paths conform to specification definition
- [ ] Whether request/response structures conform to specifications
- [ ] Whether business logic follows specification definition

### 2.2 Code Quality

- [ ] Code readability
- [ ] Naming conventions
- [ ] Error handling completeness
- [ ] Comment quality

### 2.3 Security

- [ ] Parameter validation
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] Permission validation

### 2.4 Performance

- [ ] Database query efficiency
- [ ] Loop processing optimization
- [ ] Cache usage

### 2.5 Business Logic

- [ ] State transition correctness
- [ ] Business rule execution
- [ ] Exception handling

---

## 3. Issue Classification

### 3.1 CRITICAL - Must Fix

- Feature implementation severely deviates from specifications
- Core business process has errors
- Severe security vulnerabilities
- Data consistency issues

### 3.2 WARNING - Recommended to Fix

- Code readability issues
- Incomplete error handling
- Potential performance issues
- Non-compliance with coding standards

### 3.3 SUGGESTION - Optional Optimization

- Code optimization suggestions
- Refactoring suggestions
- Best practice recommendations

---

## 4. Process Steps

### Step 1: Collect Code Files

Collect code files to be reviewed:
- Backend code: Controller, Service, Mapper, Domain
- Frontend code: Vue components, API interfaces
- Database scripts: SQL files

### Step 2: Read Development Specifications

Read specification definitions from `dev-specs/FP-{number}/spec.md`.

### Step 3: Execute Basic Review

Review against specifications item by item:

**a. Interface Review**
- Whether interface path is correct
- Whether request method is correct
- Whether parameter handling is complete
- Whether response structure matches

**b. Business Logic Review**
- Whether processing flow is correct
- Whether state transitions are complete
- Whether validation rules are executed

**c. Data Model Review**
- Whether field mapping is correct
- Whether type definitions are consistent
- Whether audit fields are complete

### Step 4: Execute Code Quality Review

**Invoke expert-code-quality** (if code quality issues discovered):
- Code smell detection
- Refactoring suggestions
- Design pattern recommendations

### Step 5: Architecture Deviation Check

**Invoke software-architect** (if architecture issues discovered):
- Module boundary check
- Interface design check
- Architecture pattern check

### Step 6: Generate Review Report

Output review report to `docs/reviews/review-{timestamp}.md`:

```markdown
# Code Review Report

## Basic Information
| Item | Content |
|------|------|
| Feature Point | FP-XXX-NNN |
| Review Date | {date} |
| Reviewer | AI |
| Code Files | [...files...] |

## Review Results

### Passed Items
| Review Item | Status | Description |
|--------|------|------|
| Interface Design | ✓ | Conforms to specifications |
| ... | ... | ... |

### CRITICAL Issues
| No. | Issue Description | File | Recommendation |
|------|---------|------|------|
| 1 | ... | file.java | Fix solution |

### WARNING Issues
| No. | Issue Description | File | Recommendation |
|------|---------|------|------|
| 1 | ... | file.java | Optimization suggestion |

### SUGGESTION Issues
| No. | Issue Description | File | Recommendation |
|------|---------|------|------|
| 1 | ... | file.java | Refactoring suggestion |

## Architecture Review (if any)
### software-architect Review Comments
### system-architect Review Comments

## Conclusion
- [ ] Passed review
- [ ] Requires fix and re-review
```

### Step 7: Output Issue List

Return issue list for fixing:
```json
{
  "critical": [...],
  "warning": [...],
  "suggestion": [...]
}
```

---

## 5. Architecture Review Process

```
pdd-code-reviewer discovers architecture issues
    │
    ├─► Determine architecture issue type
    │       │
    │       ├── Software architecture issues
    │       │       │
    │       │       ▼
    │       │   software-architect consultation
    │       │       │
    │       │       ▼
    │       │   Return architecture recommendations
    │       │
    │       └── System architecture issues
    │               │
    │               ▼
    │           system-architect consultation
    │               │
    │               ▼
    │           Return system recommendations
    │
    └─► Integrate into review report
```

### 5.1 software-architect Invocation Example

```
Trigger condition: Module boundaries unclear discovered
Invoke: software-architect
Input:
  - Problem description: Module A depends on Module C, violating layering principles
  - Related code: [code snippet]
  - Existing architecture: [module relationship diagram]

Return:
  - Architecture issue analysis
  - Refactoring recommendations
  - Design pattern recommendations
```

### 5.2 system-architect Invocation Example

```
Trigger condition: System scalability issues discovered
Invoke: system-architect
Input:
  - Problem description: Current architecture cannot support future multi-tenant expansion
  - Existing architecture: [architecture diagram]
  - Expansion requirements: Support 100+ tenants

Return:
  - Architecture evaluation
  - Evolution roadmap
  - Technical decision recommendations
```

---

## 6. Guardrails

- Must review against specifications item by item
- Issues must accurately reference related code
- CRITICAL issues must be fixed before passing
- Review reports must completely record all issues
- **Architecture issues must consult architect skills**
- **Code quality issues must consult expert-code-quality**

---

## 7. Collaboration with expert-code-quality

### 7.1 Responsibility Boundaries

| Skill | Positioning | Core Responsibility | Blocking |
|------|------|---------|--------|
| **pdd-code-reviewer** | Process compliance review | Verify whether code implements specification requirements | Critical issues block |
| **expert-code-quality** | Code quality deep analysis | Identify code smells, recommend design patterns, refactoring suggestions | Does not block process |

### 7.2 Collaboration Process

```
Code implementation completed
    │
    ▼
┌─────────────────────────────────┐
│   pdd-code-reviewer             │
│   (Compliance review)           │
│                                 │
│   - Verify specification implementation │
│   - Check interface consistency  │
│   - Verify business rules        │
└─────────────────────────────────┘
    │
    ├── Has Critical issues → Return to pdd-implement-feature for fixing
    │
    └── No Critical issues
            │
            ▼
    ┌─────────────────────────────────┐
    │   expert-code-quality           │
    │   (Quality deep analysis)       │
    │                                 │
    │   - Code smell detection        │
    │   - Design pattern recommendations │
    │   - Refactoring suggestions     │
    └─────────────────────────────────┘
            │
            ▼
    ┌─────────────────────────────────┐
    │   Generate quality improvement tasks │
    │   (improvement-tasks.md)        │
    │                                 │
    │   - Does not block current process │
    │   - Record to future optimization list │
    └─────────────────────────────────┘
            │
            ▼
        Enter pdd-verify-feature
```

### 7.3 Issue Handling Strategy

| Issue Source | Level | Blocking | Handling Method |
|---------|------|---------|---------|
| pdd-code-reviewer | Critical | ✅ Blocks | Must fix before continuing |
| pdd-code-reviewer | Warning | ❌ Does not block | Record, recommend fixing |
| pdd-code-reviewer | Suggestion | ❌ Does not block | Record, optional optimization |
| expert-code-quality | Any level | ❌ Does not block | Record to quality improvement list |

### 7.4 Quality Improvement Task Handling

- **Timing**: Process uniformly after all feature points in module are completed
- **Output file**: `dev-specs/FP-{module}-{number}/improvement-tasks.md`
- **Process**: Batch refactoring → Design pattern application → Code optimization → Re-verification

---

## 8. Collaboration with Other Skills

| Collaborative Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **software-architect** | Consultation | Architecture issues | Architecture recommendations |
| **system-architect** | Consultation | System issues | System recommendations |
| **expert-code-quality** | Consultation | Code issues | Refactoring solutions |
| **expert-ruoyi** | Consultation | Framework issues | Best practices |
| **pdd-implement-feature** | Loop | Issue list | Fixed code |
| **pdd-verify-feature** | Sequential | Code passed review | Acceptance report |
