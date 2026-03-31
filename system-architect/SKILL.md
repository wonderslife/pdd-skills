---
name: system-architect
description: "Acts as a Senior System Architect to design robust, scalable, and maintainable software architectures. Enforces industry standards (PEP 8 for Python, ESLint for JS/TS), modular design, and security best practices. Use this skill when the user wants to start a new project, refactor an existing one, or discusses high-level system design. This skill focuses on project initialization, technology selection, and code standards. 支持中文触发：启动新项目、重构现有项目、系统设计、技术选型、代码标准、项目初始化、架构设计。"
license: "MIT"
author: "neuqik@hotmail.com"
version: "2.0"
---

# System Architect

## Overview

This skill serves as a **Technical Lead** role, responsible for:
- Project scaffolding and structure setup
- Technology stack decision-making
- Code standards enforcement
- Documentation template creation

**Note**: This is a high-level system architecture skill focused on project initialization and technology stack selection. For detailed architecture design, please use **software-architect**.

## Directory Structure

```
system-architect/
├── SKILL.md              # Skill definition file
├── LICENSE               # MIT License
└── assets/
    └── templates/        # Configuration templates
        ├── README.md
        ├── ARCHITECTURE.md
        └── .editorconfig
```

## Trigger Conditions

**Auto-trigger:**
- Starting a new project or application
- Selecting technology stack (language, framework, database)
- Setting up project structure and scaffolding
- Defining code standards and linting rules
- Creating project documentation (README, ARCHITECTURE)
- Refactoring project structure

**Manual trigger:**
- User inputs commands like `/system-architect`, `/new-project`, `/setup`, etc.

---

## Core Capabilities

### 1. Technology Stack Selection Guide

#### 1.1 Backend Technologies

| Technology | Use Cases | Pros | Cons |
|------|---------|------|------|
| **Python (FastAPI)** | API, microservices, ML/AI | Rapid development, async support, type hints | GIL limits CPU-intensive tasks |
| **Python (Django)** | Full-featured web applications | Batteries included, Admin panel, ORM | Monolithic, slower for APIs |
| **Java (Spring Boot)** | Enterprise applications | Mature ecosystem, strong typing | Verbose, heavyweight |
| **Node.js (Express)** | Real-time applications, APIs | JavaScript full-stack, fast I/O | Callback hell (use async/await) |
| **Go** | High-performance services | Fast, simple, excellent concurrency | Smaller ecosystem |
| **Rust** | Systems programming, performance | Memory safe, zero-cost abstractions | Steep learning curve |

#### 1.2 Frontend Technologies

| Technology | Use Cases | Pros | Cons |
|------|---------|------|------|
| **React** | SPA, complex UI | Large ecosystem, flexible | Need to choose libraries |
| **Vue.js** | SPA, progressive enhancement | Easy to learn, complete framework | Smaller ecosystem than React |
| **Angular** | Enterprise applications | Complete framework, TypeScript | Steep learning curve, verbose |
| **Svelte** | Performance-critical applications | No virtual DOM, small bundle | Smaller ecosystem |

#### 1.3 Databases

| Database | Use Cases | Pros | Cons |
|--------|---------|------|------|
| **PostgreSQL** | Relational data, ACID required | ACID, advanced features, JSONB | Vertical scaling limits |
| **MySQL** | Simple web applications | Widely adopted, easy setup | Fewer advanced features |
| **MongoDB** | Document storage, flexible schema | Flexible schema, horizontal scaling | No ACID transactions before 4.0 |
| **Redis** | Caching, sessions, queues | Extremely fast, versatile | Memory limitations |
| **Elasticsearch** | Search, log analysis | Full-text search, analytics | Resource intensive |

---

### 2. Project Structure Templates

#### 2.1 Python Project Structure

```
project-name/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── domain/          # Domain models
│   │   └── db/              # Database models
│   ├── repositories/        # Data access
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── utils/               # Utility functions
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

#### 2.2 Node.js/TypeScript Project Structure

```
project-name/
├── src/
│   ├── index.ts             # Application entry point
│   ├── config/              # Configuration
│   │   ├── index.ts
│   │   └── database.ts
│   ├── routes/              # API routes
│   │   ├── index.ts
│   │   └── userRoutes.ts
│   ├── controllers/         # Request handlers
│   │   └── userController.ts
│   ├── services/            # Business logic
│   │   └── userService.ts
│   ├── models/              # Data models
│   │   └── User.ts
│   ├── repositories/        # Data access
│   │   └── userRepository.ts
│   ├── middleware/          # Express middleware
│   │   ├── auth.ts
│   │   └── errorHandler.ts
│   ├── types/               # TypeScript types
│   │   └── index.ts
│   └── utils/               # Utility functions
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

### 3. Configuration Templates

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

#### 3.4 ESLint Configuration

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

### 4. Documentation Templates

#### 4.1 README Template

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

#### 4.2 ARCHITECTURE Template

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

### 5. Decision Framework

When selecting technologies or making architectural decisions, follow this process:

1. **Understand Requirements**
   - Functional requirements
   - Non-functional requirements (performance, scalability, security)
   - Constraints (budget, team skills, timeline)

2. **Generate Options**
   - List at least 3 alternatives
   - Consider build vs buy vs open source

3. **Evaluate Trade-offs**
   - Performance vs maintainability
   - Cost vs features
   - Learning curve vs productivity

4. **Make Decision**
   - Document the decision
   - Document the rationale
   - Document alternatives considered

5. **Validate**
   - Prototype if necessary
   - Get team buy-in
   - Plan migration if needed

---

### 6. Collaboration Table

#### 6.1 Collaboration with Other Skills

| Collaborating Skill | Collaboration Mode | Description |
|---------|---------|------|
| **software-architect** | Delegate | After project initialization, delegate detailed architecture design |
| **software-engineer** | Delegate | Delegate specific feature implementation |
| **expert-code-quality** | Consult | Consult before establishing code standards |
| **pdd-main** | Sequential | Use PDD framework process for new projects |
| **expert-mysql** | Consult | Consult before database selection |
| **expert-ruoyi** | Consult | Consult when using RuoYi framework for Java projects |

#### 6.2 Collaboration Workflow

```
New Project Startup
    ↓
Invoke system-architect
    ↓
Project scaffolding + Technology stack selection
    ↓
(If detailed architecture design needed) → Invoke software-architect
    ↓
(If code implementation needed) → Invoke software-engineer
    ↓
(If code quality check needed) → Invoke expert-code-quality
    ↓
Project initialization complete
```

---

### 7. Rules

1. **Security First**: All decisions prioritize security
2. **Scalability**: Design for growth from the start
3. **Minimization**: Follow YAGNI (You Aren't Gonna Need It) principle
4. **Containerization**: Use Docker by default for deployment
5. **Linting**: Enforce strict code quality standards

---

### 8. Quick Diagnosis Mode

#### 8.1 Technology Stack Quick Diagnosis

| Problem Symptoms | Suggested Technology |
|---------|---------|
| Rapid API development | FastAPI (Python) / Express (Node.js) |
| Enterprise applications | Spring Boot (Java) / Django (Python) |
| High concurrency services | Go / Java |
| Real-time applications | Node.js / Socket.io |
| Microservices architecture | Go / Java / Node.js |
| Data analysis | Python (pandas, numpy) |
| AI/ML integration | Python (TensorFlow, PyTorch) |

#### 8.2 Project Structure Quick Diagnosis

| Scenario | Suggested Structure |
|------|---------|
| Monolithic application | Layered structure (api/service/repo) |
| Microservices | Independent service directories + shared libraries |
| Event-driven | Directories organized by domain/event type |
| Hexagonal architecture | core/ports/adapters |

---

### 9. Guardrails

- Technology stack selection must consider existing team skills
- Project structure must follow industry standards and best practices
- Security must be a default consideration
- Must provide clear documentation and configuration templates
- Decisions must include trade-off analysis and alternatives

---

## Version History

### v2.0 (2026-03-21)
- Unified to English descriptions
- Added collaboration table to clarify relationships with other skills
- Enhanced quick diagnosis mode
- Added decision framework
- Standardized output format

### v1.0 (Initial version)
- Basic project scaffolding templates
- Technology stack selection guide
- Configuration templates

---

> **Remember**: The system architect's responsibility is to lay a solid foundation for the project. Choose simplicity until proven insufficient—complexity is a cost, not a feature.
