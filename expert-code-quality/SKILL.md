---
name: expert-code-quality
description: "Code quality expert integrating Martin Fowler's refactoring techniques and GoF design patterns to help developers systematically improve code quality. Triggers when users ask about code review, refactoring, design patterns, code smells, SOLID principles, or software architecture improvements. 支持中文触发：代码审查、重构、设计模式、代码异味、SOLID原则、软件架构改进、代码质量。"
license: "MIT"
author: "neuqik@hotmail.com"
version: "2.0"
---

# Code Quality Expert

## Overview

This skill integrates two foundational software engineering disciplines:
1. **Refactoring** - Improving code structure without changing behavior
2. **Design Patterns** - Proven solutions to common design problems

Combined, they form a powerful toolkit for writing clean, maintainable, and extensible code.

## Directory Structure

```
expert-code-quality/
├── SKILL.md              # Skill definition file
├── LICENSE               # MIT License
└── references/           # Reference documents
    ├── refactoring-catalog.md    # Complete catalog of refactoring techniques
    ├── design-patterns.md         # 23 GoF patterns
    ├── code-smells.md             # Detailed description of code smells
    └── solid-principles.md        # In-depth analysis of SOLID principles
```

## Trigger Conditions

**Automatic Triggers:**
- User asks about code quality issues
- Need to identify code smells
- Request for design pattern recommendations
- Performing code refactoring
- Evaluating SOLID principle compliance

**Manual Triggers:**
- User enters commands like `/code-quality`, `/refactor`, `/pattern`, etc.

---

## Core Capabilities

### 1. Code Smell Detection

#### 1.1 Quick Reference: 22 Code Smells

**Method-Level Smells:**

| Smell | Detection Pattern | Severity |
|-------|------------------|----------|
| **Long Method** | Method > 20 lines | High |
| **Duplicated Code** | Similar code blocks | Critical |
| **Long Parameter List** | Parameters > 4 | Medium |
| **Switch Statements** | Large switch/case blocks | Medium |

**Class-Level Smells:**

| Smell | Detection Pattern | Severity |
|-------|------------------|----------|
| **Large Class** | Class > 300 lines or > 10 fields | High |
| **Divergent Change** | One class changes for multiple reasons | High |
| **Shotgun Surgery** | One change requires modifying many classes | High |
| **Feature Envy** | Method uses data from other classes more | Medium |

**Relationship-Level Smells:**

| Smell | Detection Pattern | Severity |
|-------|------------------|----------|
| **Inappropriate Intimacy** | Classes access each other's private parts | Medium |
| **Message Chains** | `a.b().c().d()` chains | Medium |
| **Middle Man** | Class only does delegation | Low |
| **Data Clumps** | Same data items always appear together | Medium |

#### 1.2 Smell Detection Checklist

When reviewing code, check:
- [ ] Are there methods longer than 20 lines?
- [ ] Is there duplicated code?
- [ ] Are there classes with more than 10 fields?
- [ ] Are there switch statements that could use polymorphism?
- [ ] Are there methods with more than 4 parameters?
- [ ] Is there deep inheritance hierarchy (> 3 levels)?
- [ ] Does the class change for multiple reasons?
- [ ] Are there message chains with more than 3 calls?
- [ ] Are there "data classes" with only data and no behavior?
- [ ] Are there "lazy classes" that do almost nothing?

---

### 2. Refactoring Techniques

#### 2.1 Refactoring Principles

**Two Hats (Kent Beck):**

| Hat | Activity | Rule |
|-----|----------|------|
| **Adding Features** | Add new functionality | Don't modify existing code |
| **Refactoring** | Improve structure | Don't add new features |

**Never wear both hats at the same time!**

**Refactoring Rhythm:**
```
Test → Small Change → Test → Small Change → Test
```

#### 2.2 Key Refactoring Techniques

**Composing Methods:**

| Refactoring | When to Use | Steps |
|-------------|-------------|-------|
| **Extract Method** | Method too long, code block needs naming | 1.Create new method 2.Copy code 3.Replace original code with call |
| **Inline Method** | Method body as clear as its name | 1.Replace calls with method body 2.Delete method |
| **Replace Temp with Query** | Temporary variable holds expression | 1.Extract expression to method 2.Replace temp with call |
| **Replace Method with Method Object** | Too many temporaries in long method | 1.Create class for method 2.Temporaries become fields |

**Moving Features:**

| Refactoring | When to Use | Steps |
|-------------|-------------|-------|
| **Move Method** | Method uses other class more | 1.Copy to target 2.Delegate in source 3.Delete source method |
| **Extract Class** | Class does too much | 1.Create new class 2.Move fields/methods 3.Link classes |
| **Hide Delegate** | Client knows delegation chain | 1.Add delegate method 2.Hide chain |

**Simplifying Conditionals:**

| Refactoring | When to Use | Steps |
|-------------|-------------|-------|
| **Decompose Conditional** | Complex conditional logic | 1.Extract condition 2.Extract then/else |
| **Consolidate Conditional** | Multiple checks with same result | 1.Combine with && or \|\| 2.Extract method |
| **Replace Nested Conditional with Guard Clauses** | Deeply nested if-else | 1.Add guard clause returns 2.Flatten structure |
| **Replace Conditional with Polymorphism** | Switch by type | 1.Create subclasses 2.Move behavior to each subclass |

#### 2.3 Refactoring Decision Tree

```
Found code smell?
    │
    ├─ Do you have tests?
    │   ├─ No → Write tests first
    │   └─ Yes → Continue
    │
    ├─ Do you understand the code?
    │   ├─ No → Refactor to understand
    │   └─ Yes → Continue
    │
    └─ Choose refactoring approach:
        │
        ├─ Method too long → Extract Method
        ├─ Duplicated code → Extract Method / Pull Up
        ├─ Class too large → Extract Class
        ├─ Parameter list too long → Introduce Parameter Object
        ├─ Switch statement → Replace with Polymorphism
        └─ Complex conditionals → Decompose / Guard Clauses
```

---

### 3. Design Patterns

#### 3.1 SOLID Principles Foundation

Before applying patterns, ensure understanding of SOLID principles:

| Principle | Name | Description |
|-----------|------|-------------|
| **S** | Single Responsibility | One reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subtypes must be substitutable |
| **I** | Interface Segregation | Small, focused interfaces |
| **D** | Dependency Inversion | Depend on abstractions |

#### 3.2 Selection by Problem Type

| Problem | Pattern | Key Benefit |
|---------|---------|-------------|
| Need single instance | Singleton | Controlled access |
| Flexible object creation | Factory Method | Decouple creation |
| Create families of objects | Abstract Factory | Consistent products |
| Build complex objects | Builder | Step-by-step construction |
| Incompatible interfaces | Adapter | Make incompatible work |
| Dynamically add responsibilities | Decorator | Flexible extension |
| Control access | Proxy | Indirection layer |
| Simplify complex system | Facade | Simple interface |
| Tree structure | Composite | Uniform handling |
| Switch algorithms | Strategy | Interchangeable behaviors |
| Event notification | Observer | Loose coupling |
| Encapsulate requests | Command | Undo/redo support |
| State-dependent behavior | State | Clear state transitions |

#### 3.3 Selection by Code Smell

| Smell | Pattern Solution |
|-------|------------------|
| Large switch statement | State, Strategy |
| Multiple conditionals | Strategy, State, Null Object |
| Tight coupling | Observer, Mediator, Facade |
| Difficult object creation | Factory, Builder |
| Hard to extend class | Decorator, Adapter |
| Complex subsystem | Facade |
| Need varying algorithms | Strategy, Template Method |

#### 3.4 Pattern Quick Reference

**Creational Patterns:**

| Pattern | When to Use |
|---------|-------------|
| Singleton | Need single instance |
| Factory Method | Don't know exact class to create |
| Abstract Factory | Need families of related objects |
| Builder | Complex object with many options |
| Prototype | Clone existing objects |

**Structural Patterns:**

| Pattern | When to Use |
|---------|-------------|
| Adapter | Incompatible interfaces |
| Decorator | Dynamically add responsibilities |
| Proxy | Control access, lazy loading |
| Facade | Simplify complex interfaces |
| Composite | Tree structure, uniform handling |
| Flyweight | Many similar objects, share state |
| Bridge | Separate abstraction from implementation |

**Behavioral Patterns:**

| Pattern | When to Use |
|---------|-------------|
| Strategy | Interchangeable algorithms |
| Observer | One-to-many notifications |
| Command | Encapsulate requests, undo/redo |
| State | State-dependent behavior |
| Template Method | Algorithm skeleton, varying steps |
| Iterator | Uniform collection traversal |
| Mediator | Complex object interactions |
| Memento | Save/restore state |
| Chain of Resp. | Request has multiple handlers |
| Visitor | Add operations to object structure |

---

### 4. Integrated Workflow

#### 4.1 Code Quality Improvement Process

```
1. IDENTIFY
   └── Detect code smells
       └── Use smell checklist
           └── Rate severity (Critical/High/Medium/Low)

2. DIAGNOSE
   └── Understand root cause
       └── Why does this smell exist?
           └── What problems will it cause?

3. PLAN
   └── Choose refactoring or pattern
       └── Consider dependencies
           └── Estimate impact

4. PREPARE
   └── Ensure tests exist
       └── Run tests to verify behavior
           └── Create tests if missing

5. EXECUTE
   └── Apply small changes
       └── Test after each change
           └── Keep code working

6. VERIFY
   └── Run all tests
       └── Check for new smells
           └── Confirm improvement
```

#### 4.2 Smell→Refactoring→Pattern Flow

```
Detected code smell
        │
        ▼
┌───────────────────┐
│ Is this a method  │
│ level problem?    │
└────────┬──────────┘
         │
    ┌────┴────┐
    │ Yes     │ No
    ▼         ▼
Extract    Is this a class
Method     level problem?
              │
         ┌────┴────┐
         │ Yes     │ No
         ▼         ▼
    Extract    Is this a
    Class      relationship
              problem?
                  │
             ┌────┴────┐
             │ Yes     │ No
             ▼         ▼
        Move/Hide   Consider
        Delegate    Pattern
                        │
                        ▼
                  ┌──────────────┐
                  │ Which        │
                  │ pattern fits │
                  │ best?        │
                  └──────┬───────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    Creational      Structural      Behavioral
    Patterns        Patterns        Patterns
```

---

### 5. Collaboration Table

#### 5.1 Collaboration with Other Skills

| Collaborating Skill | Collaboration Mode | Description |
|--------------------|-------------------|-------------|
| **test-driven-development** | Sequential | Write tests before refactoring |
| **systematic-debugging** | Consultation | Find root cause before fixing |
| **requesting-code-review** | Reference | Get feedback on refactored code |
| **pdd-code-reviewer** | Reference | Get PDD project code review |
| **software-engineer** | Delegation | Quality check after code implementation |

#### 5.2 Collaboration Workflow

```
Code quality issue detected
    ↓
Invoke expert-code-quality
    ↓
Identify code smells + Recommend refactoring/patterns
    ↓
(If tests needed first) → Invoke test-driven-development
    ↓
(If code implementation needed) → Invoke software-engineer
    ↓
Complete code quality improvement
```

---

### 6. Quick Decision Matrix

| Scenario | Primary Action |
|----------|---------------|
| Found duplicated code | Extract Method |
| Method too long | Extract Method |
| Class too large | Extract Class |
| Parameter list too long | Introduce Parameter Object |
| Switch by type | Replace with Polymorphism |
| Need single instance | Consider Singleton |
| Need flexible creation | Factory Method or Builder |
| Incompatible interfaces | Adapter |
| Need to add behavior | Decorator |
| Complex subsystem | Facade |
| Need varying algorithms | Strategy |
| Need event notification | Observer |

---

### 7. Anti-Patterns

#### 7.1 Refactoring Anti-Patterns

| Anti-Pattern | Description | Correct Approach |
|--------------|-------------|------------------|
| **Big Bang Refactoring** | Rewrite everything at once | Small incremental changes |
| **Refactoring Without Tests** | Change code without safety net | Write tests first |
| **Over-Refactoring** | Refactor clean code | Stop when code is clear |
| **Refactoring Addiction** | Only refactor, never deliver | Balance refactoring with features |
| **Random Refactoring** | No clear goal | Identify smells first |

#### 7.2 Pattern Anti-Patterns

| Anti-Pattern | Description | Correct Approach |
|--------------|-------------|------------------|
| **Pattern Obsession** | Use patterns everywhere | Use patterns to solve problems |
| **Singleton Abuse** | Everything is singleton | Use only when truly needed |
| **Factory Overkill** | Factory for single product | Use factory for multiple products |
| **Decorator Nesting** | Too many decorator layers | Limit nesting depth |
| **Premature Pattern** | Use pattern before needed | Let patterns emerge from refactoring |

---

### 8. Practice Checklists

#### 8.1 Code Review Checklist

Before approving code, verify:
- [ ] No critical code smells
- [ ] Reasonable method size (< 20 lines)
- [ ] Class has single responsibility
- [ ] No duplicated code
- [ ] Clear conditionals
- [ ] Meaningful names
- [ ] Tests exist and pass
- [ ] Follows SOLID principles
- [ ] Patterns used appropriately (not overused)

#### 8.2 Refactoring Safety Checklist

Before refactoring:
- [ ] All tests pass
- [ ] Tests cover code to refactor
- [ ] Understand code functionality
- [ ] Have rollback plan
- [ ] Make small changes
- [ ] Test after each change

#### 8.3 Pattern Application Checklist

Before applying pattern:
- [ ] Problem matches pattern intent
- [ ] Pattern solves real problem (not imagined)
- [ ] Team understands pattern
- [ ] Pattern doesn't overcomplicate
- [ ] Alternatives considered
- [ ] Pattern fits project context

---

## Guardrails

- Must provide suggestions based on Martin Fowler's refactoring catalog and GoF design patterns
- Refactoring suggestions need specific code transformation examples
- Pattern application needs to weigh pros and cons, not blindly recommend
- Code review needs to specifically point out problems and improvement suggestions
- Clearly state uncertain issues to avoid misleading

---

## Version History

### v2.0 (2026-03-21)
- Unified to Chinese description
- Added collaboration table, clarified collaboration with other skills
- Enhanced quick decision matrix
- Optimized refactoring decision tree
- Added anti-pattern checklist

### v1.0 (Initial version)
- Basic code quality detection
- Refactoring technique catalog
- Design pattern reference

---

> **Remember**: Good code isn't about being clever—it's about being clear. Refactoring and patterns are tools to achieve clarity, not ends in themselves.
