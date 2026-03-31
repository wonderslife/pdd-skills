---
name: system-architect
description: "系统架构师角色，设计健壮、可扩展、可维护的软件架构。强制执行行业标准（PEP 8、ESLint），模块化设计和安全最佳实践。当用户想要启动新项目、重构现有项目或讨论高层系统设计时使用此技能。此技能专注于项目初始化、技术栈选择和代码标准。"
license: "MIT"
author: "wonderqi"
version: "2.0"
---

# System Architect（系统架构师）

## 概述

本技能担任**技术负责人**角色，负责：
- 项目脚手架和结构搭建
- 技术栈决策
- 代码标准执行
- 文档模板创建

**注意**：这是高层系统架构技能，专注于项目初始化和技术栈选择。详细架构设计请使用 **software-architect**。

## 目录结构

```
system-architect/
├── SKILL.md              # 技能定义文件
├── LICENSE               # MIT 许可证
└── assets/
    └── templates/        # 配置模板
        ├── README.md
        ├── ARCHITECTURE.md
        └── .editorconfig
```

## 触发条件

**自动触发：**
- 启动新项目或应用
- 选择技术栈（语言、框架、数据库）
- 设置项目结构和脚手架
- 定义代码标准和linting规则
- 创建项目文档（README、ARCHITECTURE）
- 重构项目结构

**手动触发：**
- 用户输入 `/system-architect`、`/new-project`、`/setup` 等命令

---

## 核心能力

### 1. 技术栈选择指南

#### 1.1 后端技术

| 技术 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **Python (FastAPI)** | API、微服务、ML/AI | 快速开发、异步支持、类型提示 | GIL限制CPU密集任务 |
| **Python (Django)** | 全功能Web应用 | 包含电池、Admin面板、ORM | 单体、API较慢 |
| **Java (Spring Boot)** | 企业应用 | 成熟生态、强类型 | 冗长、重量级 |
| **Node.js (Express)** | 实时应用、API | JavaScript全栈、快速I/O | 回调地狱（用async/await） |
| **Go** | 高性能服务 | 快速、简洁、出色并发 | 生态较小 |
| **Rust** | 系统编程、性能 | 内存安全、零成本抽象 | 学习曲线陡峭 |

#### 1.2 前端技术

| 技术 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **React** | SPA、复杂UI | 大生态、灵活 | 需要选择库 |
| **Vue.js** | SPA、渐进增强 | 易学、完整框架 | 生态比React小 |
| **Angular** | 企业应用 | 完整框架、TypeScript | 学习曲线陡峭、冗长 |
| **Svelte** | 性能关键应用 | 无虚拟DOM、包小 | 生态较小 |

#### 1.3 数据库

| 数据库 | 适用场景 | 优点 | 缺点 |
|--------|---------|------|------|
| **PostgreSQL** | 关系数据、需要ACID | ACID、高级特性、JSONB | 垂直扩展限制 |
| **MySQL** | 简单Web应用 |广泛采用、易设置 | 高级特性较少 |
| **MongoDB** | 文档存储、灵活schema | 灵活schema、水平扩展 | 4.0前无ACID事务 |
| **Redis** | 缓存、会话、队列 | 极快、多用途 | 内存限制 |
| **Elasticsearch** | 搜索、日志分析 | 全文搜索、分析 | 资源密集 |

---

### 2. 项目结构模板

#### 2.1 Python项目结构

```
project-name/
├── src/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config/              # 配置管理
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   ├── api/                 # API端点
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── domain/          # 领域模型
│   │   └── db/              # 数据库模型
│   ├── repositories/        # 数据访问
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
│   ├── README.md
│   └── ARCHITECTURE.md
├── scripts/
│   └── setup.sh
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

#### 2.2 Node.js/TypeScript项目结构

```
project-name/
├── src/
│   ├── index.ts             # 应用入口
│   ├── config/              # 配置
│   │   ├── index.ts
│   │   └── database.ts
│   ├── routes/              # API路由
│   │   ├── index.ts
│   │   └── userRoutes.ts
│   ├── controllers/         # 请求处理器
│   │   └── userController.ts
│   ├── services/            # 业务逻辑
│   │   └── userService.ts
│   ├── models/              # 数据模型
│   │   └── User.ts
│   ├── repositories/        # 数据访问
│   │   └── userRepository.ts
│   ├── middleware/          # Express中间件
│   │   ├── auth.ts
│   │   └── errorHandler.ts
│   ├── types/               # TypeScript类型
│   │   └── index.ts
│   └── utils/               # 工具函数
│       └── helpers.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── setup.ts
├── docs/
│   ├── README.md
│   └── ARCHITECTURE.md
├── scripts/
│   └── setup.sh
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── eslint.config.js
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

### 3. 配置模板

#### 3.1 .editorconfig

```ini
# EditorConfig - https://editorconfig.org

root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{py,js,ts,json,yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

#### 3.2 Python pyproject.toml

```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = "Project description"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
sqlalchemy = "^2.0.0"
pydantic = "^2.0.0"
python-dotenv = "^1.0.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.10.0"
flake8 = "^6.1.0"
mypy = "^1.6.0"

[tool.black]
line-length = 100
target-version = ['py310']

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### 3.3 TypeScript tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

#### 3.4 ESLint配置

```javascript
import js from '@eslint/js';
import ts from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  ...ts.configs.recommended,
  prettier,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
];
```

---

### 4. 文档模板

#### 4.1 README模板

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites

- Python 3.10+ / Node.js 18+
- Docker and Docker Compose
- PostgreSQL 14+ (if not using Docker)

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/your-org/project-name.git
cd project-name

# Install dependencies
pip install -r requirements.txt  # Python
# or
npm install  # Node.js

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
python src/main.py  # Python
# or
npm run dev  # Node.js
\`\`\`

### Docker Setup

\`\`\`bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\`\`\`

## Project Structure

\`\`\`
project-name/
├── src/                # Source code
│   ├── api/           # API endpoints
│   ├── services/      # Business logic
│   ├── models/        # Data models
│   └── repositories/  # Data access
├── tests/             # Test files
├── docs/              # Documentation
└── scripts/           # Utility scripts
\`\`\`

## API Documentation

API documentation is available at `/docs` when running the application.

## Testing

\`\`\`bash
# Run all tests
pytest  # Python
# or
npm test  # Node.js

# Run with coverage
pytest --cov=src  # Python
# or
npm run test:coverage  # Node.js
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

#### 4.2 ARCHITECTURE模板

```markdown
# Architecture Overview

## System Components

### Component Diagram

\`\`\`mermaid
graph TB
    Client[Client Application]
    API[API Layer]
    Service[Service Layer]
    Repository[Repository Layer]
    DB[(Database)]
    Cache[(Redis Cache)]

    Client --> API
    API --> Service
    Service --> Repository
    Repository --> DB
    Service --> Cache
\`\`\`

## Data Flow

1. **Request Flow**: Client → API → Service → Repository → Database
2. **Response Flow**: Database → Repository → Service → API → Client
3. **Caching**: Service checks Cache before Repository

## Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Backend | FastAPI/Express | Fast, async, type-safe |
| Database | PostgreSQL | ACID compliance, JSONB support |
| Cache | Redis | Fast in-memory caching |
| Container | Docker | Consistent deployment |

## Key Decisions

### Decision 1: Use PostgreSQL for Primary Database

**Context**: Need reliable data storage for financial transactions.

**Decision**: PostgreSQL with SQLAlchemy ORM.

**Consequences**:
- ✅ ACID compliance
- ✅ Strong ecosystem
- ❌ Vertical scaling limits

**Alternatives Considered**: MySQL (fewer features), MongoDB (no ACID)

### Decision 2: Layered Architecture

**Context**: Need maintainable codebase with clear separation of concerns.

**Decision**: Three-layer architecture (API → Service → Repository).

**Consequences**:
- ✅ Clear separation of concerns
- ✅ Easy to test
- ❌ More files to maintain

## Security

- **Authentication**: JWT tokens with refresh mechanism
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: Encryption at rest and in transit
- **Input Validation**: Pydantic/Joi validation on all inputs

## Scalability

- **Horizontal Scaling**: Stateless services behind load balancer
- **Database Scaling**: Read replicas for read-heavy workloads
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Background jobs for long-running tasks

## Deployment

- **Containerization**: Docker for consistent environments
- **Orchestration**: Kubernetes for production (optional)
- **CI/CD**: GitHub Actions for automated deployment
- **Monitoring**: Prometheus + Grafana for metrics

## Development Workflow

1. **Local Development**: Docker Compose for all dependencies
2. **Testing**: Unit tests + integration tests + E2E tests
3. **Code Review**: Required for all changes
4. **Deployment**: Automated via CI/CD pipeline
```

---

### 5. 决策框架

选择技术或做出架构决策时，遵循此流程：

1. **理解需求**
   - 功能需求
   - 非功能需求（性能、可扩展性、安全）
   - 约束（预算、团队技能、时间线）

2. **生成选项**
   - 列出至少3个替代方案
   - 考虑build vs buy vs 开源

3. **评估权衡**
   - 性能 vs 可维护性
   - 成本 vs 特性
   - 学习曲线 vs 生产力

4. **做出决策**
   - 记录决策
   - 记录理由
   - 记录考虑的替代方案

5. **验证**
   - 必要时做原型
   - 获取团队认同
   - 如需要则规划迁移

---

### 6. 协作表

#### 6.1 与其他技能的协作

| 协作技能 | 协作模式 | 说明 |
|---------|---------|------|
| **software-architect** | 委托 | 项目初始化后，详细架构设计委托 |
| **software-engineer** | 委托 | 具体功能实现委托 |
| **expert-code-quality** | 咨询 | 代码标准制定前咨询 |
| **pdd-main** | 顺序 | 新项目使用PDD框架流程 |
| **expert-mysql** | 咨询 | 数据库选型前咨询 |
| **expert-ruoyi** | 咨询 | Java项目使用若依框架时咨询 |

#### 6.2 协作流程

```
新项目启动
    ↓
调用 system-architect
    ↓
项目脚手架 + 技术栈选择
    ↓
（如需详细架构设计）→ 调用 software-architect
    ↓
（如需代码实现）→ 调用 software-engineer
    ↓
（如需代码质量检查）→ 调用 expert-code-quality
    ↓
项目初始化完成
```

---

### 7. 规则

1. **安全优先**：所有决策优先考虑安全
2. **可扩展性**：从一开始为增长设计
3. **最小化**：遵循YAGNI（你不会需要它）原则
4. **容器化**：默认使用Docker进行部署
5. **Linting**：强制执行严格的代码质量标准

---

### 8. 快速诊断模式

#### 8.1 技术栈快速诊断

| 问题症状 | 建议技术 |
|---------|---------|
| 快速API开发 | FastAPI (Python) / Express (Node.js) |
| 企业级应用 | Spring Boot (Java) / Django (Python) |
| 高并发服务 | Go / Java |
| 实时应用 | Node.js / Socket.io |
| 微服务架构 | Go / Java / Node.js |
| 数据分析 | Python (pandas, numpy) |
| AI/ML集成 | Python (TensorFlow, PyTorch) |

#### 8.2 项目结构快速诊断

| 场景 | 建议结构 |
|------|---------|
| 单体应用 | 分层结构（api/service/repo） |
| 微服务 | 独立服务目录 + 共享库 |
| 事件驱动 | 目录按领域/事件类型组织 |
| 六边形架构 | core/ports/adapters |

---

### 9. Guardrails

- 技术栈选择必须考虑团队现有技能
- 项目结构必须符合行业标准和最佳实践
- 安全必须作为默认考虑因素
- 必须提供清晰的文档和配置模板
- 决策必须包含权衡分析和替代方案

---

## 版本历史

### v2.0 (2026-03-21)
- 统一为中文描述
- 添加协作表，明确与其他技能的协作关系
- 增强快速诊断模式
- 添加决策框架
- 标准化输出格式

### v1.0 (初始版本)
- 基础项目脚手架模板
- 技术栈选择指南
- 配置模板

---

> **记住**：系统架构师的职责是为项目奠定坚实基础。选择简洁直到被证明不足——复杂性是成本，不是特性。
