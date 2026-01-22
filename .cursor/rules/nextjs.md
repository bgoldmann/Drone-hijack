# Next.js Development Guide

Comprehensive guide for building applications with Next.js in Cursor IDE. Covers App Router, Server Components, Server Actions, routing, data fetching, and optimization.

## Overview

Next.js 13+ features:
- **App Router**: File-based routing with layouts
- **Server Components**: Components that render on the server by default
- **Server Actions**: Server-side functions called from client components
- **Streaming**: Progressive page rendering
- **Image Optimization**: Automatic image optimization
- **API Routes**: Serverless API endpoints

## Project Structure

```
app/
├── layout.tsx              # Root layout
├── page.tsx                # Home page
├── (routes)/
│   ├── about/
│   │   └── page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── blog/
│       ├── [slug]/
│       │   └── page.tsx
│       └── page.tsx
├── api/
│   └── users/
│       └── route.ts
└── components/
    ├── client-component.tsx
    └── server-component.tsx
```

## Routing

### File-Based Routing

```typescript
// app/page.tsx - Home page (/)
export default function Home() {
  return <div>Home</div>;
}

// app/about/page.tsx - /about
export default function About() {
  return <div>About</div>;
}

// app/blog/[slug]/page.tsx - /blog/:slug
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <div>Post: {params.slug}</div>;
}

// app/shop/[...slug]/page.tsx - /shop/* (catch-all)
export default function Shop({ params }: { params: { slug: string[] } }) {
  return <div>Shop: {params.slug.join('/')}</div>;
}
```

### Layouts

```typescript
// app/layout.tsx - Root layout
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}

// app/dashboard/layout.tsx - Nested layout
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Sidebar />
      <main>{children}</main>
    </div>
  );
}
```

### Navigation

```typescript
'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();
  const router = useRouter();
  
  return (
    <nav>
      <Link href="/" className={pathname === '/' ? 'active' : ''}>
        Home
      </Link>
      <Link href="/about">About</Link>
      <button onClick={() => router.push('/dashboard')}>
        Go to Dashboard
      </button>
    </nav>
  );
}
```

## Server Components vs Client Components

### Server Components (Default)

```typescript
// app/components/data.tsx - Server Component
// No 'use client' directive

async function DataComponent() {
  // Direct database/API access (runs on server)
  const data = await fetchData();
  
  return <div>{data}</div>;
}
```

### Client Components

```typescript
'use client';

import { useState, useEffect } from 'react';

export function ClientComponent() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    // Client-side effects
  }, []);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

## Data Fetching

### Server Components

```typescript
// app/users/page.tsx
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    cache: 'no-store', // Always fetch fresh
    // or
    // next: { revalidate: 3600 } // Revalidate every hour
  });
  
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

export default async function UsersPage() {
  const users = await getUsers();
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### Loading States

```typescript
// app/users/loading.tsx
export default function Loading() {
  return <div>Loading users...</div>;
}

// app/users/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Suspense

```typescript
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <UserList />
      </Suspense>
    </div>
  );
}
```

## Server Actions

```typescript
// app/actions/user.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  
  // Validate
  if (!name || !email) {
    return { error: 'Missing required fields' };
  }
  
  // Create user (database operation)
  const user = await db.user.create({ data: { name, email } });
  
  // Revalidate cache
  revalidatePath('/users');
  
  return { success: true, user };
}

// app/components/user-form.tsx
'use client';

import { createUser } from '@/app/actions/user';

export function UserForm() {
  async function handleSubmit(formData: FormData) {
    const result = await createUser(formData);
    if (result.error) {
      alert(result.error);
    }
  }
  
  return (
    <form action={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  );
}
```

## API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await getUsers();
  return NextResponse.json({ users });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await createUser(body);
  return NextResponse.json({ user }, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await getUserById(params.id);
  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  return NextResponse.json({ user });
}
```

## Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: '/dashboard/:path*',
};
```

## Metadata & SEO

```typescript
// app/page.tsx
export const metadata = {
  title: 'Home Page',
  description: 'Welcome to our site',
};

// Or dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      images: [post.image],
    },
  };
}
```

## Image Optimization

```typescript
import Image from 'next/image';

export function OptimizedImage() {
  return (
    <Image
      src="/image.jpg"
      alt="Description"
      width={800}
      height={600}
      priority // Load immediately
      placeholder="blur" // Blur placeholder
    />
  );
}

// Remote images
<Image
  src="https://example.com/image.jpg"
  alt="Description"
  width={800}
  height={600}
  unoptimized // Or configure next.config.js
/>
```

## Caching & Revalidation

```typescript
// Static (build time)
export const revalidate = false; // Default for static pages

// ISR (Incremental Static Regeneration)
export const revalidate = 3600; // Revalidate every hour

// Dynamic (always fetch fresh)
export const dynamic = 'force-dynamic';
export const revalidate = 0;

// Cache control
fetch(url, {
  cache: 'no-store', // Always fetch
  // or
  next: { revalidate: 3600 }, // Revalidate after 1 hour
});
```

## Best Practices

### 1. Use Server Components by Default

Only use `'use client'` when necessary (interactivity, hooks, browser APIs).

### 2. Colocate Components

Keep components close to where they're used.

### 3. Error Boundaries

```typescript
// app/error.tsx - Root error boundary
'use client';

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### 4. Not Found Pages

```typescript
// app/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  );
}
```

## Checklist for Next.js

Before deploying:

- [ ] Server Components used by default
- [ ] Client Components marked with 'use client'
- [ ] Data fetching with proper caching strategy
- [ ] Loading states for async operations
- [ ] Error boundaries implemented
- [ ] Metadata configured for SEO
- [ ] Images optimized with next/image
- [ ] API routes handle errors properly
- [ ] Middleware configured (if needed)
- [ ] Static generation used where possible
- [ ] ISR configured for dynamic content
