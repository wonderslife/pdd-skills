---
name: pdd-verify-feature
description: Verify whether feature implementation meets development specifications and acceptance criteria. Invoke this Skill when users want to verify implemented features. This skill adopts a three-dimensional verification model of Completeness, Correctness, and Coherence to ensure feature implementation meets specification requirements. 支持中文触发：验证功能、验收功能、功能验收、验证实现、PDD验证。
license: MIT
compatibility: Requires feature code and acceptance criteria
metadata:
  author: neuqik@hotmail.com
  version: "4.0"
  parent: pdd-main
  triggers:
    - "verify feature" | "acceptance" | "/verify"
    - "feature acceptance" | "checklist verification"
---

# PDD-Verify Feature - Feature Verification Skill

## 1. Skill Overview

### 1.1 Core Positioning
Verify whether feature implementation meets development specifications and acceptance criteria to ensure delivery quality.

### 1.2 Three-Dimensional Verification Model

```yaml
Verification Dimensions:
  Completeness:
    Definition: Whether all functions required by specifications have been implemented
    Verification Points:
      - Whether interfaces are complete
      - Whether fields are comprehensive
      - Whether business rules are covered

  Correctness:
    Definition: Whether implementation conforms to specification definitions
    Verification Points:
      - Whether interface logic is correct
      - Whether data processing is accurate
      - Whether business rules are correct

  Coherence:
    Definition: Whether frontend and backend, documentation and code are consistent
    Verification Points:
      - Whether frontend and backend interfaces are consistent
      - Whether documentation and code are consistent
      - Whether naming conventions are unified
```

### 1.3 Issue Classification

| Level | Symbol | Description | Handling Method |
|------|------|------|---------|
| **Critical** | 🔴 | Must be fixed, otherwise acceptance fails | Re-verify after fixing |
| **Warning** | 🟡 | Recommended to fix, does not affect acceptance pass | Record, pending future processing |
| **Suggestion** | 🔵 | Optional optimization | Record, as future improvement item |

## 2. Verification Process

### Step 1: Collect Verification Materials

```yaml
Verification Materials:
  Code Files:
    - Backend Code: Controller, Service, Mapper
    - Frontend Code: Vue Components, API Interfaces
    - Database Scripts: SQL Files

  Specification Documents:
    - spec.md: Development Specifications
    - checklist.md: Acceptance Criteria

  Others:
    - Business Analysis Report
    - PRD Document
```

### Step 2: Completeness Verification

```markdown
### 2.1 Interface Completeness Check

| Specification Required Interface | Actual Implementation | Status |
|--------------|---------|------|
| POST /api/xxx | ✓ Implemented | 🟢 |
| GET /api/xxx/{id} | ✓ Implemented | 🟢 |
| PUT /api/xxx | ✗ Not Implemented | 🔴 |
| DELETE /api/xxx/{id} | ✓ Implemented | 🟢 |

### 2.2 Field Completeness Check

| Specification Required Field | Actual Implementation | Status |
|--------------|---------|------|
| companyName | ✓ String | 🟢 |
| evaluationValue | ✓ BigDecimal | 🟢 |
| floorPrice | ✗ Missing | 🔴 |
```

### Step 3: Correctness Verification

```markdown
### 3.1 Interface Logic Correctness

| Check Item | Verification Result | Status |
|-------|---------|------|
| Application Submission Interface Logic | Correct | 🟢 |
| State Transition Logic | Correct | 🟢 |
| Permission Verification Logic | Missing | 🔴 |

### 3.2 Business Rule Correctness

| Business Rule | Specification Requirement | Implementation Status | Status |
|---------|---------|---------|------|
| Transfer Floor Price >= Valuation * 90% | Must Verify | Verified | 🟢 |
| Must Upload Attachments | Must Verify | Not Verified | 🔴 |
```

### Step 4: Coherence Verification

```markdown
### 4.1 Frontend-Backend Consistency

| Interface/Field | Backend Definition | Frontend Definition | Status |
|----------|---------|---------|------|
| companyName | String | String | 🟢 |
| evaluationValue | BigDecimal | Number | 🟢 |
| floorPrice | BigDecimal | String | 🟡 |

### 4.2 Documentation-Code Consistency

| Documentation Description | Code Implementation | Status |
|---------|---------|------|
| Interface Path: /api/apply | @RequestMapping("/apply") | 🟢 |
| Response Structure: {code, msg, data} | AjaxResult | 🟢 |
```

## 3. Verification Checklist

### 3.1 Interface Verification

```yaml
Interface Verification Items:
  - [ ] Whether interface path conforms to specifications
  - [ ] Whether request method is correct
  - [ ] Whether request parameters are complete
  - [ ] Whether response structure conforms to specifications
  - [ ] Whether error codes are correct
```

### 3.2 Business Logic Verification

```yaml
Business Logic Verification Items:
  - [ ] Whether state transitions are correct
  - [ ] Whether business rules are executed
  - [ ] Whether validation logic is complete
  - [ ] Whether exception handling is appropriate
```

### 3.3 Data Verification

```yaml
Data Verification Items:
  - [ ] Whether field types are correct
  - [ ] Whether field lengths are sufficient
  - [ ] Whether required fields are validated
  - [ ] Whether data formats are correct
```

### 3.4 Permission Verification

```yaml
Permission Verification Items:
  - [ ] Whether permission annotations exist
  - [ ] Whether data permissions are configured
  - [ ] Whether button permissions are controlled
```

### 3.5 Frontend-Backend Consistency Verification

```yaml
Consistency Verification Items:
  - [ ] Whether interface paths are consistent
  - [ ] Whether field names are consistent
  - [ ] Whether data types are consistent
  - [ ] Whether validation rules are consistent
```

## 4. Output Specifications

### 4.1 Acceptance Report Template

```markdown
# [Feature Name] Acceptance Report

## Basic Information
| Item | Content |
|------|------|
| Feature ID | FP-xxx |
| Acceptance Date | yyyy-MM-dd |
| Acceptance Person | AI/Manual |
| Acceptance Result | Pass/Fail |

## Three-Dimensional Verification Results

### Completeness
| Verification Item | Result | Issue Count |
|-------|------|-------|
| Interface Completeness | 🟢 Pass | 0 |
| Field Completeness | 🟡 Pass | 2 |
| Business Rule Coverage | 🔴 Fail | 1 |

### Correctness
| Verification Item | Result | Issue Count |
|-------|------|-------|
| Interface Logic | 🟢 Pass | 0 |
| Business Rules | 🟢 Pass | 0 |
| Data Processing | 🟡 Pass | 1 |

### Coherence
| Verification Item | Result | Issue Count |
|-------|------|-------|
| Frontend-Backend Consistency | 🟢 Pass | 0 |
| Documentation-Code Consistency | 🟢 Pass | 0 |
| Naming Conventions | 🟡 Pass | 1 |

## Issue List

### 🔴 Critical Issues
| No. | Issue Description | Location | Suggested Fix |
|------|---------|------|---------|
| 1 | [Issue] | [File] | [Suggestion] |

### 🟡 Warning Issues
| No. | Issue Description | Location | Suggested Fix |
|------|---------|------|---------|
| 1 | [Issue] | [File] | [Suggestion] |

### 🔵 Suggestion Issues
| No. | Issue Description | Location | Suggested Fix |
|------|---------|------|---------|
| 1 | [Issue] | [File] | [Suggestion] |

## Acceptance Conclusion

- [ ] **Passed Acceptance**: All Critical issues have been fixed
- [ ] **Conditionally Passed**: Critical issues recorded, pending fix
- [ ] **Failed Acceptance**: Unfixed Critical issues exist

## Signature
| Role | Signature | Date |
|------|------|------|
| AI Verification |  |  |
| Manual Review |  |  |
```

## 5. Verification Heuristics

### 5.1 Common Omission Checks

```yaml
Omission Checks:
  - [ ] Whether pagination parameters are handled
  - [ ] Whether sorting parameters are handled
  - [ ] Whether export functionality is implemented
  - [ ] Whether import functionality is implemented
  - [ ] Whether batch operations are handled
```

### 5.2 Common Error Checks

```yaml
Error Checks:
  - [ ] Null pointer exception handling
  - [ ] Array bounds checking
  - [ ] Type conversion checking
  - [ ] Date format checking
  - [ ] Number precision checking
```

### 5.3 Degraded Processing Strategy

When complete verification is not possible:

```yaml
Degraded Strategy:
  1. Code Review Degradation:
     - Missing tests -> Perform code review
     - Missing documentation -> Reference existing code

  2. Partial Verification:
     - Core functions verified first
     - Non-core functions can be marked "pending verification"

  3. Record Unverified Items:
     - Clearly mark unverified content
     - Record reasons and risks
```

## 6. Guardrails

### 6.1 Mandatory Verification Items
- [ ] All Critical issues must be fixed
- [ ] Acceptance report must be complete
- [ ] Three-dimensional verification must be covered

### 6.2 Avoidance Items
- ❌ Skip any Critical issues
- ❌ Verbal acceptance without documentation
- ❌ Degraded processing without risk explanation

## 7. Collaboration with Other Skills

| Collaborative Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **pdd-code-reviewer** | Sequential | Review Report | Issue List |
| **pdd-implement-feature** | Loop | Acceptance Failed | Fixed Code |
| **pdd-main** | Sequential | Acceptance Report | Final Delivery Confirmation |

## 8. Version History

| Version | Date | Changes |
|-----|------|---------|
| 4.1 | 2026-03-22 | Added checkpoint resume and error handling specification references |
| 4.0 | 2026-03-21 | Adopted three-dimensional verification model (Completeness/Correctness/Coherence) |

---

## 9. Checkpoint Resume and Error Handling Specifications

This Skill follows PDD framework implementation specifications, see [pdd-framework-design.md Chapter 9](../docs/pdd-framework-design.md#9-pdd-实施规范).

### 9.1 Checkpoint Resume

- **State File**: `.pdd-state.json`
- **Trigger Method**: User issues "continue execution" command
- **State Content**: Current stage, completed features, pending features

### 9.2 Error Handling

- **Retry Limit**: Maximum 3 times for the same feature
- **Exceeded Limit**: Pause process, await manual decision
- **Failure Record**: Record to `dev-specs/FP-{Module}-{Sequence}/review-report.md`

### 9.3 Quality Improvement Tasks

- **Processing Timing**: After all features in module are completed, process quality improvement tasks uniformly
- **Output File**: `dev-specs/FP-{Module}-{Sequence}/improvement-tasks.md`
