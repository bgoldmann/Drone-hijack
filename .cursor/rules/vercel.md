# Vercel Deployment Guide

Comprehensive guide for deploying and managing applications on Vercel in Cursor IDE. Covers Next.js deployment, serverless functions, edge functions, environment variables, and optimization.

## Overview

Vercel provides:
- **Automatic Deployments**: Git-based continuous deployment
- **Next.js Optimization**: Built-in optimizations for Next.js apps
- **Serverless Functions**: API routes and serverless functions
- **Edge Functions**: Deploy code at the edge for low latency
- **Preview Deployments**: Automatic preview URLs for PRs
- **Analytics**: Performance and usage analytics

## Setup & Installation

### Install Vercel CLI

```bash
npm install -g vercel
```

### Login

```bash
vercel login
```

### Link Project

```bash
# In your project directory
vercel link

# Or deploy for first time
vercel
```

## Project Configuration

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

### Next.js Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static exports if needed
  // output: 'export',
  
  // Image optimization
  images: {
    domains: ['example.com'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Environment variables (public)
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  
  // Experimental features
  experimental: {
    // Add experimental features here
  },
}

module.exports = nextConfig
```

## Environment Variables

### Setting Environment Variables

#### Via Vercel Dashboard

1. Go to Project Settings → Environment Variables
2. Add variable with name and value
3. Select environments (Production, Preview, Development)
4. Deploy to apply changes

#### Via CLI

```bash
# Add environment variable
vercel env add VARIABLE_NAME production

# Pull environment variables
vercel env pull .env.local
```

### Environment Variable Types

```bash
# .env.local (local development)
NEXT_PUBLIC_API_URL=http://localhost:3000
DATABASE_URL=postgresql://...

# .env.production (Vercel Production)
# Set in Vercel Dashboard
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://...
```

**Important**:
- Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Never expose secrets with `NEXT_PUBLIC_` prefix
- Use Vercel dashboard for production secrets

## Deployment

### Automatic Deployments

Vercel automatically deploys on:
- Push to main/master → Production deployment
- Push to other branches → Preview deployment
- Pull requests → Preview deployment

### Manual Deployment

```bash
# Deploy to production
vercel --prod

# Deploy preview
vercel

# Deploy specific directory
vercel --cwd ./path/to/project
```

### Deploy Configuration

```json
// vercel.json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "production": true
    }
  }
}
```

## Next.js Deployment

### App Router (Next.js 13+)

Vercel automatically detects and optimizes:

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

// app/page.tsx
export default function Home() {
  return <div>Home Page</div>;
}

// Automatically deployed as server component
// API routes in app/api/ automatically become serverless functions
```

### API Routes

```typescript
// app/api/users/route.ts (App Router)
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
```

```typescript
// pages/api/users.ts (Pages Router)
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const users = await getUsers();
    return res.status(200).json({ users });
  }
  
  if (req.method === 'POST') {
    const user = await createUser(req.body);
    return res.status(201).json({ user });
  }
  
  res.setHeader('Allow', ['GET', 'POST']);
  return res.status(405).end();
}
```

### Server Components vs Client Components

```typescript
// app/dashboard/page.tsx - Server Component (default)
export default async function Dashboard() {
  const data = await fetchData(); // Runs on server
  
  return <div>{data}</div>;
}

// app/dashboard/client-component.tsx - Client Component
'use client';

import { useState } from 'react';

export function InteractiveComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

## Serverless Functions

### Node.js Functions

```typescript
// api/hello.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(req: VercelRequest, res: VercelResponse) {
  res.json({ message: 'Hello from Vercel!' });
}
```

### Python Functions

```python
# api/hello.py
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"message": "Hello from Vercel Python!"}')
```

### Function Configuration

```json
// vercel.json
{
  "functions": {
    "api/**/*.ts": {
      "runtime": "nodejs18.x",
      "memory": 1024,
      "maxDuration": 10
    }
  }
}
```

## Edge Functions

Deploy code to the edge for low latency:

```typescript
// middleware.ts (Next.js)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add custom header
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  return response;
}

export const config = {
  matcher: '/api/:path*',
};
```

```typescript
// app/api/edge/route.ts
export const runtime = 'edge';

export async function GET() {
  return new Response(JSON.stringify({ message: 'Edge function' }), {
    headers: { 'content-type': 'application/json' },
  });
}
```

## Custom Domains

### Adding Custom Domain

1. Go to Project Settings → Domains
2. Add domain name
3. Configure DNS records as shown:
   - A Record: `@` → `76.76.21.21`
   - CNAME: `www` → `cname.vercel-dns.com`

### SSL Certificates

Vercel automatically provisions SSL certificates for custom domains.

### Domain Configuration

```json
// vercel.json
{
  "domains": ["example.com", "www.example.com"]
}
```

## Preview Deployments

### Automatic Previews

Every PR/branch gets a preview URL:
- Format: `https://your-project-git-branch.vercel.app`
- Automatically deployed on push
- Updates on new commits

### Accessing Preview

```bash
# List preview deployments
vercel ls

# Get preview URL from PR comment (automatic)
```

### Preview Environment Variables

Set in Vercel Dashboard:
- Project Settings → Environment Variables
- Select "Preview" environment

## Performance Optimization

### Image Optimization

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
```

### Static Generation

```typescript
// Static at build time
export async function generateStaticParams() {
  return [
    { id: '1' },
    { id: '2' },
  ];
}

// Revalidate periodically (ISR)
export const revalidate = 3600; // 1 hour
```

### Incremental Static Regeneration (ISR)

```typescript
// app/products/[id]/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id);
  return <div>{product.name}</div>;
}
```

### Analytics

Enable Vercel Analytics:

```bash
npm install @vercel/analytics
```

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

## Monitoring & Debugging

### Function Logs

```bash
# View logs
vercel logs [deployment-url]

# Follow logs in real-time
vercel logs --follow

# Filter logs
vercel logs --since 1h
```

### Error Tracking

```typescript
// Add error tracking
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.VERCEL_ENV || 'development',
});
```

## CI/CD Integration

### GitHub Integration

Vercel automatically integrates with GitHub:
1. Connect repository in Vercel Dashboard
2. Enable deployments for branches
3. Configure build settings

### GitLab/Bitbucket

Similar setup via dashboard:
1. Project Settings → Git
2. Connect repository
3. Configure deployments

### Deployment Hooks

```bash
# Run command after deployment
vercel env add DEPLOY_HOOK_URL production

# In your project
curl $DEPLOY_HOOK_URL
```

## Best Practices

### 1. Environment Variables

- Never commit `.env` files
- Use Vercel Dashboard for production secrets
- Use `NEXT_PUBLIC_` only for safe, public variables
- Document required variables in README

### 2. Build Optimization

```javascript
// next.config.js
module.exports = {
  // Optimize bundle size
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },
  
  // Compress responses
  compress: true,
  
  // Reduce JavaScript
  swcMinify: true,
};
```

### 3. Function Limits

- **Maximum execution time**: 10 seconds (Hobby), 60 seconds (Pro)
- **Maximum memory**: 1024 MB
- **Request body size**: 4.5 MB

### 4. Database Connections

Use connection pooling for serverless:

```typescript
// lib/db.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 1, // Single connection for serverless
});

export { pool };
```

### 5. Caching

```typescript
// Cache API responses
export async function GET() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }, // Cache for 1 hour
  });
  
  return Response.json(await data.json());
}
```

## Troubleshooting

### Build Failures

```bash
# Debug build locally
vercel build

# View build logs
vercel logs [deployment-url] --debug
```

### Function Timeouts

- Reduce function execution time
- Use background jobs for long-running tasks
- Split large operations into smaller functions

### Environment Variable Issues

```bash
# Verify environment variables
vercel env ls

# Pull and check locally
vercel env pull .env.local
cat .env.local
```

## Common Patterns

### Redirects

```json
// vercel.json
{
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ]
}
```

### Headers

```json
// vercel.json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

### CORS Configuration

```typescript
// app/api/cors.ts
export async function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

## Checklist for Vercel Deployment

Before deploying to Vercel:

- [ ] Environment variables set in Vercel Dashboard
- [ ] `vercel.json` configured (if needed)
- [ ] Build command works locally (`npm run build`)
- [ ] No hardcoded secrets in code
- [ ] Images optimized with Next.js Image component
- [ ] API routes handle errors properly
- [ ] CORS configured for API routes (if needed)
- [ ] Database connections use pooling
- [ ] Functions respect timeout limits
- [ ] Custom domain configured (if applicable)
- [ ] Analytics enabled (optional)
- [ ] Error tracking configured (optional)
