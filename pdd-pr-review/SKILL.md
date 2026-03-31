# pdd-pr-review

**Description**: 汇总审查结果，给出建议操作。支持 GitHub 模式和本地模式。

**Details**: 查看 PR 审查结果和建议

**Input**: OpenSpec Change ID 或 PR 编号

## 执行流程

### 1. 获取 PR 状态

```
GitHub 模式:
├── 从 GitHub API 获取 PR 信息
├── 获取 PR 状态、评论、检查结果
└── 获取关联的 Change ID

本地模式:
├── 读取 pr-record.md
├── 解析审查记录
└── 获取 Change ID
```

### 2. 读取审查报告

```
读取: openspec/changes/{change-id}/review-report.md

解析:
├── Blocking 问题数量
├── Warning 问题数量
├── Suggestion 数量
├── 测试覆盖率
└── 各检查项状态
```

### 3. 汇总审查结果

```
统计:
├── Blocking 问题: 0 → ✅ 可合并
├── Warning 问题: ≤3 → ⚠️ 建议修复后合并
└── Warning 问题: >3 → ❌ 建议修复
```

### 4. 生成建议

```
判断逻辑:
├── 无 Blocking + Warning ≤ 3 → 建议: 通过
├── 有 Blocking → 建议: 需修复
└── Warning > 3 → 建议: 建议修复
```

### 5. 输出结果

```
输出:
├── 审查结果汇总表
├── 问题列表（可选详细模式）
├── 建议操作
└── 等待用户决策
```

## 输出格式

### 简洁模式（默认）

```markdown
## PR 审查报告

**PR 编号**: #123
**Change ID**: c-001-xxx
**标题**: feat(workflow): 添加权限控制

### 审查结果汇总

| 级别 | 数量 | 状态 |
|------|------|------|
| 🔴 Blocking | 0 | ✅ |
| 🟡 Warning | 2 | ⚠️ |
| 💡 Suggestion | 3 | ℹ️ |

### 建议操作

**✅ 可以合并** - 无 Blocking 问题，Warning 数量在可接受范围内

### 操作选项

- 确认合并: `/pdd-pr-merge c-001-xxx`
- 修复后重新审查: 修复问题后执行 `/pdd-pr-create c-001-xxx --re-review`
- 查看详细问题: `/pdd-pr-review c-001-xxx --detail`
```

### 详细模式（--detail）

```markdown
## PR 审查报告（详细）

**PR 编号**: #123
**Change ID**: c-001-xxx
**标题**: feat(workflow): 添加权限控制

### 审查结果汇总

| 级别 | 数量 | 状态 |
|------|------|------|
| 🔴 Blocking | 0 | ✅ |
| 🟡 Warning | 2 | ⚠️ |
| 💡 Suggestion | 3 | ℹ️ |

### 🟡 Warning 问题

#### [W-001] 方法参数命名不一致

- **文件**: WorkflowController.java:45
- **描述**: 参数名 `userId` 与其他方法不一致
- **建议**: 统一使用 `user_id` 或 `userId`

#### [W-002] 缺少 JavaDoc 注释

- **文件**: WorkflowService.java:78
- **描述**: 公共方法缺少文档注释
- **建议**: 添加方法功能说明和参数说明

### 💡 Suggestion

#### [S-001] 可优化循环逻辑

- **文件**: WorkflowService.java:102
- **描述**: 可使用 Stream API 简化代码
- **建议**: `list.stream().filter(...).collect(...)`

### 测试覆盖详情

| 模块 | 覆盖率 | 状态 |
|------|--------|------|
| asset-admin | 85% | ✅ |
| asset-system | 72% | ✅ |

### 建议操作

**✅ 可以合并**

### 操作选项

- 确认合并: `/pdd-pr-merge c-001-xxx`
- 修复后重新审查: 修复问题后执行 `/pdd-pr-create c-001-xxx --re-review`
```

## 参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `change_id` | string | 否 | - | OpenSpec Change ID |
| `pr_number` | number | 否 | - | GitHub PR 编号 |
| `detail` | boolean | 否 | false | 是否显示详细问题列表 |

## 错误处理

### PR 不存在

```
❌ PR 不存在

**Change ID**: c-001-xxx

请先创建 PR: `/pdd-pr-create c-001-xxx`
```

### 本地模式无记录

```
❌ 本地 PR 记录不存在

**Change ID**: c-001-xxx

请先创建 PR: `/pdd-pr-create c-001-xxx`
```

## 与其他技能的协作

```
pdd-pr-review
    │
    ├── 被调用方
    │   ├── pdd-pr-create (创建后查看)
    │   └── 用户直接调用
    │
    └── 调用方
        └── pdd-pr-merge (合并前查看)
```

---

## PR管理规范

详见 [pdd-pr-create SKILL.md](./pdd-pr-create/SKILL.md#pr管理规范)

---

## PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。
