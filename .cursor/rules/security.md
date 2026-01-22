# Security Best Practices Guide

Comprehensive security guide for web development in Cursor IDE. Covers authentication, authorization, input validation, common vulnerabilities, and security patterns.

## Core Principles

1. **Never Trust User Input**: Validate and sanitize all inputs
2. **Principle of Least Privilege**: Grant minimum necessary permissions
3. **Defense in Depth**: Multiple layers of security
4. **Secure by Default**: Secure configuration from the start
5. **Regular Updates**: Keep dependencies updated

## Authentication & Authorization

### Password Security

```typescript
import bcrypt from 'bcrypt';

// Hash password (12+ rounds recommended)
const saltRounds = 12;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// Verify password
const isValid = await bcrypt.compare(plainPassword, hashedPassword);
```

### JWT Security

```typescript
import jwt from 'jsonwebtoken';

// Sign token with expiration
const token = jwt.sign(
  { userId },
  process.env.JWT_SECRET!,
  { expiresIn: '7d' }
);

// Verify token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET!);
} catch (error) {
  // Token invalid or expired
}

// Refresh tokens for long sessions
```

### Session Management

```typescript
// Secure cookie settings
res.cookie('session', token, {
  httpOnly: true, // Prevent XSS
  secure: process.env.NODE_ENV === 'production', // HTTPS only
  sameSite: 'strict', // CSRF protection
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
});
```

## Input Validation

### Schema Validation

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().int().min(13).max(120),
});

// Validate input
const result = userSchema.safeParse(input);
if (!result.success) {
  return { error: result.error.errors };
}
```

### SQL Injection Prevention

```typescript
// BAD - SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${email}'`;

// GOOD - Parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);
```

### XSS Prevention

```typescript
// Sanitize user input
import DOMPurify from 'isomorphic-dompurify';

const cleanHtml = DOMPurify.sanitize(userInput);

// React automatically escapes by default
// But be careful with dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: cleanHtml }} />
```

## HTTPS & SSL

```typescript
// Force HTTPS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.header('x-forwarded-proto') !== 'https') {
      res.redirect(`https://${req.header('host')}${req.url}`);
    } else {
      next();
    }
  });
}
```

## Security Headers

```typescript
// Express middleware
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// Next.js headers
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  }
];
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests',
});

app.use('/api/', limiter);

// Stricter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
});

app.use('/api/auth/login', authLimiter);
```

## Environment Variables

```typescript
// Never commit secrets
// .env.local (gitignored)
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
API_KEY=your-api-key

// Validate required variables
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET'];
requiredEnvVars.forEach(envVar => {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
});
```

## CSRF Protection

```typescript
// CSRF tokens for state-changing operations
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/process', csrfProtection, (req, res) => {
  // Protected route
});
```

## File Upload Security

```typescript
// Validate file types
const allowedTypes = ['image/jpeg', 'image/png'];
if (!allowedTypes.includes(file.mimetype)) {
  throw new Error('Invalid file type');
}

// Validate file size
const maxSize = 5 * 1024 * 1024; // 5MB
if (file.size > maxSize) {
  throw new Error('File too large');
}

// Sanitize filename
const sanitizedFilename = file.originalname.replace(/[^a-zA-Z0-9.-]/g, '_');
```

## API Security

### API Keys

```typescript
// Validate API key middleware
function validateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  
  if (apiKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  
  next();
}

app.use('/api/', validateApiKey);
```

### CORS Configuration

```typescript
// Strict CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
```

## Checklist for Security

Before deploying:

- [ ] All user inputs validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (input sanitization)
- [ ] Passwords hashed (bcrypt)
- [ ] JWT tokens with expiration
- [ ] HTTPS enforced in production
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Environment variables for secrets
- [ ] API keys secured
- [ ] CORS properly configured
- [ ] File uploads validated
- [ ] Dependencies updated (npm audit)
