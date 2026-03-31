---
name: expert-activiti
description: Activiti工作流引擎专家，精通Activiti 7 Core/Cloud架构、BPMN 2.0规范、流程设计与开发。当用户涉及工作流设计、流程引擎开发、BPMN建模、流程部署管理等问题时自动触发。提供BPMN建模、最佳实践和解决方案。
license: MIT
compatibility: Activiti 7.x
metadata:
  author: asset-platform
  version: "2.0"
  triggers:
    - "/activiti" | "/bpmn" | "/workflow"
    - "工作流" | "流程设计" | "BPMN"
    - "流程部署" | "任务管理" | "Activiti"
---

# Activiti工作流引擎专家

## 1. 技能概述

### 1.1 核心能力

```yaml
核心能力:
  - BPMN建模: BPMN 2.0流程设计与规范
  - 流程引擎: Activiti 7 Core/Cloud架构
  - 流程部署: 流程定义、版本管理
  - 任务管理: 用户任务、候选组、代理规则
  - 表达式: UEL表达式、脚本任务

适用场景:
  - 流程设计与建模
  - 流程部署与版本管理
  - 任务查询与办理
  - 流程变量处理
  - 事件与监听器配置
```

### 1.2 与其他技能协作

| 协作技能 | 协作方式 | 传入数据 | 期望输出 |
|---------|---------|---------|---------|
| **pdd-implement-feature** | Consultation | 工作流问题 | 解决方案 |
| **software-architect** | Consultation | 流程架构 | 模块划分建议 |

## 2. BPMN 2.0 核心元素

### 2.1 流程元素分类

```yaml
流程元素:
  启动事件:
    - Start Event: 流程开始
    - Intermediate Event: 流程中间事件
    - End Event: 流程结束

  活动:
    - Task: 用户任务
    - Service Task: 服务任务
    - Script Task: 脚本任务
    - Call Activity: 调用活动
    - Subprocess: 子流程

  网关:
    - Exclusive Gateway: 排他网关
    - Parallel Gateway: 并行网关
    - Inclusive Gateway: 包容网关
    - Event Gateway: 事件网关

  序列流:
    - Sequential Flow: 顺序流
    - Default Flow: 默认流
    - Conditional Flow: 条件流
```

### 2.2 BPMN元素速查表

| 元素 | XML标签 | 说明 |
|------|---------|------|
| 开始事件 | `<startEvent>` | 流程启动点 |
| 结束事件 | `<endEvent>` | 流程结束点 |
| 用户任务 | `<userTask>` | 人工处理 |
| 服务任务 | `<serviceTask>` | 自动处理 |
| 排他网关 | `<exclusiveGateway>` | 选一分支 |
| 并行网关 | `<parallelGateway>` | 并行执行 |
| 顺序流 | `<sequenceFlow>` | 连接元素 |

## 3. 快速诊断模式

### 3.1 流程部署问题

```
问题: 流程部署失败

诊断流程:
1. 检查 BPMN 文件格式
   - 文件后缀: .bpmn20.xml 或 .bpmn
   - XML必须符合BPMN规范

2. 检查流程定义ID
   - 必须唯一
   - 不能使用特殊字符

3. 检查 Start Event
   - 每个流程必须有一个Start Event
   - Start Event不能有多个Outgoing Sequence Flow

4. 检查 Gateway 条件
   - 排他网关必须设置条件
   - 条件表达式必须正确

5. 检查服务任务实现
   - Delegate Expression 指向存在的Bean
   - Class 指向存在的类
```

### 3.2 任务查询问题

```
问题: 用户看不到待办任务

诊断流程:
1. 检查任务候选用户
   - candidateUser 或 candidateGroup
   - 用户是否在候选组中

2. 检查任务 assignee
   - 任务是否已签收
   - 签收用户是否正确

3. 检查流程变量
   - 是否设置了正确的候选人
   - 候选人是否正确存储

4. 检查权限配置
   - 用户是否有任务查看权限
```

## 4. 核心配置规范

### 4.1 流程定义部署

```java
// 方式一: 通过 BPMN 文件部署
@Deployment
@Test
public void deploymentTest() {
    repositoryService.createDeployment()
        .name("转让审批流程")
        .key("transfer-approval")
        .addClasspathResource("processes/TransferApproval.bpmn20.xml")
        .deploy();
}

// 方式二: 通过 ZIP 包部署
@Deployment
public void deploymentZipTest() {
    ZipInputStream zipInputStream = new ZipInputStream(
        this.getClass().getClassLoader().getResourceAsStream("processes/diagrams.zip")
    );
    repositoryService.createDeployment()
        .name("转让审批流程")
        .addZipInputStream(zipInputStream)
        .deploy();
}
```

### 4.2 用户任务配置

```xml
<!-- 用户任务完整配置 -->
<userTask id="approveTask" name="审批任务">
    <!-- 候选用户 -->
    <extensionElements>
        <activiti:potentialOwner>
            <resourceAssignmentExpression>
                <formalExpression>group(manager)</formalExpression>
            </resourceAssignmentExpression>
        </activiti:potentialOwner>
    </extensionElements>

    <!-- 候选用户 (直接指定) -->
    <extensionElements>
        <activiti:candidateUsers>
            <activiti:resourceAssignmentExpression>
                <formalExpression>user1,user2</formalExpression>
            </resourceAssignmentExpression>
        </activiti:candidateUsers>
    </extensionElements>

    <!-- 任务监听器 -->
    <activiti:taskListener event="create" delegateExpression="${taskListenerBean}">
        <activiti:field name="action">
            <activiti:expression>${action}</activiti:expression>
        </activiti:field>
    </activiti:taskListener>
</userTask>
```

### 4.3 网关配置

```xml
<!-- 排他网关 (XOR) -->
<exclusiveGateway id="approvalGateway" name="审批网关" default="defaultFlow">
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
    <!-- 无条件，作为默认路径 -->
</sequenceFlow>

<!-- 并行网关 (AND) -->
<parallelGateway id="parallelGateway" name="并行网关">
    <incoming>flow1</incoming>
    <outgoing>flowA</outgoing>
    <outgoing>flowB</outgoing>
</parallelGateway>

<parallelGateway id="joinGateway" name="汇聚网关">
    <incoming>flowA</incoming>
    <incoming>flowB</incoming>
    <outgoing>flowEnd</outgoing>
</parallelGateway>
```

### 4.4 服务任务配置

```xml
<!-- 方式一: 调用 Bean 方法 -->
<serviceTask id="serviceTask1" name="服务任务"
    activiti:delegateExpression="${myDelegateBean}">
</serviceTask>

<!-- 方式二: 调用 Java 类 -->
<serviceTask id="serviceTask2" name="服务任务"
    activiti:class="com.example.MyDelegate">
</serviceTask>

<!-- 方式三: 表达式 -->
<serviceTask id="serviceTask3" name="服务任务"
    activiti:expression="${orderService.process(order)}">
</serviceTask>

<!-- 方式四: 脚本任务 -->
<scriptTask id="scriptTask" name="脚本任务"
    scriptFormat="javascript">
    <script>
        var order = execution.getVariable("order");
        order.setStatus("PROCESSED");
        execution.setVariable("order", order);
    </script>
</scriptTask>
```

## 5. 常见问题解决方案

### 5.1 流程部署失败

**问题**: BPMN 文件部署失败

**排查步骤**:
```java
// 检查流程定义
ProcessDefinition processDefinition = repositoryService
    .createProcessDefinitionQuery()
    .processDefinitionKey("transfer-approval")
    .latestVersion()
    .singleResult();

// 检查 XML 语法
BpmnModel bpmnModel = new BpmnXMLLoader()
    .loadXML(inputStream);

// 检查资源文件
InputStream resource = runtimeService.getProcessEngine()
    .getRepositoryService()
    .getResourceAsStream(deploymentId, "process.bpmn20.xml");
```

**解决方案**:
1. 确保 BPMN XML 语法正确
2. 检查 Start Event 和 End Event 配置
3. 验证 Gateway 条件表达式
4. 确保服务任务指向存在的 Bean/类

### 5.2 任务查询为空

**问题**: 用户登录后看不到待办任务

**排查步骤**:
```java
// 查询候选任务 (用户所在组)
List<Task> candidateTasks = taskService.createTaskQuery()
    .taskCandidateUser("userId")
    .taskCandidateGroup("groupId")
    .list();

// 查询已签收任务
List<Task> assignedTasks = taskService.createTaskQuery()
    .taskAssignee("userId")
    .list();

// 查询个人任务
List<Task> personalTasks = taskService.createTaskQuery()
    .taskOwner("userId")
    .list();
```

**解决方案**:
1. 确认用户属于正确的候选组
2. 检查任务的 assignee 和 candidateUser
3. 验证流程变量中存储的用户/组信息
4. 使用正确的方式查询任务

### 5.3 流程变量获取失败

**问题**: 在任务监听器中获取流程变量为null

**排查步骤**:
```java
// 在任务监听器中获取变量
public class MyTaskListener implements TaskListener {
    @Override
    public void notify(DelegateTask delegateTask) {
        // 正确方式
        String variable = delegateTask.getVariable("variableName");
        String executionVariable = delegateTask.getExecution().getVariable("variableName");

        // 设置变量
        delegateTask.setVariable("taskVar", "value");
        delegateTask.getExecution().setVariable("executionVar", "value");
    }
}
```

**解决方案**:
1. 确认变量在正确的范围设置 (execution vs task)
2. 检查变量设置的时机
3. 使用 TaskListener 的 DelegateTask 获取变量
4. 使用 Execution 获取流程级别的变量

### 5.4 网关条件不生效

**问题**: 网关条件判断不正确，流程走向错误

**排查步骤**:
```xml
<!-- 检查条件表达式格式 -->
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

**解决方案**:
1. 使用正确的条件表达式语法 `${condition}`
2. 排他网关确保有且只有一个条件为true
3. 设置默认流避免无匹配情况
4. 检查变量类型和值

## 6. 最佳实践清单

### 6.1 BPMN建模规范

```yaml
建模规范:
  - [ ] 每个流程有且只有一个Start Event
  - [ ] 每个流程至少有一个End Event
  - [ ] 用户任务必须配置候选用户或候选组
  - [ ] 排他网关必须设置默认流
  - [ ] 服务任务必须指向存在的实现
  - [ ] 流程Key使用 kebab-case (如: transfer-approval)
  - [ ] 流程ID唯一
```

### 6.2 流程变量命名

```yaml
命名规范:
  - 使用 camelCase: transferAmount
  - 避免使用保留字: processInstanceId, taskId
  - 前缀区分: biz_业务变量, sys_系统变量
  - 示例: biz_transferId, sys_approver
```

### 6.3 异常处理

```java
// 方式一: 边界事件捕获
<boundaryEvent id="errorBoundary" attachedToRef="serviceTask">
    <errorEventDefinition errorCode="SERVICE_ERROR"/>
</boundaryEvent>

// 方式二: 错误结束事件
<endEvent id="errorEnd">
    <errorEventDefinition errorCode="VALIDATION_ERROR"/>
</endEvent>

// 方式三: 异常流程变量
try {
    // 业务逻辑
} catch (Exception e) {
    execution.setVariable("errorMessage", e.getMessage());
    execution.setVariable("errorCode", "BUSINESS_ERROR");
}
```

## 7. Guardrails

### 7.1 必须遵守

- [ ] BPMN文件必须符合BPMN 2.0规范
- [ ] 每个流程必须有Start Event和End Event
- [ ] 排他网关必须设置默认流
- [ ] 用户任务必须配置候选人
- [ ] 服务任务实现类必须存在

### 7.2 避免事项

- ❌ 在用户任务中硬编码候选人
- ❌ 省略End Event
- ❌ 使用复杂的嵌套网关
- ❌ 在流程中存储大量数据

## 8. 本地开发指南

本项目有特定的开发规范和历史经验，请在提供建议时优先参考：

### 8.1 项目规则文件

| 文件 | 路径 | 内容 |
|------|------|------|
| **项目规则** | `.trae/rules/project_rules.md` | 目录结构、命名规范，开发规范 |
| **经验教训** | `.trae/rules/lessons.md` | 历史问题和解决方案 |

### 8.2 本地 Activiti 开发文档

项目在 `Asset-Management-Platform/docs/activiti7/` 目录下有完整的中文开发文档：

| 文档 | 路径 | 内容 |
|------|------|------|
| **Activiti 7 开发指南** | `docs/activiti7/README.md` | 文档索引和概述 |
| **01-概述** | `docs/activiti7/01-概述.md` | Activiti Cloud 概述 |
| **02-快速入门** | `docs/activiti7/02-快速入门.md` | 快速入门指南 |
| **03-组件架构** | `docs/activiti7/03-组件架构.md` | 组件架构说明 |
| **04-BPMN支持** | `docs/activiti7/04-BPMN支持.md` | BPMN 元素支持 |
| **05-常见问题** | `docs/activiti7/05-常见问题.md` | 常见问题解答 |

### 8.3 项目特定检查项

```yaml
项目特定检查项:
  - [ ] 检查 lessons.md 中是否有相关问题的解决方案
  - [ ] 遵循 project_rules.md 中的命名规范
  - [ ] 参考现有代码的实现模式
  - [ ] 确认数据库配置：mysql6.sqlpub.com:3311/asset_ruoyi
```

## 9. 参考文档

### 9.1 本地文档

- [Activiti 7 开发指南](Asset-Management-Platform/docs/activiti7/README.md)
- [后端技术架构](Asset-Management-Platform/docs/architect/02-后端技术架构.md)

### 9.2 外部文档

- [Activiti 7 Developers Guide](https://activiti.gitbook.io/activiti-7-developers-guide)
- [BPMN 2.0 规范](https://www.omg.org/spec/BPMN/2.0/)

## 10. 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 2.1 | 2026-03-22 | 添加本地开发指南和文档引用 |
| 2.0 | 2026-03-21 | 标准化结构，添加诊断模式，增强协作指导 |
| 1.0 | 早期 | 初始版本 |
