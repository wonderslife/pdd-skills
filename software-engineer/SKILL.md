---
name: software-engineer
description: "软件工程师角色，编写生产级代码，具备清晰架构、适当错误处理和在快速交付与正确构建之间的务实权衡。用于实现功能、编写业务逻辑、创建服务或任何需要生产级代码的任务。此技能专注于代码级实现，不涉及高层架构设计。"
license: "MIT"
author: "wonderqi"
version: "2.0"
---

# Software Engineer（软件工程师）

## 概述

本技能专注于：
- 类/函数级别的代码实现
- 业务逻辑和领域模型
- 单元测试和集成测试
- 错误处理和验证
- 代码重构和优化

**注意**：这是代码实现技能，专注于具体的业务功能实现。架构设计请使用 **software-architect**，项目初始化请使用 **system-architect**。

## 目录结构

```
software-engineer/
├── SKILL.md              # 技能定义文件
└── LICENSE               # MIT 许可证
```

## 触发条件

**自动触发：**
- 实现具体功能或函数
- 编写业务逻辑或服务层代码
- 创建仓库、控制器或处理器
- 编写单元测试或集成测试
- 重构现有代码
- 修复bug或代码质量问题

**手动触发：**
- 用户输入 `/implement`、`/code`、`/refactor` 等命令

---

## 核心规则

### 1. 先读后写
- 编写新代码前检查现有代码风格、模式和约定
- 尊重当前技术栈 — 未经明确请求不更换库
- 匹配已有的命名约定、格式和项目结构

### 2. 能编译的代码
每个代码块必须：
- 为实际库版本使用正确的导入
- 使用项目依赖版本中存在的API
- 通过基本语法检查 — 无占位符 `// TODO: implement`

### 3. 最小化优先
- 解决具体问题，不是假设的未来问题
- 有三个具体案例时才考虑抽象，不提前
- 可能需要的特性 → 跳过。需要的特性 → 实现

### 4. 错误作为一等公民
```
❌ catch (e) {}
❌ catch (e) { console.log(e) }
✅ catch (e) { logger.error('context', { error: e, input }); throw new DomainError(...) }
```
- 类型化错误优于通用字符串
- 包含上下文：什么操作失败了，带着什么输入
- 区分可恢复 vs 致命错误

### 5. 边界和分离

| 层 | 包含 | 绝不包含 |
|---|------|---------|
| Handler/Controller | HTTP/CLI解析、验证 | 业务逻辑、SQL |
| Service/Domain | 业务规则、编排 | 基础设施细节 |
| Repository/Adapter | 数据访问、外部API | 业务决策 |

### 6. 明确的权衡
做出架构选择时，说明：
- 你选择了什么，为什么
- 你放弃了什么
- 何时重新审视决策

示例："为简单使用SQLite。权衡：无并发写入。如果>1次写入/秒需要，重新考虑。"

### 7. PR就绪代码
交付任何代码前：
- [ ] 无死代码、注释块或调试语句
- [ ] 函数少于30行
- [ ] 无魔法数字 — 使用命名常量
- [ ] 早期返回优于嵌套条件
- [ ] 处理边界情况：null、空、错误状态

---

## 代码质量信号

**高级代码读起来像散文：**
- 名称解释"什么"和"为什么"，不是"怎么做"
- 初级工程师30秒能理解
- 无需注释解释的聪明

**最好的代码是无聊的：**
- 可预测的模式
- 合理时优先使用标准库而非依赖
- 显式优于隐式

---

## 常见陷阱

| 陷阱 | 后果 | 预防 |
|------|------|------|
| 发明API | 代码不编译 | 先在文档中验证方法存在 |
| 过度工程 | 3小时而不是30分钟 | 问："我有3个具体案例吗？" |
| 忽视上下文 | 建议错误技术栈 | 建议前先读现有文件 |
| 复制粘贴不理解 | 隐藏bug稍后暴露 | 解释代码做什么 |
| 空错误处理 | 生产环境静默失败 | 总是记录+类型化+重新抛出 |
| 过早抽象 | 复杂度无收益 | 证明需要前遵循YAGNI |

---

## 务实交付

**关键路径（正确做）：**
- 认证、授权
- 支付处理
- 数据完整性、迁移
- Secrets管理

**实验路径（快速交付，迭代）：**
- UI/UX特性
- 管理面板
- 分析
- 任何用户未验证的东西

关键路径测试："这能在凌晨3点叫醒我或丢钱吗？"

---

## 错误处理最佳实践

### 使用自定义异常

**Python示例：**
```python
class BusinessError(Exception):
    """业务逻辑错误的基类异常"""
    pass

class ValidationError(BusinessError):
    """验证失败"""
    pass

class NotFoundError(BusinessError):
    """资源未找到"""
    pass

class DuplicateError(BusinessError):
    """资源已存在"""
    pass
```

**Java示例：**
```java
public class BusinessException extends RuntimeException {
    private final String errorCode;

    public BusinessException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public BusinessException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
}

public class ValidationException extends BusinessException {
    public ValidationException(String message) {
        super("VALIDATION_ERROR", message);
    }
}
```

### 在正确层级处理

- **Handler/Controller**: 捕获并转换为HTTP响应
- **Service**: 抛出业务异常
- **Repository**: 让数据库异常冒泡

**示例 (Python):**
```python
# Service层 - 抛出业务异常
class UserService:
    def create_user(self, user_data):
        if self.user_repository.exists(user_data.email):
            raise DuplicateError(f"User with email {user_data.email} already exists")

        if not self._validate_email(user_data.email):
            raise ValidationError(f"Invalid email format: {user_data.email}")

        return self.user_repository.save(user_data)

# Handler层 - 捕获并转换为HTTP响应
@app.post("/users")
def create_user(request: CreateUserRequest):
    try:
        user = user_service.create_user(request)
        return JSONResponse(user.to_dict(), status_code=201)
    except ValidationError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except DuplicateError as e:
        return JSONResponse({"error": str(e)}, status_code=409)
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        return JSONResponse({"error": "Internal server error"}, status_code=500)
```

---

## 分层架构示例

### 项目结构
```
src/
├── handlers/          # HTTP/CLI处理器
│   └── user_handler.py
├── services/          # 业务逻辑
│   └── user_service.py
├── repositories/      # 数据访问
│   └── user_repository.py
├── models/            # 领域模型
│   └── user.py
└── exceptions/        # 自定义异常
    └── errors.py
```

### Handler层
```python
# handlers/user_handler.py
from flask import request, jsonify
from services.user_service import UserService
from exceptions.errors import ValidationError, DuplicateError

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self):
        try:
            data = request.get_json()
            user = self.user_service.create_user(data)
            return jsonify(user.to_dict()), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except DuplicateError as e:
            return jsonify({"error": str(e)}), 409
```

### Service层
```python
# services/user_service.py
from repositories.user_repository import UserRepository
from models.user import User
from exceptions.errors import ValidationError, DuplicateError

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, data: dict) -> User:
        # 业务验证
        if not data.get('email'):
            raise ValidationError("Email is required")

        if self.user_repository.exists_by_email(data['email']):
            raise DuplicateError(f"User with email {data['email']} already exists")

        # 创建用户
        user = User(
            email=data['email'],
            name=data.get('name'),
            created_at=datetime.utcnow()
        )

        return self.user_repository.save(user)
```

### Repository层
```python
# repositories/user_repository.py
from models.user import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user

    def exists_by_email(self, email: str) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None
```

---

## 测试最佳实践

### 单元测试结构（AAA模式）
```python
def test_create_user_success():
    # Arrange
    user_data = {"email": "test@example.com", "name": "Test User"}
    mock_repo = Mock()
    mock_repo.exists_by_email.return_value = False
    mock_repo.save.return_value = User(**user_data)
    service = UserService(mock_repo)

    # Act
    result = service.create_user(user_data)

    # Assert
    assert result.email == "test@example.com"
    assert result.name == "Test User"
    mock_repo.exists_by_email.assert_called_once_with("test@example.com")
    mock_repo.save.assert_called_once()
```

### 测试边界情况
```python
def test_create_user_duplicate_email():
    # Arrange
    user_data = {"email": "existing@example.com"}
    mock_repo = Mock()
    mock_repo.exists_by_email.return_value = True
    service = UserService(mock_repo)

    # Act & Assert
    with pytest.raises(DuplicateError):
        service.create_user(user_data)

def test_create_user_missing_email():
    # Arrange
    user_data = {"name": "Test User"}
    service = UserService(Mock())

    # Act & Assert
    with pytest.raises(ValidationError, match="Email is required"):
        service.create_user(user_data)
```

---

## 协作表

### 与其他技能的协作

| 协作技能 | 协作模式 | 说明 |
|---------|---------|------|
| **software-architect** | 咨询 | 实现前获取架构决策上下文 |
| **system-architect** | 咨询 | 项目结构问题时咨询 |
| **expert-code-quality** | 参考 | 代码实现后进行质量检查 |
| **pdd-implement-feature** | 顺序 | PDD项目功能实现 |
| **test-driven-development** | 顺序 | 先写测试再实现 |
| **expert-ruoyi** | 咨询 | 若依框架项目实现时咨询 |

### 协作流程

```
功能实现需求
    ↓
调用 software-engineer
    ↓
（如需架构决策）→ 调用 software-architect
    ↓
（如需先写测试）→ 调用 test-driven-development
    ↓
代码实现
    ↓
（如需代码质量检查）→ 调用 expert-code-quality
    ↓
功能实现完成
```

---

## 代码审查清单

提交代码前验证：

- [ ] **功能性**: 解决问题了吗？
- [ ] **测试**: 有快乐路径和边界情况的测试吗？
- [ ] **错误处理**: 错误被正确类型化和记录了吗？
- [ ] **命名**: 名称清晰且自文档化了吗？
- [ ] **结构**: 代码在正确的层了吗？
- [ ] **依赖**: 导入对项目版本正确吗？
- [ ] **安全性**: 输入被验证了吗？Secrets被正确处理了吗？
- [ ] **性能**: 有明显性能问题吗？
- [ ] **文档**: 复杂决策被文档化了吗？

---

## Guardrails

- 代码实现必须遵循项目现有的代码风格和模式
- 必须使用正确的导入和API（验证项目版本）
- 错误处理必须包含上下文，不得吞没异常
- 代码必须能编译，无占位符或TODO
- 提交前必须验证功能正确性

---

## 版本历史

### v2.0 (2026-03-21)
- 统一为中文描述
- 添加协作表，明确与其他技能的协作关系
- 增强错误处理最佳实践
- 添加分层架构示例
- 标准化输出格式

### v1.0 (初始版本)
- 基础代码实现规则
- 错误处理模式
- 测试最佳实践

---

> **记住**：好的代码不是关于聪明——而是关于清晰。编写简单、可维护、可测试的代码。
