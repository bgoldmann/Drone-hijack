# PostgreSQL Development Guide

Comprehensive guide for working with PostgreSQL databases in Cursor IDE. Covers SQL queries, migrations, indexing, optimization, transactions, and best practices.

## Overview

PostgreSQL is a powerful open-source relational database that provides:
- **ACID Compliance**: Transactions with atomicity, consistency, isolation, durability
- **Rich Data Types**: JSON, arrays, geometric types, and more
- **Advanced Features**: Full-text search, window functions, CTEs, recursive queries
- **Extensions**: Extensible with PostGIS, pg_trgm, and many others
- **Performance**: Excellent query optimization and indexing capabilities

## Setup & Installation

### Node.js (pg)

```bash
npm install pg
npm install -D @types/pg
```

### Python (psycopg2)

```bash
pip install psycopg2-binary
```

### Connection Pooling

```bash
# Node.js
npm install pg-pool

# Python
pip install SQLAlchemy
```

## Connection Setup

### Node.js Connection

```typescript
// lib/db.ts
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export default pool;

// Query helper
export async function query(text: string, params?: any[]) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
  } catch (error) {
    console.error('Query error', { text, error });
    throw error;
  }
}
```

### Python Connection

```python
# lib/db.py
import psycopg2
from psycopg2 import pool
import os

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min, max connections
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
)

def get_connection():
    return connection_pool.getconn()

def put_connection(conn):
    connection_pool.putconn(conn)

def query(text, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(text, params)
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        put_connection(conn)
```

## Basic Queries

### SELECT

```sql
-- Basic select
SELECT id, name, email FROM users;

-- With WHERE clause
SELECT * FROM users WHERE email = 'user@example.com';

-- With multiple conditions
SELECT * FROM users 
WHERE status = 'active' 
  AND created_at > '2024-01-01'
  AND age BETWEEN 18 AND 65;

-- With IN clause
SELECT * FROM users WHERE id IN (1, 2, 3);

-- With LIKE pattern
SELECT * FROM users WHERE name LIKE 'John%';

-- With NULL check
SELECT * FROM users WHERE email IS NOT NULL;

-- With LIMIT and OFFSET
SELECT * FROM users ORDER BY created_at DESC LIMIT 10 OFFSET 20;

-- Distinct values
SELECT DISTINCT status FROM users;
```

### INSERT

```sql
-- Single insert
INSERT INTO users (name, email, age) 
VALUES ('John Doe', 'john@example.com', 30);

-- Multiple inserts
INSERT INTO users (name, email, age) 
VALUES 
  ('John Doe', 'john@example.com', 30),
  ('Jane Smith', 'jane@example.com', 25),
  ('Bob Johnson', 'bob@example.com', 35);

-- Returning inserted row
INSERT INTO users (name, email, age)
VALUES ('John Doe', 'john@example.com', 30)
RETURNING id, name, email;
```

### UPDATE

```sql
-- Basic update
UPDATE users 
SET email = 'newemail@example.com'
WHERE id = 1;

-- Multiple columns
UPDATE users 
SET 
  name = 'John Updated',
  email = 'newemail@example.com',
  updated_at = NOW()
WHERE id = 1;

-- Conditional update
UPDATE users 
SET status = 'inactive'
WHERE last_login < NOW() - INTERVAL '90 days';

-- Returning updated rows
UPDATE users 
SET status = 'active'
WHERE id IN (1, 2, 3)
RETURNING id, name, status;
```

### DELETE

```sql
-- Delete with condition
DELETE FROM users WHERE id = 1;

-- Delete multiple
DELETE FROM users WHERE status = 'deleted';

-- Soft delete (preferred pattern)
UPDATE users 
SET deleted_at = NOW(), status = 'deleted'
WHERE id = 1;

-- Hard delete (use with caution)
DELETE FROM users WHERE id = 1;
```

## Advanced Queries

### JOINs

```sql
-- INNER JOIN
SELECT 
  u.id,
  u.name,
  u.email,
  p.title,
  p.content
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE u.status = 'active';

-- LEFT JOIN
SELECT 
  u.id,
  u.name,
  COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name;

-- RIGHT JOIN
SELECT 
  p.id,
  p.title,
  u.name as author_name
FROM posts p
RIGHT JOIN users u ON p.user_id = u.id;

-- FULL OUTER JOIN
SELECT 
  u.id,
  u.name,
  p.title
FROM users u
FULL OUTER JOIN posts p ON u.id = p.user_id;

-- Multiple JOINs
SELECT 
  u.name,
  p.title,
  c.content as comment
FROM users u
INNER JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON p.id = c.post_id;
```

### Aggregations

```sql
-- COUNT
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(DISTINCT user_id) as unique_authors FROM posts;

-- SUM, AVG, MIN, MAX
SELECT 
  SUM(amount) as total_revenue,
  AVG(amount) as average_order,
  MIN(amount) as smallest_order,
  MAX(amount) as largest_order
FROM orders;

-- GROUP BY
SELECT 
  user_id,
  COUNT(*) as post_count,
  MAX(created_at) as latest_post
FROM posts
GROUP BY user_id;

-- HAVING (filter after GROUP BY)
SELECT 
  user_id,
  COUNT(*) as post_count
FROM posts
GROUP BY user_id
HAVING COUNT(*) > 5;
```

### Window Functions

```sql
-- ROW_NUMBER
SELECT 
  id,
  name,
  email,
  ROW_NUMBER() OVER (ORDER BY created_at) as row_num
FROM users;

-- RANK and DENSE_RANK
SELECT 
  user_id,
  amount,
  RANK() OVER (ORDER BY amount DESC) as rank,
  DENSE_RANK() OVER (ORDER BY amount DESC) as dense_rank
FROM orders;

-- PARTITION BY
SELECT 
  user_id,
  post_id,
  created_at,
  COUNT(*) OVER (PARTITION BY user_id) as total_user_posts
FROM posts;

-- Running totals
SELECT 
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM daily_sales;
```

### Common Table Expressions (CTEs)

```sql
-- Simple CTE
WITH active_users AS (
  SELECT * FROM users WHERE status = 'active'
)
SELECT * FROM active_users;

-- Multiple CTEs
WITH 
  recent_posts AS (
    SELECT * FROM posts WHERE created_at > NOW() - INTERVAL '7 days'
  ),
  post_stats AS (
    SELECT 
      user_id,
      COUNT(*) as post_count
    FROM recent_posts
    GROUP BY user_id
  )
SELECT 
  u.name,
  ps.post_count
FROM users u
INNER JOIN post_stats ps ON u.id = ps.user_id;
```

### Recursive CTEs

```sql
-- Hierarchical data (e.g., categories, comments)
WITH RECURSIVE category_tree AS (
  -- Base case
  SELECT id, name, parent_id, 1 as level
  FROM categories
  WHERE parent_id IS NULL
  
  UNION ALL
  
  -- Recursive case
  SELECT 
    c.id,
    c.name,
    c.parent_id,
    ct.level + 1
  FROM categories c
  INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

## Indexes

### Creating Indexes

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index (index subset of rows)
CREATE INDEX idx_active_users_email ON users(email) 
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Full-text search index
CREATE INDEX idx_posts_content_search ON posts 
USING GIN(to_tsvector('english', content));
```

### Index Types

```sql
-- B-tree (default) - for most queries
CREATE INDEX idx_users_created_at ON users(created_at);

-- Hash - for equality only
CREATE INDEX idx_users_email_hash ON users USING HASH(email);

-- GIN - for full-text search, arrays, JSONB
CREATE INDEX idx_posts_tags_gin ON posts USING GIN(tags);

-- GiST - for geometric data, full-text search
CREATE INDEX idx_locations_point_gist ON locations USING GIST(point);
```

### Index Maintenance

```sql
-- Analyze table (update statistics)
ANALYZE users;

-- Rebuild index
REINDEX INDEX idx_users_email;

-- Drop index
DROP INDEX IF EXISTS idx_users_email;

-- Check index usage
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## Transactions

### Basic Transaction

```sql
BEGIN;

INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
INSERT INTO posts (user_id, title) VALUES (LASTVAL(), 'First Post');

COMMIT;

-- Or rollback on error
BEGIN;
-- ... operations ...
ROLLBACK;
```

### Transaction in Code (Node.js)

```typescript
async function createUserWithPost(userData: any, postData: any) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    const userResult = await client.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id',
      [userData.name, userData.email]
    );
    const userId = userResult.rows[0].id;
    
    await client.query(
      'INSERT INTO posts (user_id, title, content) VALUES ($1, $2, $3)',
      [userId, postData.title, postData.content]
    );
    
    await client.query('COMMIT');
    return userId;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

### Savepoints

```sql
BEGIN;

INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
SAVEPOINT user_created;

INSERT INTO posts (user_id, title) VALUES (LASTVAL(), 'First Post');
-- If error occurs:
ROLLBACK TO SAVEPOINT user_created;

-- Continue or commit
COMMIT;
```

## Migrations

### Migration Pattern

```sql
-- migrations/001_create_users.sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/002_add_users_status.sql
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'active';

CREATE INDEX idx_users_status ON users(status);

-- migrations/003_create_posts.sql
CREATE TABLE IF NOT EXISTS posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  status VARCHAR(50) DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status);
```

### Using Migration Tools

```bash
# Node.js: node-pg-migrate
npm install -D node-pg-migrate

# Create migration
npx node-pg-migrate create add_users_table

# Run migrations
npx node-pg-migrate up

# Rollback
npx node-pg-migrate down
```

### Migration Best Practices

- Always use `IF NOT EXISTS` / `IF EXISTS` when possible
- Include both `up` and `down` migrations
- Test migrations on staging first
- Never modify existing migrations after they've run in production
- Use transactions for migrations when possible

## JSON and JSONB

### Working with JSONB

```sql
-- Create table with JSONB
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  metadata JSONB,
  tags JSONB DEFAULT '[]'::JSONB
);

-- Insert JSON data
INSERT INTO products (name, metadata, tags)
VALUES (
  'Product 1',
  '{"price": 100, "category": "electronics"}'::JSONB,
  '["tag1", "tag2"]'::JSONB
);

-- Query JSON fields
SELECT * FROM products WHERE metadata->>'category' = 'electronics';
SELECT * FROM products WHERE metadata->>'price'::INTEGER > 50;

-- Check if key exists
SELECT * FROM products WHERE metadata ? 'price';

-- Update JSON field
UPDATE products 
SET metadata = jsonb_set(metadata, '{price}', '150'::jsonb)
WHERE id = 1;

-- Append to JSONB array
UPDATE products 
SET tags = tags || '["newtag"]'::jsonb
WHERE id = 1;

-- Index JSONB fields
CREATE INDEX idx_products_metadata_gin ON products USING GIN(metadata);
CREATE INDEX idx_products_category ON products ((metadata->>'category'));
```

## Full-Text Search

### Setting Up Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE posts ADD COLUMN search_vector tsvector;

-- Create trigger to update search vector
CREATE TRIGGER posts_search_vector_update
BEFORE INSERT OR UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);

-- Create GIN index
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Search
SELECT 
  id,
  title,
  ts_rank(search_vector, query) as rank
FROM posts, to_tsquery('english', 'search & term') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

## Performance Optimization

### Query Optimization

```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Check query plan
EXPLAIN (FORMAT JSON) SELECT * FROM users WHERE email = 'test@example.com';

-- Identify slow queries
SELECT 
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Connection Pooling

```typescript
// Use connection pooling (shown in Connection Setup section)
// Set appropriate pool size based on application needs
const pool = new Pool({
  max: 20, // Adjust based on load
  idleTimeoutMillis: 30000,
});
```

### Prepared Statements

```typescript
// PostgreSQL automatically caches prepared statements
// But you can use explicit prepared statements for complex queries

async function getUserById(id: number) {
  const query = {
    text: 'SELECT * FROM users WHERE id = $1',
    values: [id],
  };
  return await pool.query(query);
}
```

## Security

### SQL Injection Prevention

```typescript
// ✅ Always use parameterized queries
async function getUserByEmail(email: string) {
  return await pool.query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );
}

// ❌ Never concatenate user input
async function getUserByEmailBad(email: string) {
  return await pool.query(
    `SELECT * FROM users WHERE email = '${email}'` // VULNERABLE!
  );
}
```

### Row-Level Security

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY posts_user_policy ON posts
  FOR ALL
  TO authenticated_user
  USING (user_id = current_user_id());

-- Check current user function
CREATE FUNCTION current_user_id() RETURNS INTEGER AS $$
  SELECT id FROM users WHERE email = current_setting('app.current_user_email');
$$ LANGUAGE sql STABLE;
```

## Best Practices

### 1. Always Use Parameterized Queries

Prevent SQL injection by always using parameters:

```typescript
// ✅ Good
await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

// ❌ Bad
await pool.query(`SELECT * FROM users WHERE id = ${userId}`);
```

### 2. Use Transactions for Multi-Step Operations

```typescript
const client = await pool.connect();
try {
  await client.query('BEGIN');
  // ... multiple operations ...
  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
} finally {
  client.release();
}
```

### 3. Index Strategically

- Index foreign keys
- Index frequently queried columns
- Index columns used in WHERE, ORDER BY, JOIN
- Use composite indexes for multi-column queries
- Monitor index usage and remove unused indexes

### 4. Use Appropriate Data Types

```sql
-- Use VARCHAR with length limits
name VARCHAR(255) NOT NULL

-- Use TEXT for long content
content TEXT

-- Use appropriate numeric types
price DECIMAL(10, 2)  -- For currency
quantity INTEGER      -- For counts

-- Use TIMESTAMP WITH TIME ZONE
created_at TIMESTAMPTZ DEFAULT NOW()

-- Use UUID for distributed systems
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

### 5. Normalize Data

Avoid storing redundant data. Use foreign keys and JOINs instead.

### 6. Use Soft Deletes

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Instead of DELETE, use:
UPDATE users SET deleted_at = NOW() WHERE id = 1;

-- Filter deleted records in queries
SELECT * FROM users WHERE deleted_at IS NULL;
```

### 7. Monitor Query Performance

Regularly check slow queries and optimize them:

```sql
SELECT * FROM pg_stat_statements 
ORDER BY mean_exec_time DESC;
```

## Checklist for PostgreSQL Development

Before committing PostgreSQL-related code:

- [ ] All queries use parameterized statements (no SQL injection risk)
- [ ] Transactions used for multi-step operations
- [ ] Appropriate indexes created for query patterns
- [ ] Foreign keys defined with proper constraints
- [ ] Migrations tested on staging environment
- [ ] Soft deletes implemented (if needed)
- [ ] JSONB indexes created for JSON queries
- [ ] Full-text search indexes created (if applicable)
- [ ] Connection pooling configured appropriately
- [ ] Query performance analyzed with EXPLAIN ANALYZE
- [ ] Row-level security enabled (if multi-tenant)
- [ ] Backup strategy in place
- [ ] Data types appropriate for use case
- [ ] NULL constraints defined correctly