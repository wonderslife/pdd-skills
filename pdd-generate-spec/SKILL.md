---
name: pdd-generate-spec
description: 根据功能点矩阵生成开发规格和验收标准。当用户想要生成功能点的技术规格时调用此Skill。
license: MIT
compatibility: 需要先完成功能点提取
metadata:
  author: asset-platform
  version: "2.0"
  parent: pdd-main
---

规格生成 - 根据功能点生成开发规格和验收标准

**输入**: 功能点矩阵 (feature-matrix.md)

**输出**:
- spec.md (开发规格)
- checklist.md (验收标准)

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 2.1 | 2026-03-22 | 添加文档体系规范、PDD实施规范引用 |
| 2.0 | 2026-03-21 | 新增架构师咨询流程 |
| 1.0 | 早期 | 初始版本 |

---

## 1. 技能整合

### 1.1 架构师咨询

在规格生成过程中，可按需调用架构师技能：

| 架构师技能 | 调用时机 | 服务内容 |
|-----------|---------|---------|
| **system-architect** | 技术选型、系统架构 | 技术栈推荐、架构决策、系统结构 |
| **software-architect** | 模块划分、接口设计 | 模块边界、接口规范、设计模式 |

### 1.2 调用条件

**必须调用 system-architect**：
- 新技术栈引入
- 系统架构变更
- 重大技术决策

**必须调用 software-architect**：
- 模块边界不清晰
- 接口设计复杂
- 需要设计模式建议

---

## 2. 流程步骤

### Step 1: 读取功能点矩阵

从 `dev-specs/feature-matrix.md` 读取功能点清单和详情。

### Step 2: 确定技术栈

根据项目配置确定技术栈：
- 后端：Spring Boot + MyBatis (若依框架)
- 前端：Vue.js + Element UI
- 数据库：MySQL

**架构咨询（按需）**：
如果涉及新技术选型，调用 `system-architect` 获取推荐。

### Step 3: 模块设计

分析功能点归属的模块：
- 确定模块边界
- 确定模块依赖关系

**架构咨询（按需）**：
如果模块边界不清晰，调用 `software-architect` 获取建议。

### Step 4: 为每个功能点生成规格

按优先级顺序处理功能点：

**a. 分析功能点需求**
- 业务描述
- 前置/后置条件
- 业务规则
- 测试场景

**b. 设计接口**
- 确定接口路径（RESTful风格）
- 确定请求方法（GET/POST/PUT/DELETE）
- 设计请求参数
- 设计响应结构
- 定义错误码

**接口命名规范**：

| 操作类型 | 接口路径 | 请求方法 |
|----------|----------|----------|
| 列表查询 | /api/{module}/list | GET |
| 详情查询 | /api/{module}/{id} | GET |
| 新增 | /api/{module} | POST |
| 修改 | /api/{module} | PUT |
| 删除 | /api/{module}/{id} | DELETE |
| 审批操作 | /api/{module}/approve | POST |
| 退回操作 | /api/{module}/reject | POST |
| 终止操作 | /api/{module}/terminate | POST |

**c. 设计数据模型**

数据模型命名规范：

| 类型 | 命名规范 | 示例 |
|------|----------|------|
| 实体类 | {业务名} | TransferApplication |
| 主键 | id | id |
| 创建时间 | createTime | createTime |
| 更新时间 | updateTime | updateTime |
| 创建人 | createBy | createBy |
| 更新人 | updateBy | updateBy |
| 状态 | status | status |
| 删除标志 | delFlag | delFlag |

**d. 设计业务逻辑**
- 处理流程
- 校验规则
- 状态转换
- 异常处理

**架构咨询（按需）**：
如果业务逻辑复杂，调用 `software-architect` 获取设计建议。

**e. 设计测试用例**
- 正向场景
- 异常场景
- 边界条件

### Step 5: 生成开发规格文档

输出到 `dev-specs/FP-{序号}/spec.md`：

```markdown
# {功能点名称} 开发规格

## 文档信息
| 项目 | 内容 |
|------|------|
| 规格ID | SPEC-{模块编号}-{功能点序号} |
| 关联功能点 | FP-XXX-NNN |

## 接口定义
### 接口1: {接口名称}
- 接口路径: `/api/xxx`
- 请求方法: POST
- 请求参数: [...]
- 响应结构: {...}
- 错误码: [...]

## 数据模型
### 实体: {实体名称}
| 字段名 | 类型 | 必填 | 说明 |

## 业务逻辑
### 处理流程
### 校验规则
### 状态转换

## 测试用例
### 正向场景
### 异常场景
### 边界条件
```

### Step 6: 生成验收标准文档

输出到 `dev-specs/FP-{序号}/checklist.md`：

```markdown
# {功能点名称} 验收标准

## 文档信息
| 项目 | 内容 |
|------|------|
| 验收标准ID | AC-{模块编号}-{功能点序号} |

## 业务验收
| 序号 | 验收场景 | 预期结果 | 验证方法 | 状态 |

## 技术验收
| 序号 | 验收项 | 标准 | 状态 |

## 集成验收
| 序号 | 验收项 | 验证方法 | 状态 |
```

### Step 7: 生成代码框架（可选）

对于P0功能点，生成代码框架：
- 后端Controller/Service/Mapper/Domain
- 前端Vue组件

---

## 3. 架构咨询流程

```
pdd-generate-spec 开始
    │
    ├─► 识别技术选型需求
    │       │
    │       ▼
    │   system-architect 咨询
    │       │
    │       ▼
    │   返回技术栈推荐
    │
    ├─► 识别模块设计需求
    │       │
    │       ▼
    │   software-architect 咨询
    │       │
    │       ▼
    │   返回模块边界建议
    │
    └─► 继续生成规格
```

### 3.1 system-architect 调用示例

```
触发条件: 需要引入新技木栈
调用: system-architect
输入:
  - 功能需求: 消息推送功能
  - 约束: 需要支持多渠道推送
  - 现有技术栈: Spring Boot

返回:
  - 技术选型建议
  - 架构决策记录 (ADR)
  - 项目结构建议
```

### 3.2 software-architect 调用示例

```
触发条件: 模块边界不清晰
调用: software-architect
输入:
  - 功能需求: 转让申请与审批模块
  - 现有模块: 资产管理基础模块
  - 复杂度: 高

返回:
  - 模块划分方案
  - 接口边界定义
  - 设计模式建议
```

---

## 4. Guardrails

- 接口设计必须遵循RESTful规范
- 数据模型必须包含审计字段
- 业务规则必须与PRD保持一致
- 测试用例必须覆盖所有业务规则
- **架构决策必须咨询架构师技能**
- **模块设计必须遵循高内聚低耦合原则**

---

## 5. 与其他技能协作

| 协作技能 | 协作方式 | 传入数据 | 期望输出 |
|---------|---------|---------|---------|
| **system-architect** | Consultation | 技术需求、约束 | 技术选型、架构决策 |
| **software-architect** | Consultation | 模块需求、接口设计 | 模块划分、接口规范 |
| **pdd-implement-feature** | Sequential | spec.md, checklist.md | 代码实现 |
| **pdd-code-reviewer** | Sequential | 代码+规格 | 审查报告 |

---

## 6. 文档体系规范

本Skill遵循PDD框架文档体系规范。

### 6.1 输出文档

| 文档类型 | 文件名 | 核心内容 |
|---------|--------|---------|
| 开发规格 | spec.md | 接口设计、数据模型、业务逻辑、技术实现 |
| 验收标准 | checklist.md | 验收项、验收条件、验收方法 |

### 6.2 命名规范

```
dev-specs/FP-{模块编号}-{序号}/
├── spec.md
└── checklist.md
```

### 6.3 版本管理

- 每次修改文档必须更新变更历史
- 记录修改日期、修改人、变更内容

---

## 7. PDD实施规范引用

本Skill遵循PDD框架实施规范，详见 [pdd-framework-design.md 第9章](../docs/pdd-framework-design.md#9-pdd-实施规范)。
