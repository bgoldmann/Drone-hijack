# Backend Development Guidelines

Comprehensive guide for building robust, secure, and maintainable backend systems in Cursor IDE. Use these guidelines when implementing APIs, server actions, database operations, authentication, and backend services.

## Core Principles

1. **Security First**: Never trust user input. Always validate and sanitize.
2. **Explicit Over Implicit**: Make errors, types, and behaviors clear.
3. **Fail Fast**: Validate early, return clear error messages.
4. **Idempotency**: Design operations to be safely repeatable.
5. **Separation of Concerns**: Database, business logic, and API layers are distinct.

## API Design

### RESTful Conventions

Use standard HTTP methods and status codes:

```typescript
// GET - Retrieve resources
GET /api/users          // List users
GET /api/users/:id      // Get specific user

// POST - Create resources
POST /api/users         // Create new user
POST /api/users/:id/activate  // Actions as resources

// PUT/PATCH - Update resources
PUT /api/users/:id      // Full update
PATCH /api/users/:id    // Partial update

// DELETE - Remove resources
DELETE /api/users/:id   // Delete user
```

### Response Format

Use consistent response structures:

```typescript
// Success response
{
  "data": { ... },
  "meta": { // Optional pagination, etc.
    "page": 1,
    "total": 100
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "details": { // Optional field-level errors
      "email": "Must be a valid email"
    }
  }
}
```

### Status Codes

Use appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST (resource created)
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors, malformed request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict (duplicate, etc.)
- `422 Unprocessable Entity` - Business logic validation failed
- `500 Internal Server Error` - Server errors (log, don't expose details)

## Database Operations

### Migration Patterns

Always use migrations for schema changes:

```sql
-- Good: Idempotent migration
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

**Patterns:**
- Use `IF NOT EXISTS` / `IF EXISTS` for idempotency
- Always include `created_at` and `updated_at` timestamps
- Use UUIDs for primary keys (security + distributed systems)
- Add indexes for foreign keys and frequently queried columns
- Use constraints (UNIQUE, NOT NULL, CHECK) at the database level

### Query Patterns

Avoid N+1 queries:

```typescript
// BAD - N+1 query problem
const users = await db.query('SELECT * FROM users');
for (const user of users) {
  user.posts = await db.query('SELECT * FROM posts WHERE user_id = $1', [user.id]);
}

// GOOD - Single query with JOIN
const users = await db.query(`
  SELECT 
    u.*,
    json_agg(p.*) as posts
  FROM users u
  LEFT JOIN posts p ON p.user_id = u.id
  GROUP BY u.id
`);
```

**Query Best Practices:**
- Use parameterized queries (prevent SQL injection)
- Index frequently queried columns
- Use transactions for related operations
- Batch operations when possible
- Use pagination for large result sets

### Data Access Layer

Separate database logic from business logic:

```typescript
// Database layer (data access)
export async function getUserById(id: string) {
  const result = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [id]
  );
  return result.rows[0] || null;
}

// Business logic layer
export async function getUserProfile(userId: string) {
  const user = await getUserById(userId);
  if (!user) {
    throw new NotFoundError('User not found');
  }
  return sanitizeUserProfile(user); // Remove sensitive fields
}
```

## Input Validation

### Schema Validation

Validate all inputs with schemas (Zod, Yup, etc.):

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(1, 'Name is required').max(100),
});

// In handler
export async function createUser(req: Request) {
  const validation = createUserSchema.safeParse(req.body);
  if (!validation.success) {
    throw new ValidationError(validation.error.errors);
  }
  const { email, password, name } = validation.data;
  // Proceed with validated data
}
```

### Validation Rules

- **Email**: Validate format, check uniqueness
- **Passwords**: Minimum length (8+), complexity requirements
- **IDs**: Validate format (UUID, numeric)
- **Enums**: Validate against allowed values
- **Dates**: Parse and validate format
- **Strings**: Length limits, sanitize HTML/scripts

## Error Handling

### Error Types

Create specific error types:

```typescript
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500,
    public details?: any
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

class ValidationError extends AppError {
  constructor(message: string, details?: any) {
    super('VALIDATION_ERROR', message, 400, details);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super('UNAUTHORIZED', message, 401);
  }
}
```

### Error Handler Middleware

Centralized error handling:

```typescript
export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      }
    });
  }

  // Log unexpected errors (don't expose to client)
  console.error('Unexpected error:', err);
  
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}
```

## Authentication & Authorization

### Authentication

Use secure token-based authentication:

```typescript
import jwt from 'jsonwebtoken';

// Generate token
export function generateToken(userId: string): string {
  return jwt.sign(
    { userId },
    process.env.JWT_SECRET!,
    { expiresIn: '7d' }
  );
}

// Verify token middleware
export async function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    throw new UnauthorizedError();
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { userId: string };
    req.userId = decoded.userId;
    next();
  } catch (err) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

### Authorization

Check permissions at the business logic layer:

```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // Check if requester has permission
  if (userId !== requesterId && !await isAdmin(requesterId)) {
    throw new ForbiddenError('Not authorized to delete this user');
  }
  
  // Proceed with deletion
  await db.query('DELETE FROM users WHERE id = $1', [userId]);
}
```

**Authorization Patterns:**
- Role-based: Check user roles (admin, user, etc.)
- Resource-based: Check ownership of the resource
- Action-based: Check specific permissions for actions
- Always fail closed (deny by default)

## Security Best Practices

### Password Handling

Never store plain text passwords:

```typescript
import bcrypt from 'bcrypt';

// Hash password
export async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
}

// Verify password
export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### SQL Injection Prevention

Always use parameterized queries:

```typescript
// BAD - SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${email}'`;

// GOOD - Parameterized query
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);
```

### XSS Prevention

Sanitize user input and escape output:

```typescript
import DOMPurify from 'isomorphic-dompurify';

// Sanitize HTML input
export function sanitizeHtml(input: string): string {
  return DOMPurify.sanitize(input);
}

// For JSON responses, frameworks usually handle escaping
// But be careful with user-controlled JSON fields
```

### Rate Limiting

Protect against abuse:

```typescript
import rateLimit from 'express-rate-limit';

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
```

### Environment Variables

Never commit secrets:

```typescript
// BAD - Hardcoded secret
const secret = 'my-secret-key';

// GOOD - Environment variable
const secret = process.env.JWT_SECRET;
if (!secret) {
  throw new Error('JWT_SECRET environment variable is required');
}
```

## Performance Optimization

### Caching

Cache expensive operations:

```typescript
import NodeCache from 'node-cache';

const cache = new NodeCache({ stdTTL: 300 }); // 5 minutes

export async function getUserByIdCached(id: string) {
  const cacheKey = `user:${id}`;
  const cached = cache.get(cacheKey);
  
  if (cached) {
    return cached;
  }
  
  const user = await getUserById(id);
  if (user) {
    cache.set(cacheKey, user);
  }
  
  return user;
}
```

### Pagination

Always paginate large datasets:

```typescript
export async function getUsers(page: number = 1, limit: number = 20) {
  const offset = (page - 1) * limit;
  
  const [users, count] = await Promise.all([
    db.query('SELECT * FROM users LIMIT $1 OFFSET $2', [limit, offset]),
    db.query('SELECT COUNT(*) FROM users')
  ]);
  
  return {
    data: users.rows,
    pagination: {
      page,
      limit,
      total: parseInt(count.rows[0].count),
      totalPages: Math.ceil(parseInt(count.rows[0].count) / limit)
    }
  };
}
```

### Database Indexing

Add indexes for frequently queried columns:

```sql
-- Index foreign keys
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Index frequently filtered columns
CREATE INDEX idx_users_email ON users(email);

-- Composite indexes for common query patterns
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
```

## Testing

### Unit Tests

Test business logic in isolation:

```typescript
import { describe, it, expect } from 'vitest';
import { validateEmail } from './validation';

describe('validateEmail', () => {
  it('accepts valid email addresses', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  it('rejects invalid email addresses', () => {
    expect(validateEmail('invalid')).toBe(false);
  });
});
```

### Integration Tests

Test API endpoints:

```typescript
import request from 'supertest';
import { app } from './app';

describe('POST /api/users', () => {
  it('creates a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      })
      .expect(201);
    
    expect(response.body.data.email).toBe('test@example.com');
  });

  it('rejects invalid email', async () => {
    await request(app)
      .post('/api/users')
      .send({ email: 'invalid' })
      .expect(400);
  });
});
```

## Code Organization

### Project Structure

```
backend/
├── src/
│   ├── api/              # API routes/handlers
│   ├── services/         # Business logic
│   ├── db/               # Database access layer
│   ├── models/           # Data models/schemas
│   ├── middleware/       # Express middleware
│   ├── utils/            # Utility functions
│   ├── types/            # TypeScript types
│   └── config/           # Configuration
├── migrations/           # Database migrations
├── tests/                # Test files
└── scripts/              # Utility scripts
```

### Naming Conventions

- **Functions**: `camelCase` (e.g., `getUserById`)
- **Classes**: `PascalCase` (e.g., `ValidationError`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- **Files**: `kebab-case` (e.g., `user-service.ts`)
- **Database tables**: `snake_case` (e.g., `user_profiles`)

## Common Patterns

### Transaction Pattern

Use transactions for related operations:

```typescript
export async function transferMoney(fromId: string, toId: string, amount: number) {
  await db.transaction(async (client) => {
    // Deduct from sender
    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );
    
    // Add to receiver
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );
  });
}
```

### Repository Pattern

Abstract database access:

```typescript
export class UserRepository {
  async findById(id: string): Promise<User | null> {
    // Database access logic
  }

  async create(data: CreateUserData): Promise<User> {
    // Creation logic
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    // Update logic
  }
}
```

## Checklist for Backend Changes

Before committing backend code:

- [ ] All inputs validated with schemas
- [ ] Errors handled with appropriate types and status codes
- [ ] Database queries use parameterized statements
- [ ] Passwords hashed (never stored plain text)
- [ ] Authentication/authorization checks in place
- [ ] SQL queries have appropriate indexes
- [ ] No N+1 query problems
- [ ] Tests written for critical paths
- [ ] Environment variables used for secrets
- [ ] Rate limiting on public endpoints
- [ ] Logging for errors (not sensitive data)
- [ ] API responses follow consistent format
