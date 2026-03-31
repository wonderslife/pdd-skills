---
name: pdd-main
description: PRD驱动开发的主入口Skill，协调整个开发流程。当用户想要基于PRD文档进行功能开发时调用此Skill。
license: MIT
compatibility: 需要完整的PRD文档体系
metadata:
  author: asset-platform
  version: "3.2"
---

# PDD-MAIN - PRD驱动开发主入口

**核心理念**: PDD (PRD-Driven Development) 是一种结合领域专家能力的开发方法论，通过整合 system-architect、software-architect、software-engineer 以及 expert-xxx 等专业技能，实现从需求分析到最终交付的全面智能化。

**输入**: PRD文档目录路径

**输出**: 完成的功能点代码和验收报告

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 3.4 | 2026-03-22 | 添加PDD实施规范引用，更新技能协作流程 |
| 3.3 | 2026-03-21 | 修正代码目录生成规则：新业务功能创建独立Maven模块，不放asset-system |
| 3.2 | 2026-03-21 | 添加代码目录自动生成能力（模块编号→代码路径映射） |
| 3.1 | 2026-03-21 | 添加智能PRD发现能力（模块编号自动发现+手动指定文档） |
| 3.0 | 2026-03-21 | 整合 system-architect、software-architect、software-engineer 技能 |
| 2.0 | 2026-03-08 | 完善四阶段流程，增强验证机制 |
| 1.0 | 早期 | 初始版本 |

---

## 1. 方法论架构

### 1.1 PDD 技能体系

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDD-MAIN (主入口)                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │  流程编排   │  状态管理   │  上下文传递 │  结果汇总   │      │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   PDD流程层   │     │   架构师层   │     │   工程师层   │
├───────────────┤     ├───────────────┤     ├───────────────┤
│ pdd-ba        │     │system-architect│     │software-eng  │
│ pdd-extract   │◄───►│              │◄───►│              │
│ pdd-generate  │     │software-arch  │     │ expert-xxx   │
│ pdd-implement │     │              │     │              │
│ pdd-review    │     │              │     │              │
│ pdd-verify    │     │              │     │              │
└───────────────┘     └───────────────┘     └───────────────┘
```

### 1.2 技能分类与职责

| 类别 | 技能名称 | 核心职责 | 能力边界 |
|------|---------|---------|---------|
| **主入口** | pdd-main | 流程编排、状态管理、上下文传递 | 不直接实现代码 |
| **PDD流程** | pdd-ba, pdd-extract-features, pdd-generate-spec, pdd-implement-feature, pdd-code-reviewer, pdd-verify-feature | 业务分析、规格生成、代码实现、审查验证 | 各自负责特定阶段 |
| **架构师** | system-architect | 系统架构设计、技术选型 | 高层次设计、架构决策 |
| | software-architect | 软件架构设计、模块划分 | 模块设计、接口规范 |
| **工程师** | software-engineer | 代码实现、测试编写 | 依据规格执行实现 |
| **专家** | expert-ruoyi | 若依框架专属问题 | 框架配置、代码生成 |
| | expert-activiti | Activiti工作流引擎 | BPMN设计、流程部署 |
| | expert-mysql | MySQL数据库优化 | SQL优化、索引设计 |
| | expert-code-quality | 代码质量与重构 | 异味检测、设计模式 |

---

## 2. 完整流程

### 2.1 六阶段流程

```
阶段一：业务分析与功能点提取
  PRD文档 → 5W1H分析 → 用例图 → 流程图 → 状态图 → 功能点矩阵

阶段二：开发规格生成
  功能点矩阵 → 架构咨询 → 接口设计 → 数据模型 → 开发规格 + 验收标准

阶段三：功能点循环
  对每个功能点：实现 → 审查 → 修复 → 验收

阶段四：架构评审整合
  按需调用 system-architect / software-architect

阶段五：专家技能整合
  按需调用 expert-xxx

阶段六：交付与复盘
  开发报告 → 文档归档 → 经验教训
```

### 2.2 详细流程步骤

#### Step 1: 解析输入并发现PRD文档

**支持两种输入模式**：

**模式A：模块编号自动发现**
- 用户输入模块编号（如 `ZCCZ-2`、`ZCCZ-1`）
- 自动扫描 `docs/业务分析/` 目录
- 匹配目录名（如 `ZCCZ-2-资产转让`）
- 自动聚合该目录下所有设计文档

**模式B：手动指定文档**
- 用户直接指定一个或多个设计文档路径
- 支持单个文件：`docs/xxx/ZCCZ-2/PRD-资产转让.md`
- 支持多个文件：用逗号或换行分隔
- 支持目录路径：自动发现目录下所有.md文档

**标准PRD文档结构**：
```
docs/业务分析/{业务领域}/
├── PRD-{模块名称}.md              # 需求文档
├── 用例图-{模块名称}.md           # 用例图
├── 业务流程图-{模块名称}.md       # 流程图
├── 状态图-{模块名称}.md           # 状态图
├── 序列图-{模块名称}.md           # 序列图（可选）
└── 表单设计/                      # 表单设计文档（可选）
```

**自动发现流程**：
```
用户输入: "ZCCZ-2"
    ↓
扫描 docs/业务分析/*/ZCCZ-2*/
    ↓
匹配到: docs/业务分析/资产处置/ZCCZ-2-资产转让/
    ↓
聚合文档:
  - PRD-资产转让.md
  - 用例图-资产转让.md
  - 业务流程图-资产转让.md
  - 状态图-资产转让.md
  - 序列图-资产转让流程.md
    ↓
确认文档完整性
```

#### Step 2: 确认模块信息

从PRD文档中提取模块编号和名称：
- 模块编号: ZCCZ-1, ZCCZ-2, ...
- 模块名称: 国有产权转让, 资产转让, ...

#### Step 3: 识别技术栈

分析项目技术栈，确定需要调用的技能：
- 若依框架项目 → software-engineer + expert-ruoyi
- 工作流项目 → expert-activiti
- 数据库密集型 → expert-mysql
- 架构设计阶段 → system-architect / software-architect

#### Step 4: 调用业务分析

调用 `pdd-ba` skill：
- 输入: PRD文档路径
- 输出: 业务分析报告
- 使用 5W1H、MECE、CRUD 等方法论

#### Step 5: 调用功能点提取

调用 `pdd-extract-features` skill：
- 输入: PRD文档路径 + 业务分析报告
- 输出: feature-matrix.md

#### Step 6: 人工审核功能点

等待用户审核功能点矩阵：
- 确认功能点完整性
- 确认复杂度评估
- 确认测试策略
- 确认AI角色分配

#### Step 7: 调用规格生成

调用 `pdd-generate-spec` skill：
- 输入: 功能点矩阵
- 输出: spec.md, checklist.md

**架构咨询（按需）**：
- 调用 `system-architect`：技术选型、系统架构
- 调用 `software-architect`：模块划分、接口设计

#### Step 8: 人工审核规格

等待用户审核开发规格：
- 确认接口设计
- 确认数据模型
- 确认业务逻辑
- 确认测试用例

#### Step 8.1: 生成代码目录结构

根据模块编号和功能，自动生成符合规范的代码目录。

**⚠️ 重要原则**：
- **新业务功能应创建独立的 Maven 模块**，不要放到 `asset-system` 中
- `asset-system` 是系统管理模块，只放系统相关代码（用户、角色、菜单等）
- 业务模块命名规范：`asset-{业务领域}`（如 `asset-disposition`、`asset-equity`）

**模块编号到代码路径映射**：

| 模块编号 | 功能名称 | Maven模块 | 后端包路径 | 前端路径 |
|---------|---------|----------|-----------|---------|
| ZCCZ-1 | 国有产权转让 | asset-equity | com.sjjk.equity.transfer | equity-transfer |
| ZCCZ-2 | 资产转让 | asset-equity | com.sjjk.equity.transfer | asset-transfer |
| ZCCZ-3 | 企业增资 | asset-equity | com.sjjk.equity.capital | capital-increase |
| ZCCZ-4 | 国有产权无偿划转 | asset-equity | com.sjjk.equity.allocation | equity-allocation |
| ZCCZ-5 | 资产租赁 | asset-lease | com.sjjk.lease | asset-lease |
| ZCCZ-6 | 企业担保 | asset-guarantee | com.sjjk.guarantee | enterprise-guarantee |
| ZCCZ-7 | 固定资产报废 | asset-disposition | com.sjjk.disposition | fixed-asset-scrap |

**后端模块目录结构**：

```
asset-{业务领域}/                    # 独立的 Maven 模块
├── pom.xml
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/sjjk/{module}/
    │   │       ├── controller/        # 控制器
    │   │       ├── domain/            # 实体类
    │   │       │   └── vo/            # VO对象
    │   │       ├── mapper/            # Mapper接口
    │   │       ├── service/           # 服务接口
    │   │       │   └── impl/          # 服务实现
    │   │       ├── constant/          # 常量类
    │   │       └── util/              # 工具类
    │   └── resources/
    │       └── mapper/
    │           └── {module}/          # Mapper XML
    └── test/
        └── java/
            └── com/sjjk/{module}/     # 测试类
```

**前端目录结构**：

```
asset-ui/src/
├── api/
│   └── {module}/              # API接口
│       └── {feature}.js
└── views/
    └── {module}/              # 视图页面（驼峰命名）
        ├── index.vue          # 列表页
        ├── form.vue           # 表单页
        └── detail.vue         # 详情页
```

**示例：ZCCZ-1 国有产权转让**

```
后端:
  asset-equity/                          # 新建独立模块
  ├── pom.xml
  └── src/main/java/com/sjjk/equity/transfer/
      ├── controller/
      │   └── EquityTransferApplyController.java
      ├── domain/
      │   ├── EquityTransferApply.java
      │   └── vo/
      ├── mapper/
      ├── service/
      │   └── impl/
      └── constant/
  └── src/main/resources/mapper/equity/transfer/

前端:
  asset-ui/src/api/equity/transfer.js
  asset-ui/src/views/equity-transfer/
  ├── index.vue
  ├── form.vue
  └── detail.vue
```

**已有模块复用规则**：

| 已有模块 | 适用业务 | 说明 |
|---------|---------|------|
| asset-disposition | 资产处置类 | 固定资产报废、资产核销等（已存在） |
| asset-equity | 股权交易类 | 国有产权转让、企业增资等（需新建） |
| asset-admin | 系统管理 | 控制器入口、配置等 |
| asset-system | 系统功能 | 用户、角色、菜单等（不放业务代码） |

**错误示例（需避免）**：

```
❌ 错误：将业务代码放到 asset-system
asset-system/src/main/java/com/sjjk/equity/  # 错误！

✅ 正确：创建独立的业务模块
asset-equity/src/main/java/com/sjjk/equity/  # 正确！
```

#### Step 9: 循环实现功能点

对每个功能点（按优先级 P0 → P1 → P2）：

**a. 调用功能点实现**
- 调用 `pdd-implement-feature` skill
- 输入: 开发规格, 验收标准
- 输出: 代码文件

**b. 调用软件工程师**
- 调用 `software-engineer` skill
- 职责: 依据规格执行代码实现

**c. 专家咨询（按需）**
- 若依问题 → `expert-ruoyi`
- 数据库问题 → `expert-mysql`
- 代码质量问题 → `expert-code-quality`

**d. 调用代码审查**
- 调用 `pdd-code-reviewer` skill
- 输入: 代码文件, 开发规格, 验收标准
- 输出: 审查报告

**e. 架构评审（按需）**
- 发现架构问题 → `software-architect`
- 发现系统问题 → `system-architect`

**f. 处理审查结果**
- 无Critical问题 → 继续验收
- 有Critical问题 → 修复后重新审查

**g. 调用功能点验证**
- 调用 `pdd-verify-feature` skill
- 输入: 代码文件, 开发规格, 验收标准
- 输出: 验收报告

**h. 处理验收结果**
- 通过 → 标记功能点完成
- 有条件通过 → 修复问题后重新验证
- 不通过 → 重新开发

#### Step 10: 输出开发报告

生成最终开发报告

---

## 3. 技能整合

### 3.1 system-architect 整合

**触发条件**：
- 新项目初始化
- 技术栈选型
- 系统架构设计
- 重大架构变更

**服务内容**：
- 项目结构设计
- 技术栈推荐
- 代码标准定义
- 架构决策记录 (ADR)

### 3.2 software-architect 整合

**触发条件**：
- 模块划分决策
- 接口设计评审
- 数据架构设计
- 发现架构偏离

**服务内容**：
- 模块边界定义
- 接口规范设计
- 设计模式推荐
- 架构建议

### 3.3 software-engineer 整合

**触发条件**：
- 代码实现阶段
- 单元测试编写
- 代码重构
- 缺陷修复

**服务内容**：
- 依据规格实现代码
- 遵循项目编码规范
- 错误处理最佳实践
- 分层架构实现

### 3.4 expert-xxx 整合

| 专家技能 | 触发条件 | 期望输出 |
|---------|---------|---------|
| **expert-ruoyi** | 若依框架问题 | 解决方案 + 最佳实践 |
| **expert-activiti** | 工作流问题 | BPMN设计建议 |
| **expert-mysql** | 数据库问题 | SQL优化方案 |
| **expert-code-quality** | 代码质量问题 | 重构方案 |

---

## 4. AI协作模式

根据功能点复杂度自动选择AI角色：

| 复杂度 | AI角色 | 人工参与度 | 适用场景 |
|--------|--------|-----------|----------|
| P0 | 协作者 + 架构师 + 专家 | 高 | 核心业务流程、复杂状态转换 |
| P1 | 协作者 + 架构师 | 中 | 重要功能、中等复杂度 |
| P2 | 主导者 + 工程师 | 低 | 简单功能、辅助功能 |

### 复杂度与技能调用策略

```
P0 (核心业务):
  pdd-main + pdd-ba + pdd-generate-spec
    ↓ 架构咨询
  system-architect + software-architect
    ↓
  pdd-implement-feature + software-engineer
    ↓ + expert-ruoyi + expert-mysql
  pdd-code-reviewer + software-architect
    ↓
  pdd-verify-feature

P1 (重要功能):
  pdd-main + pdd-extract + pdd-generate-spec
    ↓ 按需咨询
  software-architect (如需要)
    ↓
  pdd-implement-feature + software-engineer
    ↓ + expert-xxx (按需)
  pdd-code-reviewer
    ↓
  pdd-verify-feature

P2 (辅助功能):
  pdd-main + pdd-generate-spec
    ↓
  pdd-implement-feature + software-engineer (主导)
    ↓
  pdd-code-reviewer (简化)
    ↓
  pdd-verify-feature
```

---

## 5. 子Skill清单

| Skill名称 | 功能描述 | 输入 | 输出 | 触发时机 |
|-----------|---------|------|------|----------|
| **pdd-ba** | 业务分析，运用专业方法论进行需求推演 | PRD文档路径 | 业务分析报告 | 流程开始时 |
| **pdd-extract-features** | 从PRD提取功能点矩阵 | PRD文档路径 | feature-matrix.md | 业务分析后 |
| **pdd-generate-spec** | 生成开发规格 | 功能点矩阵 | spec.md, checklist.md | 功能点确认后 |
| **pdd-implement-feature** | 实现功能点代码 | 开发规格 | 代码文件 | 规格确认后 |
| **pdd-code-reviewer** | 代码审查，验证实现是否符合规格 | 代码+规格 | 审查报告 | 代码实现后 |
| **pdd-verify-feature** | 验证功能点实现 | 代码+验收标准 | 验收报告 | 代码审查后 |
| **pdd-doc-change** | 文档变更管理 | 变更需求 | 更新的文档 | 需求变更时 |
| **system-architect** | 系统架构咨询 | 架构需求 | 架构方案 | 按需触发 |
| **software-architect** | 软件架构咨询 | 模块需求 | 模块设计 | 按需触发 |
| **software-engineer** | 代码实现与测试 | 规格文档 | 代码文件 | 实现阶段 |
| **expert-ruoyi** | 若依框架专家咨询 | 技术问题 | 解决方案 | 按需触发 |
| **expert-activiti** | Activiti工作流专家 | 流程问题 | 解决方案 | 按需触发 |
| **expert-mysql** | MySQL数据库专家 | SQL/结构问题 | 优化建议 | 按需触发 |
| **expert-code-quality** | 代码质量专家 | 代码片段 | 重构方案 | 按需触发 |

---

## 6. 流程图

### 6.1 主流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                        PDD-MAIN 主流程                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRD文档 ──→ pdd-ba ──→ 业务分析报告                            │
│                │                                                │
│                ↓                                                │
│  pdd-extract-features ──→ 功能点矩阵                            │
│                │                                                │
│                ↓                                                │
│           [人工审核]                                             │
│                │                                                │
│                ↓                                                │
│  pdd-generate-spec ──→ 开发规格 + 验收标准                      │
│                │                                                │
│                ├────── (按需) ──→ system-architect            │
│                │                                                │
│                ├────── (按需) ──→ software-architect          │
│                │                                                │
│                ↓                                                │
│           [人工审核]                                             │
│                │                                                │
│                ↓                                                │
│  ┌──────────────────────────────────────┐                       │
│  │        功能点循环处理                  │                       │
│  │  ┌────────────────────────────────┐  │                       │
│  │  │ pdd-implement-feature          │  │                       │
│  │  │         ↓                      │  │                       │
│  │  │ software-engineer              │  │                       │
│  │  │         ↓ (按需)                │  │                       │
│  │  │   expert-ruoyi / expert-mysql   │  │                       │
│  │  │         ↓                       │  │                       │
│  │  │ pdd-code-reviewer              │  │                       │
│  │  │         ↓ (按需)                │  │                       │
│  │  │   software-architect           │  │                       │
│  │  │         ↓                      │  │                       │
│  │  │ [Critical问题?] ─→ 修复 ─┐     │  │                       │
│  │  │         ↓ (无)            │     │  │                       │
│  │  │ pdd-verify-feature        │     │  │                       │
│  │  │         ↓                 │     │  │                       │
│  │  │ [验收通过?] ─→ 下一功能点 │     │  │                       │
│  │  │         ↓ (不通过)        │     │  │                       │
│  │  │      重新开发 ←───────────┘     │  │                       │
│  │  └────────────────────────────────┘  │                       │
│  └──────────────────────────────────────┘                       │
│                │                                                │
│                ↓                                                │
│           开发报告                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 技能协作图

```
┌─────────────────────────────────────────────────────────────────┐
│                      技能协作流程                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                               │
│  │ PDD流程技能 │  发现需要专业支持的问题                         │
│  └──────┬──────┘                                               │
│         │                                                        │
│         ├──────────────────────────────┐                        │
│         │                              │                        │
│         ▼                              ▼                        │
│  ┌──────────────┐            ┌──────────────┐                │
│  │system-arch  │            │software-arch │                │
│  │(系统架构)    │            │(软件架构)    │                │
│  └──────┬──────┘            └──────┬───────┘                │
│         │                           │                         │
│         ├───────────────────────────┼─────────────────────────┤ │
│         │                           │                         │ │
│         ▼                           ▼                         │ │
│  ┌──────────────┐            ┌──────────────┐                │ │
│  │software-eng  │            │ expert-xxx   │                │ │
│  │(代码实现)    │            │(领域专家)    │                │ │
│  └──────┬──────┘            └──────┬───────┘                │ │
│         │                           │                         │ │
│         └───────────────────────────┼─────────────────────────┘ │
│                                     │                           │
│                           ┌──────────┴──────────┐              │
│                           ▼                       ▼              │
│                    返回PDD流程技能              结果反馈         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. AI角色协作矩阵

```
                    ┌─────────────────────────────────────────┐
                    │              PDD AI 协作矩阵              │
                    └─────────────────────────────────────────┘

    技能/角色       │  调度者  │  分析者  │  设计者  │  实现者  │  审查者  │  专家
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    pdd-main        │    ●    │         │         │         │         │
    pdd-ba          │         │    ●    │         │         │         │
    pdd-extract     │         │    ●    │         │         │         │
    pdd-generate    │         │         │    ●    │         │         │
    pdd-implement   │         │         │         │    ●    │         │
    pdd-reviewer    │         │         │         │         │    ●    │
    pdd-verify      │         │         │         │         │    ●    │
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    system-arch     │         │         │    ●    │         │    ○    │
    software-arch   │         │         │    ●    │    ○    │    ○    │
    software-eng    │         │         │         │    ●    │         │
    ────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼────────
    expert-ruoyi    │         │         │    ○    │    ○    │    ○    │    ●
    expert-activiti │         │         │    ○    │    ○    │         │    ●
    expert-mysql    │         │         │    ○    │    ○    │    ○    │    ●
    expert-code     │         │         │    ○    │    ○    │    ●    │    ●

    图例: ● 主要职责  ○ 辅助参与  │ 空格 不参与
```

---

## 8. Guardrails

- 必须先进行业务分析再提取功能点
- 必须等待人工审核功能点矩阵
- 必须等待人工审核开发规格
- 代码实现后必须进行代码审查
- 每个功能点必须通过验收才能标记完成
- 代码变更后必须同步更新规格文档
- 问题必须记录到经验教训库
- **架构决策必须咨询架构师技能**
- **技术问题必须咨询专家技能**
- **专家建议必须整合到代码实现中**

---

## 9. 使用示例

### 9.1 模式A：模块编号自动发现

```
用户: 我想开发ZCCZ-2资产转让模块
AI: [调用pdd-main skill]
     正在扫描 docs/业务分析/ 目录...
     发现模块: ZCCZ-2-资产转让
     路径: docs/业务分析/资产处置/ZCCZ-2-资产转让/

     已聚合以下设计文档:
     ✓ PRD-资产转让.md
     ✓ 用例图-资产转让.md
     ✓ 业务流程图-资产转让.md
     ✓ 状态图-资产转让.md
     ✓ 序列图-资产转让流程.md

     请确认是否开始业务分析？ [Y/n]
```

### 9.2 模式B：手动指定文档

```
用户: 我想基于这些文档开发
     - docs/业务分析/资产处置/ZCCZ-1/PRD-国有产权转让.md
     - docs/业务分析/资产处置/ZCCZ-1/业务流程图-国有产权转让.md
     - docs/业务分析/资产处置/ZCCZ-1/状态图-国有产权转让.md

AI: [调用pdd-main skill]
     已接收3个设计文档:
     ✓ PRD-国有产权转让.md
     ✓ 业务流程图-国有产权转让.md
     ✓ 状态图-国有产权转让.md

     开始业务分析...
```

### 9.2 架构咨询使用

```
用户: 这个模块需要支持多租户架构
AI: [调用 software-architect skill]
     咨询问题: 多租户架构设计
     传入数据:
       - 功能需求: 国有产权转让模块
       - 现有架构: 单体应用
       - 约束: 需要兼容现有权限体系

     [software-architect 返回架构方案]
     架构方案:
       1. 租户标识字段设计 (tenant_id)
       2. 数据隔离策略 (共享表+租户字段过滤)
       3. 租户上下文传递机制
       4. 关键改造点清单

     已将架构约束整合到开发规格中
```

### 9.3 专家咨询使用

```
用户: 实现转让申请列表功能时遇到权限问题
AI: [调用 expert-ruoyi skill]
     咨询问题: 转让申请列表接口权限校验失败
     传入数据:
       - 接口路径: /equity/transfer/apply/list
       - 错误信息: 权限校验异常
       - 相关代码片段: [代码]

     [expert-ruoyi 返回解决方案]
     解决方案:
       1. 检查 @PreAuthorize 注解配置
       2. 确认 sys_menu 表中权限标识符
       3. 验证角色菜单分配

     已整合解决方案到代码实现中
```

---

## 10. 需求变更处理

当需求发生变更时：

```
需求变更
    ↓
pdd-doc-change 分析变更影响
    ↓
更新相关规格文档
    ↓
通知受影响的功能点
    ↓
┌─────────────────────────────────────┐
│ 如涉及架构变更:                       │
│   → system-architect 重新评审        │
│ 如涉及技术方案变更:                    │
│   → 相关 expert-xxx 重新咨询         │
└─────────────────────────────────────┘
    ↓
重新执行代码审查和验证
```

---

## 11. PDD实施规范

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。

### 11.1 核心规范摘要

| 规范 | 核心内容 |
|------|---------|
| **技能边界** | pdd-code-reviewer（合规性）→ expert-code-quality（质量深度），先审查后分析 |
| **上下文传递** | 文件系统传递，目录结构规范，支持断点续传 |
| **人工审核** | 批量审核 + 关键功能点详细审核 |
| **错误处理** | Critical阻塞，3次重试后暂停等待人工 |
| **PR管理** | 手动触发，Change粒度PR，手动归档 |
| **文档体系** | 9种核心文档类型，命名规范，文档内变更历史 |

### 11.2 审查与质量分析协作

```
代码实现完成
    │
    ▼
pdd-code-reviewer (合规性审查)
    │
    ├── 有Critical问题 → 返回修复 → 重新审查
    │
    └── 无Critical问题
            │
            ▼
    expert-code-quality (质量深度分析)
            │
            ▼
    生成质量改进任务 (improvement-tasks.md)
            │
            ▼
    进入下一阶段
```

### 11.3 断点续传

- **状态文件**: `.pdd-state.json`
- **触发方式**: 用户发出"继续执行"命令
- **状态内容**: 当前阶段、已完成功能点、待处理功能点

---

## 12. 参考文档

- [PDD框架设计文档](../docs/pdd-framework-design.md)
- [PDD技能关系规范](../docs/pdd-skill-relationships.md)
- [system-architect SKILL.md](../system-architect/SKILL.md)
- [software-architect SKILL.md](../software-architect/SKILL.md)
- [software-engineer SKILL.md](../software-engineer/SKILL.md)
- [expert-ruoyi SKILL.md](../expert-ruoyi/SKILL.md)
- [expert-activiti SKILL.md](../expert-activiti/SKILL.md)
- [expert-mysql SKILL.md](../expert-mysql/SKILL.md)
- [expert-code-quality SKILL.md](../expert-code-quality/SKILL.md)
