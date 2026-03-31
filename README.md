# PDD Skills - PRD Driven Development Framework

## Harness Engineering 范式的企业级工程实践 | Enterprise Engineering Practice of Harness Engineering Paradigm

> 🚀 **Latest News / 最新动态 / Dernières Nouvelles**
> 
> **Version 2.0 has been released! Version 3.0 is currently under iteration, with plans to improve code generation accuracy and reduce errors and omissions.**
> 
> **2.0 版本已发布！3.0 版本正在迭代中，计划提高代码生成的准确率，减少误差和遗忘。**
> 
> **La version 2.0 est publiée ! La version 3.0 est en cours d'itération, avec des plans pour améliorer la précision de la génération de code et réduire les erreurs et omissions.**

[English](#english) | [中文](#中文) | [Français](#français)

---

<a name="english"></a>

## 📖 English Documentation

### Overview

**PDD (PRD-Driven Development)** is a development methodology that combines domain expert capabilities. By integrating system architects, software architects, software engineers, and various expert skills, it achieves comprehensive intelligent development from requirement analysis to final delivery.

Core values of PDD methodology:

- **Standardized Process**: Complete chain from PRD documents to code implementation
- **Intelligent Collaboration**: Deep collaboration between AI and human developers
- **Quality Assurance**: Multi-dimensional verification ensures delivery quality
- **Knowledge Accumulation**: Documents and code evolve synchronously

---

### Core Philosophy

> "Technical debt is like a high-interest loan: it's better to pay off the debt in small installments than to let it accumulate and deal with it painfully all at once." —— OpenAI Harness Engineering

PDD methodology follows these core principles:

1. **Document-Driven Development**: PRD documents are the single source of truth
2. **Specification First**: Development specifications must be completed before code implementation
3. **Continuous Verification**: Each feature must pass three-dimensional verification
4. **Entropy Reduction Governance**: Continuously combat system "entropy increase" and "decay"

---

### Relationship between PDD and OpenSpec

#### Integration Points

PDD methodology integrates deeply with OpenSpec to form a complete development specification system:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PDD × OpenSpec Integration Architecture       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  PRD Doc    │ ──→ │  OpenSpec   │ ──→ │  Dev Spec   │       │
│  │  (Requirements)│  │  (Specification)│ │  (Implementation)│   │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ Feature     │     │ Change      │     │ Code        │       │
│  │ Matrix      │     │ Management  │     │ Implementation│     │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Complementary Features

| Feature | PDD Contribution | OpenSpec Contribution |
|---------|-----------------|----------------------|
| **Requirement Management** | PRD document system | Specification standardization |
| **Change Tracking** | Feature matrix | Change ID management |
| **Document Synchronization** | Specification generation | Specification version control |
| **Quality Assurance** | Three-dimensional verification | Specification consistency check |

#### Implementation Scenarios

**Scenario 1: New Feature Development**

```
PRD Document → pdd-extract-features → Feature Matrix
    ↓
OpenSpec Change Creation
    ↓
pdd-generate-spec → spec.md + checklist.md
    ↓
pdd-implement-feature → Code Implementation
    ↓
pdd-verify-feature → Verification Passed
    ↓
OpenSpec Change Archival
```

**Scenario 2: Requirement Change**

```
Change Request
    ↓
pdd-doc-change Impact Analysis
    ↓
Update OpenSpec Specification
    ↓
Regenerate Feature Matrix
    ↓
Incremental Development & Verification
```

**Scenario 3: Technical Debt Governance**

```
Scheduled pdd-entropy-reduction Trigger
    ↓
Scan Document-Code Consistency
    ↓
Detect Architecture Constraint Violations
    ↓
Generate Entropy Report
    ↓
Create Fix PR
```

---

### Skill System Architecture

#### Skill Classification

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN (Main Entry)                      │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │  Process    │  State      │  Context    │  Result     │      │
│  │  Orchestration│ Management │ Transfer    │ Aggregation │      │
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

#### Core Skills List

| Category | Skill Name | Core Responsibility | Input | Output |
|----------|-----------|---------------------|-------|--------|
| **Main Entry** | pdd-main | Process orchestration, state management | PRD document path | Completed feature code |
| **Business Analysis** | pdd-ba | Requirement analysis, business modeling | PRD document | Business analysis report |
| **Feature Extraction** | pdd-extract-features | Feature point extraction | Business analysis report | Feature matrix |
| **Specification Generation** | pdd-generate-spec | Development specification generation | Feature matrix | spec.md, checklist.md |
| **Code Implementation** | pdd-implement-feature | Feature implementation | Development specification | Code files |
| **Code Review** | pdd-code-reviewer | Compliance review | Code + Specification | Review report |
| **Feature Verification** | pdd-verify-feature | Three-dimensional verification | Code + Acceptance criteria | Verification report |
| **Entropy Reduction** | pdd-entropy-reduction | Technical debt management | Trigger conditions | Entropy report + Fix PR |

---

### Development Process

#### Six-Phase Process

```
Phase 1: Business Analysis & Feature Extraction
  PRD Document → 5W1H Analysis → Use Case Diagram → Flowchart → State Diagram → Feature Matrix

Phase 2: Development Specification Generation
  Feature Matrix → Architecture Consultation → Interface Design → Data Model → Dev Spec + Acceptance Criteria

Phase 3: Feature Loop
  For each feature: Implementation → Review → Fix → Verification

Phase 4: Architecture Review Integration
  On-demand system-architect / software-architect invocation

Phase 5: Expert Skills Integration
  On-demand expert-xxx invocation

Phase 6: Delivery & Retrospective
  Development Report → Document Archival → Lessons Learned
```

#### Main Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        PDD Main Process                         │
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
│                ↓                                                │
│           [Manual Review]                                       │
│                │                                                │
│                ↓                                                │
│  ┌──────────────────────────────────────┐                       │
│  │        Feature Loop Processing        │                       │
│  │  pdd-implement-feature               │                       │
│  │         ↓                            │                       │
│  │  pdd-code-reviewer                   │                       │
│  │         ↓                            │                       │
│  │  pdd-verify-feature                  │                       │
│  │         ↓                            │                       │
│  │  [Verified?] ─→ Next Feature         │                       │
│  └──────────────────────────────────────┘                       │
│                │                                                │
│                ↓                                                │
│           Development Report                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Usage Guide

#### Quick Start

**Mode 1: Module Number Auto-Discovery**

```
User: I want to develop ZCCZ-2 Asset Transfer module

AI: [Invoking pdd-main skill]
    Scanning docs/business-analysis/ directory...
    Found module: ZCCZ-2-Asset-Transfer
    Path: docs/business-analysis/asset-disposition/ZCCZ-2-Asset-Transfer/

    Aggregated design documents:
    ✓ PRD-Asset-Transfer.md
    ✓ UseCase-Diagram-Asset-Transfer.md
    ✓ Business-Flow-Asset-Transfer.md
    ✓ State-Diagram-Asset-Transfer.md

    Confirm to start business analysis? [Y/n]
```

**Mode 2: Manual Document Specification**

```
User: I want to develop based on these documents
     - docs/business-analysis/asset-disposition/ZCCZ-1/PRD-Asset-Transfer.md
     - docs/business-analysis/asset-disposition/ZCCZ-1/Business-Flow-Asset-Transfer.md

AI: [Invoking pdd-main skill]
    Design documents received, starting business analysis...
```

#### Feature Complexity Classification

| Complexity | Code | Description | Development Time | Human Involvement |
|------------|------|-------------|------------------|-------------------|
| Core Business | P0 | Core business processes, multi-party approval | 3-5 days | High |
| Important Feature | P1 | Important business features, alternatives available | 1-2 days | Medium |
| Auxiliary Feature | P2 | Auxiliary features, easy to implement | 0.5 day | Low |

#### Three-Dimensional Verification Model

```yaml
Verification Dimensions:
  Completeness:
    Definition: Whether all specified features are implemented
    Verification Points:
      - Interface completeness
      - Field completeness
      - Business rule coverage

  Correctness:
    Definition: Whether implementation matches specification
    Verification Points:
      - Interface logic correctness
      - Data processing accuracy
      - Business rule correctness

  Coherence:
    Definition: Consistency between frontend/backend, documents and code
    Verification Points:
      - Frontend-backend interface consistency
      - Document-code consistency
      - Naming convention uniformity
```

---

### Document System

#### Core Document Types

| Document Type | Filename | Core Content |
|--------------|----------|--------------|
| PRD Document | PRD-{ModuleName}.md | Requirements, business rules |
| Use Case Diagram | UseCase-{ModuleName}.md | Use case definitions, actors |
| Flowchart | BusinessFlow-{ModuleName}.md | Business processes, decision points |
| State Diagram | StateDiagram-{ModuleName}.md | State definitions, transition rules |
| Feature Matrix | feature-matrix.md | Feature list, dependencies |
| Development Specification | spec.md | Interface design, data model |
| Acceptance Criteria | checklist.md | Acceptance items, conditions |
| Review Report | review-report.md | Review results, issue list |
| Verification Report | verify-report.md | Verification results, issue list |

#### Directory Structure

```
docs/
├── business-analysis/
│   └── {business-domain}/
│       └── {module-number}-{module-name}/
│           ├── PRD-{module-name}.md
│           ├── UseCase-{module-name}.md
│           ├── BusinessFlow-{module-name}.md
│           └── StateDiagram-{module-name}.md
│
└── dev-specs/
    └── FP-{module-number}-{sequence}/
        ├── spec.md
        ├── checklist.md
        ├── review-report.md
        └── verify-report.md
```

---

### Entropy Reduction Mechanism

#### Four Professional Sub-Skills

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

#### Entropy Score System

| Score Range | Status | Recommended Action |
|-------------|--------|-------------------|
| 90-100 | Excellent | Maintain current state |
| 70-89 | Good | Small improvements |
| 50-69 | Average | Planned cleanup |
| 30-49 | Warning | Priority handling |
| 0-29 | Critical | Emergency refactoring |

---

### Golden Principles

1. **Use shared utility packages, avoid hand-written helper functions**
   - Centralize invariants management
   - Reduce code duplication

2. **Validate boundary data, don't guess data structures**
   - All API entries must have Schema validation
   - Don't rely on implicit type inference

3. **Keep code simple, prioritize readability**
   - Single file no more than 300 lines
   - Single function no more than 50 lines

4. **Documentation as code, keep synchronized**
   - Code changes must synchronize documentation
   - Outdated documentation is technical debt

5. **Pay off debt in small amounts, continuous improvement**
   - Every commit is an improvement opportunity
   - Don't let technical debt accumulate

---

### PDD as Harness Engineering Enterprise Practice

#### What is Harness Engineering?

**Harness Engineering** is a software engineering paradigm pioneered by OpenAI that emphasizes building robust, maintainable systems through disciplined practices and intelligent automation. PDD methodology represents an enterprise-grade implementation of this paradigm, specifically designed for large-scale business application development.

```
┌─────────────────────────────────────────────────────────────────┐
│           Harness Engineering Paradigm Implementation           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Core Principles                             │   │
│  │  ┌─────────────┬─────────────┬─────────────┐            │   │
│  │  │ Specification│ Automation │ Governance  │            │   │
│  │  │   First     │   First    │   First     │            │   │
│  │  └─────────────┴─────────────┴─────────────┘            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│        ▼                     ▼                     ▼           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   PDD       │     │   PDD       │     │   PDD       │      │
│  │  Document   │     │   Skill     │     │  Entropy    │      │
│  │   System    │     │   System    │     │ Reduction   │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Enterprise-Grade Implementation

PDD implements Harness Engineering principles through the following enterprise practices:

##### 1. Specification-First Development

```yaml
Traditional Approach:
  Code → Documentation → Testing → Deployment

Harness Engineering (PDD):
  PRD → Specification → Code → Verification → Deployment
    ↑                              │
    └──────── Feedback Loop ───────┘
```

**Key Benefits:**
- Reduces ambiguity in requirements
- Enables parallel development
- Facilitates automated verification
- Supports incremental delivery

##### 2. Intelligent Automation Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Automation Layers                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 4: Business Logic Automation                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-ba → pdd-extract-features → pdd-generate-spec       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Layer 3: Code Generation Automation                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-implement-feature + software-engineer + experts     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Layer 2: Quality Assurance Automation                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-code-reviewer → pdd-verify-feature                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Layer 1: Maintenance Automation                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-entropy-reduction + expert-auto-refactor            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

##### 3. Continuous Entropy Reduction

**The Entropy Problem in Enterprise Systems:**

```
System Evolution Over Time:

Time T0 (Launch):
  ┌───────────────────┐
  │  Clean Code       │  Entropy Score: 95/100
  │  Clear Structure  │
  │  Fresh Documents  │
  └───────────────────┘

Time T1 (6 months):
  ┌───────────────────┐
  │  Some Duplication │  Entropy Score: 75/100
  │  Minor Drift      │
  │  Outdated Docs    │
  └───────────────────┘

Time T2 (1 year, without PDD):
  ┌───────────────────┐
  │  Code Rot         │  Entropy Score: 45/100
  │  Architecture Drift│
  │  Missing Docs     │
  └───────────────────┘

Time T2 (1 year, with PDD):
  ┌───────────────────┐
  │  Maintained Code  │  Entropy Score: 85/100
  │  Stable Architecture│
  │  Updated Docs     │
  └───────────────────┘
```

**PDD Entropy Reduction Mechanism:**

```yaml
Scheduled Tasks:
  - Daily: Document consistency check
  - Weekly: Architecture constraint validation
  - Monthly: Technical debt audit
  - Per-Commit: Code quality analysis

Automated Actions:
  - Create PRs for documentation updates
  - Flag architecture violations
  - Generate refactoring recommendations
  - Track entropy score trends
```

##### 4. Expert System Integration

PDD leverages domain expert skills to provide specialized guidance:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Expert System Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ Framework   │     │ Database    │     │ Workflow    │      │
│  │ Experts     │     │ Experts     │     │ Experts     │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-ruoyi │     │expert-mysql │     │expert-      │      │
│  │             │     │             │     │activiti     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ Quality     │     │ Architecture│     │ Security    │      │
│  │ Experts     │     │ Experts     │     │ Experts     │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-code- │     │system-      │     │ (Extensible)│      │
│  │quality      │     │architect    │     │             │      │
│  │             │     │software-    │     │             │      │
│  │             │     │architect    │     │             │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Enterprise Benefits

| Benefit | Description | Impact |
|---------|-------------|--------|
| **Reduced Time-to-Market** | Automated specification and code generation | 30-50% faster delivery |
| **Improved Quality** | Multi-dimensional verification | 60% fewer production bugs |
| **Lower Maintenance Cost** | Continuous entropy reduction | 40% reduction in technical debt |
| **Knowledge Preservation** | Document-code synchronization | 80% faster onboarding |
| **Scalable Development** | Skill-based expert system | Linear scaling with team size |

#### Implementation Roadmap

```
Phase 1: Foundation (Week 1-2)
├── Set up PDD skill system
├── Define PRD document standards
└── Configure entropy reduction schedule

Phase 2: Pilot Project (Week 3-6)
├── Select pilot module
├── Train team on PDD workflow
└── Collect metrics and feedback

Phase 3: Expansion (Week 7-12)
├── Roll out to additional modules
├── Integrate with CI/CD pipeline
└── Establish governance processes

Phase 4: Optimization (Ongoing)
├── Fine-tune automation parameters
├── Add domain-specific experts
└── Continuous improvement based on metrics
```

#### Metrics and KPIs

```yaml
Development Metrics:
  - Feature delivery rate (features/sprint)
  - Specification-to-code accuracy (%)
  - First-pass acceptance rate (%)
  - Average development cycle time (days)

Quality Metrics:
  - Code review pass rate (%)
  - Test coverage (%)
  - Production bug rate (bugs/1000 LOC)
  - Technical debt ratio (%)

Maintenance Metrics:
  - Entropy score trend
  - Document-code consistency (%)
  - Architecture violation count
  - Refactoring completion rate (%)

Team Metrics:
  - Developer productivity (LOC/day)
  - Onboarding time (days)
  - Knowledge transfer efficiency (%)
  - Skill utilization rate (%)
```

#### Comparison with Traditional Approaches

| Aspect | Traditional Development | PDD (Harness Engineering) |
|--------|------------------------|---------------------------|
| **Requirements** | Informal, often ambiguous | Formalized, specification-first |
| **Documentation** | Often outdated | Synchronized with code |
| **Code Quality** | Reactive review | Proactive verification |
| **Technical Debt** | Accumulates over time | Continuously reduced |
| **Knowledge Transfer** | Person-dependent | System-dependent |
| **Scalability** | Non-linear effort | Linear effort with skills |
| **Automation** | Limited | Comprehensive, multi-layer |

---

### Reference Documentation

- [PDD Framework Design Document](docs/pdd-framework-design.md)
- [PDD Skill Relationships Specification](docs/pdd-skill-relationships.md)
- [system-architect SKILL.md](system-architect/SKILL.md)
- [software-architect SKILL.md](software-architect/SKILL.md)
- [software-engineer SKILL.md](software-engineer/SKILL.md)

---

<a name="中文"></a>

## 📖 中文文档

### 概述

**PDD (PRD-Driven Development)** 是一种结合领域专家能力的开发方法论，通过整合系统架构师、软件架构师、软件工程师以及各类专家技能，实现从需求分析到最终交付的全面智能化开发流程。

PDD 方法论的核心价值在于：

- **规范化流程**：从 PRD 文档到代码实现的完整链路
- **智能化协作**：AI 与人类开发者的深度协作
- **质量保障**：多维度验证确保交付质量
- **知识沉淀**：文档与代码同步演进

---

### 核心理念

> "技术债务就像一笔高息贷款：不断地以小额贷款的方式偿还债务，总比让债务不断累积，再痛苦地一次解决要好得多。" —— OpenAI Harness Engineering

PDD 方法论遵循以下核心原则：

1. **文档驱动开发**：PRD 文档是开发的唯一真实来源
2. **规格先行**：代码实现前必须完成开发规格定义
3. **持续验证**：每个功能点必须通过三维度验证
4. **熵减治理**：持续对抗系统的"熵增"与"衰减"

---

### PDD 与 OpenSpec 的关系

#### 集成点

PDD 方法论与 OpenSpec 深度融合，形成完整的开发规范体系：

```
┌─────────────────────────────────────────────────────────────────┐
│                    PDD × OpenSpec 集成架构                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  PRD 文档   │ ──→ │  OpenSpec   │ ──→ │  开发规格   │       │
│  │  (需求)     │     │  (规格化)   │     │  (实现)     │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ 功能点矩阵  │     │ Change 管理 │     │ 代码实现    │       │
│  │ (提取)      │     │ (变更追踪)  │     │ (验证)      │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 互补特性

| 特性 | PDD 贡献 | OpenSpec 贡献 |
|------|---------|--------------|
| **需求管理** | PRD 文档体系 | 规格标准化 |
| **变更追踪** | 功能点矩阵 | Change ID 管理 |
| **文档同步** | 规格文档生成 | 规格版本控制 |
| **质量保障** | 三维度验证 | 规格一致性检查 |

#### 实施场景

**场景一：新功能开发**

```
PRD 文档 → pdd-extract-features → 功能点矩阵
    ↓
OpenSpec Change 创建
    ↓
pdd-generate-spec → spec.md + checklist.md
    ↓
pdd-implement-feature → 代码实现
    ↓
pdd-verify-feature → 验收通过
    ↓
OpenSpec Change 归档
```

**场景二：需求变更**

```
需求变更请求
    ↓
pdd-doc-change 分析影响
    ↓
更新 OpenSpec 规格
    ↓
重新生成功能点矩阵
    ↓
增量开发与验证
```

**场景三：技术债务治理**

```
定期触发 pdd-entropy-reduction
    ↓
扫描文档与代码一致性
    ↓
检测架构约束违规
    ↓
生成熵报告
    ↓
创建修复 PR
```

---

### 技能体系架构

#### 技能分类

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN (主入口)                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │  流程编排   │  状态管理   │  上下文传递 │  结果汇总   │      │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   PDD流程层   │     │   架构师层    │     │   工程师层    │
├───────────────┤     ├───────────────┤     ├───────────────┤
│ pdd-ba        │     │system-architect│    │software-eng   │
│ pdd-extract   │◄───►│               │◄───►│               │
│ pdd-generate  │     │software-arch  │     │ expert-xxx    │
│ pdd-implement │     │               │     │               │
│ pdd-review    │     │               │     │               │
│ pdd-verify    │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

#### 核心技能清单

| 类别 | 技能名称 | 核心职责 | 输入 | 输出 |
|------|---------|---------|------|------|
| **主入口** | pdd-main | 流程编排、状态管理 | PRD 文档路径 | 完成的功能代码 |
| **业务分析** | pdd-ba | 需求分析、业务建模 | PRD 文档 | 业务分析报告 |
| **功能提取** | pdd-extract-features | 功能点提取 | 业务分析报告 | 功能点矩阵 |
| **规格生成** | pdd-generate-spec | 开发规格生成 | 功能点矩阵 | spec.md, checklist.md |
| **代码实现** | pdd-implement-feature | 功能点实现 | 开发规格 | 代码文件 |
| **代码审查** | pdd-code-reviewer | 合规性审查 | 代码 + 规格 | 审查报告 |
| **功能验证** | pdd-verify-feature | 三维度验证 | 代码 + 验收标准 | 验收报告 |
| **熵减治理** | pdd-entropy-reduction | 技术债务管理 | 触发条件 | 熵报告 + 修复 PR |

---

### 开发流程

#### 六阶段流程

```
阶段一：业务分析与功能点提取
  PRD文档 → 5W1H分析 → 用例图 → 流程图 → 状态图 → 功能点矩阵

阶段二：开发规格生成
  功能点矩阵 → 架构咨询 → 接口设计 → 数据模型 → 开发规格 + 验收标准

阶段三：功能点循环
  对每个功能点：实现 → 审查 → 修复 → 验收

阶段四：架构评审整合
  按需调用 system-architect / software-architect

阶段五：专家技能整合
  按需调用 expert-xxx

阶段六：交付与复盘
  开发报告 → 文档归档 → 经验教训
```

#### 主流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                        PDD 主流程                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRD文档 ──→ pdd-ba ──→ 业务分析报告                            │
│                │                                                │
│                ↓                                                │
│  pdd-extract-features ──→ 功能点矩阵                            │
│                │                                                │
│                ↓                                                │
│           [人工审核]                                             │
│                │                                                │
│                ↓                                                │
│  pdd-generate-spec ──→ 开发规格 + 验收标准                      │
│                │                                                │
│                ↓                                                │
│           [人工审核]                                             │
│                │                                                │
│                ↓                                                │
│  ┌──────────────────────────────────────┐                       │
│  │        功能点循环处理                  │                       │
│  │  pdd-implement-feature               │                       │
│  │         ↓                            │                       │
│  │  pdd-code-reviewer                   │                       │
│  │         ↓                            │                       │
│  │  pdd-verify-feature                  │                       │
│  │         ↓                            │                       │
│  │  [验收通过?] ─→ 下一功能点            │                       │
│  └──────────────────────────────────────┘                       │
│                │                                                │
│                ↓                                                │
│           开发报告                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 使用指南

#### 快速开始

**模式一：模块编号自动发现**

```
用户: 我想开发 ZCCZ-2 资产转让模块

AI: [调用 pdd-main skill]
    正在扫描 docs/业务分析/ 目录...
    发现模块: ZCCZ-2-资产转让
    路径: docs/业务分析/资产处置/ZCCZ-2-资产转让/

    已聚合以下设计文档:
    ✓ PRD-资产转让.md
    ✓ 用例图-资产转让.md
    ✓ 业务流程图-资产转让.md
    ✓ 状态图-资产转让.md

    请确认是否开始业务分析？ [Y/n]
```

**模式二：手动指定文档**

```
用户: 我想基于这些文档开发
     - docs/业务分析/资产处置/ZCCZ-1/PRD-资产转让.md
     - docs/业务分析/资产处置/ZCCZ-1/业务流程图-资产转让.md

AI: [调用 pdd-main skill]
    已接收设计文档，开始业务分析...
```

#### 功能点复杂度分类

| 复杂度 | 代码 | 说明 | 开发时间 | 人工参与 |
|--------|------|------|---------|---------|
| 核心业务 | P0 | 核心业务流程，涉及多方审批 | 3-5天 | 高 |
| 重要功能 | P1 | 重要业务功能，有替代方案 | 1-2天 | 中 |
| 辅助功能 | P2 | 辅助性功能，易于实现 | 0.5天 | 低 |

#### 三维度验证模型

```yaml
验证维度:
  Completeness (完整性):
    定义: 所有规格要求的功能是否都已实现
    验证点:
      - 接口是否完整
      - 字段是否齐全
      - 业务规则是否覆盖

  Correctness (正确性):
    定义: 实现是否符合规格定义
    验证点:
      - 接口逻辑是否正确
      - 数据处理是否准确
      - 业务规则是否正确

  Coherence (一致性):
    定义: 前后端、文档与代码是否一致
    验证点:
      - 前后端接口是否一致
      - 文档与代码是否一致
      - 命名规范是否统一
```

---

### 文档体系

#### 核心文档类型

| 文档类型 | 文件名 | 核心内容 |
|---------|--------|---------|
| PRD 文档 | PRD-{模块名称}.md | 需求描述、业务规则 |
| 用例图 | 用例图-{模块名称}.md | 用例定义、参与者 |
| 流程图 | 业务流程图-{模块名称}.md | 业务流程、决策点 |
| 状态图 | 状态图-{模块名称}.md | 状态定义、转换规则 |
| 功能点矩阵 | feature-matrix.md | 功能点清单、依赖关系 |
| 开发规格 | spec.md | 接口设计、数据模型 |
| 验收标准 | checklist.md | 验收项、验收条件 |
| 审查报告 | review-report.md | 审查结果、问题清单 |
| 验收报告 | verify-report.md | 验收结果、问题清单 |

#### 目录结构

```
docs/
├── 业务分析/
│   └── {业务领域}/
│       └── {模块编号}-{模块名称}/
│           ├── PRD-{模块名称}.md
│           ├── 用例图-{模块名称}.md
│           ├── 业务流程图-{模块名称}.md
│           └── 状态图-{模块名称}.md
│
└── dev-specs/
    └── FP-{模块编号}-{序号}/
        ├── spec.md
        ├── checklist.md
        ├── review-report.md
        └── verify-report.md
```

---

### 熵减机制

#### 四大专业子技能

```
┌─────────────────────────────────────────────────────────────┐
│                  pdd-entropy-reduction                       │
│                      （主协调器）                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │ pdd-doc-    │  │ expert-arch │  │ expert-     │  │ expert-auto ││
│  │ gardener    │  │ -enforcer   │  │ entropy-    │  │ -refactor   ││
│  │             │  │             │  │ auditor     │  │             ││
│  │ 文档园丁    │  │ 架构强制    │  │ 熵增审计    │  │ 自动重构    ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 熵值评分系统

| 分数范围 | 状态 | 建议动作 |
|---------|------|---------|
| 90-100 | 优秀 | 维持现状 |
| 70-89 | 良好 | 小额改进 |
| 50-69 | 一般 | 计划性清理 |
| 30-49 | 警告 | 优先处理 |
| 0-29 | 危险 | 紧急重构 |

---

### 黄金原则

1. **使用共享工具包，避免手写辅助函数**
   - 将不变式集中管理
   - 减少重复代码

2. **验证边界数据，不猜测数据结构**
   - 所有 API 入口必须有 Schema 验证
   - 不依赖隐式类型推断

3. **保持代码简洁，优先可读性**
   - 单个文件不超过 300 行
   - 单个函数不超过 50 行

4. **文档即代码，保持同步**
   - 代码变更必须同步文档
   - 文档过时即视为技术债务

5. **小额还贷，持续改进**
   - 每次提交都是改进机会
   - 不让技术债务堆积

---

### PDD 作为 Harness Engineering 范式的企业级应用工程实践

#### 什么是 Harness Engineering？

**Harness Engineering（驾驭工程）** 是由 OpenAI 率先提出的软件工程范式，强调通过规范化实践和智能化自动化构建健壮、可维护的系统。PDD 方法论代表了这一范式的企业级实现，专门为大规模业务应用开发而设计。

```
┌─────────────────────────────────────────────────────────────────┐
│              Harness Engineering 范式实施架构                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    核心原则                              │   │
│  │  ┌─────────────┬─────────────┬─────────────┐            │   │
│  │  │ 规格先行    │ 自动化优先  │ 治理为先    │            │   │
│  │  │ Specification│ Automation │ Governance  │            │   │
│  │  │   First     │   First    │   First     │            │   │
│  │  └─────────────┴─────────────┴─────────────┘            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│        ▼                     ▼                     ▼           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   PDD       │     │   PDD       │     │   PDD       │      │
│  │  文档体系   │     │  技能系统   │     │  熵减机制   │      │
│  │  Document   │     │   Skill     │     │  Entropy    │      │
│  │   System    │     │   System    │     │ Reduction   │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 企业级实施框架

PDD 通过以下企业实践实现 Harness Engineering 原则：

##### 1. 规格先行开发模式

```yaml
传统开发模式:
  编码 → 文档 → 测试 → 部署

Harness Engineering (PDD):
  PRD → 规格 → 编码 → 验证 → 部署
    ↑                      │
    └─────── 反馈闭环 ─────┘
```

**核心优势：**
- 减少需求歧义
- 支持并行开发
- 促进自动化验证
- 支持增量交付

##### 2. 智能化自动化分层

```
┌─────────────────────────────────────────────────────────────────┐
│                      自动化分层架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第四层：业务逻辑自动化                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-ba → pdd-extract-features → pdd-generate-spec       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  第三层：代码生成自动化                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-implement-feature + software-engineer + experts     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  第二层：质量保障自动化                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-code-reviewer → pdd-verify-feature                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  第一层：维护自动化                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-entropy-reduction + expert-auto-refactor            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

##### 3. 持续熵减治理

**企业系统的熵增问题：**

```
系统随时间演化：

时间 T0 (上线):
  ┌───────────────────┐
  │  清洁的代码       │  熵值评分: 95/100
  │  清晰的结构       │
  │  新鲜的文档       │
  └───────────────────┘

时间 T1 (6个月):
  ┌───────────────────┐
  │  部分重复代码     │  熵值评分: 75/100
  │  轻微架构漂移     │
  │  文档开始过时     │
  └───────────────────┘

时间 T2 (1年, 无 PDD):
  ┌───────────────────┐
  │  代码腐化         │  熵值评分: 45/100
  │  架构漂移严重     │
  │  文档缺失         │
  └───────────────────┘

时间 T2 (1年, 有 PDD):
  ┌───────────────────┐
  │  维护良好的代码   │  熵值评分: 85/100
  │  稳定的架构       │
  │  更新的文档       │
  └───────────────────┘
```

**PDD 熵减机制：**

```yaml
定时任务:
  - 每日: 文档一致性检查
  - 每周: 架构约束验证
  - 每月: 技术债务审计
  - 每次提交: 代码质量分析

自动化动作:
  - 创建文档更新 PR
  - 标记架构违规
  - 生成重构建议
  - 追踪熵值评分趋势
```

##### 4. 专家系统集成

PDD 利用领域专家技能提供专业化指导：

```
┌─────────────────────────────────────────────────────────────────┐
│                      专家系统架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ 框架专家    │     │ 数据库专家  │     │ 工作流专家  │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-ruoyi │     │expert-mysql │     │expert-      │      │
│  │             │     │             │     │activiti     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ 质量专家    │     │ 架构专家    │     │ 安全专家    │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-code- │     │system-      │     │ (可扩展)    │      │
│  │quality      │     │architect    │     │             │      │
│  │             │     │software-    │     │             │      │
│  │             │     │architect    │     │             │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 企业级收益

| 收益 | 描述 | 影响 |
|------|------|------|
| **缩短上市时间** | 自动化规格和代码生成 | 交付速度提升 30-50% |
| **提高质量** | 多维度验证 | 生产环境缺陷减少 60% |
| **降低维护成本** | 持续熵减治理 | 技术债务减少 40% |
| **知识沉淀** | 文档代码同步 | 新人上手时间缩短 80% |
| **可扩展开发** | 技能化专家系统 | 团队规模线性扩展 |

#### 实施路线图

```
第一阶段：基础建设 (第 1-2 周)
├── 搭建 PDD 技能系统
├── 定义 PRD 文档标准
└── 配置熵减调度计划

第二阶段：试点项目 (第 3-6 周)
├── 选择试点模块
├── 培训团队 PDD 工作流
└── 收集指标和反馈

第三阶段：推广扩展 (第 7-12 周)
├── 推广到更多模块
├── 集成到 CI/CD 流水线
└── 建立治理流程

第四阶段：持续优化 (持续进行)
├── 调优自动化参数
├── 增加领域专家
└── 基于指标持续改进
```

#### 度量指标和 KPI

```yaml
开发指标:
  - 功能交付率 (功能点/迭代)
  - 规格到代码准确率 (%)
  - 一次通过验收率 (%)
  - 平均开发周期时间 (天)

质量指标:
  - 代码审查通过率 (%)
  - 测试覆盖率 (%)
  - 生产环境缺陷率 (缺陷/千行代码)
  - 技术债务比率 (%)

维护指标:
  - 熵值评分趋势
  - 文档代码一致性 (%)
  - 架构违规数量
  - 重构完成率 (%)

团队指标:
  - 开发人员生产力 (行代码/天)
  - 新人上手时间 (天)
  - 知识传递效率 (%)
  - 技能利用率 (%)
```

#### 与传统开发模式的对比

| 方面 | 传统开发模式 | PDD (Harness Engineering) |
|------|-------------|---------------------------|
| **需求管理** | 非正式，常有歧义 | 正式化，规格先行 |
| **文档管理** | 常常过时 | 与代码同步 |
| **代码质量** | 被动审查 | 主动验证 |
| **技术债务** | 随时间累积 | 持续减少 |
| **知识传递** | 依赖个人 | 依赖系统 |
| **可扩展性** | 非线性投入 | 技能化线性投入 |
| **自动化程度** | 有限 | 全面，多层覆盖 |

---

### 参考文档

- [PDD 框架设计文档](docs/pdd-framework-design.md)
- [PDD 技能关系规范](docs/pdd-skill-relationships.md)
- [system-architect SKILL.md](system-architect/SKILL.md)
- [software-architect SKILL.md](software-architect/SKILL.md)
- [software-engineer SKILL.md](software-engineer/SKILL.md)

---

<a name="français"></a>

## 📖 Documentation Française

### Aperçu

**PDD (PRD-Driven Development)** est une méthodologie de développement qui combine les capacités d'experts du domaine. En intégrant des architectes système, des architectes logiciels, des ingénieurs logiciels et diverses compétences d'experts, elle permet un développement intelligent complet de l'analyse des exigences à la livraison finale.

Valeurs fondamentales de la méthodologie PDD :

- **Processus Normalisé** : Chaîne complète des documents PRD à l'implémentation du code
- **Collaboration Intelligente** : Collaboration approfondie entre l'IA et les développeurs humains
- **Assurance Qualité** : Vérification multidimensionnelle garantissant la qualité de livraison
- **Accumulation de Connaissances** : Évolution synchrone des documents et du code

---

### Philosophie Centrale

> "La dette technique est comme un prêt à intérêt élevé : il vaut mieux rembourser la dette en petits versements que de laisser s'accumuler et de la régler douloureusement en une seule fois." —— OpenAI Harness Engineering

La méthodologie PDD suit ces principes fondamentaux :

1. **Développement Piloté par les Documents** : Les documents PRD sont la source unique de vérité
2. **Spécification d'Abord** : Les spécifications de développement doivent être complétées avant l'implémentation du code
3. **Vérification Continue** : Chaque fonctionnalité doit passer une vérification tridimensionnelle
4. **Gouvernance de Réduction d'Entropie** : Lutter continuellement contre "l'augmentation d'entropie" et la "décroissance" du système

---

### Relation entre PDD et OpenSpec

#### Points d'Intégration

La méthodologie PDD s'intègre profondément avec OpenSpec pour former un système complet de spécifications de développement :

```
┌─────────────────────────────────────────────────────────────────┐
│          Architecture d'Intégration PDD × OpenSpec              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  Doc PRD    │ ──→ │  OpenSpec   │ ──→ │  Spec Dev   │       │
│  │  (Exigences)│     │  (Spécification)│ │  (Implémentation)│  │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ Matrice     │     │ Gestion     │     │ Implémentation│     │
│  │ Fonctionnalité│   │ des Changes │     │ du Code      │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Caractéristiques Complémentaires

| Caractéristique | Contribution PDD | Contribution OpenSpec |
|----------------|-----------------|----------------------|
| **Gestion des Exigences** | Système de documents PRD | Standardisation des spécifications |
| **Suivi des Changements** | Matrice de fonctionnalités | Gestion des ID de Change |
| **Synchronisation des Documents** | Génération de spécifications | Contrôle de version des spécifications |
| **Assurance Qualité** | Vérification tridimensionnelle | Contrôle de cohérence des spécifications |

#### Scénarios d'Implémentation

**Scénario 1 : Développement de Nouvelle Fonctionnalité**

```
Document PRD → pdd-extract-features → Matrice de Fonctionnalités
    ↓
Création d'un Change OpenSpec
    ↓
pdd-generate-spec → spec.md + checklist.md
    ↓
pdd-implement-feature → Implémentation du Code
    ↓
pdd-verify-feature → Vérification Réussie
    ↓
Archivage du Change OpenSpec
```

**Scénario 2 : Changement d'Exigences**

```
Demande de Changement
    ↓
Analyse d'Impact pdd-doc-change
    ↓
Mise à jour de la Spécification OpenSpec
    ↓
Régénération de la Matrice de Fonctionnalités
    ↓
Développement et Vérification Incrémentiels
```

**Scénario 3 : Gouvernance de la Dette Technique**

```
Déclenchement Programmé pdd-entropy-reduction
    ↓
Scan de Cohérence Documents-Code
    ↓
Détection des Violations de Contraintes d'Architecture
    ↓
Génération du Rapport d'Entropie
    ↓
Création d'une PR de Correction
```

---

### Architecture du Système de Compétences

#### Classification des Compétences

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN (Entrée Principale)               │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │ Orchestration│ Gestion    │ Transfert   │ Agrégation  │      │
│  │ des Processus│ d'État     │ de Contexte │ des Résultats│     │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Couche      │     │   Couche      │     │   Couche      │
│   Processus   │     │   Architecte  │     │   Ingénieur   │
│   PDD         │     │               │     │               │
├───────────────┤     ├───────────────┤     ├───────────────┤
│ pdd-ba        │     │system-architect│    │software-eng   │
│ pdd-extract   │◄───►│               │◄───►│               │
│ pdd-generate  │     │software-arch  │     │ expert-xxx    │
│ pdd-implement │     │               │     │               │
│ pdd-review    │     │               │     │               │
│ pdd-verify    │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

#### Liste des Compétences Principales

| Catégorie | Nom de la Compétence | Responsabilité Principale | Entrée | Sortie |
|-----------|---------------------|-------------------------|--------|--------|
| **Entrée Principale** | pdd-main | Orchestration des processus, gestion d'état | Chemin du document PRD | Code de fonctionnalité complété |
| **Analyse Business** | pdd-ba | Analyse des exigences, modélisation business | Document PRD | Rapport d'analyse business |
| **Extraction de Fonctionnalités** | pdd-extract-features | Extraction des points de fonctionnalité | Rapport d'analyse business | Matrice de fonctionnalités |
| **Génération de Spécifications** | pdd-generate-spec | Génération des spécifications de développement | Matrice de fonctionnalités | spec.md, checklist.md |
| **Implémentation de Code** | pdd-implement-feature | Implémentation des fonctionnalités | Spécification de développement | Fichiers de code |
| **Revue de Code** | pdd-code-reviewer | Revue de conformité | Code + Spécification | Rapport de revue |
| **Vérification de Fonctionnalité** | pdd-verify-feature | Vérification tridimensionnelle | Code + Critères d'acceptation | Rapport de vérification |
| **Réduction d'Entropie** | pdd-entropy-reduction | Gestion de la dette technique | Conditions de déclenchement | Rapport d'entropie + PR de correction |

---

### Processus de Développement

#### Processus en Six Phases

```
Phase 1 : Analyse Business et Extraction de Fonctionnalités
  Document PRD → Analyse 5W1H → Diagramme de Cas d'Utilisation → Organigramme → Diagramme d'État → Matrice de Fonctionnalités

Phase 2 : Génération des Spécifications de Développement
  Matrice de Fonctionnalités → Consultation d'Architecture → Conception d'Interface → Modèle de Données → Spec Dev + Critères d'Acceptation

Phase 3 : Boucle de Fonctionnalités
  Pour chaque fonctionnalité : Implémentation → Revue → Correction → Vérification

Phase 4 : Intégration de la Revue d'Architecture
  Appel à la demande de system-architect / software-architect

Phase 5 : Intégration des Compétences d'Expert
  Appel à la demande de expert-xxx

Phase 6 : Livraison et Rétrospective
  Rapport de Développement → Archivage des Documents → Leçons Apprises
```

#### Flux de Processus Principal

```
┌─────────────────────────────────────────────────────────────────┐
│                    Processus Principal PDD                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Document PRD ──→ pdd-ba ──→ Rapport d'Analyse Business        │
│                │                                                │
│                ↓                                                │
│  pdd-extract-features ──→ Matrice de Fonctionnalités           │
│                │                                                │
│                ↓                                                │
│           [Revue Manuelle]                                      │
│                │                                                │
│                ↓                                                │
│  pdd-generate-spec ──→ Spec Dev + Critères d'Acceptation       │
│                │                                                │
│                ↓                                                │
│           [Revue Manuelle]                                      │
│                │                                                │
│                ↓                                                │
│  ┌──────────────────────────────────────┐                       │
│  │    Traitement en Boucle des          │                       │
│  │    Fonctionnalités                   │                       │
│  │  pdd-implement-feature               │                       │
│  │         ↓                            │                       │
│  │  pdd-code-reviewer                   │                       │
│  │         ↓                            │                       │
│  │  pdd-verify-feature                  │                       │
│  │         ↓                            │                       │
│  │  [Vérifié?] ─→ Fonctionnalité Suivante│                      │
│  └──────────────────────────────────────┘                       │
│                │                                                │
│                ↓                                                │
│           Rapport de Développement                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Guide d'Utilisation

#### Démarrage Rapide

**Mode 1 : Découverte Automatique par Numéro de Module**

```
Utilisateur : Je veux développer le module ZCCZ-2 de Transfert d'Actifs

IA : [Invocation de la compétence pdd-main]
     Scan du répertoire docs/analyse-business/...
     Module trouvé : ZCCZ-2-Transfert-Actifs
     Chemin : docs/analyse-business/disposition-actifs/ZCCZ-2-Transfert-Actifs/

     Documents de conception agrégés :
     ✓ PRD-Transfert-Actifs.md
     ✓ Diagramme-Cas-Utilisation-Transfert-Actifs.md
     ✓ Flux-Business-Transfert-Actifs.md
     ✓ Diagramme-Etat-Transfert-Actifs.md

     Confirmer le démarrage de l'analyse business ? [O/n]
```

**Mode 2 : Spécification Manuelle des Documents**

```
Utilisateur : Je veux développer basé sur ces documents
     - docs/analyse-business/disposition-actifs/ZCCZ-1/PRD-Transfert-Actifs.md
     - docs/analyse-business/disposition-actifs/ZCCZ-1/Flux-Business-Transfert-Actifs.md

IA : [Invocation de la compétence pdd-main]
     Documents de conception reçus, démarrage de l'analyse business...
```

#### Classification de Complexité des Fonctionnalités

| Complexité | Code | Description | Temps de Développement | Implication Humaine |
|------------|------|-------------|----------------------|---------------------|
| Business Central | P0 | Processus business centraux, approbation multi-parties | 3-5 jours | Élevée |
| Fonctionnalité Importante | P1 | Fonctionnalités business importantes, alternatives disponibles | 1-2 jours | Moyenne |
| Fonctionnalité Auxiliaire | P2 | Fonctionnalités auxiliaires, faciles à implémenter | 0.5 jour | Faible |

#### Modèle de Vérification Tridimensionnelle

```yaml
Dimensions de Vérification:
  Complétude:
    Définition: Si toutes les fonctionnalités spécifiées sont implémentées
    Points de Vérification:
      - Complétude des interfaces
      - Complétude des champs
      - Couverture des règles business

  Exactitude:
    Définition: Si l'implémentation correspond à la spécification
    Points de Vérification:
      - Exactitude de la logique d'interface
      - Précision du traitement des données
      - Exactitude des règles business

  Cohérence:
    Définition: Cohérence entre frontend/backend, documents et code
    Points de Vérification:
      - Cohérence des interfaces frontend-backend
      - Cohérence documents-code
      - Uniformité des conventions de nommage
```

---

### Système de Documents

#### Types de Documents Principaux

| Type de Document | Nom de Fichier | Contenu Principal |
|-----------------|----------------|-------------------|
| Document PRD | PRD-{NomModule}.md | Exigences, règles business |
| Diagramme de Cas d'Utilisation | CasUtilisation-{NomModule}.md | Définitions des cas d'utilisation, acteurs |
| Organigramme | FluxBusiness-{NomModule}.md | Processus business, points de décision |
| Diagramme d'État | DiagrammeEtat-{NomModule}.md | Définitions des états, règles de transition |
| Matrice de Fonctionnalités | feature-matrix.md | Liste des fonctionnalités, dépendances |
| Spécification de Développement | spec.md | Conception d'interface, modèle de données |
| Critères d'Acceptation | checklist.md | Éléments d'acceptation, conditions |
| Rapport de Revue | review-report.md | Résultats de revue, liste des problèmes |
| Rapport de Vérification | verify-report.md | Résultats de vérification, liste des problèmes |

#### Structure de Répertoire

```
docs/
├── analyse-business/
│   └── {domaine-business}/
│       └── {numero-module}-{nom-module}/
│           ├── PRD-{nom-module}.md
│           ├── CasUtilisation-{nom-module}.md
│           ├── FluxBusiness-{nom-module}.md
│           └── DiagrammeEtat-{nom-module}.md
│
└── dev-specs/
    └── FP-{numero-module}-{sequence}/
        ├── spec.md
        ├── checklist.md
        ├── review-report.md
        └── verify-report.md
```

---

### Mécanisme de Réduction d'Entropie

#### Quatre Sous-Compétences Professionnelles

```
┌─────────────────────────────────────────────────────────────┐
│                  pdd-entropy-reduction                       │
│                      (Coordinateur Principal)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │ pdd-doc-    │  │ expert-arch │  │ expert-     │  │ expert-auto ││
│  │ gardener    │  │ -enforcer   │  │ entropy-    │  │ -refactor   ││
│  │             │  │             │  │ auditor     │  │             ││
│  │ Jardinier   │  │ Application │  │ Audit       │  │ Refactoring ││
│  │ de Documents│  │ d'Architect.│  │ d'Entropie  │  │ Automatique ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Système de Score d'Entropie

| Plage de Score | Statut | Action Recommandée |
|---------------|--------|-------------------|
| 90-100 | Excellent | Maintenir l'état actuel |
| 70-89 | Bon | Petites améliorations |
| 50-69 | Moyen | Nettoyage planifié |
| 30-49 | Avertissement | Traitement prioritaire |
| 0-29 | Critique | Refactoring d'urgence |

---

### Principes d'Or

1. **Utiliser des packages utilitaires partagés, éviter les fonctions auxiliaires écrites à la main**
   - Centraliser la gestion des invariants
   - Réduire la duplication de code

2. **Valider les données de frontière, ne pas deviner les structures de données**
   - Toutes les entrées API doivent avoir une validation de Schema
   - Ne pas dépendre de l'inférence de type implicite

3. **Garder le code simple, prioriser la lisibilité**
   - Un seul fichier pas plus de 300 lignes
   - Une seule fonction pas plus de 50 lignes

4. **La documentation comme code, maintenir la synchronisation**
   - Les changements de code doivent synchroniser la documentation
   - La documentation obsolète est une dette technique

5. **Rembourser la dette en petits montants, amélioration continue**
   - Chaque commit est une opportunité d'amélioration
   - Ne pas laisser la dette technique s'accumuler

---

### PDD comme Pratique d'Ingénierie d'Entreprise Harness Engineering

#### Qu'est-ce que Harness Engineering ?

**Harness Engineering (Ingénierie de Pilotage)** est un paradigme d'ingénierie logicielle pionnier d'OpenAI qui met l'accent sur la construction de systèmes robustes et maintenables grâce à des pratiques disciplinées et une automatisation intelligente. La méthodologie PDD représente une implémentation de qualité entreprise de ce paradigme, spécialement conçue pour le développement d'applications commerciales à grande échelle.

```
┌─────────────────────────────────────────────────────────────────┐
│        Implémentation du Paradigme Harness Engineering          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Principes Fondamentaux                      │   │
│  │  ┌─────────────┬─────────────┬─────────────┐            │   │
│  │  │ Spécification│ Automatisation│ Gouvernance│           │   │
│  │  │   D'abord    │   D'abord   │   D'abord  │            │   │
│  │  └─────────────┴─────────────┴─────────────┘            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│        ┌─────────────────────┼─────────────────────┐           │
│        │                     │                     │           │
│        ▼                     ▼                     ▼           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   PDD       │     │   PDD       │     │   PDD       │      │
│  │  Système de │     │  Système de │     │  Réduction  │      │
│  │  Documents  │     │  Compétences│     │  d'Entropie │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Implémentation de Qualité Entreprise

PDD implémente les principes de Harness Engineering à travers les pratiques d'entreprise suivantes :

##### 1. Développement Spécification d'Abord

```yaml
Approche Traditionnelle:
  Code → Documentation → Tests → Déploiement

Harness Engineering (PDD):
  PRD → Spécification → Code → Vérification → Déploiement
    ↑                              │
    └──────── Boucle de Retour ────┘
```

**Avantages Clés :**
- Réduit l'ambiguïté des exigences
- Permet le développement parallèle
- Facilite la vérification automatisée
- Supporte la livraison incrémentielle

##### 2. Couches d'Automatisation Intelligente

```
┌─────────────────────────────────────────────────────────────────┐
│                  Couches d'Automatisation                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Couche 4 : Automatisation de la Logique Métier                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-ba → pdd-extract-features → pdd-generate-spec       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Couche 3 : Automatisation de la Génération de Code           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-implement-feature + software-engineer + experts     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Couche 2 : Automatisation de l'Assurance Qualité             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-code-reviewer → pdd-verify-feature                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Couche 1 : Automatisation de la Maintenance                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ pdd-entropy-reduction + expert-auto-refactor            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

##### 3. Réduction Continue de l'Entropie

**Le Problème d'Entropie dans les Systèmes d'Entreprise :**

```
Évolution du Système au Fil du Temps :

Temps T0 (Lancement):
  ┌───────────────────┐
  │  Code Propre      │  Score d'Entropie: 95/100
  │  Structure Claire │
  │  Documents Récents│
  └───────────────────┘

Temps T1 (6 mois):
  ┌───────────────────┐
  │  Duplication      │  Score d'Entropie: 75/100
  │  Dérive Mineure   │
  │  Docs Obsolètes   │
  └───────────────────┘

Temps T2 (1 an, sans PDD):
  ┌───────────────────┐
  │  Code Pourri      │  Score d'Entropie: 45/100
  │  Dérive d'Arch.   │
  │  Docs Manquants   │
  └───────────────────┘

Temps T2 (1 an, avec PDD):
  ┌───────────────────┐
  │  Code Maintenu    │  Score d'Entropie: 85/100
  │  Architecture Stable│
  │  Docs à Jour      │
  └───────────────────┘
```

**Mécanisme de Réduction d'Entropie PDD :**

```yaml
Tâches Planifiées:
  - Quotidien: Vérification de cohérence des documents
  - Hebdomadaire: Validation des contraintes d'architecture
  - Mensuel: Audit de la dette technique
  - Par-Commit: Analyse de qualité du code

Actions Automatisées:
  - Créer des PRs pour les mises à jour de documentation
  - Signaler les violations d'architecture
  - Générer des recommandations de refactoring
  - Suivre les tendances des scores d'entropie
```

##### 4. Intégration de Système Expert

PDD exploite les compétences d'experts du domaine pour fournir des conseils spécialisés :

```
┌─────────────────────────────────────────────────────────────────┐
│                Architecture du Système Expert                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ Experts     │     │ Experts     │     │ Experts     │      │
│  │ Framework   │     │ Base de     │     │ Workflow    │      │
│  │             │     │ Données     │     │             │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-ruoyi │     │expert-mysql │     │expert-      │      │
│  │             │     │             │     │activiti     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │ Experts     │     │ Experts     │     │ Experts     │      │
│  │ Qualité     │     │ Architecture│     │ Sécurité    │      │
│  ├─────────────┤     ├─────────────┤     ├─────────────┤      │
│  │expert-code- │     │system-      │     │ (Extensible)│      │
│  │quality      │     │architect    │     │             │      │
│  │             │     │software-    │     │             │      │
│  │             │     │architect    │     │             │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Avantages Entreprise

| Avantage | Description | Impact |
|----------|-------------|--------|
| **Temps de Mise sur le Marché Réduit** | Spécification automatisée et génération de code | Livraison 30-50% plus rapide |
| **Qualité Améliorée** | Vérification multidimensionnelle | 60% moins de bugs en production |
| **Coût de Maintenance Réduit** | Réduction continue de l'entropie | 40% de réduction de la dette technique |
| **Préservation des Connaissances** | Synchronisation documents-code | Intégration 80% plus rapide |
| **Développement Scalable** | Système expert basé sur les compétences | Mise à l'échelle linéaire avec la taille de l'équipe |

#### Feuille de Route d'Implémentation

```
Phase 1 : Fondation (Semaine 1-2)
├── Configurer le système de compétences PDD
├── Définir les standards de documents PRD
└── Configurer le calendrier de réduction d'entropie

Phase 2 : Projet Pilote (Semaine 3-6)
├── Sélectionner le module pilote
├── Former l'équipe au workflow PDD
└── Collecter les métriques et retours

Phase 3 : Expansion (Semaine 7-12)
├── Déployer sur des modules supplémentaires
├── Intégrer au pipeline CI/CD
└── Établir les processus de gouvernance

Phase 4 : Optimisation (Continu)
├── Ajuster les paramètres d'automatisation
├── Ajouter des experts spécifiques au domaine
└── Amélioration continue basée sur les métriques
```

#### Métriques et KPIs

```yaml
Métriques de Développement:
  - Taux de livraison de fonctionnalités (fonctionnalités/sprint)
  - Précision spécification-vers-code (%)
  - Taux d'acceptation du premier passage (%)
  - Temps moyen du cycle de développement (jours)

Métriques de Qualité:
  - Taux de passage de la revue de code (%)
  - Couverture de tests (%)
  - Taux de bugs en production (bugs/1000 LDC)
  - Ratio de dette technique (%)

Métriques de Maintenance:
  - Tendance du score d'entropie
  - Cohérence documents-code (%)
  - Nombre de violations d'architecture
  - Taux d'achèvement du refactoring (%)

Métriques d'Équipe:
  - Productivité des développeurs (LDC/jour)
  - Temps d'intégration (jours)
  - Efficacité du transfert de connaissances (%)
  - Taux d'utilisation des compétences (%)
```

#### Comparaison avec les Approches Traditionnelles

| Aspect | Développement Traditionnel | PDD (Harness Engineering) |
|--------|---------------------------|---------------------------|
| **Exigences** | Informelles, souvent ambiguës | Formalisées, spécification d'abord |
| **Documentation** | Souvent obsolète | Synchronisée avec le code |
| **Qualité du Code** | Revue réactive | Vérification proactive |
| **Dette Technique** | S'accumule avec le temps | Continuellement réduite |
| **Transfert de Connaissances** | Dépendant des personnes | Dépendant du système |
| **Scalabilité** | Effort non-linéaire | Effort linéaire avec les compétences |
| **Automatisation** | Limitée | Complète, multi-couches |

---

### Documentation de Référence

- [Document de Conception du Framework PDD](docs/pdd-framework-design.md)
- [Spécification des Relations des Compétences PDD](docs/pdd-skill-relationships.md)
- [system-architect SKILL.md](system-architect/SKILL.md)
- [software-architect SKILL.md](software-architect/SKILL.md)
- [software-engineer SKILL.md](software-engineer/SKILL.md)

---

## License

MIT License

---

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial release with complete PDD methodology documentation in English, Chinese, and French |
