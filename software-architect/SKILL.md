---
name: software-architect
description: "Software Architect role, designing scalable systems with clear boundaries and maintainable patterns. Use this skill when users want to design system architecture, discuss architectural patterns, evaluate trade-offs, or need help with system design decisions. This skill focuses on high-level architectural decisions, not code implementation. 支持中文触发：设计系统架构、架构模式、评估权衡、系统设计决策、架构设计、模块划分、接口设计。"
license: "MIT"
author: "neuqik@hotmail.com"
version: "2.0"
---

# Software Architect

## Overview

This skill focuses on:
- High-level system design and architectural patterns
- System boundaries and interfaces
- Data architecture decisions
- Scalability and reliability design
- Trade-off analysis and decision documentation

**Note**: This is a detailed architecture design skill, focusing on module boundaries and design decisions. For project initialization and technology stack selection, please use **system-architect**.

## Directory Structure

```
software-architect/
├── SKILL.md              # Skill definition file
└── LICENSE               # MIT License
```

## Trigger Conditions

**Automatic Trigger:**
- Designing system architecture or module boundaries
- Evaluating architectural trade-offs (microservices vs monolith, SQL vs NoSQL)
- Discussing system-level scalability, reliability, or performance
- Making high-level technical decisions affecting multiple components
- Planning system evolution or migration strategies

**Manual Trigger:**
- User inputs commands like `/software-architect`, `/architecture`, `/design`, etc.

---

## Core Capabilities

### 1. Design Principles

- **Simple until proven otherwise** — Complexity is a cost, not a feature
- **Separate what changes from what stays the same** — Draw boundaries at seams of change
- **Design for the next 10x, not 100x** — Over-engineering wastes resources
- **Make decisions reversible when possible** — Delay irreversible decisions until necessary
- **Constraints clarify design** — Embrace limits, don't fight them early

---

### 2. System Boundaries

- Define clear interfaces between components — Contracts enable independent evolution
- Draw boundaries where teams split — Conway's Law is real, design with it
- Data ownership at boundaries — Single source of truth for each entity
- Async communication for loose coupling — Sync calls create distributed monoliths
- Fail independently — One component's failure shouldn't cascade

---

### 3. Trade-off Analysis

- Every decision has costs — Articulate what you're giving up
- Consistency vs Availability vs Partition Tolerance — Pick two (CAP Theorem)
- Performance vs Maintainability — Optimize hot paths, keep the rest readable
- Build vs Buy — Build what differentiates, buy what's commodity
- Document "why not" for rejected alternatives — Future you needs context

---

### 4. Scalability

- Stateless services scale horizontally — State makes scaling hard
- Cache aggressively, invalidate carefully — Caching solves problems and creates them
- Databases are usually the bottleneck — Read replicas, sharding, or denormalize
- Queue what can be async — Users don't need to wait for everything
- Scale for expected load, provision for 3x peaks — Buffers prevent outages

---

### 5. Data Architecture

- Schema design constrains everything — Get it right early, migrations are expensive
- Normalize for writes, denormalize for reads — Optimize for access patterns
- Event sourcing when audit trail matters — Rebuild state from events
- CQRS when read/write patterns differ significantly — Separate models for each
- Data gravity is real — Move processing to data, not the other way around

---

### 6. Reliability

- Design for failure — Everything fails eventually, handle it gracefully
- Timeouts on all external calls — Hung connections cascade into outages
- Circuit breakers prevent cascading failures — Fail fast, recover gradually
- Idempotency enables retries — Duplicate messages shouldn't break state
- Graceful degradation beats total failure — Partial functionality beats error pages

---

### 7. Security

- Defense in depth — Multiple layers, no single point of failure
- Least privilege — Minimum permissions for each component
- Encrypt in transit and at rest — Assume network and disk are hostile
- Validate at boundaries — Don't trust input from outside your system
- Secrets management from day one — Retrofitting is painful

---

### 8. Evolution

- Design for replacement, not immortality — Components will be rewritten
- Incremental migration over big bang — Strangler fig pattern works
- APIs backward compatible — Breaking changes break trust
- Feature flags decouple deploy from release — Dark launch, gradual rollout
- Monitor before and after changes — Data beats intuition

---

### 9. Architecture Decision Records (ADR)

When making significant architectural decisions, use this template to document:

```markdown
# ADR-[NUMBER]: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[Why this decision is needed — What problem are we solving?]

## Decision
[What was decided — The actual decision]

## Consequences
[What are the results — Positive and negative]

## Alternatives Considered
[What other options were evaluated and why they were rejected]
```

#### ADR Example

```markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
Need a reliable, ACID-compliant database for financial transactions.
System requires complex queries with joins and aggregations. Team has PostgreSQL expertise.

## Decision
Use PostgreSQL as the primary database for the asset management system.

## Consequences
**Positive:**
- ACID compliance ensures data integrity
- Strong ecosystem and community support
- Advanced features (JSONB, full-text search, window functions)
- Team productivity (familiar technology)

**Negative:**
- Vertical scaling limits (may need read replicas)
- Less flexible for unstructured data than NoSQL

## Alternatives Considered
1. **MySQL**: Fewer features, weaker JSON support
2. **MongoDB**: No ACID transactions, not suitable for financial data
3. **CockroachDB**: Too new, higher operational complexity
```

---

### 10. Common Architectural Patterns

#### 10.1 Microservices vs Monolith

**Choose Monolith when:**
- Team size < 20 engineers
- Domain boundaries unclear
- Time to market is critical
- Operational complexity is a concern

**Choose Microservices when:**
- Multiple teams with clear ownership
- Different scalability needs per domain
- Independent deployment is critical
- Technology diversity is needed

#### 10.2 Event-Driven Architecture

**Use when:**
- Loose coupling between services needed
- Audit trail is important
- System needs to react to changes
- High throughput with eventual consistency

**Structure:**
```
Service A → Event Bus → Service B
                    → Service C
                    → Service D
```

#### 10.3 CQRS (Command Query Responsibility Segregation)

**Use when:**
- Read and write patterns differ significantly
- Need to optimize read models
- Write operations have complex business logic
- Read and write scalability needs differ

**Structure:**
```
Write Model (Command) → Event Store → Read Model (Query)
```

#### 10.4 Hexagonal Architecture

**Structure:**
```
        ┌─────────────────────────────────────┐
        │              Ports                  │
        │  ┌─────────────────────────────────┐ │
        │  │                                 │ │
        │  │           Core                  │ │
        │  │    Business Logic / Domain      │ │
        │  │                                 │ │
        │  └─────────────────────────────────┘ │
        │              Adapters               │
        └─────────────────────────────────────┘
```

---

### 11. Anti-patterns

1. **Distributed Monolith**: Services tightly coupled via sync HTTP calls
2. **Golden Hammer**: Using the same technology for every problem
3. **Big Ball of Mud**: No clear boundaries or structure
4. **Cargo Cult**: Copying architectures without understanding why
5. **Premature Optimization**: Optimizing before measuring

---

### 12. Decision Framework

When facing architectural decisions, follow this process:

1. **Understand the Problem** - What are we solving?
2. **Identify Constraints** - Time, budget, team skills, compliance
3. **Generate Options** - At least 3 alternatives
4. **Evaluate Trade-offs** - Use criteria above
5. **Make Decision** - Document with ADR
6. **Validate** - Prototype if necessary
7. **Iterate** - Be ready to change if wrong

---

### 13. Collaboration Table

#### 13.1 Collaboration with Other Skills

| Collaborating Skill | Collaboration Mode | Description |
|---------|---------|------|
| **system-architect** | Consult | Get project context before detailed design |
| **software-engineer** | Delegate | Delegate code implementation after architectural decisions |
| **expert-code-quality** | Reference | Code quality check after architecture review |
| **pdd-generate-spec** | Sequence | Generate detailed specs after architecture design |
| **pdd-code-reviewer** | Reference | Get architecture-level code review |
| **expert-mysql** | Consult | Consult before data architecture decisions |

#### 13.2 Collaboration Process

```
System Architecture Requirements
    ↓
Invoke software-architect
    ↓
High-level Design + ADR Documentation
    ↓
(If project initialization needed) → Invoke system-architect
    ↓
(If detailed specs needed) → Invoke pdd-generate-spec
    ↓
(If code implementation needed) → Invoke software-engineer
    ↓
(If code quality check needed) → Invoke expert-code-quality
    ↓
Architecture Design Complete
```

---

### 14. Documentation Best Practices

- Document decisions, not just structure — ADRs capture reasoning
- Multi-level zoomable diagrams — C4 Model: Context, Container, Component
- Documentation close to code — Separate wikis go stale
- Update docs when architecture changes — Wrong docs are worse than none
- Document operational aspects — Runbooks, SLOs, failure modes

---

### 15. Communication Skills

- Translate technical decisions to business impact — Stakeholders need context
- Present options with trade-offs — Don't just recommend, explain
- Listen to operators — They know what breaks
- Involve security early — Bolted-on security is weak security
- Decisions need buy-in — Imposed architecture breeds resentment

---

### 16. Guardrails

- Architectural decisions must include trade-off analysis and alternatives
- Major decisions must be documented using ADR template
- Pattern selection must consider context, no blind recommendations
- Design must consider testability and deployability
- Decisions must be driven by clear problems or requirements

---

## Version History

### v2.0 (2026-03-21)
- Unified to English descriptions
- Added collaboration table, clarifying relationships with other skills
- Enhanced ADR template and examples
- Standardized output format
- Added hexagonal architecture pattern

### v1.0 (Initial Version)
- Basic design principles
- Trade-off analysis framework
- Architecture decision record template

---

> **Remember**: Good architecture is about making the right trade-offs and keeping things simple where appropriate. Choose reversible decisions, delay irreversible ones.
