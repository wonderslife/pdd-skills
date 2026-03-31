---
name: pdd-generate-spec
description: Generate development specifications and acceptance criteria based on feature point matrix. Invoke this Skill when users want to generate technical specifications for feature points. 支持中文触发：生成开发规格、生成规格、规格设计、验收标准、PDD规格生成。
license: MIT
compatibility: Feature point extraction must be completed first
metadata:
  author: neuqik@hotmail.com
  version: "2.0"
  parent: pdd-main
---

Specification Generation - Generate development specifications and acceptance criteria based on feature points

**Input**: Feature Point Matrix (feature-matrix.md)

**Output**:
- spec.md (Development Specification)
- checklist.md (Acceptance Criteria)

---

## Version History

| Version | Date | Changes |
|-----|------|---------|
| 2.1 | 2026-03-22 | Added document system specifications, PDD implementation specification references |
| 2.0 | 2026-03-21 | Added architect consultation process |
| 1.0 | Early | Initial version |

---

## 1. Skill Integration

### 1.1 Architect Consultation

During the specification generation process, architect skills can be invoked as needed:

| Architect Skill | Invocation Timing | Service Content |
|-----------|---------|---------|
| **system-architect** | Technology selection, system architecture | Technology stack recommendations, architecture decisions, system structure |
| **software-architect** | Module division, interface design | Module boundaries, interface specifications, design patterns |

### 1.2 Invocation Conditions

**Must invoke system-architect**:
- New technology stack introduction
- System architecture changes
- Major technical decisions

**Must invoke software-architect**:
- Unclear module boundaries
- Complex interface design
- Design pattern recommendations needed

---

## 2. Process Steps

### Step 1: Read Feature Point Matrix

Read the feature point list and details from `dev-specs/feature-matrix.md`.

### Step 2: Determine Technology Stack

Determine the technology stack based on project configuration:
- Backend: Spring Boot + MyBatis (RuoYi Framework)
- Frontend: Vue.js + Element UI
- Database: MySQL

**Architecture Consultation (As Needed)**:
If new technology selection is involved, invoke `system-architect` for recommendations.

### Step 3: Module Design

Analyze the modules to which feature points belong:
- Determine module boundaries
- Determine module dependencies

**Architecture Consultation (As Needed)**:
If module boundaries are unclear, invoke `software-architect` for recommendations.

### Step 4: Generate Specifications for Each Feature Point

Process feature points in priority order:

**a. Analyze Feature Point Requirements**
- Business description
- Pre-conditions/Post-conditions
- Business rules
- Test scenarios

**b. Design Interfaces**
- Determine interface paths (RESTful style)
- Determine request methods (GET/POST/PUT/DELETE)
- Design request parameters
- Design response structure
- Define error codes

**Interface Naming Conventions**:

| Operation Type | Interface Path | Request Method |
|----------|----------|----------|
| List Query | /api/{module}/list | GET |
| Detail Query | /api/{module}/{id} | GET |
| Create | /api/{module} | POST |
| Update | /api/{module} | PUT |
| Delete | /api/{module}/{id} | DELETE |
| Approval Operation | /api/{module}/approve | POST |
| Reject Operation | /api/{module}/reject | POST |
| Terminate Operation | /api/{module}/terminate | POST |

**c. Design Data Model**

Data model naming conventions:

| Type | Naming Convention | Example |
|------|----------|------|
| Entity Class | {BusinessName} | TransferApplication |
| Primary Key | id | id |
| Creation Time | createTime | createTime |
| Update Time | updateTime | updateTime |
| Creator | createBy | createBy |
| Updater | updateBy | updateBy |
| Status | status | status |
| Delete Flag | delFlag | delFlag |

**d. Design Business Logic**
- Processing flow
- Validation rules
- State transitions
- Exception handling

**Architecture Consultation (As Needed)**:
If business logic is complex, invoke `software-architect` for design recommendations.

**e. Design Test Cases**
- Positive scenarios
- Exception scenarios
- Boundary conditions

### Step 5: Generate Development Specification Document

Output to `dev-specs/FP-{sequence}/spec.md`:

```markdown
# {Feature Point Name} Development Specification

## Document Information
| Item | Content |
|------|------|
| Specification ID | SPEC-{ModuleNumber}-{FeaturePointSequence} |
| Related Feature Point | FP-XXX-NNN |

## Interface Definition
### Interface 1: {Interface Name}
- Interface Path: `/api/xxx`
- Request Method: POST
- Request Parameters: [...]
- Response Structure: {...}
- Error Codes: [...]

## Data Model
### Entity: {Entity Name}
| Field Name | Type | Required | Description |

## Business Logic
### Processing Flow
### Validation Rules
### State Transitions

## Test Cases
### Positive Scenarios
### Exception Scenarios
### Boundary Conditions
```

### Step 6: Generate Acceptance Criteria Document

Output to `dev-specs/FP-{sequence}/checklist.md`:

```markdown
# {Feature Point Name} Acceptance Criteria

## Document Information
| Item | Content |
|------|------|
| Acceptance Criteria ID | AC-{ModuleNumber}-{FeaturePointSequence} |

## Business Acceptance
| No. | Acceptance Scenario | Expected Result | Verification Method | Status |

## Technical Acceptance
| No. | Acceptance Item | Standard | Status |

## Integration Acceptance
| No. | Acceptance Item | Verification Method | Status |
```

### Step 7: Generate Code Framework (Optional)

For P0 feature points, generate code framework:
- Backend Controller/Service/Mapper/Domain
- Frontend Vue components

---

## 3. Architecture Consultation Process

```
pdd-generate-spec starts
    │
    ├─► Identify technology selection needs
    │       │
    │       ▼
    │   system-architect consultation
    │       │
    │       ▼
    │   Return technology stack recommendations
    │
    ├─► Identify module design needs
    │       │
    │       ▼
    │   software-architect consultation
    │       │
    │       ▼
    │   Return module boundary recommendations
    │
    └─► Continue generating specifications
```

### 3.1 system-architect Invocation Example

```
Trigger Condition: Need to introduce new technology stack
Invoke: system-architect
Input:
  - Feature Requirements: Message push functionality
  - Constraints: Need to support multi-channel push
  - Existing Technology Stack: Spring Boot

Return:
  - Technology selection recommendations
  - Architecture Decision Record (ADR)
  - Project structure recommendations
```

### 3.2 software-architect Invocation Example

```
Trigger Condition: Unclear module boundaries
Invoke: software-architect
Input:
  - Feature Requirements: Transfer application and approval module
  - Existing Modules: Asset management base module
  - Complexity: High

Return:
  - Module division plan
  - Interface boundary definition
  - Design pattern recommendations
```

---

## 4. Guardrails

- Interface design must follow RESTful specifications
- Data models must include audit fields
- Business rules must be consistent with PRD
- Test cases must cover all business rules
- **Architecture decisions must consult architect skills**
- **Module design must follow high cohesion and low coupling principles**

---

## 5. Collaboration with Other Skills

| Collaborative Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **system-architect** | Consultation | Technical requirements, constraints | Technology selection, architecture decisions |
| **software-architect** | Consultation | Module requirements, interface design | Module division, interface specifications |
| **pdd-implement-feature** | Sequential | spec.md, checklist.md | Code implementation |
| **pdd-code-reviewer** | Sequential | Code + specifications | Review report |

---

## 6. Document System Specifications

This Skill follows the PDD framework document system specifications.

### 6.1 Output Documents

| Document Type | File Name | Core Content |
|---------|--------|---------|
| Development Specification | spec.md | Interface design, data model, business logic, technical implementation |
| Acceptance Criteria | checklist.md | Acceptance items, acceptance conditions, acceptance methods |

### 6.2 Naming Conventions

```
dev-specs/FP-{ModuleNumber}-{Sequence}/
├── spec.md
└── checklist.md
```

### 6.3 Version Management

- Every document modification must update the change history
- Record modification date, modifier, and change content

---

## 7. PDD Implementation Specification Reference

This Skill follows the PDD framework implementation specifications, see [pdd-framework-design.md Chapter 9](../docs/pdd-framework-design.md#9-pdd-实施规范).
