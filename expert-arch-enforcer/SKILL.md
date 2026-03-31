---
name: expert-arch-enforcer
description: |
  Architecture constraint enforcement skill that monitors code for violations of preset invariants and architectural boundaries. Automatically triggered when users need architecture checks, dependency checks, or module boundary checks.
  
  Core responsibility: Ensure architectural coherence and prevent architectural drift.
  
  Trigger scenarios:
  - User requests "check architecture constraints", "check dependency direction", "check module boundaries"
  - Called by pdd-entropy-reduction coordinator
  - Automatically triggered after code commits
  
  支持中文触发：架构约束检查、依赖检查、模块边界检查、架构强制、架构漂移、PDD架构约束。
author: neuqik@hotmail.com
license: MIT
---

# Architecture Constraint Enforcement (expert-arch-enforcer)

## Core Philosophy

> "In an agent-first world, architectural coherence easily drifts over time. Constraints are the guarantee of speed, not constraints." —— Harness Engineering

The architecture constraint enforcement skill is responsible for monitoring whether code violates preset invariants and architectural boundaries, ensuring code structure maintains consistency.

## Architecture Constraint Model

### Six-Layer Dependency Model

```
Types → Config → Repo → Service → Runtime → UI

Rule: Only forward dependencies allowed, no backward dependencies
```

| Layer | Responsibility | Allowed Dependencies |
|------|------|---------|
| Types | Type definitions, data models | None |
| Config | Configuration management, constant definitions | Types |
| Repo | Data access, external service calls | Types, Config |
| Service | Business logic, domain services | Types, Config, Repo |
| Runtime | Runtime, application entry | Types, Config, Repo, Service |
| UI | User interface, presentation layer | All layers |

### Boundary Constraints

**Data Boundaries**:
- All external data must be validated
- API entry parameters must have Schema validation
- Guessing data structures is not allowed

**Module Boundaries**:
- Modules communicate through interfaces
- Direct cross-layer access is prohibited
- Shared state must be explicitly declared

---

## Detection Items

### 1. Module Dependency Direction Violation

**Detection Method**:
- Parse import/require statements
- Build dependency graph
- Check for dependency direction violations

**Example**:
```
File: src/types/User.ts
import: import { UserService } from '../service/UserService'
→ Detection result: Types layer depends on Service layer, violates dependency direction
```

### 2. Boundary Data Validation Missing

**Detection Method**:
- Scan API entry functions
- Check for Schema validation
- Mark entries lacking validation

**Example**:
```
API entry: POST /api/users
Parameter validation: None
→ Detection result: Missing parameter validation Schema
```

### 3. File Size Exceeded

**Detection Method**:
- Count file lines
- Compare against configured maximum lines
- Mark exceeded files

**Example**:
```
File: src/service/UserService.ts
Lines: 450 lines
Limit: 300 lines
→ Detection result: File too large, suggest splitting
```

### 4. Naming Convention Violation

**Detection Method**:
- Check file names, function names, variable names
- Compare against naming conventions
- Mark violating names

**Example**:
```
Function name: get_data
Convention: camelCase
→ Detection result: Non-compliant naming, should be getData
```

---

## Execution Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Parse     │ ──→ │   Build     │ ──→ │   Detect    │ ──→ │   Report    │
│             │     │             │     │             │     │             │
│ • Code files│     │ • Dependency│     │ • Dependency│     │ • Issue list│
│ • import    │     │   graph     │     │   violation │     │ • Fix       │
│ • Function  │     │ • Call      │     │ • Boundary  │     │   suggestions│
│   signatures│     │   relations │     │   violation │     │ • PR creation│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Tool Integration

### Custom Linter

```javascript
// custom-linter.js
module.exports = {
  rules: {
    'layer-dependency': {
      meta: {
        docs: { description: 'Enforce six-layer dependency direction' }
      },
      create(context) {
        const layers = ['types', 'config', 'repo', 'service', 'runtime', 'ui'];
        return {
          ImportDeclaration(node) {
            const source = node.source.value;
            const currentLayer = getCurrentLayer(context.getFilename());
            const targetLayer = getLayerFromPath(source);
            
            if (layers.indexOf(targetLayer) < layers.indexOf(currentLayer)) {
              context.report({
                node,
                message: `Dependency direction violation: ${currentLayer} cannot depend on ${targetLayer}`
              });
            }
          }
        };
      }
    }
  }
};
```

### ArchUnit Test

```java
// ArchitectureTest.java
@AnalyzeClasses(packages = "com.example")
public class ArchitectureTest {
    
    @ArchTest
    static final ArchRule layer_dependency_rule = layeredArchitecture()
        .layer("Types").definedBy("..types..")
        .layer("Config").definedBy("..config..")
        .layer("Repo").definedBy("..repo..")
        .layer("Service").definedBy("..service..")
        .layer("Runtime").definedBy("..runtime..")
        .layer("UI").definedBy("..ui..")
        .whereLayer("Types").mayNotBeAccessedByAnyLayer()
        .whereLayer("Config").mayOnlyBeAccessedByLayers("Repo", "Service", "Runtime", "UI")
        .whereLayer("Repo").mayOnlyBeAccessedByLayers("Service", "Runtime", "UI");
}
```

---

## Output Format

### Architecture Constraint Report

```markdown
# Architecture Constraint Report - YYYY-MM-DD

## Architecture Health Score: XX/100

## Dependency Graph

[Dependency relationship visualization]

## Issues Found

### Critical (Must Fix)
| File | Issue | Violation Type |
|------|------|---------|
| src/types/User.ts | Depends on Service layer | Dependency direction violation |

### Warning (Suggested Fix)
| File | Issue | Violation Type |
|------|------|---------|
| src/api/users.ts | Missing parameter validation | Boundary validation missing |

### Info (Optional Fix)
| File | Issue | Violation Type |
|------|------|---------|
| src/service/UserService.ts | File 450 lines | Size exceeded |

## Fix Recommendations

### Critical Fixes
1. Remove dependency on UserService in User.ts
2. Extract shared logic to Types layer
```

---

## Configuration Options

```yaml
# arch-enforcer-config.yaml
arch_enforcer:
  # Layer definitions
  layers:
    - name: types
      paths: ["src/types/", "src/models/"]
    - name: config
      paths: ["src/config/", "src/constants/"]
    - name: repo
      paths: ["src/repo/", "src/data/"]
    - name: service
      paths: ["src/service/", "src/domain/"]
    - name: runtime
      paths: ["src/runtime/", "src/app/"]
    - name: ui
      paths: ["src/ui/", "src/components/"]
  
  # Constraint rules
  constraints:
    max_file_lines: 300
    max_function_lines: 50
    require_schema_validation: true
  
  # Execution configuration
  execution:
    run_linter: true
    run_arch_test: true
    create_pr: true
```

---

## Usage Examples

### Example 1: Comprehensive Architecture Check

```
User: Check architecture constraints

AI:
1. Parse code files
2. Build dependency graph
3. Run Linter and ArchUnit
4. Generate report
```

### Example 2: Dependency Direction Check

```
User: Check module dependency direction

AI:
1. Parse import statements
2. Build dependency graph
3. Check for violations of six-layer model
4. Generate violation report
```

---

## Collaboration with Other Skills

- **pdd-entropy-reduction**: Called as a sub-skill by the coordinator
- **expert-auto-refactor**: Receives architecture violations, executes refactoring
- **pdd-code-reviewer**: Integrates architecture checks into code review
