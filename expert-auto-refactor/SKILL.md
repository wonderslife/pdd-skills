---
name: expert-auto-refactor
description: |
  自动化重构专家技能，将收集到的质量改进任务转化为具体的代码操作。当用户需要代码重构、消除重复、简化复杂度时自动触发。
  
  核心职责：以"小额还贷"的方式定期发起针对性的重构 PR，防止技术债务堆积。
  
  触发场景：
  - 用户请求"重构代码"、"消除重复"、"简化代码"
  - pdd-entropy-reduction 协调器调用
  - expert-entropy-auditor 传递重构建议
---

# 自动化重构专家 (expert-auto-refactor)

## 核心理念

> "以'小额还贷'的方式定期发起针对性的重构 PR，防止技术债务堆积成无法解决的'痛苦利息'。" —— Harness Engineering

自动化重构专家是 `expert-code-quality` 的升级版，不只是记录问题，而是主动执行重构操作。

## 重构类型

### 1. 提取公共方法

**场景**：多个地方有相似的代码逻辑

**重构方法**：
1. 识别相似代码
2. 提取公共方法
3. 替换原有调用

**示例**：

重构前：
```javascript
// 文件 A
function formatDate(date) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

// 文件 B
function formatDateString(d) {
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
}
```

重构后：
```javascript
// utils/dateUtils.ts
export function formatDate(date: Date): string {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

// 文件 A
import { formatDate } from '../utils/dateUtils';

// 文件 B
import { formatDate } from '../utils/dateUtils';
```

### 2. 消除重复代码

**场景**：完全相同或高度相似的代码块

**重构方法**：
1. 检测重复代码
2. 提取到共享模块
3. 更新引用

**示例**：

重构前：
```javascript
// 多处重复的验证逻辑
if (!user.email || !user.email.includes('@')) {
  throw new Error('Invalid email');
}
```

重构后：
```javascript
// utils/validators.ts
export function validateEmail(email: string): boolean {
  return email && email.includes('@');
}

// 使用
if (!validateEmail(user.email)) {
  throw new Error('Invalid email');
}
```

### 3. 简化复杂逻辑

**场景**：函数过长、嵌套过深、逻辑复杂

**重构方法**：
1. 拆分长函数
2. 提取子函数
3. 简化条件判断

**示例**：

重构前：
```javascript
function processOrder(order) {
  if (order.status === 'pending') {
    if (order.items.length > 0) {
      if (order.payment) {
        // 处理逻辑...
        if (order.shipping) {
          // 更多处理...
        }
      }
    }
  }
}
```

重构后：
```javascript
function processOrder(order) {
  if (!canProcessOrder(order)) return;
  
  processPayment(order);
  processShipping(order);
  updateOrderStatus(order);
}

function canProcessOrder(order) {
  return order.status === 'pending' 
    && order.items.length > 0 
    && order.payment;
}
```

### 4. 优化命名

**场景**：命名不规范、含义不清

**重构方法**：
1. 分析命名上下文
2. 生成更好的命名
3. 批量替换

**示例**：

重构前：
```javascript
function calc(a, b) {
  return a * b * 0.1;
}
```

重构后：
```javascript
function calculateTax(basePrice: number, quantity: number): number {
  const TAX_RATE = 0.1;
  return basePrice * quantity * TAX_RATE;
}
```

---

## 重构流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   分析      │ ──→ │   规划      │ ──→ │   执行      │ ──→ │   验证      │
│             │     │             │     │             │     │             │
│ • 代码结构  │     │ • 重构策略  │     │ • 代码修改  │     │ • 测试运行  │
│ • 依赖关系  │     │ • 影响范围  │     │ • 引用更新  │     │ • 功能验证  │
│ • 测试覆盖  │     │ • 风险评估  │     │ • 文档同步  │     │ • PR 创建   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 重构策略

### 小额还贷原则

每次重构应该：
1. **小步前进**：每次只改一小部分
2. **保持测试**：确保测试始终通过
3. **频繁提交**：每完成一个小步骤就提交
4. **可回滚**：保持每个提交可以独立回滚

### 风险评估

| 风险等级 | 条件 | 策略 |
|---------|------|------|
| 低 | 有完整测试覆盖 | 自动执行 |
| 中 | 有部分测试覆盖 | 创建 PR |
| 高 | 无测试覆盖 | 先补充测试再重构 |

---

## 输出格式

### 重构报告

```markdown
# 重构报告 - YYYY-MM-DD

## 重构范围
- 目标文件：X 个
- 影响文件：X 个
- 测试覆盖：X%

## 重构操作

### 提取公共方法
| 原文件 | 新文件 | 方法名 | 状态 |
|-------|-------|-------|------|
| utils/formatDate.js | utils/dateUtils.ts | formatDate | ✅ 完成 |

### 消除重复代码
| 文件 A | 文件 B | 重复行数 | 状态 |
|-------|-------|---------|------|
| service/UserService.ts | service/OrderService.ts | 25 行 | ✅ 完成 |

### 简化复杂逻辑
| 文件 | 函数名 | 原行数 | 新行数 | 状态 |
|------|-------|-------|-------|------|
| service/OrderService.ts | processOrder | 80 | 35 | ✅ 完成 |

## 验证结果
- 单元测试：✅ 全部通过
- 集成测试：✅ 全部通过
- 功能验证：✅ 无异常

## PR 信息
- PR 编号：#XXX
- 分支：refactor/entropy-reduction-YYYYMMDD
- 状态：待审核
```

---

## 配置选项

```yaml
# auto-refactor-config.yaml
auto_refactor:
  # 重构范围
  scope:
    code_paths: ["src/"]
    exclude: ["node_modules/", "dist/", "build/"]
  
  # 重构规则
  rules:
    max_file_lines: 300
    max_function_lines: 50
    min_similarity: 0.8
  
  # 执行策略
  execution:
    auto_fix_low_risk: true   # 自动修复低风险
    create_pr: true           # 创建 PR
    max_changes_per_run: 10   # 每次运行最大变更数
  
  # 测试要求
  testing:
    require_tests: true       # 要求有测试
    min_coverage: 80          # 最低覆盖率
```

---

## 使用示例

### 示例 1：提取重复代码

```
用户：消除代码中的重复

AI：
1. 检测重复代码
2. 分析相似度
3. 提取到共享模块
4. 更新所有引用
5. 创建 PR
```

### 示例 2：简化复杂函数

```
用户：简化 processOrder 函数

AI：
1. 分析函数结构
2. 识别可提取的子函数
3. 执行拆分重构
4. 运行测试验证
5. 创建 PR
```

### 示例 3：优化命名

```
用户：优化代码命名

AI：
1. 扫描不规范命名
2. 分析上下文
3. 生成更好的命名
4. 批量替换
5. 创建 PR
```

---

## 与其他技能的协作

- **pdd-entropy-reduction**：作为子技能被协调调用
- **expert-entropy-auditor**：接收重构建议
- **expert-arch-enforcer**：接收架构违规修复
- **pdd-code-reviewer**：重构后触发代码审查
- **pdd-doc-change**：同步更新相关文档
