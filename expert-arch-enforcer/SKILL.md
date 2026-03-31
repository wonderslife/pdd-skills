---
name: expert-arch-enforcer
description: |
  架构约束强制技能，监控代码是否违反预设的不变量和架构边界。当用户需要架构检查、依赖检查、模块边界检查时自动触发。
  
  核心职责：确保架构连贯性，防止架构漂移。
  
  触发场景：
  - 用户请求"检查架构约束"、"检查依赖方向"、"检查模块边界"
  - pdd-entropy-reduction 协调器调用
  - 代码提交后自动触发
---

# 架构约束强制 (expert-arch-enforcer)

## 核心理念

> "在智能体优先的世界中，架构连贯性容易随时间漂移。约束是速度的保障，不是束缚。" —— Harness Engineering

架构约束强制技能负责监控代码是否违反了预设的不变量和架构边界，确保代码结构保持一致性。

## 架构约束模型

### 六层依赖模型

```
Types → Config → Repo → Service → Runtime → UI

规则：只能向前依赖，不能反向依赖
```

| 层级 | 职责 | 允许依赖 |
|------|------|---------|
| Types | 类型定义、数据模型 | 无 |
| Config | 配置管理、常量定义 | Types |
| Repo | 数据访问、外部服务调用 | Types, Config |
| Service | 业务逻辑、领域服务 | Types, Config, Repo |
| Runtime | 运行时、应用入口 | Types, Config, Repo, Service |
| UI | 用户界面、展示层 | 所有层 |

### 边界约束

**数据边界**：
- 所有外部数据必须验证
- API 入口参数必须有 Schema 验证
- 不允许猜测数据结构

**模块边界**：
- 模块间通过接口通信
- 禁止跨层直接访问
- 共享状态必须显式声明

---

## 检测项

### 1. 模块依赖方向违规

**检测方法**：
- 解析 import/require 语句
- 构建依赖图
- 检查是否违反依赖方向

**示例**：
```
文件：src/types/User.ts
import: import { UserService } from '../service/UserService'
→ 检测结果：Types 层依赖 Service 层，违反依赖方向
```

### 2. 边界数据验证缺失

**检测方法**：
- 扫描 API 入口函数
- 检查是否有 Schema 验证
- 标记缺失验证的入口

**示例**：
```
API 入口：POST /api/users
参数验证：无
→ 检测结果：缺少参数验证 Schema
```

### 3. 文件大小超限

**检测方法**：
- 统计文件行数
- 对比配置的最大行数
- 标记超限文件

**示例**：
```
文件：src/service/UserService.ts
行数：450 行
限制：300 行
→ 检测结果：文件过大，建议拆分
```

### 4. 命名规范违反

**检测方法**：
- 检查文件名、函数名、变量名
- 对比命名规范
- 标记违规命名

**示例**：
```
函数名：get_data
规范：camelCase
→ 检测结果：命名不规范，应为 getData
```

---

## 执行流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   解析      │ ──→ │   构建      │ ──→ │   检测      │ ──→ │   报告      │
│             │     │             │     │             │     │             │
│ • 代码文件  │     │ • 依赖图    │     │ • 依赖违规  │     │ • 问题清单  │
│ • import    │     │ • 调用关系  │     │ • 边界违规  │     │ • 修复建议  │
│ • 函数签名  │     │ • 模块结构  │     │ • 大小违规  │     │ • PR 创建   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 工具集成

### 自定义 Linter

```javascript
// custom-linter.js
module.exports = {
  rules: {
    'layer-dependency': {
      meta: {
        docs: { description: '强制六层依赖方向' }
      },
      create(context) {
        const layers = ['types', 'config', 'repo', 'service', 'runtime', 'ui'];
        return {
          ImportDeclaration(node) {
            const source = node.source.value;
            const currentLayer = getCurrentLayer(context.getFilename());
            const targetLayer = getLayerFromPath(source);
            
            if (layers.indexOf(targetLayer) < layers.indexOf(currentLayer)) {
              context.report({
                node,
                message: `违反依赖方向: ${currentLayer} 不能依赖 ${targetLayer}`
              });
            }
          }
        };
      }
    }
  }
};
```

### ArchUnit 测试

```java
// ArchitectureTest.java
@AnalyzeClasses(packages = "com.example")
public class ArchitectureTest {
    
    @ArchTest
    static final ArchRule layer_dependency_rule = layeredArchitecture()
        .layer("Types").definedBy("..types..")
        .layer("Config").definedBy("..config..")
        .layer("Repo").definedBy("..repo..")
        .layer("Service").definedBy("..service..")
        .layer("Runtime").definedBy("..runtime..")
        .layer("UI").definedBy("..ui..")
        .whereLayer("Types").mayNotBeAccessedByAnyLayer()
        .whereLayer("Config").mayOnlyBeAccessedByLayers("Repo", "Service", "Runtime", "UI")
        .whereLayer("Repo").mayOnlyBeAccessedByLayers("Service", "Runtime", "UI");
}
```

---

## 输出格式

### 架构约束报告

```markdown
# 架构约束报告 - YYYY-MM-DD

## 架构健康度：XX/100

## 依赖图

[依赖关系可视化图]

## 发现问题

### Critical（必须修复）
| 文件 | 问题 | 违规类型 |
|------|------|---------|
| src/types/User.ts | 依赖 Service 层 | 依赖方向违规 |

### Warning（建议修复）
| 文件 | 问题 | 违规类型 |
|------|------|---------|
| src/api/users.ts | 缺少参数验证 | 边界验证缺失 |

### Info（可选修复）
| 文件 | 问题 | 违规类型 |
|------|------|---------|
| src/service/UserService.ts | 文件 450 行 | 大小超限 |

## 修复建议

### Critical 修复
1. 移除 User.ts 中对 UserService 的依赖
2. 将共享逻辑提取到 Types 层
```

---

## 配置选项

```yaml
# arch-enforcer-config.yaml
arch_enforcer:
  # 层级定义
  layers:
    - name: types
      paths: ["src/types/", "src/models/"]
    - name: config
      paths: ["src/config/", "src/constants/"]
    - name: repo
      paths: ["src/repo/", "src/data/"]
    - name: service
      paths: ["src/service/", "src/domain/"]
    - name: runtime
      paths: ["src/runtime/", "src/app/"]
    - name: ui
      paths: ["src/ui/", "src/components/"]
  
  # 约束规则
  constraints:
    max_file_lines: 300
    max_function_lines: 50
    require_schema_validation: true
  
  # 执行配置
  execution:
    run_linter: true
    run_arch_test: true
    create_pr: true
```

---

## 使用示例

### 示例 1：全面架构检查

```
用户：检查架构约束

AI：
1. 解析代码文件
2. 构建依赖图
3. 运行 Linter 和 ArchUnit
4. 生成报告
```

### 示例 2：依赖方向检查

```
用户：检查模块依赖方向

AI：
1. 解析 import 语句
2. 构建依赖图
3. 检查是否违反六层模型
4. 生成违规报告
```

---

## 与其他技能的协作

- **pdd-entropy-reduction**：作为子技能被协调调用
- **expert-auto-refactor**：接收架构违规，执行重构
- **pdd-code-reviewer**：集成架构检查到代码审查
