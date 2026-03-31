---
name: pdd-main
description: Main entry Skill for PRD-Driven Development, orchestrating the entire development process. Invoke this Skill when users want to develop features based on PRD documents. 支持中文触发：PRD驱动开发、基于PRD开发、PDD开发、功能开发、PRD开发。
license: MIT
compatibility: Requires complete PRD document system
metadata:
  author: neuqik@hotmail.com
  version: "3.2"
---

# PDD-MAIN - PRD-Driven Development Main Entry

**Core Concept**: PDD (PRD-Driven Development) is a development methodology that combines domain expert capabilities. By integrating system-architect, software-architect, software-engineer, and expert-xxx skills, it achieves comprehensive intelligence from requirement analysis to final delivery.

**Input**: PRD document directory path

**Output**: Completed feature code and verification report

---

## Version History

| Version | Date | Changes |
|-----|------|---------|
| 3.4 | 2026-03-22 | Added PDD implementation specification reference, updated skill collaboration process |
| 3.3 | 2026-03-21 | Fixed code directory generation rules: new business features create independent Maven modules, not in asset-system |
| 3.2 | 2026-03-21 | Added automatic code directory generation capability (module number → code path mapping) |
| 3.1 | 2026-03-21 | Added intelligent PRD discovery capability (module number auto-discovery + manual document specification) |
| 3.0 | 2026-03-21 | Integrated system-architect, software-architect, software-engineer skills |
| 2.0 | 2026-03-08 | Rined four-phase process, enhanced verification mechanism |
| 1.0 | Early | Initial version |

---

## 1. Methodology Architecture

### 1.1 PDD Skill System

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN (Main Entry)                      │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │  Process    │  State      │  Context    │  Result     │      │
│  │ Orchestration│ Management │  Transfer   │ Aggregation │      │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   PDD Process │     │  Architect    │     │   Engineer    │
│     Layer     │     │    Layer      │     │    Layer      │
├───────────────┤     ├───────────────┤     ├───────────────┤
│ pdd-ba        │     │system-architect│    │software-eng   │
│ pdd-extract   │◄───►│               │◄───►│               │
│ pdd-generate  │     │software-arch  │     │ expert-xxx    │
│ pdd-implement │     │               │     │               │
│ pdd-review    │     │               │     │               │
│ pdd-verify    │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

### 1.2 Skill Classification and Responsibilities

| Category | Skill Name | Core Responsibility | Capability Boundary |
|------|---------|---------|---------|
| **Main Entry** | pdd-main | Process orchestration, state management, context transfer | Does not directly implement code |
| **PDD Process** | pdd-ba, pdd-extract-features, pdd-generate-spec, pdd-implement-feature, pdd-code-reviewer, pdd-verify-feature | Business analysis, specification generation, code implementation, review verification | Each responsible for specific phase |
| **Architect** | system-architect | System architecture design, technology selection | High-level design, architecture decisions |
| | software-architect | Software architecture design, module division | Module design, interface specification |
| **Engineer** | software-engineer | Code implementation, test writing | Execute implementation based on specification |
| **Expert** | expert-ruoyi | RuoYi framework specific issues | Framework configuration, code generation |
| | expert-activiti | Activiti workflow engine | BPMN design, process deployment |
| | expert-mysql | MySQL database optimization | SQL optimization, index design |
| | expert-code-quality | Code quality and refactoring | Smell detection, design patterns |

---

## 2. Complete Process

### 2.1 Six-Phase Process

```
Phase 1: Business Analysis and Feature Extraction
  PRD Document → 5W1H Analysis → Use Case Diagram → Flowchart → State Diagram → Feature Matrix

Phase 2: Development Specification Generation
  Feature Matrix → Architecture Consultation → Interface Design → Data Model → Dev Spec + Acceptance Criteria

Phase 3: Feature Loop
  For each feature: Implementation → Review → Fix → Acceptance

Phase 4: Architecture Review Integration
  On-demand system-architect / software-architect invocation

Phase 5: Expert Skills Integration
  On-demand expert-xxx invocation

Phase 6: Delivery and Retrospective
  Development Report → Document Archival → Lessons Learned
```

### 2.2 Detailed Process Steps

#### Step 1: Parse Input and Discover PRD Documents

**Two Input Modes Supported**:

**Mode A: Module Number Auto-Discovery**
- User inputs module number (e.g., `ZCCZ-2`, `ZCCZ-1`)
- Automatically scans `docs/business-analysis/` directory
- Matches directory names (e.g., `ZCCZ-2-Asset-Transfer`)
- Automatically aggregates all design documents in that directory

**Mode B: Manual Document Specification**
- User directly specifies one or more design document paths
- Supports single file: `docs/xxx/ZCCZ-2/PRD-Asset-Transfer.md`
- Supports multiple files: separated by comma or newline
- Supports directory path: automatically discovers all .md documents in directory

**Standard PRD Document Structure**:
```
docs/business-analysis/{business-domain}/
├── PRD-{module-name}.md              # Requirements document
├── UseCase-{module-name}.md          # Use case diagram
├── BusinessFlow-{module-name}.md     # Flowchart
├── StateDiagram-{module-name}.md     # State diagram
├── SequenceDiagram-{module-name}.md  # Sequence diagram (optional)
└── FormDesign/                       # Form design documents (optional)
```

**Auto-Discovery Process**:
```
User Input: "ZCCZ-2"
    ↓
Scan docs/business-analysis/*/ZCCZ-2*/
    ↓
Match: docs/business-analysis/asset-disposition/ZCCZ-2-Asset-Transfer/
    ↓
Aggregate Documents:
  - PRD-Asset-Transfer.md
  - UseCase-Asset-Transfer.md
  - BusinessFlow-Asset-Transfer.md
  - StateDiagram-Asset-Transfer.md
  - SequenceDiagram-Asset-Transfer-Process.md
    ↓
Confirm Document Completeness
```

#### Step 2: Confirm Module Information

Extract module number and name from PRD document:
- Module Number: ZCCZ-1, ZCCZ-2, ...
- Module Name: Equity Transfer, Asset Transfer, ...

#### Step 3: Identify Technology Stack

Analyze project technology stack, determine which skills to invoke:
- RuoYi framework project → software-engineer + expert-ruoyi
- Workflow project → expert-activiti
- Database intensive → expert-mysql
- Architecture design phase → system-architect / software-architect

#### Step 4: Invoke Business Analysis

Invoke `pdd-ba` skill:
- Input: PRD document path
- Output: Business analysis report
- Uses 5W1H, MECE, CRUD methodologies

#### Step 5: Invoke Feature Extraction

Invoke `pdd-extract-features` skill:
- Input: PRD document path + Business analysis report
- Output: feature-matrix.md

#### Step 6: Manual Review of Feature Matrix

Wait for user to review feature matrix:
- Confirm feature completeness
- Confirm complexity assessment
- Confirm test strategy
- Confirm AI role assignment

#### Step 7: Invoke Specification Generation

Invoke `pdd-generate-spec` skill:
- Input: Feature matrix
- Output: spec.md, checklist.md

**Architecture Consultation (On-Demand)**:
- Invoke `system-architect`: Technology selection, system architecture
- Invoke `software-architect`: Module division, interface design

#### Step 8: Manual Review of Specification

Wait for user to review development specification:
- Confirm interface design
- Confirm data model
- Confirm business logic
- Confirm test cases

#### Step 8.1: Generate Code Directory Structure

Automatically generate code directory that conforms to standards based on module number and functionality.

**⚠️ Important Principles**:
- **New business features should create independent Maven modules**, do not put in `asset-system`
- `asset-system` is the system management module, only contains system-related code (users, roles, menus, etc.)
- Business module naming convention: `asset-{business-domain}` (e.g., `asset-disposition`, `asset-equity`)

**Module Number to Code Path Mapping**:

| Module Number | Feature Name | Maven Module | Backend Package Path | Frontend Path |
|---------|---------|----------|-----------|---------|
| ZCCZ-1 | Equity Transfer | asset-equity | com.example.equity.transfer | equity-transfer |
| ZCCZ-2 | Asset Transfer | asset-equity | com.example.equity.transfer | asset-transfer |
| ZCCZ-3 | Enterprise Capital Increase | asset-equity | com.example.equity.capital | capital-increase |
| ZCCZ-4 | Equity Free Allocation | asset-equity | com.example.equity.allocation | equity-allocation |
| ZCCZ-5 | Asset Lease | asset-lease | com.example.lease | asset-lease |
| ZCCZ-6 | Enterprise Guarantee | asset-guarantee | com.example.guarantee | enterprise-guarantee |
| ZCCZ-7 | Fixed Asset Disposal | asset-disposition | com.example.disposition | fixed-asset-scrap |

**Backend Module Directory Structure**:

```
asset-{business-domain}/                    # Independent Maven module
├── pom.xml
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/example/{module}/
    │   │       ├── controller/        # Controllers
    │   │       ├── domain/            # Entity classes
    │   │       │   └── vo/            # VO objects
    │   │       ├── mapper/            # Mapper interfaces
    │   │       ├── service/           # Service interfaces
    │   │       │   └── impl/          # Service implementations
    │   │       ├── constant/          # Constant classes
    │   │       └── util/              # Utility classes
    │   └── resources/
    │       └── mapper/
    │           └── {module}/          # Mapper XML
    └── test/
        └── java/
            └── com/example/{module}/     # Test classes
```

**Frontend Directory Structure**:

```
asset-ui/src/
├── api/
│   └── {module}/              # API interfaces
│       └── {feature}.js
└── views/
    └── {module}/              # View pages (camelCase)
        ├── index.vue          # List page
        ├── form.vue           # Form page
        └── detail.vue         # Detail page
```

**Example: ZCCZ-1 Equity Transfer**

```
Backend:
  asset-equity/                          # Create independent module
  ├── pom.xml
  └── src/main/java/com/example/equity/transfer/
      ├── controller/
      │   └── EquityTransferApplyController.java
      ├── domain/
      │   ├── EquityTransferApply.java
      │   └── vo/
      ├── mapper/
      ├── service/
      │   └── impl/
      └── constant/
  └── src/main/resources/mapper/equity/transfer/

Frontend:
  asset-ui/src/api/equity/transfer.js
  asset-ui/src/views/equity-transfer/
  ├── index.vue
  ├── form.vue
  └── detail.vue
```

**Existing Module Reuse Rules**:

| Existing Module | Applicable Business | Description |
|---------|---------|------|
| asset-disposition | Asset disposal type | Fixed asset disposal, asset write-off, etc. (already exists) |
| asset-equity | Equity transaction type | Equity transfer, enterprise capital increase, etc. (needs to be created) |
| asset-admin | System management | Controller entry, configuration, etc. |
| asset-system | System functions | Users, roles, menus, etc. (do not put business code) |

**Error Examples (To Avoid)**:

```
❌ Wrong: Put business code in asset-system
asset-system/src/main/java/com/example/equity/  # Wrong!

✅ Correct: Create independent business module
asset-equity/src/main/java/com/example/equity/  # Correct!
```

#### Step 9: Loop Through Feature Implementation

For each feature (by priority P0 → P1 → P2):

**a. Invoke Feature Implementation**
- Invoke `pdd-implement-feature` skill
- Input: Development specification, Acceptance criteria
- Output: Code files

**b. Invoke Software Engineer**
- Invoke `software-engineer` skill
- Responsibility: Execute code implementation based on specification

**c. Expert Consultation (On-Demand)**
- RuoYi issues → `expert-ruoyi`
- Database issues → `expert-mysql`
- Code quality issues → `expert-code-quality`

**d. Invoke Code Review**
- Invoke `pdd-code-reviewer` skill
- Input: Code files, Development specification, Acceptance criteria
- Output: Review report

**e. Architecture Review (On-Demand)**
- Found architecture issues → `software-architect`
- Found system issues → `system-architect`

**f. Handle Review Results**
- No Critical issues → Continue to acceptance
- Has Critical issues → Fix and re-review

**g. Invoke Feature Verification**
- Invoke `pdd-verify-feature` skill
- Input: Code files, Development specification, Acceptance criteria
- Output: Acceptance report

**h. Handle Acceptance Results**
- Passed → Mark feature as complete
- Conditionally passed → Fix issues and re-verify
- Not passed → Re-develop

#### Step 10: Output Development Report

Generate final development report

---

## 3. Skill Integration

### 3.1 system-architect Integration

**Trigger Conditions**:
- New project initialization
- Technology stack selection
- System architecture design
- Major architecture changes

**Service Content**:
- Project structure design
- Technology stack recommendation
- Code standard definition
- Architecture Decision Records (ADR)

### 3.2 software-architect Integration

**Trigger Conditions**:
- Module division decisions
- Interface design review
- Data architecture design
- Architecture drift detected

**Service Content**:
- Module boundary definition
- Interface specification design
- Design pattern recommendation
- Architecture recommendations

### 3.3 software-engineer Integration

**Trigger Conditions**:
- Code implementation phase
- Unit test writing
- Code refactoring
- Defect fixing

**Service Content**:
- Implement code based on specification
- Follow project coding standards
- Error handling best practices
- Layered architecture implementation

### 3.4 expert-xxx Integration

| Expert Skill | Trigger Condition | Expected Output |
|---------|---------|---------|
| **expert-ruoyi** | RuoYi framework issues | Solution + Best practices |
| **expert-activiti** | Workflow issues | BPMN design recommendations |
| **expert-mysql** | Database issues | SQL optimization plan |
| **expert-code-quality** | Code quality issues | Refactoring plan |

---

## 4. AI Collaboration Mode

Automatically select AI role based on feature complexity:

| Complexity | AI Role | Human Involvement | Applicable Scenarios |
|--------|--------|-----------|----------|
| P0 | Collaborator + Architect + Expert | High | Core business processes, complex state transitions |
| P1 | Collaborator + Architect | Medium | Important features, medium complexity |
| P2 | Leader + Engineer | Low | Simple features, auxiliary features |

### Complexity and Skill Invocation Strategy

```
P0 (Core Business):
  pdd-main + pdd-ba + pdd-generate-spec
    ↓ Architecture consultation
  system-architect + software-architect
    ↓
  pdd-implement-feature + software-engineer
    ↓ + expert-ruoyi + expert-mysql
  pdd-code-reviewer + software-architect
    ↓
  pdd-verify-feature

P1 (Important Features):
  pdd-main + pdd-extract + pdd-generate-spec
    ↓ On-demand consultation
  software-architect (if needed)
    ↓
  pdd-implement-feature + software-engineer
    ↓ + expert-xxx (on-demand)
  pdd-code-reviewer
    ↓
  pdd-verify-feature

P2 (Auxiliary Features):
  pdd-main + pdd-generate-spec
    ↓
  pdd-implement-feature + software-engineer (lead)
    ↓
  pdd-code-reviewer (simplified)
    ↓
  pdd-verify-feature
```

---

## 5. Sub-Skill List

| Skill Name | Description | Input | Output | Trigger Timing |
|-----------|---------|------|------|----------|
| **pdd-ba** | Business analysis, using professional methodologies for requirement derivation | PRD document path | Business analysis report | At process start |
| **pdd-extract-features** | Extract feature matrix from PRD | PRD document path | feature-matrix.md | After business analysis |
| **pdd-generate-spec** | Generate development specification | Feature matrix | spec.md, checklist.md | After feature confirmation |
| **pdd-implement-feature** | Implement feature code | Development specification | Code files | After specification confirmation |
| **pdd-code-reviewer** | Code review, verify implementation conforms to specification | Code + Specification | Review report | After code implementation |
| **pdd-verify-feature** | Verify feature implementation | Code + Acceptance criteria | Acceptance report | After code review |
| **pdd-doc-change** | Document change management | Change requirements | Updated documents | When requirements change |
| **system-architect** | System architecture consultation | Architecture requirements | Architecture plan | On-demand trigger |
| **software-architect** | Software architecture consultation | Module requirements | Module design | On-demand trigger |
| **software-engineer** | Code implementation and testing | Specification document | Code files | Implementation phase |
| **expert-ruoyi** | RuoYi framework expert consultation | Technical issues | Solution | On-demand trigger |
| **expert-activiti** | Activiti workflow expert | Process issues | Solution | On-demand trigger |
| **expert-mysql** | MySQL database expert | SQL/structure issues | Optimization recommendations | On-demand trigger |
| **expert-code-quality** | Code quality expert | Code snippets | Refactoring plan | On-demand trigger |

---

## 6. Flowcharts

### 6.1 Main Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN Main Process                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRD Document ──→ pdd-ba ──→ Business Analysis Report          │
│                │                                                │
│                ↓                                                │
│  pdd-extract-features ──→ Feature Matrix                       │
│                │                                                │
│                ↓                                                │
│           [Manual Review]                                       │
│                │                                                │
│                ↓                                                │
│  pdd-generate-spec ──→ Dev Spec + Acceptance Criteria          │
│                │                                                │
│                ├────── (on-demand) ──→ system-architect        │
│                │                                                │
│                ├────── (on-demand) ──→ software-architect      │
│                │                                                │
│                ↓                                                │
│           [Manual Review]                                       │
│                │                                                │
│                ↓                                                │
│  ┌──────────────────────────────────────┐                       │
│  │        Feature Loop Processing        │                       │
│  │  ┌────────────────────────────────┐  │                       │
│  │  │ pdd-implement-feature          │  │                       │
│  │  │         ↓                      │  │                       │
│  │  │ software-engineer              │  │                       │
│  │  │         ↓ (on-demand)          │  │                       │
│  │  │   expert-ruoyi / expert-mysql  │  │                       │
│  │  │         ↓                      │  │                       │
│  │  │ pdd-code-reviewer              │  │                       │
│  │  │         ↓ (on-demand)          │  │                       │
│  │  │   software-architect           │  │                       │
│  │  │         ↓                      │  │                       │
│  │  │ [Critical issues?] ─→ Fix ─┐   │  │                       │
│  │  │         ↓ (none)           │   │  │                       │
│  │  │ pdd-verify-feature          │   │  │                       │
│  │  │         ↓                   │   │  │                       │
│  │  │ [Passed?] ─→ Next feature   │   │  │                       │
│  │  │         ↓ (not passed)      │   │  │                       │
│  │  │      Re-develop ←───────────┘   │  │                       │
│  │  └────────────────────────────────┘  │                       │
│  └──────────────────────────────────────┘                       │
│                │                                                │
│                ↓                                                │
│           Development Report                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Skill Collaboration Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Skill Collaboration Process                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                               │
│  │ PDD Process │  Discovers issues requiring professional support│
│  │   Skills    │                                               │
│  └──────┬──────┘                                               │
│         │                                                        │
│         ├──────────────────────────────┐                        │
│         │                              │                        │
│         ▼                              ▼                        │
│  ┌──────────────┐            ┌──────────────┐                │
│  │system-arch   │            │software-arch │                │
│  │(System Arch) │            │(Software Arch)│               │
│  └──────┬──────┘            └──────┬───────┘                │
│         │                           │                         │
│         ├───────────────────────────┼─────────────────────────┤ │
│         │                           │                         │ │
│         ▼                           ▼                         │ │
│  ┌──────────────┐            ┌──────────────┐                │ │
│  │software-eng  │            │ expert-xxx   │                │ │
│  │(Code Impl)   │            │(Domain Expert)│               │ │
│  └──────┬──────┘            └──────┬───────┘                │ │
│         │                           │                         │ │
│         └───────────────────────────┼─────────────────────────┘ │
│                                     │                           │
│                           ┌──────────┴──────────┐              │
│                           ▼                       ▼              │
│                    Return to PDD Process      Result Feedback   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. AI Role Collaboration Matrix

```
                    ┌─────────────────────────────────────────┐
                    │           PDD AI Collaboration Matrix    │
                    └─────────────────────────────────────────┘

    Skill/Role      │ Scheduler│ Analyzer │ Designer │Implementer│ Reviewer │ Expert
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    pdd-main        │    ●    │         │         │         │         │
    pdd-ba          │         │    ●    │         │         │         │
    pdd-extract     │         │    ●    │         │         │         │
    pdd-generate    │         │         │    ●    │         │         │
    pdd-implement   │         │         │         │    ●    │         │
    pdd-reviewer    │         │         │         │         │    ●    │
    pdd-verify      │         │         │         │         │    ●    │
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    system-arch     │         │         │    ●    │         │    ○    │
    software-arch   │         │         │    ●    │    ○    │    ○    │
    software-eng    │         │         │         │    ●    │         │
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    expert-ruoyi    │         │         │    ○    │    ○    │    ○    │    ●
    expert-activiti │         │         │    ○    │    ○    │         │    ●
    expert-mysql    │         │         │    ○    │    ○    │    ○    │    ●
    expert-code     │         │         │    ○    │    ○    │    ●    │    ●

    Legend: ● Primary Responsibility  ○ Auxiliary Participation  │ Space Not Involved
```

---

## 8. Guardrails

- Must perform business analysis before extracting features
- Must wait for manual review of feature matrix
- Must wait for manual review of development specification
- Must perform code review after code implementation
- Each feature must pass acceptance before being marked complete
- Must synchronously update specification documents after code changes
- Issues must be recorded in lessons learned repository
- **Architecture decisions must consult architect skills**
- **Technical issues must consult expert skills**
- **Expert recommendations must be integrated into code implementation**

---

## 9. Usage Examples

### 9.1 Mode A: Module Number Auto-Discovery

```
User: I want to develop ZCCZ-2 Asset Transfer module
AI: [Invoking pdd-main skill]
     Scanning docs/business-analysis/ directory...
     Found module: ZCCZ-2-Asset-Transfer
     Path: docs/business-analysis/asset-disposition/ZCCZ-2-Asset-Transfer/

     Aggregated design documents:
     ✓ PRD-Asset-Transfer.md
     ✓ UseCase-Asset-Transfer.md
     ✓ BusinessFlow-Asset-Transfer.md
     ✓ StateDiagram-Asset-Transfer.md
     ✓ SequenceDiagram-Asset-Transfer-Process.md

     Confirm to start business analysis? [Y/n]
```

### 9.2 Mode B: Manual Document Specification

```
User: I want to develop based on these documents
     - docs/business-analysis/asset-disposition/ZCCZ-1/PRD-Equity-Transfer.md
     - docs/business-analysis/asset-disposition/ZCCZ-1/BusinessFlow-Equity-Transfer.md
     - docs/business-analysis/asset-disposition/ZCCZ-1/StateDiagram-Equity-Transfer.md

AI: [Invoking pdd-main skill]
     Received 3 design documents:
     ✓ PRD-Equity-Transfer.md
     ✓ BusinessFlow-Equity-Transfer.md
     ✓ StateDiagram-Equity-Transfer.md

     Starting business analysis...
```

### 9.3 Architecture Consultation Usage

```
User: This module needs to support multi-tenant architecture
AI: [Invoking software-architect skill]
     Consultation issue: Multi-tenant architecture design
     Passed data:
       - Feature requirements: Equity Transfer module
       - Existing architecture: Monolithic application
       - Constraints: Need to be compatible with existing permission system

     [software-architect returns architecture plan]
     Architecture Plan:
       1. Tenant identifier field design (tenant_id)
       2. Data isolation strategy (shared table + tenant field filtering)
       3. Tenant context transfer mechanism
       4. Key transformation points list

     Architecture constraints have been integrated into development specification
```

### 9.4 Expert Consultation Usage

```
User: Encountered permission issue when implementing transfer application list feature
AI: [Invoking expert-ruoyi skill]
     Consultation issue: Transfer application list interface permission check failed
     Passed data:
       - Interface path: /equity/transfer/apply/list
       - Error message: Permission check exception
       - Related code snippet: [code]

     [expert-ruoyi returns solution]
     Solution:
       1. Check @PreAuthorize annotation configuration
       2. Confirm permission identifier in sys_menu table
       3. Verify role menu assignment

     Solution has been integrated into code implementation
```

---

## 10. Requirement Change Handling

When requirements change:

```
Requirement Change
    ↓
pdd-doc-change analyzes change impact
    ↓
Update related specification documents
    ↓
Notify affected features
    ↓
┌─────────────────────────────────────┐
│ If architecture change involved:    │
│   → system-architect re-review      │
│ If technical solution change:       │
│   → Related expert-xxx re-consult   │
└─────────────────────────────────────┘
    ↓
Re-execute code review and verification
```

---

## 11. PDD Implementation Specification

This Skill follows PDD framework implementation specification, see [pdd-framework-design.md Chapter 9](../docs/pdd-framework-design.md#9-pdd-implementation-specification).

### 11.1 Core Specification Summary

| Specification | Core Content |
|------|---------|
| **Skill Boundary** | pdd-code-reviewer (compliance) → expert-code-quality (quality depth), review first then analyze |
| **Context Transfer** | File system transfer, directory structure specification, supports checkpoint resumption |
| **Manual Review** | Batch review + detailed review for key features |
| **Error Handling** | Critical blocks, pause and wait for human after 3 retries |
| **PR Management** | Manual trigger, Change-grained PR, manual archival |
| **Document System** | 9 core document types, naming convention, document internal change history |

### 11.2 Review and Quality Analysis Collaboration

```
Code Implementation Complete
    │
    ▼
pdd-code-reviewer (Compliance Review)
    │
    ├── Has Critical issues → Return to fix → Re-review
    │
    └── No Critical issues
            │
            ▼
    expert-code-quality (Quality Depth Analysis)
            │
            ▼
    Generate Quality Improvement Tasks (improvement-tasks.md)
            │
            ▼
    Enter Next Phase
```

### 11.3 Checkpoint Resumption

- **State File**: `.pdd-state.json`
- **Trigger Method**: User issues "continue execution" command
- **State Content**: Current phase, completed features, pending features

---

## 12. Reference Documentation

- [PDD Framework Design Document](../docs/pdd-framework-design.md)
- [PDD Skill Relationships Specification](../docs/pdd-skill-relationships.md)
- [system-architect SKILL.md](../system-architect/SKILL.md)
- [software-architect SKILL.md](../software-architect/SKILL.md)
- [software-engineer SKILL.md](../software-engineer/SKILL.md)
- [expert-ruoyi SKILL.md](../expert-ruoyi/SKILL.md)
- [expert-activiti SKILL.md](../expert-activiti/SKILL.md)
- [expert-mysql SKILL.md](../expert-mysql/SKILL.md)
- [expert-code-quality SKILL.md](../expert-code-quality/SKILL.md)
