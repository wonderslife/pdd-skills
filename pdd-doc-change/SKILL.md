---
name: pdd-doc-change
description: |
  Document Change Management skill under PDD framework, managing the modification workflow of development specification documents. Invoked when requirement changes need to update specification documents.
  
  支持中文触发：文档变更、规格变更、需求变更、更新规格、PDD文档变更。
license: MIT
compatibility: Requires existing development specification documents
metadata:
  author: neuqik@hotmail.com
  version: "1.0"
  parent: pdd-main
---

# PDD Document Change Management (pdd-doc-change)

## Overview

This skill is a document change management component under the PRD-Driven Development (PDD) framework, specifically designed to manage the modification workflow of development specification documents, ensuring systematic, complete, and traceable document changes.

## Trigger Scenarios

**Automatic Trigger:**
- Requirement changes need to update development specifications
- Specification issues discovered during feature implementation

**Manual Trigger:**
- User inputs commands like `/change`, `/audit`, `/doc`
- User explicitly requests professional analysis and requirement modeling for business processes, management systems, or Excel forms
- User needs to modify design documents based on requirement changes or communication records

## Core Capabilities

### 1. Document Import and Analysis

- Receive and parse existing development specification documents
- Extract key modification points from change requirements
- Build document structure index and content understanding
- Identify dependencies between related documents

### 2. Modification Plan Generation

- Based on change requirement content, compare and analyze existing specification documents
- Generate systematic modification plan:
  - Modification scope (which documents need modification)
  - Modification content (specific modification points)
  - Priority (P0-Urgent and Important, P1-Important Not Urgent, P2-Can Optimize)
  - Implementation steps (modification order and dependencies)

### 3. TODO.md Generation

- Convert modification plan into structured TODO.md file
- Include fields:
  - Task ID (unique identifier)
  - Modification content description
  - Related document path
  - Priority
  - Status (pending/in_progress/completed)
  - Modification notes

### 4. Document Modification Execution

- Execute modification operations on specified specification documents according to TODO.md content
- Ensure modifications comply with technical specifications and design standards
- Maintain consistency in document style and format

### 5. CHANGELOG.md Maintenance

- Record detailed change information for each modified specification document
- Record content includes:
  - Modification time
  - Modified document
  - Modification content summary
  - Before/after comparison (key changes)
  - Related requirement change ID

### 6. Change Verification and Reconciliation

- After completing all TODO tasks, automatically compare TODO.md and CHANGELOG.md content
- Verify all planned modifications have been correctly implemented and recorded
- Check consistency between documents
- Identify missing or conflicting modifications

### 7. Result Report Generation

- Generate requirement change completion result report
- Include:
  - Overall completion status
  - List of completed modifications
  - Description of incomplete items
  - Document consistency verification results
  - Follow-up recommendations

## Workflow

```
Receive Modification Request
    ↓
Analyze Change Documents/Requirements
    ↓
Compare with Existing Specification Documents
    ↓
Generate Modification Plan
    ↓
Create TODO.md
    ↓
Execute Document Modifications
    ↓
Update CHANGELOG.md
    ↓
Change Verification
    ↓
All Tasks Completed?
    ├── Yes → Generate Result Report
    └── No → Continue Executing Modifications
```

## Integration with PDD Process

```
Requirement Change Occurs
    ↓
pdd-doc-change Analyzes Change Impact
    ↓
Determine Specification Documents to Modify
    ↓
Generate Modification Plan and TODO
    ↓
Execute Document Modifications
    ↓
Update CHANGELOG
    ↓
Verify Change Completeness
    ↓
Notify Related Feature Points for Re-verification
```

## Use Cases

1. **Requirement Change Management**: Systematically update related specification documents when business requirements change
2. **Version Iteration Update**: Synchronous update of specification documents during product version iteration
3. **Issue Fix Recording**: Fix errors or omissions in documents based on user feedback
4. **Compliance Adjustment**: Adjust specification content according to new regulations or internal policies
5. **Process Optimization**: Update specification documents after business process optimization

## Operating Standards

### Document Naming Conventions

- TODO.md: Place in the `dev-specs/` directory of the modification module
- CHANGELOG.md: Place in the `dev-specs/` directory of the modification module
- Modification Plan: `变更计划.md`
- Result Report: `变更完成报告.md`

### Task Priority Definition

| Priority | Name | Definition | Handling |
| --- | ----- | --------------- | ----- |
| P0 | Urgent and Important | Modifications affecting core business processes or compliance | Execute immediately |
| P1 | Important Not Urgent | Important feature improvements | Complete in short term |
| P2 | Can Optimize | Experience optimization or supplementary explanations | Can be deferred |

### Change Log Format

```markdown
### [Version] - YYYY-MM-DD

#### Added
- New features or document content

#### Changed
- Modified features or content, explain reason for modification

#### Removed
- Removed features or content

#### Fixed
- Fixed issues
```

## Output Templates

### TODO.md Template

```markdown
# Specification Document Modification Task List

## Modification Background
[Brief description of the reason and background for modification]

## Related Feature Points
- FP-XXX-001: Feature point name
- FP-XXX-002: Feature point name

## Task List

### [Task ID] - [Task Name]
- **Priority**: P0/P1/P2
- **Related Document**: [Document path]
- **Modification Content**: [Detailed description]
- **Status**: pending/in_progress/completed
- **Notes**: [Supplementary notes]
```

### Change Completion Report Template

```markdown
# Specification Document Change Completion Report

## Basic Information
| Item | Content |
|------|---------|
| Change Subject | [Subject name] |
| Change Date | [YYYY-MM-DD] |
| Change Owner | [Owner] |
| Related Requirement | [Requirement ID or description] |

## Completion Status
| Item | Count |
|------|-------|
| Total Tasks | X |
| Completed | Y |
| Completion Rate | Z% |

## Completed Modifications
[List all completed modifications]

## Document Consistency Verification
[Verification result description]

## Affected Feature Points
| Feature Point ID | Feature Point Name | Impact Level | Needs Re-verification |
|----------|-----------|----------|-------------|
| FP-XXX-001 | xxx | High/Medium/Low | Yes/No |

## Follow-up Recommendations
[Improvement suggestions or action items]
```

## Best Practices

1. **Backup Before Modification**: Create document backup before executing modifications
2. **Small Steps, Quick Iterations**: Break large modifications into multiple small tasks, complete one by one
3. **Timely Recording**: Update CHANGELOG immediately after completing each modification
4. **Cross-verification**: Perform consistency check between documents after modification
5. **Stakeholder Confirmation**: Important modifications need stakeholder confirmation before submission

## Notes

1. **Maintain Document Style Consistency**: Follow original document structure and style during modification
2. **Avoid Over-Modification**: Only modify necessary content, do not change unrelated parts
3. **Terminology Consistency**: Ensure consistent terminology usage throughout the document
4. **Link Validity**: Update cross-document reference links
5. **Version Compatibility**: Consider impact of modifications on other versions

## Guardrails

- Modifying specification documents must synchronously update CHANGELOG
- After modification, must notify related feature points for re-verification
- Must maintain consistency between documents
- Must record change impact scope

## Usage Example

```
User: /analyze Need to modify the approval process for transfer application

AI: [Invoking pdd-doc-change skill]
    1. Analyze change requirements ✓
    2. Identify affected feature points: FP-ZCCZ1-001, FP-ZCCZ1-002
    3. Generate modification plan...
    4. Create TODO.md

Change analysis complete!
Affected feature points: 2
Documents to modify:
- dev-specs/FP-ZCCZ1-001/spec.md
- dev-specs/FP-ZCCZ1-002/spec.md

Modification plan generated: dev-specs/变更计划.md
TODO list: dev-specs/TODO.md

Start executing modifications?
```
