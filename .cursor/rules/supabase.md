# Supabase Development Guide

Comprehensive guide for using Supabase in Cursor IDE for authentication, database operations, real-time features, and storage. Covers integration with Next.js and FastAPI.

## Overview

Supabase provides:
- **PostgreSQL Database**: Full PostgreSQL with PostgREST API
- **Authentication**: Built-in auth with JWT tokens
- **Row Level Security (RLS)**: Database-level security policies
- **Real-time**: WebSocket subscriptions to database changes
- **Storage**: File storage with CDN
- **Edge Functions**: Serverless functions at the edge

## Setup & Configuration

### Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# .env (FastAPI/Backend)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # Server-side only!
SUPABASE_ANON_KEY=your-anon-key
```

**Critical**: Never expose `SERVICE_ROLE_KEY` in frontend code. It bypasses RLS.

### Client Initialization

#### Next.js (Client & Server)

```typescript
// lib/supabase/client.ts - Browser client
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}

// lib/supabase/server.ts - Server components/actions
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              cookieStore.set(name, value, options);
            });
          } catch (error) {
            // Handle cookie setting errors
          }
        },
      },
    }
  );
}
```

#### FastAPI (Python)

```python
# lib/supabase/client.py
from supabase import create_client, Client
import os

def create_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")  # Service role for backend
    
    return create_client(url, key)

# For user-authenticated requests, use anon key with user's JWT
def create_user_client(jwt_token: str) -> Client:
    url = os.environ.get("SUPABASE_URL")
    anon_key = os.environ.get("SUPABASE_ANON_KEY")
    
    return create_client(url, anon_key, {
        "headers": {
            "Authorization": f"Bearer {jwt_token}"
        }
    })
```

## Authentication

### Sign Up

#### Next.js

```typescript
import { createClient } from '@/lib/supabase/client';

export async function signUp(email: string, password: string) {
  const supabase = createClient();
  
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`,
    },
  });
  
  if (error) throw error;
  return data;
}
```

#### FastAPI

```python
from supabase import create_client

def sign_up(email: str, password: str):
    supabase = create_supabase_client()
    
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })
    
    if response.user:
        return response.user
    else:
        raise Exception("Sign up failed")
```

### Sign In

#### Next.js

```typescript
export async function signIn(email: string, password: string) {
  const supabase = createClient();
  
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  if (error) throw error;
  return data;
}
```

### Sign Out

```typescript
export async function signOut() {
  const supabase = createClient();
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}
```

### Get Current User

#### Next.js (Server)

```typescript
import { createClient } from '@/lib/supabase/server';

export async function getCurrentUser() {
  const supabase = await createClient();
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error || !user) return null;
  return user;
}
```

#### Next.js (Client)

```typescript
import { createClient } from '@/lib/supabase/client';
import { useEffect, useState } from 'react';

export function useUser() {
  const [user, setUser] = useState(null);
  const supabase = createClient();
  
  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });
    
    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );
    
    return () => subscription.unsubscribe();
  }, []);
  
  return user;
}
```

### Auth Callback (Email Verification)

```typescript
// app/auth/callback/route.ts (Next.js App Router)
import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  
  if (code) {
    const supabase = await createClient();
    await supabase.auth.exchangeCodeForSession(code);
  }
  
  return NextResponse.redirect(new URL('/dashboard', requestUrl.origin));
}
```

## Database Operations

### Querying Data

#### Next.js (Server Actions)

```typescript
import { createClient } from '@/lib/supabase/server';

export async function getUsers() {
  const supabase = await createClient();
  
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .order('created_at', { ascending: false });
  
  if (error) throw error;
  return data;
}

// With filters
export async function getUserByEmail(email: string) {
  const supabase = await createClient();
  
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('email', email)
    .single();  // Expect single result
  
  if (error) throw error;
  return data;
}
```

#### FastAPI

```python
def get_users():
    supabase = create_supabase_client()
    
    response = supabase.table("users").select("*").order("created_at", desc=True).execute()
    return response.data

def get_user_by_email(email: str):
    supabase = create_supabase_client()
    
    response = supabase.table("users").select("*").eq("email", email).single().execute()
    return response.data
```

### Inserting Data

```typescript
export async function createUser(userData: {
  email: string;
  name: string;
}) {
  const supabase = await createClient();
  
  const { data, error } = await supabase
    .from('users')
    .insert(userData)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

### Updating Data

```typescript
export async function updateUser(userId: string, updates: Partial<User>) {
  const supabase = await createClient();
  
  const { data, error } = await supabase
    .from('users')
    .update(updates)
    .eq('id', userId)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

### Deleting Data

```typescript
export async function deleteUser(userId: string) {
  const supabase = await createClient();
  
  const { error } = await supabase
    .from('users')
    .delete()
    .eq('id', userId);
  
  if (error) throw error;
}
```

### Advanced Queries

```typescript
// Joins
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:users(*),
    comments:comments(*)
  `);

// Pagination
const { data } = await supabase
  .from('posts')
  .select('*')
  .range(0, 9);  // First 10 items

// Filtering
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('status', 'published')
  .gt('views', 100)
  .or('category.eq.tech,category.eq.design');

// Full-text search
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', 'search term');
```

## Row Level Security (RLS)

### Enabling RLS

```sql
-- Enable RLS on a table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Policy Examples

```sql
-- Users can only read their own posts
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own posts
CREATE POLICY "Users can insert own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Public read access
CREATE POLICY "Posts are publicly readable"
ON posts FOR SELECT
USING (status = 'published');

-- Admin full access (using service role key bypasses RLS)
-- Service role is used server-side only
```

### Checking RLS in Code

```typescript
// Client-side queries automatically respect RLS
const { data } = await supabase
  .from('posts')
  .select('*');
// Only returns posts user can access based on RLS policies

// Server-side with service role bypasses RLS
// Use carefully - prefer using user's JWT token when possible
```

## Real-time Subscriptions

### Subscribing to Changes

```typescript
// Next.js Client Component
'use client';

import { useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';

export function PostsList() {
  const supabase = createClient();
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    // Initial fetch
    supabase
      .from('posts')
      .select('*')
      .then(({ data }) => setPosts(data || []));
    
    // Subscribe to changes
    const channel = supabase
      .channel('posts-changes')
      .on(
        'postgres_changes',
        {
          event: '*',  // INSERT, UPDATE, DELETE
          schema: 'public',
          table: 'posts',
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setPosts((prev) => [payload.new, ...prev]);
          } else if (payload.eventType === 'UPDATE') {
            setPosts((prev) =>
              prev.map((post) =>
                post.id === payload.new.id ? payload.new : post
              )
            );
          } else if (payload.eventType === 'DELETE') {
            setPosts((prev) =>
              prev.filter((post) => post.id !== payload.old.id)
            );
          }
        }
      )
      .subscribe();
    
    return () => {
      supabase.removeChannel(channel);
    };
  }, []);
  
  return <div>{/* Render posts */}</div>;
}
```

## Storage

### Uploading Files

```typescript
export async function uploadFile(file: File, bucket: string = 'public') {
  const supabase = createClient();
  
  const fileExt = file.name.split('.').pop();
  const fileName = `${Math.random()}.${fileExt}`;
  const filePath = `uploads/${fileName}`;
  
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(filePath, file);
  
  if (error) throw error;
  return data;
}
```

### Getting Public URL

```typescript
export function getPublicUrl(bucket: string, path: string) {
  const supabase = createClient();
  
  const { data } = supabase.storage
    .from(bucket)
    .getPublicUrl(path);
  
  return data.publicUrl;
}
```

### Downloading Files

```typescript
export async function downloadFile(bucket: string, path: string) {
  const supabase = createClient();
  
  const { data, error } = await supabase.storage
    .from(bucket)
    .download(path);
  
  if (error) throw error;
  return data;
}
```

## Database Functions (Edge Functions)

### Creating a Function

```sql
-- supabase/migrations/20240101000000_create_function.sql
CREATE OR REPLACE FUNCTION get_user_stats(user_id UUID)
RETURNS JSON AS $$
BEGIN
  RETURN json_build_object(
    'total_posts', (SELECT COUNT(*) FROM posts WHERE user_id = $1),
    'total_likes', (SELECT COUNT(*) FROM likes WHERE user_id = $1)
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Calling from Code

```typescript
const { data, error } = await supabase.rpc('get_user_stats', {
  user_id: userId,
});
```

## Best Practices

### 1. Always Use RLS

Enable RLS on all tables containing user data:

```sql
-- Never create tables without RLS for user data
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  content TEXT NOT NULL
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### 2. Use TypeScript Types

Generate types from your database:

```bash
# Install Supabase CLI
npm install supabase --save-dev

# Generate types
npx supabase gen types typescript --project-id your-project-id > types/supabase.ts
```

```typescript
import type { Database } from '@/types/supabase';

const supabase = createClient<Database>();
```

### 3. Server vs Client Clients

- **Browser**: Use `createBrowserClient` - respects RLS, uses user's session
- **Server (Next.js)**: Use `createServerClient` - has access to cookies, uses user's session
- **Backend (FastAPI)**: Use service role for admin operations, user JWT for user operations

### 4. Error Handling

```typescript
const { data, error } = await supabase
  .from('posts')
  .select('*');

if (error) {
  if (error.code === 'PGRST116') {
    // No rows returned
    return [];
  }
  // Handle other errors
  throw new Error(error.message);
}

return data;
```

### 5. Migrations

Always use migrations for schema changes:

```sql
-- supabase/migrations/20240101000000_add_status_to_posts.sql
ALTER TABLE posts
ADD COLUMN status TEXT DEFAULT 'draft'
CHECK (status IN ('draft', 'published', 'archived'));
```

### 6. Indexes

Add indexes for frequently queried columns:

```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

## Common Patterns

### User Profile Pattern

```typescript
// Create profile on user signup
export async function createUserProfile(userId: string, data: {
  email: string;
  name?: string;
}) {
  const supabase = createClient();
  
  const { error } = await supabase
    .from('profiles')
    .insert({
      id: userId,  // Use auth.users.id as FK
      email: data.email,
      name: data.name,
    });
  
  if (error) throw error;
}
```

### Transaction Pattern (Using Database Functions)

```sql
CREATE OR REPLACE FUNCTION transfer_money(
  from_account_id UUID,
  to_account_id UUID,
  amount DECIMAL
)
RETURNS VOID AS $$
BEGIN
  UPDATE accounts SET balance = balance - amount WHERE id = from_account_id;
  UPDATE accounts SET balance = balance + amount WHERE id = to_account_id;
END;
$$ LANGUAGE plpgsql;
```

## Checklist for Supabase Changes

Before committing Supabase-related code:

- [ ] RLS enabled on new tables with appropriate policies
- [ ] Migrations created for schema changes
- [ ] Indexes added for frequently queried columns
- [ ] Service role key never exposed in frontend code
- [ ] Types generated and used (`supabase gen types`)
- [ ] Error handling for all Supabase operations
- [ ] Real-time subscriptions cleaned up (unsubscribe in cleanup)
- [ ] Storage buckets have appropriate policies
- [ ] Auth callbacks configured correctly
- [ ] Environment variables documented in `.env.example`
