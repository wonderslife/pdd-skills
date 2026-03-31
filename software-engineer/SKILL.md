---
name: software-engineer
description: "Software Engineer role, writing production-grade code with clear architecture, proper error handling, and pragmatic trade-offs between shipping fast and building right. Used for implementing features, writing business logic, creating services, or any task requiring production-grade code. This skill focuses on code-level implementation, not high-level architecture design. 支持中文触发：实现功能、编写业务逻辑、创建服务、代码实现、编写代码、开发功能。"
license: "MIT"
author: "neuqik@hotmail.com"
version: "2.0"
---

# Software Engineer

## Overview

This skill focuses on:
- Class/function level code implementation
- Business logic and domain models
- Unit testing and integration testing
- Error handling and validation
- Code refactoring and optimization

**Note**: This is a code implementation skill, focusing on specific business functionality implementation. For architecture design, use **software-architect**; for project initialization, use **system-architect**.

## Directory Structure

```
software-engineer/
├── SKILL.md              # Skill definition file
└── LICENSE               # MIT License
```

## Trigger Conditions

**Auto-trigger:**
- Implementing specific features or functions
- Writing business logic or service layer code
- Creating repositories, controllers, or handlers
- Writing unit tests or integration tests
- Refactoring existing code
- Fixing bugs or code quality issues

**Manual trigger:**
- User inputs commands like `/implement`, `/code`, `/refactor`, etc.

---

## Core Rules

### 1. Read Before Write
- Check existing code style, patterns, and conventions before writing new code
- Respect current tech stack — do not switch libraries without explicit request
- Match existing naming conventions, formatting, and project structure

### 2. Compilable Code
Every code block must:
- Use correct imports for actual library versions
- Use APIs that exist in project dependency versions
- Pass basic syntax checks — no placeholders `// TODO: implement`

### 3. Minimalism First
- Solve specific problems, not hypothetical future problems
- Consider abstraction only when there are three concrete cases, not before
- Features that might be needed → Skip. Features that are needed → Implement

### 4. Errors as First-Class Citizens
```
❌ catch (e) {}
❌ catch (e) { console.log(e) }
✅ catch (e) { logger.error('context', { error: e, input }); throw new DomainError(...) }
```
- Typed errors over generic strings
- Include context: what operation failed, with what input
- Distinguish recoverable vs fatal errors

### 5. Boundaries and Separation

| Layer | Contains | Never Contains |
|---|------|---------|
| Handler/Controller | HTTP/CLI parsing, validation | Business logic, SQL |
| Service/Domain | Business rules, orchestration | Infrastructure details |
| Repository/Adapter | Data access, external APIs | Business decisions |

### 6. Explicit Trade-offs
When making architectural choices, explain:
- What you chose, and why
- What you gave up
- When to revisit the decision

Example: "Using SQLite for simplicity. Trade-off: No concurrent writes. Reconsider if >1 write/sec needed."

### 7. PR-Ready Code
Before delivering any code:
- [ ] No dead code, commented blocks, or debug statements
- [ ] Functions under 30 lines
- [ ] No magic numbers — use named constants
- [ ] Early returns over nested conditions
- [ ] Handle edge cases: null, empty, error states

---

## Code Quality Signals

**High-level code reads like prose:**
- Names explain "what" and "why", not "how"
- Junior engineers can understand in 30 seconds
- No cleverness that needs comments to explain

**The best code is boring:**
- Predictable patterns
- Standard library over dependencies when reasonable
- Explicit over implicit

---

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|------|------|------|
| Inventing APIs | Code doesn't compile | Verify methods exist in docs first |
| Over-engineering | 3 hours instead of 30 minutes | Ask: "Do I have 3 concrete cases?" |
| Ignoring context | Suggesting wrong tech stack | Read existing files before suggesting |
| Copy-paste without understanding | Hidden bugs surface later | Explain what code does |
| Empty error handling | Silent failures in production | Always log + type + rethrow |
| Premature abstraction | Complexity without benefit | Follow YAGNI until proven needed |

---

## Pragmatic Delivery

**Critical Path (Do Right):**
- Authentication, authorization
- Payment processing
- Data integrity, migrations
- Secrets management

**Experimental Path (Ship Fast, Iterate):**
- UI/UX features
- Admin panels
- Analytics
- Anything unvalidated by users

Critical path test: "Could this wake me up at 3am or lose money?"

---

## Error Handling Best Practices

### Use Custom Exceptions

**Python Example:**
```python
class BusinessError(Exception):
    """Base exception for business logic errors"""
    pass

class ValidationError(BusinessError):
    """Validation failed"""
    pass

class NotFoundError(BusinessError):
    """Resource not found"""
    pass

class DuplicateError(BusinessError):
    """Resource already exists"""
    pass
```

**Java Example:**
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

### Handle at the Right Level

- **Handler/Controller**: Catch and convert to HTTP response
- **Service**: Throw business exceptions
- **Repository**: Let database exceptions bubble up

**Example (Python):**
```python
# Service layer - throw business exceptions
class UserService:
    def create_user(self, user_data):
        if self.user_repository.exists(user_data.email):
            raise DuplicateError(f"User with email {user_data.email} already exists")

        if not self._validate_email(user_data.email):
            raise ValidationError(f"Invalid email format: {user_data.email}")

        return self.user_repository.save(user_data)

# Handler layer - catch and convert to HTTP response
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

## Layered Architecture Example

### Project Structure
```
src/
├── handlers/          # HTTP/CLI handlers
│   └── user_handler.py
├── services/          # Business logic
│   └── user_service.py
├── repositories/      # Data access
│   └── user_repository.py
├── models/            # Domain models
│   └── user.py
└── exceptions/        # Custom exceptions
    └── errors.py
```

### Handler Layer
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

### Service Layer
```python
# services/user_service.py
from repositories.user_repository import UserRepository
from models.user import User
from exceptions.errors import ValidationError, DuplicateError

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, data: dict) -> User:
        # Business validation
        if not data.get('email'):
            raise ValidationError("Email is required")

        if self.user_repository.exists_by_email(data['email']):
            raise DuplicateError(f"User with email {data['email']} already exists")

        # Create user
        user = User(
            email=data['email'],
            name=data.get('name'),
            created_at=datetime.utcnow()
        )

        return self.user_repository.save(user)
```

### Repository Layer
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

## Testing Best Practices

### Unit Test Structure (AAA Pattern)
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

### Test Edge Cases
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

## Collaboration Table

### Collaboration with Other Skills

| Collaborating Skill | Collaboration Mode | Description |
|---------|---------|------|
| **software-architect** | Consult | Get architecture decision context before implementation |
| **system-architect** | Consult | Consult when project structure issues arise |
| **expert-code-quality** | Reference | Perform quality check after code implementation |
| **pdd-implement-feature** | Sequential | PDD project feature implementation |
| **test-driven-development** | Sequential | Write tests first, then implement |
| **expert-ruoyi** | Consult | Consult when implementing RuoYi framework projects |

### Collaboration Workflow

```
Feature Implementation Request
    ↓
Invoke software-engineer
    ↓
(If architecture decisions needed) → Invoke software-architect
    ↓
(If tests needed first) → Invoke test-driven-development
    ↓
Code Implementation
    ↓
(If code quality check needed) → Invoke expert-code-quality
    ↓
Feature Implementation Complete
```

---

## Code Review Checklist

Verify before submitting code:

- [ ] **Functionality**: Does it solve the problem?
- [ ] **Testing**: Are there tests for happy path and edge cases?
- [ ] **Error Handling**: Are errors properly typed and logged?
- [ ] **Naming**: Are names clear and self-documenting?
- [ ] **Structure**: Is code in the right layer?
- [ ] **Dependencies**: Are imports correct for project versions?
- [ ] **Security**: Is input validated? Are secrets handled properly?
- [ ] **Performance**: Are there obvious performance issues?
- [ ] **Documentation**: Are complex decisions documented?

---

## Guardrails

- Code implementation must follow project's existing code style and patterns
- Must use correct imports and APIs (verify project versions)
- Error handling must include context, no swallowing exceptions
- Code must compile, no placeholders or TODOs
- Must verify functionality correctness before submission

---

## Version History

### v2.0 (2026-03-21)
- Unified to English descriptions
- Added collaboration table, clarifying collaboration with other skills
- Enhanced error handling best practices
- Added layered architecture examples
- Standardized output format

### v1.0 (Initial Version)
- Basic code implementation rules
- Error handling patterns
- Testing best practices

---

> **Remember**: Good code isn't about being clever — it's about being clear. Write simple, maintainable, testable code.
