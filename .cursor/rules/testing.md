# Testing Guide

Comprehensive guide for writing tests in Cursor IDE. Covers unit tests, integration tests, E2E tests, mocking, and test patterns for JavaScript/TypeScript, Python, and React.

## Overview

Types of tests:
- **Unit Tests**: Test individual functions/components in isolation
- **Integration Tests**: Test multiple components/services working together
- **E2E Tests**: Test complete user flows in a real browser
- **Snapshot Tests**: Verify UI output hasn't changed unexpectedly

## JavaScript/TypeScript Testing

### Jest/Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom', // For React component testing
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});

// package.json scripts
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage"
  }
}
```

### Unit Tests

```typescript
// utils/calculate.test.ts
import { describe, it, expect } from 'vitest';
import { calculateTotal, formatCurrency } from './calculate';

describe('calculateTotal', () => {
  it('should sum array of numbers', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle negative numbers', () => {
    expect(calculateTotal([-1, 2, -3])).toBe(-2);
  });
});

describe('formatCurrency', () => {
  it('should format number as currency', () => {
    expect(formatCurrency(1000)).toBe('$1,000.00');
  });

  it('should handle decimal values', () => {
    expect(formatCurrency(99.99)).toBe('$99.99');
  });
});
```

### React Component Tests

```typescript
// components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

### Testing Async Code

```typescript
// services/api.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchUser } from './api';

describe('fetchUser', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('should fetch user data', async () => {
    const mockUser = { id: 1, name: 'John' };
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const user = await fetchUser(1);
    expect(user).toEqual(mockUser);
    expect(global.fetch).toHaveBeenCalledWith('/api/users/1');
  });

  it('should throw error on fetch failure', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('Network error'));

    await expect(fetchUser(1)).rejects.toThrow('Network error');
  });
});
```

### Mocking

```typescript
// Mock modules
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

// Mock functions
const mockFn = vi.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: 'value' });
mockFn.mockRejectedValue(new Error('Error'));

// Mock timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();
```

## Python Testing (FastAPI)

### Pytest Setup

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*

# conftest.py - Shared fixtures
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db():
    # Setup test database
    yield
    # Teardown
```

### Unit Tests

```python
# tests/test_utils.py
import pytest
from app.utils import calculate_total, validate_email

def test_calculate_total():
    assert calculate_total([1, 2, 3]) == 6
    assert calculate_total([]) == 0
    assert calculate_total([-1, 2]) == 1

def test_validate_email():
    assert validate_email("user@example.com") == True
    assert validate_email("invalid") == False
    assert validate_email("") == False

@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("test@domain", False),
])
def test_validate_email_multiple(email, expected):
    assert validate_email(email) == expected
```

### API Integration Tests

```python
# tests/test_api.py
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user(client):
    response = client.post(
        "/api/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
```

### Database Tests

```python
# tests/test_database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    user = User(email="test@example.com", name="Test")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
```

## E2E Testing

### Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
  },
});
```

### E2E Test Examples

```typescript
// e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });
});
```

## Test Patterns

### Arrange-Act-Assert (AAA)

```typescript
describe('UserService', () => {
  it('should update user email', async () => {
    // Arrange
    const userId = '123';
    const newEmail = 'new@example.com';
    const mockUser = { id: userId, email: 'old@example.com' };
    mockAPI.getUser.mockResolvedValue(mockUser);

    // Act
    const updated = await userService.updateEmail(userId, newEmail);

    // Assert
    expect(updated.email).toBe(newEmail);
    expect(mockAPI.updateUser).toHaveBeenCalledWith(userId, { email: newEmail });
  });
});
```

### Test Fixtures

```typescript
// Shared test utilities
export function createMockUser(overrides = {}) {
  return {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    ...overrides,
  };
}

// Usage
const user = createMockUser({ email: 'custom@example.com' });
```

### Test Coverage

```bash
# Run with coverage
npm test -- --coverage

# Coverage thresholds
// vitest.config.ts
coverage: {
  thresholds: {
    lines: 80,
    functions: 80,
    branches: 80,
    statements: 80,
  },
}
```

## Best Practices

### 1. Test Independence

Each test should be independent and not rely on other tests:

```typescript
// BAD - Tests depend on order
describe('User', () => {
  let user;
  
  it('creates user', () => {
    user = createUser(); // Used in next test
  });
  
  it('updates user', () => {
    updateUser(user.id); // Depends on previous test
  });
});

// GOOD - Each test is independent
describe('User', () => {
  it('creates user', () => {
    const user = createUser();
    expect(user.id).toBeDefined();
  });
  
  it('updates user', () => {
    const user = createUser();
    const updated = updateUser(user.id);
    expect(updated).toBeDefined();
  });
});
```

### 2. Descriptive Test Names

```typescript
// BAD
it('works', () => { ... });
it('test1', () => { ... });

// GOOD
it('should return error when email is invalid', () => { ... });
it('should calculate total price with tax correctly', () => { ... });
```

### 3. Test What Matters

```typescript
// Don't test implementation details
it('should call setState', () => { ... }); // BAD

// Test behavior
it('should update displayed count when button clicked', () => { ... }); // GOOD
```

### 4. Clean Up

```typescript
afterEach(() => {
  vi.clearAllMocks();
  vi.useRealTimers();
});

afterAll(() => {
  // Cleanup test database, etc.
});
```

## Checklist for Testing

Before committing:

- [ ] Unit tests for utility functions
- [ ] Component tests for UI components
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical user flows
- [ ] Error cases tested
- [ ] Edge cases covered
- [ ] Mocks used for external dependencies
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe what they test
- [ ] Coverage meets project standards
