---
name: pdd-pr-merge
description: 合并 PR 并触发归档流程。支持 GitHub 模式和本地模式。支持中文触发：合并PR、PR归档、合并请求、归档流程。
author: neuqik@hotmail.com
license: MIT
---

# pdd-pr-merge

**Description**: 合并 PR 并触发归档流程。支持 GitHub 模式和本地模式。

**Details**: 合并 PR 并触发归档

**Input**: OpenSpec Change ID 或 PR 编号

## 执行流程

### 1. 前置检查

```
1. 获取 PR 状态
   ├── GitHub 模式: 从 GitHub API 获取
   └── 本地模式: 从 pr-record.md 获取

2. 确认 PR 状态为 Open
   └── 已合并/已关闭的 PR 无法再次合并

3. 确认无 Blocking 问题
   ├── 有 Blocking → 提示用户修复
   └── force=true → 跳过检查

4. 确认用户有合并权限
   └── 本地模式: 跳过权限检查
```

### 2. 合并 PR

```
GitHub 模式:
├── 执行 GitHub Merge
│   ├── squash=true → Squash and merge
│   └── squash=false → Merge commit
├── 添加合并记录
└── 更新 PR 状态为 merged

本地模式:
├── 切换到 main 分支
├── 合并 Feature Branch
│   ├── squash=true → git merge --squash
│   └── squash=false → git merge
├── 提交合并
└── 更新 pr-record.md 状态
```

### 3. 清理分支

```
GitHub 模式:
├── 删除远程 Feature Branch
└── 删除本地 Feature Branch

本地模式:
└── 删除本地 Feature Branch
```

### 4. 触发归档

```
根据来源触发归档:

OpenSpec Change:
├── 执行 /openspec-archive-change {change-id}
└── 移动到 archive 目录

PDD 功能点:
├── 更新功能点状态为 completed
└── 更新功能点矩阵

批量 PR:
├── 逐个归档所有 Change
└── 更新批量 PR 记录
```

### 5. 推送到远程

```
GitHub 模式:
└── 自动推送（已通过 GitHub API）

本地模式:
├── 不自动推送（等网络通后人工 push）
├── 只提交到本地 Git
└── 提示用户手动推送命令
```

### 6. 生成合并报告

```
输出:
├── 合并摘要
├── 变更统计
├── 归档状态
└── 后续操作
```

## 输出格式

### GitHub 模式

```markdown
## PR 合并完成

**PR 编号**: #123
**Change ID**: c-001-xxx
**合并方式**: Squash
**合并时间**: 2026-03-21 15:30:00

### 合并内容

- 提交数: 3
- 文件变更: 5
- 新增行数: +150
- 删除行数: -20

### 归档状态

- OpenSpec Change: ✅ 已归档
- 归档路径: `openspec/changes/archive/2026-03-21-c-001-xxx/`

### 后续操作

- 查看归档内容: `openspec/changes/archive/2026-03-21-c-001-xxx/`
- 查看主规格: `openspec/specs/workflow-permission-control/spec.md`
```

### 本地模式

```markdown
## PR 合并完成（本地模式）

**Change ID**: c-001-xxx
**分支**: change/c-001-xxx → main
**合并方式**: Squash
**合并时间**: 2026-03-21 15:30:00

### 合并内容

- 文件变更: 5
- 新增行数: +150
- 删除行数: -20

### 归档状态

- OpenSpec Change: ✅ 已归档
- 归档路径: `openspec/changes/archive/2026-03-21-c-001-xxx/`

### ⚠️ 推送提醒

本地模式已合并到本地 main 分支，**未推送到远程**。

网络恢复后请手动推送:
```bash
git push origin main
```

### 后续操作

- 查看归档内容: `openspec/changes/archive/2026-03-21-c-001-xxx/`
```

## 参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `change_id` | string | 否 | - | OpenSpec Change ID |
| `pr_number` | number | 否 | - | GitHub PR 编号 |
| `force` | boolean | 否 | false | 强制合并（忽略 Warning） |
| `squash` | boolean | 否 | true | 是否 Squash 合并 |

## 错误处理

### 有 Blocking 问题

```
❌ 存在 Blocking 问题，无法合并

**Blocking 问题**:
1. [B-001] 单元测试失败
2. [B-002] 测试覆盖率不足

请修复问题后重新审查: `/pdd-pr-create c-001-xxx --re-review`

如需强制合并: `/pdd-pr-merge c-001-xxx --force`
```

### PR 已合并

```
❌ PR 已合并

**PR 编号**: #123
**合并时间**: 2026-03-21 14:00:00

该 PR 已经合并，无需重复操作。
```

### 推送失败（本地模式）

```
⚠️ 推送到远程失败

**错误**: Network error

请手动推送:
```bash
git push origin main
```

推送后确认归档完成。
```

## 与其他技能的协作

```
pdd-pr-merge
    │
    ├── 被调用方
    │   ├── pdd-pr-review (确认后调用)
    │   └── 用户直接调用
    │
    └── 调用方
        └── openspec-archive-change (触发归档)
```

## 合并策略

### Squash Merge（默认）

```
优点:
├── 保持 main 分支历史整洁
├── 每个 Change 对应一个提交
└── 便于回滚整个 Change

缺点:
├── 丢失详细提交历史
└── 不适合多人协作的 Change
```

### Merge Commit

```
优点:
├── 保留完整提交历史
├── 便于追踪每个小改动
└── 适合多人协作

缺点:
├── main 分支历史复杂
└── 回滚需要多个操作
```

---

## PR管理规范

详见 [pdd-pr-create SKILL.md](./pdd-pr-create/SKILL.md#pr管理规范)

### 归档时机

- **归档**: 用户手动触发
- **命令**: `/openspec-archive-change [change-id]`
- **前提条件**:
  - PR已合并
  - 用户确认归档

---

## PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。
