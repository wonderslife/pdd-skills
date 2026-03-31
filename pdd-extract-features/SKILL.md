---
name: pdd-extract-features
description: Extract feature point matrix from PRD document system. Call this Skill when users want to extract feature points from PRD. This skill is based on business analysis results, automatically identifies and extracts feature points, generates standardized feature point matrix, and provides input for development specification generation. 支持中文触发：提取功能点、功能点矩阵、从PRD提取、功能点分析、PDD提取。
license: MIT
compatibility: Requires business analysis report and PRD document
metadata:
  author: neuqik@hotmail.com
  version: "2.0"
  parent: pdd-main
  triggers:
    - "extract feature points" | "feature point matrix" | "FP-"
    - "extract from PRD" | "feature point analysis"
---

# PDD-Extract Features - Feature Point Extraction Skill

## 1. Skill Overview

### 1.1 Core Positioning
Extract feature points from business analysis results and PRD documents, generate standardized feature point matrix.

### 1.2 Skill Boundaries
- **Input**: Business analysis report, PRD document
- **Output**: feature-matrix.md (feature point matrix)
- **Not responsible for**: Specification writing, code implementation

## 2. Feature Point Classification

### 2.1 Classification by Complexity

| Complexity | Code | Description | Development Time | Manual Involvement |
|--------|------|------|---------|---------|
| **Core Business** | P0 | Core business processes, involving multi-party approval | 3-5 days | High |
| **Important Features** | P1 | Important business features, with alternatives | 1-2 days | Medium |
| **Auxiliary Features** | P2 | Auxiliary features, easy to implement | 0.5 day | Low |

### 2.2 Classification by Operation Type

| Type | Code | Description |
|------|------|------|
| **Create** | C | Create, add new data |
| **Read** | R | Read, query/details |
| **Update** | U | Update, modify data |
| **Delete** | D | Delete, remove data |
| **Batch** | B | Batch, batch operations |
| **Approve** | A | Approve, approval workflow |
| **Export** | E | Export, data export |
| **Flow** | F | Flow, state transition |

### 2.3 Classification by AI Role

| AI Role | Code | Description | Manual Involvement |
|--------|------|------|-----------|
| **Leader** | AI-L | AI-led implementation | Low |
| **Collaborator** | AI-C | AI and human collaboration | Medium |
| **Reviewer** | AI-R | AI-assisted review | High |

## 3. Feature Point Extraction Process

### Step 1: Analyze Business Use Cases

Extract use cases from business analysis report:
- Primary actors
- Use case name
- Basic flow
- Extended flow

### Step 2: Identify Feature Operations

Identify operations for each use case:

```markdown
| Use Case | Operation | Operation Type | Complexity | AI Role |
|------|------|---------|--------|--------|
| UC-001 Transfer Application | Initiate Application | C | P0 | AI-C |
| UC-001 Transfer Application | View Application | R | P1 | AI-L |
| UC-001 Transfer Application | Modify Application | U | P1 | AI-C |
```

### Step 3: Identify Pages/Interfaces

```markdown
| Feature Point | Page Path | API Path | Method |
|--------|---------|---------|------|
| FP-001 Initiate Application | form.vue | /apply | POST |
| FP-002 View Application | detail.vue | /apply/{id} | GET |
```

### Step 4: Generate Feature Point Matrix

```markdown
# [Module Name] Feature Point Matrix

## 1. Feature Point Summary

| Feature Point ID | Feature Name | Page/Interface | Operation Type | Complexity | AI Role | Dependencies |
|---------|---------|----------|---------|--------|--------|---------|
| FP-001 | Initiate Transfer Application | form.vue | C | P0 | AI-C | - |
| FP-002 | View Transfer Application | detail.vue | R | P1 | AI-L | FP-001 |
| FP-003 | Modify Transfer Application | form.vue | U | P1 | AI-C | FP-001 |
| FP-004 | Delete Transfer Application | list.vue | D | P1 | AI-C | FP-001 |
| FP-005 | Approve Transfer Application | approval.vue | A | P0 | AI-C | FP-001 |
```

### Step 5: Feature Point Details

Generate details for each P0 feature point:

```markdown
## 2. Feature Point Details

### FP-001: Initiate Transfer Application

**Basic Information**:
| Item | Content |
|------|------|
| Feature Point ID | FP-001 |
| Feature Name | Initiate Transfer Application |
| Belonging Use Case | UC-001 |
| Operation Type | C (Create) |
| Complexity | P0 |

**Feature Description**:
Applicant fills out transfer application form, after submission enters approval workflow.

**Preconditions**:
- User has logged in
- User has permission to initiate application

**Postconditions**:
- Application record has been created
- Status changes to "Pending Review"
- Notify approver

**Input Fields**:
| Field Name | Type | Required | Description |
|--------|------|------|------|
| companyName | String | Yes | Enterprise name |
| transferType | Enum | Yes | Transfer type |
| evaluationValue | Decimal | Yes | Evaluation value |
| floorPrice | Decimal | Yes | Transfer floor price |
| attachments | File[] | Yes | Attachments |

**Output Information**:
| Information | Description |
|------|------|
| applyId | Application ID |
| applyNo | Application number |
| status | Application status |

**Business Rules**:
- Transfer floor price >= Evaluation value * 90%
- Must upload related attachments
- Same enterprise same type can only have one ongoing application

**Test Strategy**:
- Positive: Normal submission of application
- Exception: Floor price below limit, missing attachments, duplicate submission
```

## 4. Feature Point Matrix Template

```markdown
# [Module Name] Feature Point Matrix

## Matrix Information
| Item | Content |
|------|------|
| Module Number | [Number] |
| Module Name | [Name] |
| Generation Date | [Date] |
| Version | v1.0 |

## Feature Point Summary Table

### 1.1 Statistics by Complexity
| Complexity | Count | Feature Point IDs |
|--------|------|---------|
| P0 | N | FP-xxx |
| P1 | N | FP-xxx |
| P2 | N | FP-xxx |

### 1.2 Statistics by Operation Type
| Operation Type | Count | Feature Point IDs |
|---------|------|---------|
| C (Create) | N | FP-xxx |
| R (Read) | N | FP-xxx |
| U (Update) | N | FP-xxx |
| D (Delete) | N | FP-xxx |
| A (Approve) | N | FP-xxx |

## Detailed Feature Point List

| Feature Point ID | Feature Name | Page/Interface | Operation | Complexity | AI Role | Dependencies | Test Strategy |
|---------|---------|----------|------|--------|--------|------|---------|
| FP-001 | [Name] | [Path] | C | P0 | AI-C | - | [Strategy] |
```

## 5. Guardrails

### 5.1 Must Follow
- [ ] Feature point ID must be globally unique
- [ ] Each feature point must have a clear operation type
- [ ] Must mark feature point dependencies
- [ ] P0 feature points must have detailed descriptions

### 5.2 Avoid
- ❌ Feature point missing critical business operations
- ❌ Dependencies forming cycles
- ❌ Complexity assessment inconsistent with reality

## 6. Collaboration with Other Skills

| Collaborating Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **pdd-ba** | Sequential | Business analysis report | Use cases and processes |
| **pdd-generate-spec** | Sequential | Feature point matrix | spec.md |

---

## 7. Manual Review Standards

This Skill follows PDD framework manual review standards.

### 7.1 Review Checkpoint

After feature point matrix generation is complete, manual review is required.

### 7.2 Review Content

| Review Item | Description |
|--------|------|
| Feature Point Completeness | Whether all business features are covered |
| Complexity Assessment | Whether P0/P1/P2 is reasonable |
| Test Strategy | Whether complete |
| Dependencies | Whether correct |

### 7.3 Review Granularity

- **Batch Review**: Quick overview of the whole, mark content requiring detailed review
- **Critical Feature Point Detailed Review**: P0 priority, complex state transitions, external system integration, sensitive data processing

### 7.4 Review Results

- **Output File**: `review-features.md`
- **Result Type**: passed / rejected / conditional

### 7.5 Critical Feature Point Definition

- P0 priority feature points
- Involving complex state transitions
- Involving external system integration
- Involving sensitive data processing

---

## 8. PDD Implementation Standards Reference

This Skill follows PDD framework implementation standards, see [pdd-framework-design.md Chapter 9](../docs/pdd-framework-design.md#9-pdd-实施规范).

## 9. Version History

| Version | Date | Change Content |
|-----|------|---------|
| 2.1 | 2026-03-22 | Added manual review standards, PDD implementation standards reference |
| 2.0 | 2026-03-21 | Enhanced complexity assessment standards, added AI role classification |
| 1.0 | Early | Initial version |
