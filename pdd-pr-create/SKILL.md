# pdd-pr-create

**Description**: 创建 PR 并执行自动化审查。支持 GitHub 模式和本地模式（GitHub 不可访问时自动降级）。

**Details**: 创建 PR 并执行自动化审查

**Input**: OpenSpec Change ID 或功能点 ID

## 执行流程

### 1. 模式检测

```
启动时检测:
├── 尝试连接 GitHub API (gh auth status)
├── 成功 → GitHub 模式
└── 失败 → 本地模式（提示用户）
```

### 2. 准备阶段

```
1. 解析参数
   ├── 获取 change_id
   └── 确认 Change 目录存在

2. 检查 Change 状态
   ├── 读取 tasks.md
   ├── 确认所有任务已完成
   └── 如有未完成任务，提示用户

3. 检查当前分支状态
   ├── 确认在正确的分支
   ├── 确认所有代码已提交
   └── 如有未提交代码，提示用户
```

### 3. 分支管理

```
GitHub 模式:
├── 创建 Feature Branch: change/{change-id}
├── 推送到远程仓库
└── 创建 GitHub PR (Draft)

本地模式:
├── 创建 Feature Branch: change/{change-id}
├── 记录分支信息到 pr-record.md
└── 不推送（等待用户手动推送）
```

### 4. 自动化审查

```
1. 运行单元测试
   ├── Java: mvn test -pl {module}
   ├── Node.js: npm test
   └── 记录测试结果

2. 检查测试覆盖率
   ├── Java: JaCoCo report
   ├── Node.js: Jest coverage
   └── 与阈值比较

3. 运行代码质量检查
   ├── Java: SonarQube / SpotBugs
   ├── Node.js: ESLint
   └── 记录问题列表

4. 检查文档完整性
   ├── 确认 spec.md 存在
   ├── 确认 tasks.md 已更新
   └── 记录检查结果

5. 安全扫描（可选）
   └── 检查敏感信息泄露
```

### 5. 生成审查报告

```
创建: openspec/changes/{change-id}/review-report.md

内容:
├── 审查摘要
├── Blocking 问题列表
├── Warning 问题列表
├── Suggestion 列表
├── 测试覆盖详情
└── 建议操作
```

### 6. 创建 PR 记录

```
GitHub 模式:
├── 创建 GitHub PR
├── 设置标题: feat(xxx): {change-name}
├── 设置描述: 包含 Change 链接、审查摘要
└── 添加标签: change-id, priority

本地模式:
├── 创建 pr-record.md
├── 记录分支信息
├── 记录审查结果
└── 记录创建时间
```

### 7. 输出结果

```
输出摘要:
├── PR 编号 / 本地记录路径
├── 分支信息
├── 审查结果摘要表
├── 审查报告路径
└── 下一步操作提示
```

## 输出格式

### GitHub 模式

```markdown
## PR 创建完成

**PR 编号**: #123
**分支**: change/c-001-xxx → main
**状态**: Draft

### 自动化审查结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 单元测试 | ✅ 通过 | 15/15 用例通过 |
| 测试覆盖率 | ✅ 85% | 阈值: 70% |
| 代码质量 | ⚠️ 2 Warning | 详情见报告 |
| 安全扫描 | ✅ 通过 | 无漏洞 |
| 文档完整性 | ✅ 通过 | spec.md 已更新 |

### 审查报告

详细报告: `openspec/changes/c-001-xxx/review-report.md`

### 下一步操作

- 确认通过: `/pdd-pr-merge c-001-xxx`
- 查看详情: `/pdd-pr-review c-001-xxx`
- 修复问题后重新审查: `/pdd-pr-create c-001-xxx --re-review`
```

### 本地模式

```markdown
## PR 创建完成（本地模式）

⚠️ GitHub 不可访问，已切换到本地模式

**Change ID**: c-001-xxx
**分支**: change/c-001-xxx → main
**状态**: 等待审查

### 自动化审查结果

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 单元测试 | ✅ 通过 | 15/15 用例通过 |
| 测试覆盖率 | ✅ 85% | 阈值: 70% |
| 代码质量 | ⚠️ 2 Warning | 详情见报告 |

### PR 记录

已创建: `openspec/changes/c-001-xxx/pr-record.md`

### 下一步操作

- 确认合并: `/pdd-pr-merge c-001-xxx`
- 查看详情: `/pdd-pr-review c-001-xxx`
- 网络恢复后推送: `git push origin change/c-001-xxx`
```

## 参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `change_id` | string | 是 | - | OpenSpec Change ID |
| `draft` | boolean | 否 | true | 是否创建为 Draft PR |
| `coverage_threshold` | number | 否 | 70 | 测试覆盖率阈值 |
| `re_review` | boolean | 否 | false | 是否重新审查 |

## 审查检查项

### 🔴 Blocking（必须通过）

| 检查项 | 描述 | 失败条件 |
|--------|------|---------|
| `unit_test` | 单元测试通过 | 有测试失败 |
| `coverage` | 测试覆盖率达标 | 覆盖率 < 阈值 |
| `critical_issues` | 无 Critical 问题 | 有 Critical 问题 |
| `build` | 构建成功 | 构建失败 |

### 🟡 Warning（警告）

| 检查项 | 描述 | 触发条件 |
|--------|------|---------|
| `lint` | 代码风格 | 有 lint 问题 |
| `documentation` | 文档完整性 | spec.md 未更新 |
| `coverage_warning` | 覆盖率警告 | 覆盖率 < 90% 但 ≥ 70% |

### 💡 Suggestion（建议）

| 检查项 | 描述 |
|--------|------|
| `optimization` | 可优化的代码模式 |
| `performance` | 潜在的性能问题 |
| `naming` | 更好的命名建议 |

## 错误处理

### Change 未完成

```
❌ Change 任务未完成

**Change ID**: c-001-xxx
**未完成任务**: 2/10

请先完成所有任务:
- [ ] 4.1 Code Review
- [ ] 5.1 运行单元测试

完成后再执行 `/pdd-pr-create c-001-xxx`
```

### 有未提交代码

```
❌ 有未提交的代码变更

**文件**:
- src/main/java/Example.java (modified)
- src/test/java/ExampleTest.java (new)

请先提交代码:
git add .
git commit -m "feat: xxx"

然后再执行 `/pdd-pr-create c-001-xxx`
```

### 有 Blocking 问题

```
❌ 存在 Blocking 问题，无法创建 PR

**Blocking 问题**:
1. [B-001] 单元测试失败: testAddMethod
2. [B-002] 测试覆盖率不足: 45% < 70%

请修复这些问题后重新执行 `/pdd-pr-create c-001-xxx`
```

## 与其他技能的协作

```
pdd-pr-create
    │
    ├── 被调用方
    │   ├── openspec-apply-change (完成后可选调用)
    │   ├── pdd-implement-feature (每个功能点完成后调用)
    │   └── 用户直接调用
    │
    └── 调用方
        ├── pdd-pr-review (查看审查结果)
        └── pdd-pr-merge (合并 PR)
```

---

## PR管理规范

### 触发时机

- **创建PR**: 用户手动触发
- **命令**: `/pdd-pr-create [change-id]`
- **前提条件**:
  - 模块所有功能点验证通过
  - 质量改进任务已处理（如有）

### PR粒度

- **标准**: 一个Change一个PR
- **Change定义**:
  - 功能点的逻辑分组
  - 通常对应一个完整的业务功能
  - 包含相关的前后端代码、SQL、配置等

### 归档时机

- **归档**: 用户手动触发
- **命令**: `/openspec-archive-change [change-id]`
- **前提条件**:
  - PR已合并
  - 用户确认归档

---

## PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。

---

## 配置

```yaml
# .trae/config/pr-config.yaml
pr:
  coverage_threshold: 70
  warning_threshold: 3
  
  blocking_checks:
    - unit_test
    - coverage
    - critical_issues
    - build
  
  warning_checks:
    - lint
    - documentation
    - coverage_warning
```
