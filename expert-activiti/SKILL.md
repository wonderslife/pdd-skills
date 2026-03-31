---
name: expert-activiti
description: Activiti workflow engine expert, proficient in Activiti 7 Core/Cloud architecture, BPMN 2.0 specification, process design and development. Automatically triggered when users involve workflow design, process engine development, BPMN modeling, process deployment management and other issues. Provides BPMN modeling, best practices and solutions. 支持中文触发：工作流设计、流程引擎开发、BPMN建模、流程部署管理、Activiti、工作流、流程设计。
license: MIT
compatibility: Activiti 7.x
metadata:
  author: neuqik@hotmail.com
  version: "2.0"
  triggers:
    - "/activiti" | "/bpmn" | "/workflow"
    - "workflow" | "process design" | "BPMN"
    - "process deployment" | "task management" | "Activiti"
---

# Activiti Workflow Engine Expert

## 1. Skill Overview

### 1.1 Core Capabilities

```yaml
Core Capabilities:
  - BPMN Modeling: BPMN 2.0 process design and specification
  - Process Engine: Activiti 7 Core/Cloud architecture
  - Process Deployment: Process definition, version management
  - Task Management: User tasks, candidate groups, delegation rules
  - Expressions: UEL expressions, script tasks

Applicable Scenarios:
  - Process design and modeling
  - Process deployment and version management
  - Task query and processing
  - Process variable handling
  - Event and listener configuration
```

### 1.2 Collaboration with Other Skills

| Collaborating Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **pdd-implement-feature** | Consultation | Workflow issues | Solutions |
| **software-architect** | Consultation | Process architecture | Module division suggestions |

## 2. BPMN 2.0 Core Elements

### 2.1 Process Element Classification

```yaml
Process Elements:
  Start Events:
    - Start Event: Process start
    - Intermediate Event: Process intermediate event
    - End Event: Process end

  Activities:
    - Task: User task
    - Service Task: Service task
    - Script Task: Script task
    - Call Activity: Call activity
    - Subprocess: Subprocess

  Gateways:
    - Exclusive Gateway: Exclusive gateway
    - Parallel Gateway: Parallel gateway
    - Inclusive Gateway: Inclusive gateway
    - Event Gateway: Event gateway

  Sequence Flows:
    - Sequential Flow: Sequence flow
    - Default Flow: Default flow
    - Conditional Flow: Conditional flow
```

### 2.2 BPMN Element Quick Reference

| Element | XML Tag | Description |
|------|---------|------|
| Start Event | `<startEvent>` | Process start point |
| End Event | `<endEvent>` | Process end point |
| User Task | `<userTask>` | Manual processing |
| Service Task | `<serviceTask>` | Automatic processing |
| Exclusive Gateway | `<exclusiveGateway>` | Choose one branch |
| Parallel Gateway | `<parallelGateway>` | Parallel execution |
| Sequence Flow | `<sequenceFlow>` | Connection element |

## 3. Quick Diagnosis Mode

### 3.1 Process Deployment Issues

```
Issue: Process deployment failed

Diagnosis Process:
1. Check BPMN file format
   - File extension: .bpmn20.xml or .bpmn
   - XML must conform to BPMN specification

2. Check process definition ID
   - Must be unique
   - Cannot use special characters

3. Check Start Event
   - Each process must have one Start Event
   - Start Event cannot have multiple Outgoing Sequence Flows

4. Check Gateway conditions
   - Exclusive gateway must set conditions
   - Condition expressions must be correct

5. Check service task implementation
   - Delegate Expression points to existing Bean
   - Class points to existing class
```

### 3.2 Task Query Issues

```
Issue: User cannot see pending tasks

Diagnosis Process:
1. Check task candidate users
   - candidateUser or candidateGroup
   - Whether user is in candidate group

2. Check task assignee
   - Whether task has been claimed
   - Whether claiming user is correct

3. Check process variables
   - Whether correct candidates are set
   - Whether candidates are stored correctly

4. Check permission configuration
   - Whether user has task view permission
```

## 4. Core Configuration Specifications

### 4.1 Process Definition Deployment

```java
// Method 1: Deploy via BPMN file
@Deployment
@Test
public void deploymentTest() {
    repositoryService.createDeployment()
        .name("Transfer Approval Process")
        .key("transfer-approval")
        .addClasspathResource("processes/TransferApproval.bpmn20.xml")
        .deploy();
}

// Method 2: Deploy via ZIP package
@Deployment
public void deploymentZipTest() {
    ZipInputStream zipInputStream = new ZipInputStream(
        this.getClass().getClassLoader().getResourceAsStream("processes/diagrams.zip")
    );
    repositoryService.createDeployment()
        .name("Transfer Approval Process")
        .addZipInputStream(zipInputStream)
        .deploy();
}
```

### 4.2 User Task Configuration

```xml
<!-- User task complete configuration -->
<userTask id="approveTask" name="Approval Task">
    <!-- Candidate users -->
    <extensionElements>
        <activiti:potentialOwner>
            <resourceAssignmentExpression>
                <formalExpression>group(manager)</formalExpression>
            </resourceAssignmentExpression>
        </activiti:potentialOwner>
    </extensionElements>

    <!-- Candidate users (direct specification) -->
    <extensionElements>
        <activiti:candidateUsers>
            <activiti:resourceAssignmentExpression>
                <formalExpression>user1,user2</formalExpression>
            </activiti:resourceAssignmentExpression>
        </activiti:candidateUsers>
    </extensionElements>

    <!-- Task listener -->
    <activiti:taskListener event="create" delegateExpression="${taskListenerBean}">
        <activiti:field name="action">
            <activiti:expression>${action}</activiti:expression>
        </activiti:field>
    </activiti:taskListener>
</userTask>
```

### 4.3 Gateway Configuration

```xml
<!-- Exclusive Gateway (XOR) -->
<exclusiveGateway id="approvalGateway" name="Approval Gateway" default="defaultFlow">
    <incoming>flow1</incoming>
    <outgoing>flowApproved</outgoing>
    <outgoing>flowRejected</outgoing>
    <outgoing>defaultFlow</outgoing>
</exclusiveGateway>

<sequenceFlow id="flowApproved" sourceRef="approvalGateway" targetRef="approvedTask">
    <conditionExpression xsi:type="tFormalExpression">
        ${approved == true}
    </conditionExpression>
</sequenceFlow>

<sequenceFlow id="flowRejected" sourceRef="approvalGateway" targetRef="rejectedTask">
    <conditionExpression xsi:type="tFormalExpression">
        ${approved == false}
    </conditionExpression>
</sequenceFlow>

<sequenceFlow id="defaultFlow" sourceRef="approvalGateway" targetRef="defaultTask">
    <!-- No condition, as default path -->
</sequenceFlow>

<!-- Parallel Gateway (AND) -->
<parallelGateway id="parallelGateway" name="Parallel Gateway">
    <incoming>flow1</incoming>
    <outgoing>flowA</outgoing>
    <outgoing>flowB</outgoing>
</parallelGateway>

<parallelGateway id="joinGateway" name="Join Gateway">
    <incoming>flowA</incoming>
    <incoming>flowB</incoming>
    <outgoing>flowEnd</outgoing>
</parallelGateway>
```

### 4.4 Service Task Configuration

```xml
<!-- Method 1: Call Bean method -->
<serviceTask id="serviceTask1" name="Service Task"
    activiti:delegateExpression="${myDelegateBean}">
</serviceTask>

<!-- Method 2: Call Java class -->
<serviceTask id="serviceTask2" name="Service Task"
    activiti:class="com.example.MyDelegate">
</serviceTask>

<!-- Method 3: Expression -->
<serviceTask id="serviceTask3" name="Service Task"
    activiti:expression="${orderService.process(order)}">
</serviceTask>

<!-- Method 4: Script task -->
<scriptTask id="scriptTask" name="Script Task"
    scriptFormat="javascript">
    <script>
        var order = execution.getVariable("order");
        order.setStatus("PROCESSED");
        execution.setVariable("order", order);
    </script>
</scriptTask>
```

## 5. Common Problem Solutions

### 5.1 Process Deployment Failure

**Issue**: BPMN file deployment failed

**Troubleshooting Steps**:
```java
// Check process definition
ProcessDefinition processDefinition = repositoryService
    .createProcessDefinitionQuery()
    .processDefinitionKey("transfer-approval")
    .latestVersion()
    .singleResult();

// Check XML syntax
BpmnModel bpmnModel = new BpmnXMLLoader()
    .loadXML(inputStream);

// Check resource files
InputStream resource = runtimeService.getProcessEngine()
    .getRepositoryService()
    .getResourceAsStream(deploymentId, "process.bpmn20.xml");
```

**Solutions**:
1. Ensure BPMN XML syntax is correct
2. Check Start Event and End Event configuration
3. Verify Gateway condition expressions
4. Ensure service tasks point to existing Beans/classes

### 5.2 Task Query Returns Empty

**Issue**: User cannot see pending tasks after login

**Troubleshooting Steps**:
```java
// Query candidate tasks (user's group)
List<Task> candidateTasks = taskService.createTaskQuery()
    .taskCandidateUser("userId")
    .taskCandidateGroup("groupId")
    .list();

// Query claimed tasks
List<Task> assignedTasks = taskService.createTaskQuery()
    .taskAssignee("userId")
    .list();

// Query personal tasks
List<Task> personalTasks = taskService.createTaskQuery()
    .taskOwner("userId")
    .list();
```

**Solutions**:
1. Confirm user belongs to correct candidate group
2. Check task assignee and candidateUser
3. Verify user/group information stored in process variables
4. Use correct method to query tasks

### 5.3 Process Variable Retrieval Failure

**Issue**: Getting null for process variables in task listener

**Troubleshooting Steps**:
```java
// Get variables in task listener
public class MyTaskListener implements TaskListener {
    @Override
    public void notify(DelegateTask delegateTask) {
        // Correct way
        String variable = delegateTask.getVariable("variableName");
        String executionVariable = delegateTask.getExecution().getVariable("variableName");

        // Set variables
        delegateTask.setVariable("taskVar", "value");
        delegateTask.getExecution().setVariable("executionVar", "value");
    }
}
```

**Solutions**:
1. Confirm variables are set in correct scope (execution vs task)
2. Check timing of variable setting
3. Use TaskListener's DelegateTask to get variables
4. Use Execution to get process-level variables

### 5.4 Gateway Conditions Not Working

**Issue**: Gateway condition judgment incorrect, process flow wrong

**Troubleshooting Steps**:
```xml
<!-- Check condition expression format -->
<sequenceFlow id="flow1" sourceRef="gateway" targetRef="task1">
    <conditionExpression xsi:type="tFormalExpression">
        ${amount > 1000}
    </conditionExpression>
</sequenceFlow>

<sequenceFlow id="flow2" sourceRef="gateway" targetRef="task2">
    <conditionExpression xsi:type="tFormalExpression">
        ${amount <= 1000}
    </conditionExpression>
</sequenceFlow>
```

**Solutions**:
1. Use correct condition expression syntax `${condition}`
2. Ensure exclusive gateway has exactly one condition that evaluates to true
3. Set default flow to avoid no-match situations
4. Check variable types and values

## 6. Best Practices Checklist

### 6.1 BPMN Modeling Standards

```yaml
Modeling Standards:
  - [ ] Each process has exactly one Start Event
  - [ ] Each process has at least one End Event
  - [ ] User tasks must configure candidate users or candidate groups
  - [ ] Exclusive gateways must set default flow
  - [ ] Service tasks must point to existing implementations
  - [ ] Process Key uses kebab-case (e.g., transfer-approval)
  - [ ] Process ID is unique
```

### 6.2 Process Variable Naming

```yaml
Naming Conventions:
  - Use camelCase: transferAmount
  - Avoid reserved words: processInstanceId, taskId
  - Prefix distinction: biz_ for business variables, sys_ for system variables
  - Examples: biz_transferId, sys_approver
```

### 6.3 Exception Handling

```java
// Method 1: Boundary event capture
<boundaryEvent id="errorBoundary" attachedToRef="serviceTask">
    <errorEventDefinition errorCode="SERVICE_ERROR"/>
</boundaryEvent>

// Method 2: Error end event
<endEvent id="errorEnd">
    <errorEventDefinition errorCode="VALIDATION_ERROR"/>
</endEvent>

// Method 3: Exception process variables
try {
    // Business logic
} catch (Exception e) {
    execution.setVariable("errorMessage", e.getMessage());
    execution.setVariable("errorCode", "BUSINESS_ERROR");
}
```

## 7. Guardrails

### 7.1 Must Follow

- [ ] BPMN files must conform to BPMN 2.0 specification
- [ ] Each process must have Start Event and End Event
- [ ] Exclusive gateways must set default flow
- [ ] User tasks must configure candidates
- [ ] Service task implementation classes must exist

### 7.2 Avoid

- ❌ Hardcoding candidates in user tasks
- ❌ Omitting End Event
- ❌ Using complex nested gateways
- ❌ Storing large amounts of data in processes

## 8. Local Development Guide

This project has specific development standards and historical experience, please refer to them first when providing suggestions:

### 8.1 Project Rule Files

| File | Path | Content |
|------|------|------|
| **Project Rules** | `.trae/rules/project_rules.md` | Directory structure, naming conventions, development standards |
| **Lessons Learned** | `.trae/rules/lessons.md` | Historical issues and solutions |

### 8.2 Local Activiti Development Documentation

The project has complete Chinese development documentation in the `Asset-Management-Platform/docs/activiti7/` directory:

| Document | Path | Content |
|------|------|------|
| **Activiti 7 Development Guide** | `docs/activiti7/README.md` | Documentation index and overview |
| **01-Overview** | `docs/activiti7/01-Overview.md` | Activiti Cloud overview |
| **02-Quick Start** | `docs/activiti7/02-Quick-Start.md` | Quick start guide |
| **03-Component Architecture** | `docs/activiti7/03-Component-Architecture.md` | Component architecture description |
| **04-BPMN Support** | `docs/activiti7/04-BPMN-Support.md` | BPMN element support |
| **05-FAQ** | `docs/activiti7/05-FAQ.md` | Frequently asked questions |

### 8.3 Project-Specific Checklist

```yaml
Project-Specific Checklist:
  - [ ] Check if lessons.md has solutions for related issues
  - [ ] Follow naming conventions in project_rules.md
  - [ ] Reference implementation patterns from existing code
  - [ ] Confirm database configuration: mysql6.sqlpub.com:3311/asset_ruoyi
```

## 9. Reference Documentation

### 9.1 Local Documentation

- [Activiti 7 Development Guide](Asset-Management-Platform/docs/activiti7/README.md)
- [Backend Technical Architecture](Asset-Management-Platform/docs/architect/02-Backend-Technical-Architecture.md)

### 9.2 External Documentation

- [Activiti 7 Developers Guide](https://activiti.gitbook.io/activiti-7-developers-guide)
- [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/)

## 10. Version History

| Version | Date | Changes |
|-----|------|---------|
| 2.1 | 2026-03-22 | Added local development guide and documentation references |
| 2.0 | 2026-03-21 | Standardized structure, added diagnosis mode, enhanced collaboration guidance |
| 1.0 | Early | Initial version |
