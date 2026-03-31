# PDD 熵减黄金原则

> 本文档定义了 PDD 熵减机制的核心原则，所有熵减操作都应遵循这些原则。

---

## 一、核心原则概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    PDD 熵减黄金原则                              │
├─────────────────────────────────────────────────────────────────┤
│  1. 共享优先原则    - 重复是熵增之源                             │
│  2. 边界验证原则    - 越界是腐化之始                             │
│  3. 简洁代码原则    - 复杂是债务之根                             │
│  4. 文档同步原则    - 脱节是混乱之本                             │
│  5. 持续改进原则    - 停滞是衰败之门                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、原则详解

### 原则一：共享优先原则 (Shared-First)

**核心理念**: 重复是熵增之源，共享是熵减之本。

#### 2.1.1 问题场景

```typescript
// ❌ 错误：重复代码导致熵增
// 文件 A: src/service/UserService.ts
async function validateEmail(email: string): Promise<boolean> {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// 文件 B: src/service/AdminService.ts
async function validateEmail(email: string): Promise<boolean> {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// 文件 C: src/utils/helper.ts
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

#### 2.1.2 正确实践

```typescript
// ✅ 正确：提取到共享工具包
// 文件: src/shared/utils/validation.ts
export const ValidationUtils = {
  isValidEmail(email: string): boolean {
    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return EMAIL_REGEX.test(email);
  }
};

// 使用方
import { ValidationUtils } from '@shared/utils/validation';

async function processUser(email: string) {
  if (!ValidationUtils.isValidEmail(email)) {
    throw new Error('Invalid email');
  }
}
```

#### 2.1.3 检测规则

```yaml
shared_first_rules:
  - name: 重复代码检测
    threshold: 5  # 相同代码块出现次数
    action: 提取到共享模块
  
  - name: 相似函数检测
    threshold: 80%  # 相似度阈值
    action: 合并为参数化函数
  
  - name: 常量重复检测
    threshold: 2  # 相同常量出现次数
    action: 提取为共享常量
```

---

### 原则二：边界验证原则 (Boundary Validation)

**核心理念**: 越界是腐化之始，边界是秩序之基。

#### 2.2.1 六层依赖模型

```
┌─────────────────────────────────────────────────────────────────┐
│                        六层依赖模型                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Layer 6: UI          ──────→  用户界面层                      │
│        ↑                                                        │
│   Layer 5: Runtime     ──────→  运行时环境层                    │
│        ↑                                                        │
│   Layer 4: Service     ──────→  业务服务层                      │
│        ↑                                                        │
│   Layer 3: Repo        ──────→  数据仓储层                      │
│        ↑                                                        │
│   Layer 2: Config      ──────→  配置管理层                      │
│        ↑                                                        │
│   Layer 1: Types       ──────→  类型定义层                      │
│                                                                 │
│   规则：依赖只能向下，不能向上或跨层                              │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2.2 边界违规示例

```typescript
// ❌ 错误：Service 层直接引用 UI 层
// src/service/UserService.ts
import { UserForm } from '../ui/components/UserForm';  // 违规！

export class UserService {
  async createUser(data: UserData) {
    // Service 不应该知道 UI 的存在
    const form = new UserForm();  // 严重违规
    return form.submit(data);
  }
}
```

#### 2.2.3 正确实践

```typescript
// ✅ 正确：通过事件机制解耦
// src/service/UserService.ts
import { EventBus } from '@shared/events';

export class UserService {
  async createUser(data: UserData) {
    const user = await this.repo.save(data);
    // 通过事件通知，而不是直接调用 UI
    EventBus.emit('user:created', user);
    return user;
  }
}

// src/ui/components/UserForm.tsx
import { EventBus } from '@shared/events';

export function UserForm() {
  useEffect(() => {
    EventBus.on('user:created', handleUserCreated);
    return () => EventBus.off('user:created', handleUserCreated);
  }, []);
}
```

#### 2.2.4 边界检查规则

```yaml
boundary_rules:
  - layer: Types
    can_depend_on: []
    cannot_depend_on: [Config, Repo, Service, Runtime, UI]
  
  - layer: Config
    can_depend_on: [Types]
    cannot_depend_on: [Repo, Service, Runtime, UI]
  
  - layer: Repo
    can_depend_on: [Types, Config]
    cannot_depend_on: [Service, Runtime, UI]
  
  - layer: Service
    can_depend_on: [Types, Config, Repo]
    cannot_depend_on: [Runtime, UI]
  
  - layer: Runtime
    can_depend_on: [Types, Config, Repo, Service]
    cannot_depend_on: [UI]
  
  - layer: UI
    can_depend_on: [Types, Config, Repo, Service, Runtime]
    cannot_depend_on: []
```

---

### 原则三：简洁代码原则 (Simplicity)

**核心理念**: 复杂是债务之根，简洁是质量之本。

#### 2.3.1 复杂度度量

```yaml
complexity_metrics:
  cyclomatic_complexity:
    healthy: < 10
    warning: 10-20
    critical: > 20
  
  cognitive_complexity:
    healthy: < 15
    warning: 15-30
    critical: > 30
  
  function_length:
    healthy: < 50 lines
    warning: 50-100 lines
    critical: > 100 lines
  
  nesting_depth:
    healthy: < 3
    warning: 3-5
    critical: > 5
```

#### 2.3.2 复杂代码示例

```typescript
// ❌ 错误：复杂度过高
async function processOrder(order: Order): Promise<Result> {
  if (order.items && order.items.length > 0) {
    let total = 0;
    for (const item of order.items) {
      if (item.price > 0) {
        if (item.quantity > 0) {
          if (item.discount) {
            if (item.discount.type === 'percentage') {
              total += item.price * item.quantity * (1 - item.discount.value / 100);
            } else if (item.discount.type === 'fixed') {
              total += (item.price * item.quantity) - item.discount.value;
            } else {
              total += item.price * item.quantity;
            }
          } else {
            total += item.price * item.quantity;
          }
        }
      }
    }
    // ... 更多嵌套逻辑
  }
}
```

#### 2.3.3 简洁重构

```typescript
// ✅ 正确：拆分为小函数
async function processOrder(order: Order): Promise<Result> {
  if (!order.items?.length) return emptyResult();
  
  const total = order.items
    .filter(hasValidPrice)
    .filter(hasValidQuantity)
    .reduce(sumItemPrices, 0);
  
  return { total };
}

function hasValidPrice(item: OrderItem): boolean {
  return item.price > 0;
}

function hasValidQuantity(item: OrderItem): boolean {
  return item.quantity > 0;
}

function sumItemPrices(total: number, item: OrderItem): number {
  return total + calculateItemTotal(item);
}

function calculateItemTotal(item: OrderItem): number {
  const base = item.price * item.quantity;
  return applyDiscount(base, item.discount);
}

function applyDiscount(amount: number, discount?: Discount): number {
  if (!discount) return amount;
  
  const discountStrategies = {
    percentage: (a: number, d: Discount) => a * (1 - d.value / 100),
    fixed: (a: number, d: Discount) => a - d.value,
  };
  
  const strategy = discountStrategies[discount.type];
  return strategy ? strategy(amount, discount) : amount;
}
```

---

### 原则四：文档同步原则 (Doc Sync)

**核心理念**: 脱节是混乱之本，同步是信任之源。

#### 2.4.1 文档类型与同步要求

| 文档类型 | 同步触发 | 验证方式 | 容忍度 |
|---------|---------|---------|--------|
| API 文档 | 接口变更 | 自动化测试 | 零容忍 |
| 架构文档 | 结构调整 | 架构审计 | 零容忍 |
| README | 功能变更 | 人工审核 | 低容忍 |
| 注释 | 代码修改 | 静态分析 | 中容忍 |
| 设计文档 | 需求变更 | 评审会议 | 低容忍 |

#### 2.4.2 文档-代码一致性检查

```yaml
doc_sync_rules:
  - trigger: API 签名变更
    check:
      - 更新 OpenAPI/Swagger 文档
      - 更新类型定义文件
      - 更新使用示例
    auto_fix: false
  
  - trigger: 函数参数变更
    check:
      - 更新 JSDoc 注释
      - 更新参数说明
      - 更新示例代码
    auto_fix: true
  
  - trigger: 配置项变更
    check:
      - 更新配置文档
      - 更新环境变量说明
      - 更新部署文档
    auto_fix: false
```

#### 2.4.3 文档过期检测

```typescript
// 文档过期检测规则
interface DocStaleness {
  // TODO/FIXME 过期阈值
  todo_stale_days: 30;  // 30天未处理的 TODO 视为过期
  
  // 文档更新阈值
  doc_update_days: 90;  // 90天未更新的文档需要审核
  
  // 代码-文档差异阈值
  code_doc_diff_threshold: 0.2;  // 20% 以上差异需要更新
}
```

---

### 原则五：持续改进原则 (Continuous Improvement)

**核心理念**: 停滞是衰败之门，改进是进化之路。

#### 2.5.1 "小额还贷"策略

```
┌─────────────────────────────────────────────────────────────────┐
│                    技术债务偿还策略                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   传统方式（大额还贷）:                                          │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  积累债务 ──────────────────────→ 大型重构（痛苦）        │  │
│   │  (6个月)                          (2周, 高风险)           │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│   熵减方式（小额还贷）:                                          │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │  每周偿还 ─→ 每周偿还 ─→ 每周偿还 ─→ 系统持续健康        │  │
│   │  (2小时)      (2小时)      (2小时)                        │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│   关键：持续、小额、低风险                                       │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.5.2 改进任务优先级

```yaml
improvement_priority:
  critical:
    - 架构违规（立即修复）
    - 安全漏洞（立即修复）
    - 数据丢失风险（立即修复）
  
  high:
    - 性能瓶颈（本周修复）
    - 重复代码（本周修复）
    - 文档严重过期（本周修复）
  
  medium:
    - 命名不规范（本月修复）
    - 复杂度偏高（本月修复）
    - 注释缺失（本月修复）
  
  low:
    - 代码风格统一（持续改进）
    - 测试覆盖率提升（持续改进）
    - 文档完善（持续改进）
```

#### 2.5.3 改进度量指标

```yaml
improvement_metrics:
  debt_ratio:
    description: 技术债务占比
    formula: 债务工时 / 总开发工时
    healthy: < 10%
    warning: 10-20%
    critical: > 20%
  
  repayment_rate:
    description: 债务偿还率
    formula: 已偿还债务 / 总债务
    healthy: > 80%
    warning: 50-80%
    critical: < 50%
  
  entropy_trend:
    description: 熵值趋势
    healthy: 持续下降
    warning: 保持稳定
    critical: 持续上升
```

---

## 三、原则应用指南

### 3.1 日常开发中的应用

```markdown
## 开发前检查
- [ ] 新代码是否复用了现有共享模块？
- [ ] 新依赖是否符合六层模型？
- [ ] 新函数复杂度是否在健康范围？
- [ ] 是否同步更新了相关文档？

## 开发中检查
- [ ] 是否有重复代码产生？
- [ ] 是否有边界穿透？
- [ ] 复杂度是否在增长？
- [ ] 文档是否保持同步？

## 开发后检查
- [ ] 是否产生了新的技术债务？
- [ ] 是否需要创建新的共享模块？
- [ ] 是否需要重构现有代码？
- [ ] 是否需要更新架构文档？
```

### 3.2 代码评审中的应用

```yaml
code_review_checklist:
  shared_first:
    - 检查是否有重复代码
    - 检查是否可以提取共享模块
    - 检查是否使用了现有工具函数
  
  boundary_validation:
    - 检查依赖方向是否正确
    - 检查是否有跨层调用
    - 检查是否有循环依赖
  
  simplicity:
    - 检查函数复杂度
    - 检查嵌套深度
    - 检查函数长度
  
  doc_sync:
    - 检查 API 文档是否更新
    - 检查注释是否准确
    - 检查 README 是否需要更新
  
  continuous_improvement:
    - 检查是否引入新债务
    - 检查是否可以顺便修复附近债务
    - 检查是否需要创建改进任务
```

### 3.3 定期审计中的应用

```yaml
audit_schedule:
  daily:
    - 自动化熵值检测
    - 新增债务记录
  
  weekly:
    - 熵减报告生成
    - 小额还贷任务分配
    - 团队熵值评审
  
  monthly:
    - 架构合规性深度审计
    - 文档一致性全面检查
    - 技术债务趋势分析
  
  quarterly:
    - 黄金原则适用性评估
    - 熵减机制效果评估
    - 原则更新和优化
```

---

## 四、原则冲突处理

### 4.1 常见冲突场景

| 冲突场景 | 优先级判断 | 处理建议 |
|---------|-----------|---------|
| 简洁 vs 共享 | 简洁优先 | 过度抽象比重复更糟 |
| 边界 vs 快速 | 边界优先 | 技术债利息高于时间成本 |
| 文档 vs 功能 | 功能优先 | 但需创建文档任务 |
| 改进 vs 新需求 | 平衡 | 分配 20% 时间给改进 |

### 4.2 决策框架

```
当原则冲突时，按以下顺序决策：

1. 安全性 - 不妥协
2. 边界完整性 - 高优先级
3. 功能正确性 - 高优先级
4. 代码简洁性 - 中优先级
5. 共享复用 - 中优先级
6. 文档完善 - 可延后但必须记录
```

---

## 五、原则演进机制

### 5.1 原则评估指标

```yaml
principle_metrics:
  adherence_rate:
    description: 原则遵守率
    measurement: 代码评审中原则违规次数 / 总评审次数
  
  effectiveness:
    description: 原则有效性
    measurement: 遵守原则后熵值下降幅度
  
  applicability:
    description: 原则适用性
    measurement: 原则被实际应用的次数 / 原则总数
```

### 5.2 原则更新流程

```markdown
1. 收集原则应用反馈（每月）
2. 分析原则有效性数据（每季度）
3. 提出原则修订建议（每季度）
4. 团队评审和投票（每季度）
5. 更新原则文档（通过后）
6. 通知所有相关人员（更新后）
```

---

> 📌 **最后提醒**: 黄金原则不是教条，而是指南。在具体场景中，需要结合实际情况灵活应用，但核心目标始终不变——**对抗熵增，保持系统健康**。
