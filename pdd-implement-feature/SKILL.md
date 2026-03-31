---
name: pdd-implement-feature
description: 根据开发规格实现功能点代码。当用户想要开始编码实现时调用此Skill。
license: MIT
compatibility: 需要先完成规格生成
metadata:
  author: asset-platform
  version: "2.0"
  parent: pdd-main
---

功能点实现 - 根据开发规格实现功能点代码

**输入**:
- 开发规格 (spec.md)
- 验收标准 (checklist.md)
- 测试用例 (test-cases.md，可选)

**输出**:
- 代码文件
- 验收报告

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 3.2 | 2026-03-22 | 添加错误处理与回退规范、PDD实施规范引用 |
| 3.1 | 2026-03-22 | 移除自动调用 pdd-pr-* 技能，改为只提示用户手动调用 |
| 3.0 | 2026-03-21 | 新增 PR 管理层集成 (pdd-pr-*) |
| 2.0 | 2026-03-21 | 新增 software-engineer 和 expert-xxx 调用整合 |
| 1.0 | 早期 | 初始版本 |

---

## 1. 技能整合

### 1.1 软件工程师调用

在代码实现过程中，调用 `software-engineer` skill：

| 调用时机 | 服务内容 |
|---------|---------|
| 代码实现 | 依据规格执行代码实现 |
| 单元测试 | 编写单元测试和集成测试 |
| 代码重构 | 遵循编码规范的代码优化 |
| 缺陷修复 | 错误处理和问题修复 |

### 1.2 专家技能调用

在实现过程中遇到技术问题时，按需调用 expert-xxx：

| 专家技能 | 触发条件 | 期望输出 |
|---------|---------|---------|
| **expert-ruoyi** | 若依框架问题 | 解决方案 + 最佳实践 |
| **expert-activiti** | 工作流问题 | BPMN设计建议 |
| **expert-mysql** | 数据库问题 | SQL优化方案 |
| **expert-code-quality** | 代码质量问题 | 重构方案 |

### 1.3 调用条件

**必须调用 software-engineer**：
- 进入代码实现阶段
- 需要编写测试代码

**按需调用 expert-xxx**：
- 遇到若依框架问题
- 遇到数据库设计问题
- 遇到代码质量问题

---

## 2. 流程步骤

### Step 1: 读取开发规格

从 `dev-specs/FP-{序号}/spec.md` 读取：
- 接口定义
- 数据模型
- 业务逻辑
- 测试用例

### Step 2: 读取验收标准

从 `dev-specs/FP-{序号}/checklist.md` 读取验收项。

### Step 3: 确定实现顺序

根据功能点依赖关系确定实现顺序：
- 数据模型 → 数据库脚本
- 后端接口 → Controller/Service/Mapper
- 前端页面 → Vue组件

### Step 4: 生成数据库脚本

根据数据模型生成SQL脚本：
```sql
CREATE TABLE `{table_name}` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  -- 业务字段
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建人',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新人',
  `status` char(1) DEFAULT '0' COMMENT '状态',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{表注释}';
```

### Step 5: 生成后端代码

**调用 software-engineer** 生成符合规范的代码：

**a. Domain实体类**
```java
@Data
@TableName("{table_name}")
public class {EntityName} {
    @TableId(type = IdType.AUTO)
    private Long id;
    // 业务字段
    @TableField(fill = FieldFill.INSERT)
    private Date createTime;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date updateTime;
    // ...
}
```

**b. Mapper接口**
```java
@Mapper
public interface {EntityName}Mapper extends BaseMapper<{EntityName}> {
    // 自定义查询方法
}
```

**c. Service接口和实现**
```java
public interface I{EntityName}Service extends IService<{EntityName}> {
    // 业务方法
}

@Service
public class {EntityName}ServiceImpl extends ServiceImpl<{EntityName}Mapper, {EntityName}> implements I{EntityName}Service {
    // 业务实现
}
```

**d. Controller控制器**
```java
@RestController
@RequestMapping("/{module}")
public class {EntityName}Controller {
    @Autowired
    private I{EntityName}Service service;

    // 接口方法
}
```

### Step 6: 生成前端代码

**调用 software-engineer** 生成前端代码：

**a. API接口**
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

**b. Vue组件**
```vue
<template>
  <!-- 页面模板 -->
</template>

<script>
export default {
  name: '{EntityName}',
  data() {
    return {
      // 数据
    }
  },
  methods: {
    // 方法
  }
}
</script>
```

### Step 7: 实现业务逻辑

根据规格中的业务逻辑实现：
- 处理流程
- 校验规则
- 状态转换
- 异常处理

**专家咨询（按需）**：
- 若依问题 → `expert-ruoyi`
- 数据库问题 → `expert-mysql`

### Step 8: 运行测试验证

如果有测试用例，运行测试验证：
- 单元测试
- 接口测试
- 集成测试

### Step 9: 更新验收状态

更新 `checklist.md` 中的验收状态：
- 业务验收项
- 技术验收项
- 集成验收项

### Step 10: 生成验收报告

输出验收结果：
```markdown
## 验收报告

**功能点**: FP-XXX-NNN
**功能名称**: xxx
**验收日期**: {日期}

### 业务验收
| 序号 | 验收场景 | 预期结果 | 实际结果 | 状态 |
|------|---------|---------|---------|------|
| 1 | xxx | xxx | xxx | ✓/✗ |

### 技术验收
| 序号 | 验收项 | 标准 | 实际 | 状态 |

### 问题记录
- [问题1]: 描述
- [问题2]: 描述

### 结论
- [ ] 通过
- [ ] 不通过，需修改
```

---

## 3. 专家咨询流程

```
pdd-implement-feature 开始
    │
    ├─► 识别若依框架问题
    │       │
    │       ▼
    │   expert-ruoyi 咨询
    │       │
    │       ▼
    │   返回解决方案
    │
    ├─► 识别数据库问题
    │       │
    │       ▼
    │   expert-mysql 咨询
    │       │
    │       ▼
    │   返回优化方案
    │
    ├─► 识别代码质量问题
    │       │
    │       ▼
    │   expert-code-quality 咨询
    │       │
    │       ▼
    │   返回重构建议
    │
    └─► 继续实现
```

### 3.1 expert-ruoyi 调用示例

```
触发条件: 遇到权限校验问题
调用: expert-ruoyi
输入:
  - 问题: @PreAuthorize 注解不生效
  - 代码片段: [相关代码]
  - 错误信息: 权限校验失败

返回:
  - 解决方案
  - 最佳实践
  - sys_menu 配置建议
```

### 3.2 expert-mysql 调用示例

```
触发条件: 遇到查询性能问题
调用: expert-mysql
输入:
  - SQL: SELECT * FROM large_table WHERE ...
  - 表大小: 1000万条
  - 执行计划: [EXPLAIN结果]

返回:
  - 优化方案
  - 索引建议
  - SQL重写
```

---

## 4. 代码规范

### 4.1 后端规范

- 类名使用大驼峰命名
- 方法名使用小驼峰命名
- 常量使用全大写下划线分隔
- 注释使用Javadoc格式

### 4.2 前端规范

- 组件名使用大驼峰命名
- 方法名使用小驼峰命名
- CSS类名使用kebab-case
- 使用ES6+语法

### 4.3 software-engineer 规范

遵循 software-engineer skill 的核心规则：
- 读取现有代码风格后再写新代码
- 错误处理优先
- 保持最小化
- PR-ready 代码

---

## 5. Guardrails

- 代码必须符合项目规范
- 必须实现规格中定义的所有接口
- 必须处理规格中定义的所有异常
- 必须通过所有验收项才能标记完成
- 代码变更后必须同步更新规格文档
- **遇到技术问题必须咨询专家技能**
- **代码实现必须遵循 software-engineer 规范**

---

## 6. 与其他技能协作

| 协作技能 | 协作方式 | 传入数据 | 期望输出 |
|---------|---------|---------|---------|
| **software-engineer** | Delegation | 规格文档 | 符合规范的代码 |
| **expert-ruoyi** | Consultation | 技术问题 | 解决方案 |
| **expert-mysql** | Consultation | SQL问题 | 优化方案 |
| **expert-code-quality** | Consultation | 代码问题 | 重构建议 |
| **pdd-code-reviewer** | Sequential | 代码+规格 | 审查报告 |
| **pdd-pr-create** | Sequential | Change ID | PR + 审查报告 |
| **pdd-pr-merge** | Sequential | Change ID | 合并 + 归档 |

---

## 7. PR 管理层提示

### 7.1 功能点完成后的提示

功能点实现并验证通过后，**提示**用户可以使用 PR 管理技能：

```
## 功能点实现完成

**功能点**: FP-XXX-NNN
**状态**: 验收通过

### 可用的 PR 管理操作

如需创建 PR，可手动调用以下技能：
- `/pdd-pr-create {change-id}` - 创建 PR 并执行自动化审查
- `/pdd-pr-review {change-id}` - 查看 PR 审查结果
- `/pdd-pr-merge {change-id}` - 合并 PR 并归档

### 手动操作步骤

1. 创建 OpenSpec Change（可选）:
   ```
   /openspec-new-change {change-name}
   ```

2. 创建 PR:
   ```
   /pdd-pr-create {change-id}
   ```

3. 确认合并:
   ```
   /pdd-pr-merge {change-id}
   ```
```

### 7.2 不自动调用 PR 技能

**重要原则**：
- PDD 框架 **不会自动调用** pdd-pr-* 技能
- 用户需要 **手动决定** 是否使用 PR 管理功能
- PR 管理技能是 **可选的**，不是必需的

### 7.3 PR 管理技能说明

| 技能 | 功能 | 调用方式 |
|------|------|---------|
| `pdd-pr-create` | 创建 PR 并执行自动化审查 | 用户手动调用 |
| `pdd-pr-review` | 查看 PR 审查结果 | 用户手动调用 |
| `pdd-pr-merge` | 合并 PR 并归档 | 用户手动调用 |
| `pdd-pr-batch` | 批量处理多个 PR | 用户手动调用 |

---

## 8. Guardrails（更新）

- 代码必须符合项目规范
- 必须实现规格中定义的所有接口
- 必须处理规格中定义的所有异常
- 必须通过所有验收项才能标记完成
- 代码变更后必须同步更新规格文档
- **遇到技术问题必须咨询专家技能**
- **代码实现必须遵循 software-engineer 规范**
- **功能点完成后提示用户可使用 PR 管理技能，但不自动调用**

---

## 9. 错误处理与回退规范

### 9.1 错误分级

| 级别 | 定义 | 阻塞性 |
|------|------|--------|
| Critical | 必须修复，阻塞流程 | ✅ 阻塞 |
| Warning | 建议修复，不阻塞 | ❌ 不阻塞 |
| Suggestion | 可选优化 | ❌ 不阻塞 |

### 9.2 重试策略

```yaml
限制: 同一功能点最多3次
计数: 每次修复后重新审查/验证算1次
超过限制: 暂停流程，等待人工决策
```

### 9.3 回退规则

| 失败场景 | 回退位置 | 重新执行 |
|---------|---------|---------|
| pdd-code-reviewer 审查失败 | pdd-implement-feature | 修复后重新审查 |
| pdd-verify-feature 验证失败 | pdd-implement-feature | 修复后重新验证 |

### 9.4 失败记录

- **位置**: `dev-specs/FP-{模块}-{序号}/review-report.md`
- **记录内容**:
  - 失败时间
  - 失败阶段
  - 失败原因
  - 尝试次数
  - 相关错误日志

### 9.5 人工介入流程

```
重试次数超过3次
    │
    ▼
暂停流程
    │
    ▼
生成暂停报告
    ├── 当前状态
    ├── 失败历史
    ├── 已尝试的修复
    └── 需人工决策的问题
    │
    ▼
等待人工决策
    ├── 继续修复
    ├── 跳过当前功能点
    ├── 终止流程
    └── 其他方案
```

---

## 10. PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。

### 核心规范摘要

| 规范 | 核心内容 |
|------|---------|
| **技能边界** | pdd-code-reviewer（合规性）→ expert-code-quality（质量深度） |
| **上下文传递** | 文件系统传递，目录结构规范，支持断点续传 |
| **人工审核** | 批量审核 + 关键功能点详细审核 |
| **错误处理** | Critical阻塞，3次重试后暂停等待人工 |
| **PR管理** | 手动触发，Change粒度PR，手动归档 |
| **文档体系** | 9种核心文档类型，命名规范，文档内变更历史 |
