# Code Patterns — Software Engineer

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Boolean | `is`, `has`, `should`, `can` | `isActive`, `hasPermission` |
| Function | verb + noun | `getUserById`, `validateEmail` |
| Handler | `handle` + event | `handleSubmit`, `handleError` |
| Transform | `to` + target | `toDTO`, `toJSON` |

**Avoid:** `data`, `info`, `temp`, `result`, `handle` without context.

## Function Structure

```
function goodFunction(input) {
  // 1. Validate early, return/throw fast
  if (!input) throw new ValidationError('input required');
  
  // 2. Main logic (single responsibility)
  const processed = transform(input);
  
  // 3. Return explicitly
  return processed;
}
```

**Max lines:** 20-30. If longer, extract.

## Error Handling Patterns

### Typed Errors
```typescript
class DomainError extends Error {
  constructor(
    message: string,
    public code: string,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'DomainError';
  }
}

// Usage
throw new DomainError('User not found', 'USER_NOT_FOUND', { userId });
```

### Result Pattern (No Exceptions)
```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function divide(a: number, b: number): Result<number, 'DIVISION_BY_ZERO'> {
  if (b === 0) return { ok: false, error: 'DIVISION_BY_ZERO' };
  return { ok: true, value: a / b };
}
```

## Conditional Patterns

### Early Returns
```
// ❌ Pyramid
function process(user) {
  if (user) {
    if (user.active) {
      if (user.verified) {
        return doWork(user);
      }
    }
  }
  return null;
}

// ✅ Flat
function process(user) {
  if (!user) return null;
  if (!user.active) return null;
  if (!user.verified) return null;
  return doWork(user);
}
```

### Guard Clauses
Put validation at the top, happy path at the bottom.

## Async Patterns

### Sequential (when order matters)
```javascript
const user = await getUser(id);
const orders = await getOrders(user.id);
const summary = await buildSummary(orders);
```

### Parallel (when independent)
```javascript
const [user, config, permissions] = await Promise.all([
  getUser(id),
  getConfig(),
  getPermissions(id)
]);
```

### Error Boundaries
```javascript
try {
  await riskyOperation();
} catch (error) {
  if (error instanceof NetworkError) {
    // Retry logic
  } else if (error instanceof ValidationError) {
    // Return user-friendly message
  } else {
    // Log and rethrow unknown errors
    logger.error('Unexpected error', { error });
    throw error;
  }
}
```

## Immutability Patterns

```javascript
// ❌ Mutation
user.name = newName;
users.push(newUser);

// ✅ New object
const updatedUser = { ...user, name: newName };
const updatedUsers = [...users, newUser];
```

## Dependency Injection (Simple)

```typescript
// ❌ Hard coupling
class UserService {
  private db = new Database();
}

// ✅ Injection
class UserService {
  constructor(private db: Database) {}
}

// Usage
const service = new UserService(new PostgresDatabase());
const testService = new UserService(new MockDatabase());
```
