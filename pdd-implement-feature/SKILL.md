---
name: pdd-implement-feature
description: Implement feature point code based on development specifications. Call this Skill when users want to start coding implementation. 支持中文触发：实现功能点、编码实现、开始编码、功能开发、代码实现、PDD实现。
license: MIT
compatibility: Requires specification generation to be completed first
metadata:
  author: neuqik@hotmail.com
  version: "2.0"
  parent: pdd-main
---

Feature Point Implementation - Implement feature point code based on development specifications

**Input**:
- Development Specification (spec.md)
- Acceptance Criteria (checklist.md)
- Test Cases (test-cases.md, optional)

**Output**:
- Code files
- Acceptance report

---

## Version History

| Version | Date | Changes |
|-----|------|---------|
| 3.2 | 2026-03-22 | Added error handling and fallback specifications, PDD implementation specification references |
| 3.1 | 2026-03-22 | Removed automatic calling of pdd-pr-* skills, changed to only prompt user for manual calling |
| 3.0 | 2026-03-21 | Added PR management layer integration (pdd-pr-*) |
| 2.0 | 2026-03-21 | Added software-engineer and expert-xxx calling integration |
| 1.0 | Early | Initial version |

---

## 1. Skill Integration

### 1.1 Software Engineer Invocation

During code implementation, call the `software-engineer` skill:

| Invocation Timing | Service Content |
|---------|---------|
| Code Implementation | Execute code implementation based on specifications |
| Unit Testing | Write unit tests and integration tests |
| Code Refactoring | Code optimization following coding standards |
| Defect Fixing | Error handling and issue resolution |

### 1.2 Expert Skill Invocation

When encountering technical issues during implementation, call expert-xxx as needed:

| Expert Skill | Trigger Condition | Expected Output |
|---------|---------|---------|
| **expert-ruoyi** | RuoYi framework issues | Solution + Best practices |
| **expert-activiti** | Workflow issues | BPMN design recommendations |
| **expert-mysql** | Database issues | SQL optimization solution |
| **expert-code-quality** | Code quality issues | Refactoring solution |

### 1.3 Invocation Conditions

**Must call software-engineer**:
- Entering code implementation phase
- Need to write test code

**Call expert-xxx as needed**:
- Encountering RuoYi framework issues
- Encountering database design issues
- Encountering code quality issues

---

## 2. Process Steps

### Step 1: Read Development Specification

Read from `dev-specs/FP-{sequence}/spec.md`:
- Interface definitions
- Data models
- Business logic
- Test cases

### Step 2: Read Acceptance Criteria

Read acceptance items from `dev-specs/FP-{sequence}/checklist.md`.

### Step 3: Determine Implementation Order

Determine implementation order based on feature point dependencies:
- Data models → Database scripts
- Backend interfaces → Controller/Service/Mapper
- Frontend pages → Vue components

### Step 4: Generate Database Scripts

Generate SQL scripts based on data models:
```sql
CREATE TABLE `{table_name}` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  -- Business fields
  `create_time` datetime DEFAULT NULL COMMENT 'Creation Time',
  `update_time` datetime DEFAULT NULL COMMENT 'Update Time',
  `create_by` varchar(64) DEFAULT NULL COMMENT 'Creator',
  `update_by` varchar(64) DEFAULT NULL COMMENT 'Updater',
  `status` char(1) DEFAULT '0' COMMENT 'Status',
  `del_flag` char(1) DEFAULT '0' COMMENT 'Delete Flag',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{Table Comment}';
```

### Step 5: Generate Backend Code

**Call software-engineer** to generate code that complies with standards:

**a. Domain Entity Class**
```java
@Data
@TableName("{table_name}")
public class {EntityName} {
    @TableId(type = IdType.AUTO)
    private Long id;
    // Business fields
    @TableField(fill = FieldFill.INSERT)
    private Date createTime;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date updateTime;
    // ...
}
```

**b. Mapper Interface**
```java
@Mapper
public interface {EntityName}Mapper extends BaseMapper<{EntityName}> {
    // Custom query methods
}
```

**c. Service Interface and Implementation**
```java
public interface I{EntityName}Service extends IService<{EntityName}> {
    // Business methods
}

@Service
public class {EntityName}ServiceImpl extends ServiceImpl<{EntityName}Mapper, {EntityName}> implements I{EntityName}Service {
    // Business implementation
}
```

**d. Controller**
```java
@RestController
@RequestMapping("/{module}")
public class {EntityName}Controller {
    @Autowired
    private I{EntityName}Service service;

    // Interface methods
}
```

### Step 6: Generate Frontend Code

**Call software-engineer** to generate frontend code:

**a. API Interface**
```javascript
import request from '@/utils/request'

export function list{EntityName}(query) {
  return request({
    url: '/{module}/list',
    method: 'get',
    params: query
  })
}
```

**b. Vue Component**
```vue
<template>
  <!-- Page template -->
</template>

<script>
export default {
  name: '{EntityName}',
  data() {
    return {
      // Data
    }
  },
  methods: {
    // Methods
  }
}
</script>
```

### Step 7: Implement Business Logic

Implement based on business logic in specifications:
- Processing flow
- Validation rules
- State transitions
- Exception handling

**Expert Consultation (as needed)**:
- RuoYi issues → `expert-ruoyi`
- Database issues → `expert-mysql`

### Step 8: Run Test Validation

If test cases exist, run test validation:
- Unit tests
- Interface tests
- Integration tests

### Step 9: Update Acceptance Status

Update acceptance status in `checklist.md`:
- Business acceptance items
- Technical acceptance items
- Integration acceptance items

### Step 10: Generate Acceptance Report

Output acceptance results:
```markdown
## Acceptance Report

**Feature Point**: FP-XXX-NNN
**Feature Name**: xxx
**Acceptance Date**: {Date}

### Business Acceptance
| No. | Acceptance Scenario | Expected Result | Actual Result | Status |
|------|---------|---------|---------|------|
| 1 | xxx | xxx | xxx | ✓/✗ |

### Technical Acceptance
| No. | Acceptance Item | Standard | Actual | Status |

### Issue Log
- [Issue1]: Description
- [Issue2]: Description

### Conclusion
- [ ] Pass
- [ ] Fail, needs modification
```

---

## 3. Expert Consultation Process

```
pdd-implement-feature starts
    │
    ├─► Identify RuoYi framework issues
    │       │
    │       ▼
    │   expert-ruoyi consultation
    │       │
    │       ▼
    │   Return solution
    │
    ├─► Identify database issues
    │       │
    │       ▼
    │   expert-mysql consultation
    │       │
    │       ▼
    │   Return optimization solution
    │
    ├─► Identify code quality issues
    │       │
    │       ▼
    │   expert-code-quality consultation
    │       │
    │       ▼
    │   Return refactoring recommendations
    │
    └─► Continue implementation
```

### 3.1 expert-ruoyi Invocation Example

```
Trigger Condition: Encountering permission validation issues
Call: expert-ruoyi
Input:
  - Issue: @PreAuthorize annotation not working
  - Code snippet: [Related code]
  - Error message: Permission validation failed

Return:
  - Solution
  - Best practices
  - sys_menu configuration recommendations
```

### 3.2 expert-mysql Invocation Example

```
Trigger Condition: Encountering query performance issues
Call: expert-mysql
Input:
  - SQL: SELECT * FROM large_table WHERE ...
  - Table size: 10 million records
  - Execution plan: [EXPLAIN result]

Return:
  - Optimization solution
  - Index recommendations
  - SQL rewrite
```

---

## 4. Code Standards

### 4.1 Backend Standards

- Class names use PascalCase
- Method names use camelCase
- Constants use UPPER_SNAKE_CASE
- Comments use Javadoc format

### 4.2 Frontend Standards

- Component names use PascalCase
- Method names use camelCase
- CSS class names use kebab-case
- Use ES6+ syntax

### 4.3 software-engineer Standards

Follow the core rules of software-engineer skill:
- Read existing code style before writing new code
- Error handling first
- Keep it minimal
- PR-ready code

---

## 5. Guardrails

- Code must comply with project standards
- Must implement all interfaces defined in specifications
- Must handle all exceptions defined in specifications
- Must pass all acceptance items before marking as complete
- Must synchronize specification documents after code changes
- **Must consult expert skills when encountering technical issues**
- **Code implementation must follow software-engineer standards**

---

## 6. Collaboration with Other Skills

| Collaborative Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **software-engineer** | Delegation | Specification documents | Standards-compliant code |
| **expert-ruoyi** | Consultation | Technical issues | Solutions |
| **expert-mysql** | Consultation | SQL issues | Optimization solutions |
| **expert-code-quality** | Consultation | Code issues | Refactoring recommendations |
| **pdd-code-reviewer** | Sequential | Code + Specifications | Review report |
| **pdd-pr-create** | Sequential | Change ID | PR + Review report |
| **pdd-pr-merge** | Sequential | Change ID | Merge + Archive |

---

## 7. PR Management Layer Prompts

### 7.1 Prompt After Feature Point Completion

After feature point implementation and validation passes, **prompt** user that PR management skills can be used:

```
## Feature Point Implementation Complete

**Feature Point**: FP-XXX-NNN
**Status**: Acceptance passed

### Available PR Management Operations

If you need to create a PR, you can manually call the following skills:
- `/pdd-pr-create {change-id}` - Create PR and execute automated review
- `/pdd-pr-review {change-id}` - View PR review results
- `/pdd-pr-merge {change-id}` - Merge PR and archive

### Manual Operation Steps

1. Create OpenSpec Change (optional):
   ```
   /openspec-new-change {change-name}
   ```

2. Create PR:
   ```
   /pdd-pr-create {change-id}
   ```

3. Confirm merge:
   ```
   /pdd-pr-merge {change-id}
   ```
```

### 7.2 Do Not Automatically Call PR Skills

**Important Principles**:
- PDD framework **will not automatically call** pdd-pr-* skills
- Users need to **manually decide** whether to use PR management features
- PR management skills are **optional**, not required

### 7.3 PR Management Skill Description

| Skill | Function | Invocation Method |
|------|------|---------|
| `pdd-pr-create` | Create PR and execute automated review | User manual call |
| `pdd-pr-review` | View PR review results | User manual call |
| `pdd-pr-merge` | Merge PR and archive | User manual call |
| `pdd-pr-batch` | Batch process multiple PRs | User manual call |

---

## 8. Guardrails (Updated)

- Code must comply with project standards
- Must implement all interfaces defined in specifications
- Must handle all exceptions defined in specifications
- Must pass all acceptance items before marking as complete
- Must synchronize specification documents after code changes
- **Must consult expert skills when encountering technical issues**
- **Code implementation must follow software-engineer standards**
- **Prompt user about available PR management skills after feature point completion, but do not automatically call**

---

## 9. Error Handling and Fallback Specifications

### 9.1 Error Classification

| Level | Definition | Blocking |
|------|------|--------|
| Critical | Must fix, blocks process | ✅ Blocking |
| Warning | Recommended to fix, non-blocking | ❌ Non-blocking |
| Suggestion | Optional optimization | ❌ Non-blocking |

### 9.2 Retry Strategy

```yaml
Limit: Maximum 3 times per feature point
Count: Each re-review/validation after fix counts as 1 time
Exceed limit: Pause process, wait for manual decision
```

### 9.3 Fallback Rules

| Failure Scenario | Fallback Position | Re-execution |
|---------|---------|---------|
| pdd-code-reviewer review failed | pdd-implement-feature | Re-review after fix |
| pdd-verify-feature validation failed | pdd-implement-feature | Re-validate after fix |

### 9.4 Failure Recording

- **Location**: `dev-specs/FP-{module}-{sequence}/review-report.md`
- **Record Content**:
  - Failure time
  - Failure stage
  - Failure reason
  - Number of attempts
  - Related error logs

### 9.5 Manual Intervention Process

```
Retry count exceeds 3 times
    │
    ▼
Pause process
    │
    ▼
Generate pause report
    ├── Current status
    ├── Failure history
    ├── Attempted fixes
    └── Issues requiring manual decision
    │
    ▼
Wait for manual decision
    ├── Continue fixing
    ├── Skip current feature point
    ├── Terminate process
    └── Other solutions
```

---

## 10. PDD Implementation Specification Reference

This Skill follows the PDD framework implementation specifications. For details, see [pdd-framework-design.md Chapter 9](../docs/pdd-framework-design.md#9-pdd-实施规范).

### Core Specification Summary

| Specification | Core Content |
|------|---------|
| **Skill Boundaries** | pdd-code-reviewer (compliance) → expert-code-quality (quality depth) |
| **Context Passing** | File system passing, directory structure standards, supports checkpoint resumption |
| **Manual Review** | Batch review + detailed review of critical feature points |
| **Error Handling** | Critical blocking, pause after 3 retries waiting for manual intervention |
| **PR Management** | Manual trigger, Change-granularity PR, manual archiving |
| **Documentation System** | 9 core document types, naming conventions, in-document change history |
