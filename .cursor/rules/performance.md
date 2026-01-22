# Performance Optimization Guide

Comprehensive guide for optimizing application performance in Cursor IDE. Covers frontend optimization, backend optimization, database queries, caching, and monitoring.

## Frontend Optimization

### Code Splitting

```typescript
// Lazy load components
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
    </Suspense>
  );
}

// Dynamic imports
const loadModule = async () => {
  const module = await import('./heavy-module');
  return module.default;
};
```

### Image Optimization

```typescript
// Next.js Image component
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  loading="lazy" // Lazy load
  placeholder="blur" // Blur placeholder
/>
```

### Bundle Size

```typescript
// Analyze bundle
npm run build -- --analyze

// Tree shaking
// Use ES modules and avoid side effects

// Remove unused code
// Use barrel exports carefully
```

### Memoization

```typescript
import { useMemo, useCallback } from 'react';

// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

## Backend Optimization

### Database Queries

```typescript
// Avoid N+1 queries
// BAD
const users = await db.user.findMany();
for (const user of users) {
  user.posts = await db.post.findMany({ where: { userId: user.id } });
}

// GOOD - Use joins or includes
const users = await db.user.findMany({
  include: { posts: true },
});
```

### Caching

```typescript
// In-memory cache
import NodeCache from 'node-cache';

const cache = new NodeCache({ stdTTL: 300 });

async function getCachedData(key: string) {
  const cached = cache.get(key);
  if (cached) return cached;
  
  const data = await fetchData();
  cache.set(key, data);
  return data;
}

// HTTP cache headers
res.setHeader('Cache-Control', 'public, max-age=3600');
```

### Connection Pooling

```typescript
// Database connection pool
const pool = new Pool({
  max: 20, // Maximum connections
  min: 5,  // Minimum connections
  idleTimeoutMillis: 30000,
});
```

## Checklist for Performance

Before deploying:

- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] Bundle size analyzed and optimized
- [ ] Expensive operations memoized
- [ ] Database queries optimized (no N+1)
- [ ] Caching strategy implemented
- [ ] Connection pooling configured
- [ ] Performance monitoring set up
