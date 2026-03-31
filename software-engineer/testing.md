# Testing Practices — Software Engineer

## Test Pyramid

```
        ╱╲
       ╱E2E╲        Few: Critical user flows
      ╱──────╲
     ╱ Integr. ╲    Some: API endpoints, DB queries
    ╱────────────╲
   ╱    Unit      ╲  Many: Pure functions, business logic
  ╱────────────────╲
```

## Unit Test Structure

**Arrange-Act-Assert:**
```typescript
test('calculateDiscount applies 10% for orders over 100', () => {
  // Arrange
  const order = { total: 150 };
  
  // Act
  const discount = calculateDiscount(order);
  
  // Assert
  expect(discount).toBe(15);
});
```

**Test naming:** `[function] [scenario] [expected result]`

## What to Test

| Test | Don't Test |
|------|------------|
| Business logic | Framework internals |
| Edge cases: null, empty, limits | Getters/setters |
| Error paths | Third-party libraries |
| Public API | Implementation details |

## Edge Cases to Cover

Every function should test:
- [ ] Happy path
- [ ] Empty input (`[]`, `""`, `{}`)
- [ ] Null/undefined input
- [ ] Boundary values (0, -1, max)
- [ ] Invalid input types
- [ ] Error conditions

## Mocking Strategy

**Mock when:**
- External APIs (network)
- Database (for unit tests)
- Time-dependent code
- Random/non-deterministic behavior

**Don't mock:**
- Your own code (test the real thing)
- Pure utility functions
- Data structures

```typescript
// ✅ Mock external service
const mockPaymentService = {
  charge: jest.fn().mockResolvedValue({ success: true })
};

// ❌ Don't mock your own functions
const mockCalculateTotal = jest.fn(); // Test the real one
```

## Integration Test Patterns

```typescript
describe('POST /users', () => {
  beforeEach(async () => {
    await db.clear('users');
  });

  test('creates user with valid data', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test' });

    expect(response.status).toBe(201);
    expect(response.body.data.email).toBe('test@example.com');
    
    // Verify side effects
    const user = await db.findOne('users', { email: 'test@example.com' });
    expect(user).toBeDefined();
  });

  test('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({ email: 'not-an-email', name: 'Test' });

    expect(response.status).toBe(400);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## Assertions

```
❌ expect(result).toBeTruthy()     // Too vague
❌ expect(result).toBeDefined()    // Doesn't check value
✅ expect(result).toBe(42)         // Exact value
✅ expect(result).toEqual({ ... }) // Object equality
✅ expect(fn).toThrow(CustomError) // Specific error type
```

## Test Cleanup

```typescript
afterEach(() => {
  jest.clearAllMocks();  // Reset call counts
});

afterAll(async () => {
  await db.close();      // Close connections
});
```

## Flaky Test Prevention

- Don't depend on execution order
- Don't share state between tests
- Use fixed timestamps in tests
- Seed random generators
- Wait for async operations properly (no arbitrary sleeps)
