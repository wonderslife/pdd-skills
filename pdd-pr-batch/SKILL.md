# pdd-pr-batch

**Description**: 批量合并多个 Change 为一个 PR。适用于多个小改动打包发布的场景。

**Details**: 批量合并多个 Change 为一个 PR

**Input**: 多个 OpenSpec Change ID

## 使用场景

```
适用场景:
├── 多个小修复打包发布
├── 相关功能点一起上线
├── 配置文件批量更新
└── 文档批量更新

不适用场景:
├── Change 之间有依赖冲突
├── 需要独立回滚的 Change
└── 不同优先级的 Change
```

## 执行流程

### 1. 验证所有 Change

```
for each change_id in change_ids:
    ├── 检查 Change 目录存在
    ├── 读取 tasks.md 确认完成
    ├── 检查代码已提交
    └── 记录 Change 信息
```

### 2. 创建批量分支

```
分支命名: batch/{date}

示例: batch/2026-03-21

操作:
├── git checkout main
├── git pull origin main
└── git checkout -b batch/2026-03-21
```

### 3. 合并代码

```
for each change_id in change_ids:
    ├── 找到 Change 对应的 Feature Branch
    ├── cherry-pick 或 merge 该分支的提交
    ├── 解决可能的冲突
    └── 记录合并结果
```

### 4. 批量审查

```
运行所有 Change 的测试:
├── 汇总所有测试用例
├── 批量运行测试
├── 汇总测试覆盖率
└── 生成批量审查报告

审查报告: openspec/batch/{date}/review-report.md
```

### 5. 创建批量 PR

```
GitHub 模式:
├── 推送批量分支到远程
├── 创建 GitHub PR
│   ├── 标题: batch: {title} ({n} changes)
│   ├── 描述: 列出所有 Change
│   └── 标签: batch
└── 记录 PR 编号

本地模式:
├── 创建批量 PR 记录
│   └── openspec/batch/{date}/pr-record.md
└── 记录所有 Change ID
```

### 6. 输出结果

```
输出:
├── PR 编号 / 本地记录路径
├── 包含的 Change 列表
├── 批量审查结果
└── 等待确认
```

## 输出格式

```markdown
## 批量 PR 创建完成

**PR 编号**: #125
**分支**: batch/2026-03-21 → main
**包含变更**: 3 个

### 变更列表

| Change ID | 标题 | 状态 | 审查结果 |
|-----------|------|------|---------|
| c-001-xxx | 权限控制 | ✅ 完成 | ✅ 通过 |
| c-002-yyy | 日志记录 | ✅ 完成 | ⚠️ 1 Warning |
| c-003-zzz | 参数校验 | ✅ 完成 | ✅ 通过 |

### 批量审查结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 单元测试 | ✅ 通过 | 45/45 用例通过 |
| 测试覆盖率 | ✅ 82% | 阈值: 70% |
| 代码质量 | ⚠️ 3 Warning | 详情见报告 |
| 冲突检查 | ✅ 无冲突 | - |

### 审查报告

详细报告: `openspec/batch/2026-03-21/review-report.md`

### 下一步操作

- 确认合并: `/pdd-pr-merge --pr-number 125`
- 查看详情: `/pdd-pr-review --pr-number 125`
- 单独处理某个 Change: `/pdd-pr-review c-001-xxx`
```

## 参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `change_ids` | array | 是 | - | OpenSpec Change ID 列表 |
| `title` | string | 否 | - | PR 标题 |
| `draft` | boolean | 否 | true | 是否创建为 Draft PR |

## 冲突处理

### 检测到冲突

```
⚠️ 检测到代码冲突

**冲突文件**:
- src/main/java/WorkflowController.java

**冲突 Change**:
- c-001-xxx: 修改了第 45 行
- c-002-yyy: 修改了第 45 行

### 解决方案

1. 手动解决冲突:
   - 编辑冲突文件
   - git add .
   - git commit

2. 跳过冲突 Change:
   - `/pdd-pr-batch c-001-xxx,c-003-zzz` (排除 c-002-yyy)

3. 分开处理:
   - 先合并 c-001-xxx
   - 再合并 c-002-yyy
```

## 批量归档

合并批量 PR 后，会逐个归档所有 Change：

```
pdd-pr-merge (批量 PR)
    │
    └── for each change_id:
            │
            ├── openspec-archive-change {change-id}
            │
            └── 更新 Change 状态
```

### 批量归档输出

```markdown
## 批量 PR 合并完成

**PR 编号**: #125
**合并时间**: 2026-03-21 16:00:00

### 归档状态

| Change ID | 归档状态 | 归档路径 |
|-----------|---------|---------|
| c-001-xxx | ✅ 已归档 | archive/2026-03-21-c-001-xxx/ |
| c-002-yyy | ✅ 已归档 | archive/2026-03-21-c-002-yyy/ |
| c-003-zzz | ✅ 已归档 | archive/2026-03-21-c-003-zzz/ |

### 后续操作

- 查看批量归档: `openspec/batch/2026-03-21/`
```

## 目录结构

```
openspec/
├── changes/
│   ├── c-001-xxx/
│   ├── c-002-yyy/
│   └── c-003-zzz/
├── batch/
│   └── 2026-03-21/
│       ├── pr-record.md
│       ├── review-report.md
│       └── merge-report.md
└── archive/
    ├── 2026-03-21-c-001-xxx/
    ├── 2026-03-21-c-002-yyy/
    └── 2026-03-21-c-003-zzz/
```

## 错误处理

### 有未完成的 Change

```
❌ 部分 Change 未完成

**未完成列表**:
- c-002-yyy: 2/10 任务未完成

请先完成所有 Change 后再执行批量操作。
```

### Change 不存在

```
❌ Change 不存在

**无效 ID**: c-004-xxx

请确认 Change ID 正确:
- c-001-xxx ✅
- c-002-yyy ✅
- c-003-zzz ✅
- c-004-xxx ❌ 不存在
```

## 与其他技能的协作

```
pdd-pr-batch
    │
    ├── 被调用方
    │   └── 用户直接调用
    │
    └── 调用方
        ├── pdd-pr-review (查看批量审查)
        └── pdd-pr-merge (批量合并)
```

## 最佳实践

### 推荐批量场景

1. **同类型修复**: 多个 Bug 修复一起发布
2. **配置更新**: 多个配置文件修改
3. **文档更新**: 多个文档修改
4. **依赖升级**: 多个依赖版本更新

### 不推荐批量场景

1. **跨模块修改**: 可能影响其他模块
2. **紧急修复**: 应该单独快速发布
3. **大改动**: 应该独立审查和回滚

---

## PR管理规范

详见 [pdd-pr-create SKILL.md](./pdd-pr-create/SKILL.md#pr管理规范)

---

## PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。
