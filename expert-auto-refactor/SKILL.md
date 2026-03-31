---
name: expert-auto-refactor
description: |
  Automated refactoring expert skill that transforms collected quality improvement tasks into concrete code operations. Automatically triggers when users need code refactoring, duplicate elimination, or complexity simplification. 支持中文触发：重构代码、消除重复、简化代码、代码重构、自动重构。
  
  Core responsibility: Initiate targeted refactoring PRs regularly in a "small debt repayment" manner to prevent technical debt accumulation.
  
  Trigger scenarios:
  - User requests "refactor code", "eliminate duplicates", "simplify code"
  - Called by pdd-entropy-reduction coordinator
  - Refactoring suggestions passed from expert-entropy-auditor
  
  支持中文触发：自动重构、代码重构、消除重复、简化代码、重构专家、PDD重构。
author: neuqik@hotmail.com
license: MIT
---

# Automated Refactoring Expert (expert-auto-refactor)

## Core Philosophy

> "Initiate targeted refactoring PRs regularly in a 'small debt repayment' manner to prevent technical debt from accumulating into unmanageable 'painful interest'." —— Harness Engineering

The automated refactoring expert is an upgraded version of `expert-code-quality`, not just recording issues but actively executing refactoring operations.

## Refactoring Types

### 1. Extract Common Methods

**Scenario**: Similar code logic in multiple places

**Refactoring Method**:
1. Identify similar code
2. Extract common methods
3. Replace original calls

**Example**:

Before refactoring:
```javascript
// File A
function formatDate(date) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

// File B
function formatDateString(d) {
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
}
```

After refactoring:
```javascript
// utils/dateUtils.ts
export function formatDate(date: Date): string {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

// File A
import { formatDate } from '../utils/dateUtils';

// File B
import { formatDate } from '../utils/dateUtils';
```

### 2. Eliminate Duplicate Code

**Scenario**: Identical or highly similar code blocks

**Refactoring Method**:
1. Detect duplicate code
2. Extract to shared module
3. Update references

**Example**:

Before refactoring:
```javascript
// Repeated validation logic in multiple places
if (!user.email || !user.email.includes('@')) {
  throw new Error('Invalid email');
}
```

After refactoring:
```javascript
// utils/validators.ts
export function validateEmail(email: string): boolean {
  return email && email.includes('@');
}

// Usage
if (!validateEmail(user.email)) {
  throw new Error('Invalid email');
}
```

### 3. Simplify Complex Logic

**Scenario**: Functions that are too long, deeply nested, or have complex logic

**Refactoring Method**:
1. Split long functions
2. Extract sub-functions
3. Simplify conditional logic

**Example**:

Before refactoring:
```javascript
function processOrder(order) {
  if (order.status === 'pending') {
    if (order.items.length > 0) {
      if (order.payment) {
        // Processing logic...
        if (order.shipping) {
          // More processing...
        }
      }
    }
  }
}
```

After refactoring:
```javascript
function processOrder(order) {
  if (!canProcessOrder(order)) return;
  
  processPayment(order);
  processShipping(order);
  updateOrderStatus(order);
}

function canProcessOrder(order) {
  return order.status === 'pending' 
    && order.items.length > 0 
    && order.payment;
}
```

### 4. Optimize Naming

**Scenario**: Non-standard naming, unclear meaning

**Refactoring Method**:
1. Analyze naming context
2. Generate better naming
3. Batch replacement

**Example**:

Before refactoring:
```javascript
function calc(a, b) {
  return a * b * 0.1;
}
```

After refactoring:
```javascript
function calculateTax(basePrice: number, quantity: number): number {
  const TAX_RATE = 0.1;
  return basePrice * quantity * TAX_RATE;
}
```

---

## Refactoring Process

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Analyze   │ ──→ │    Plan     │ ──→ │   Execute   │ ──→ │   Verify    │
│             │     │             │     │             │     │             │
│ • Code      │     │ • Refactor  │     │ • Code      │     │ • Test      │
│   structure │     │   strategy  │     │   changes   │     │   execution │
│ •           │     │ • Impact    │     │ • Reference │     │ • Function  │
│ Dependencies│     │   scope     │     │   updates   │     │   validation│
│ • Test      │     │ • Risk      │     │ • Document  │     │ • PR        │
│   coverage  │     │   assessment│     │   sync      │     │   creation  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Refactoring Strategy

### Small Debt Repayment Principle

Each refactoring should:
1. **Small steps**: Only change a small part each time
2. **Maintain tests**: Ensure tests always pass
3. **Frequent commits**: Commit after each small step
4. **Rollback capable**: Keep each commit independently rollbackable

### Risk Assessment

| Risk Level | Condition | Strategy |
|---------|------|------|
| Low | Complete test coverage | Auto execute |
| Medium | Partial test coverage | Create PR |
| High | No test coverage | Add tests first then refactor |

---

## Output Format

### Refactoring Report

```markdown
# Refactoring Report - YYYY-MM-DD

## Refactoring Scope
- Target files: X
- Affected files: X
- Test coverage: X%

## Refactoring Operations

### Extract Common Methods
| Original File | New File | Method Name | Status |
|-------|-------|-------|------|
| utils/formatDate.js | utils/dateUtils.ts | formatDate | ✅ Completed |

### Eliminate Duplicate Code
| File A | File B | Duplicate Lines | Status |
|-------|-------|---------|------|
| service/UserService.ts | service/OrderService.ts | 25 lines | ✅ Completed |

### Simplify Complex Logic
| File | Function Name | Original Lines | New Lines | Status |
|------|-------|-------|-------|------|
| service/OrderService.ts | processOrder | 80 | 35 | ✅ Completed |

## Verification Results
- Unit tests: ✅ All passed
- Integration tests: ✅ All passed
- Functional verification: ✅ No anomalies

## PR Information
- PR number: #XXX
- Branch: refactor/entropy-reduction-YYYYMMDD
- Status: Pending review
```

---

## Configuration Options

```yaml
# auto-refactor-config.yaml
auto_refactor:
  # Refactoring scope
  scope:
    code_paths: ["src/"]
    exclude: ["node_modules/", "dist/", "build/"]
  
  # Refactoring rules
  rules:
    max_file_lines: 300
    max_function_lines: 50
    min_similarity: 0.8
  
  # Execution strategy
  execution:
    auto_fix_low_risk: true   # Auto fix low risk
    create_pr: true           # Create PR
    max_changes_per_run: 10   # Max changes per run
  
  # Testing requirements
  testing:
    require_tests: true       # Require tests
    min_coverage: 80          # Minimum coverage
```

---

## Usage Examples

### Example 1: Extract Duplicate Code

```
User: Eliminate duplicates in code

AI:
1. Detect duplicate code
2. Analyze similarity
3. Extract to shared module
4. Update all references
5. Create PR
```

### Example 2: Simplify Complex Function

```
User: Simplify processOrder function

AI:
1. Analyze function structure
2. Identify extractable sub-functions
3. Execute split refactoring
4. Run test verification
5. Create PR
```

### Example 3: Optimize Naming

```
User: Optimize code naming

AI:
1. Scan non-standard naming
2. Analyze context
3. Generate better naming
4. Batch replacement
5. Create PR
```

---

## Collaboration with Other Skills

- **pdd-entropy-reduction**: Called as a sub-skill by the coordinator
- **expert-entropy-auditor**: Receive refactoring suggestions
- **expert-arch-enforcer**: Receive architecture violation fixes
- **pdd-code-reviewer**: Trigger code review after refactoring
- **pdd-doc-change**: Synchronously update related documentation
