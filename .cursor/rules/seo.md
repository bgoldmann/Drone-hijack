# SEO (Search Engine Optimization) Guide

Comprehensive guide for implementing SEO best practices in web applications. Covers meta tags, structured data, sitemaps, performance optimization, and content optimization for search engines.

## Overview

SEO involves optimizing your website to improve visibility in search engine results. This guide covers technical SEO, on-page optimization, and best practices for modern web applications.

## Meta Tags & HTML Structure

### Basic Meta Tags

```html
<!-- Essential meta tags -->
<head>
  <!-- Character encoding -->
  <meta charset="UTF-8" />
  
  <!-- Viewport for mobile -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  
  <!-- Primary meta tags -->
  <title>Page Title | Site Name</title>
  <meta name="title" content="Page Title | Site Name" />
  <meta name="description" content="Clear, concise description (150-160 characters)" />
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://example.com/page" />
  <meta property="og:title" content="Page Title" />
  <meta property="og:description" content="Description for social sharing" />
  <meta property="og:image" content="https://example.com/image.jpg" />
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="https://example.com/page" />
  <meta name="twitter:title" content="Page Title" />
  <meta name="twitter:description" content="Description for Twitter" />
  <meta name="twitter:image" content="https://example.com/image.jpg" />
  
  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/page" />
</head>
```

### Next.js Metadata (App Router)

```typescript
// app/page.tsx or layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'Page Title',
    template: '%s | Site Name',
  },
  description: 'Clear, concise description (150-160 characters)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Author Name' }],
  creator: 'Site Name',
  publisher: 'Site Name',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://example.com'),
  alternates: {
    canonical: '/',
    languages: {
      'en-US': '/en-US',
      'es-ES': '/es-ES',
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    siteName: 'Site Name',
    title: 'Page Title',
    description: 'Description for social sharing',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Page Title',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Page Title',
    description: 'Description for Twitter',
    images: ['/twitter-image.jpg'],
    creator: '@username',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
      publishedTime: post.publishedAt,
      authors: [post.author],
      type: 'article',
    },
  };
}
```

## Structured Data (JSON-LD)

### Article Schema

```typescript
// components/StructuredData.tsx
export function ArticleStructuredData({ article }) {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: article.title,
    description: article.description,
    image: article.image,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt,
    author: {
      '@type': 'Person',
      name: article.author.name,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Site Name',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.jpg',
      },
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  );
}
```

### Organization Schema

```typescript
const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Site Name',
  url: 'https://example.com',
  logo: 'https://example.com/logo.jpg',
  contactPoint: {
    '@type': 'ContactPoint',
    telephone: '+1-123-456-7890',
    contactType: 'customer service',
  },
  sameAs: [
    'https://twitter.com/username',
    'https://facebook.com/username',
  ],
};
```

### Breadcrumb Schema

```typescript
const breadcrumbSchema = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: 'https://example.com',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'Category',
      item: 'https://example.com/category',
    },
    {
      '@type': 'ListItem',
      position: 3,
      name: 'Page',
      item: 'https://example.com/category/page',
    },
  ],
};
```

## Sitemap Generation

### Next.js Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://example.com';
  
  // Static routes
  const staticRoutes = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 1,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    },
  ];
  
  // Dynamic routes (from database)
  const blogPosts = getBlogPosts();
  const dynamicRoutes = blogPosts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }));
  
  return [...staticRoutes, ...dynamicRoutes];
}
```

### Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

## Content Optimization

### Heading Structure

```html
<!-- Proper heading hierarchy -->
<h1>Main Page Title (Only one per page)</h1>
  <h2>Section Title</h2>
    <h3>Subsection</h3>
    <h3>Another Subsection</h3>
  <h2>Another Section</h2>
```

### Image Optimization

```typescript
import Image from 'next/image';

// Optimized image with SEO attributes
<Image
  src="/image.jpg"
  alt="Descriptive alt text that describes the image content"
  width={800}
  height={600}
  priority={isAboveFold}
  loading={isAboveFold ? undefined : 'lazy'}
/>
```

### Internal Linking

```typescript
// Good internal linking structure
<Link href="/related-article">
  <a>Related Article Title</a>
</Link>

// Use descriptive anchor text, not "click here"
```

### URL Structure

```typescript
// Good URLs
https://example.com/blog/seo-best-practices-2024
https://example.com/products/wireless-headphones

// Bad URLs
https://example.com/page?id=123
https://example.com/blog/post?p=456&cat=tech
```

## Performance Optimization

### Core Web Vitals

Optimize for Google's Core Web Vitals:

1. **Largest Contentful Paint (LCP)**: < 2.5 seconds
   - Optimize images
   - Use CDN
   - Minimize render-blocking resources

2. **First Input Delay (FID)**: < 100 milliseconds
   - Minimize JavaScript execution
   - Use code splitting
   - Defer non-critical JavaScript

3. **Cumulative Layout Shift (CLS)**: < 0.1
   - Set dimensions on images and videos
   - Reserve space for ads and embeds
   - Avoid inserting content above existing content

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={1200}
  height={630}
  quality={85}
  format="webp"
  placeholder="blur"
/>
```

### Code Splitting

```typescript
// Lazy load components
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false, // If client-only
});
```

## Mobile Optimization

### Responsive Design

```css
/* Mobile-first approach */
.container {
  width: 100%;
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
}
```

### Mobile-Friendly Meta Tags

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-capable" content="yes" />
```

## Technical SEO

### HTTPS

Always use HTTPS:
- Required for modern SEO
- Required for many browser features
- Improves security and trust

### Page Speed

```typescript
// Next.js optimization
// next.config.js
module.exports = {
  compress: true,
  poweredByHeader: false,
  generateEtags: true,
};
```

### Caching Headers

```typescript
// API route with caching
export async function GET() {
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

## Local SEO (if applicable)

### Local Business Schema

```typescript
const localBusinessSchema = {
  '@context': 'https://schema.org',
  '@type': 'LocalBusiness',
  name: 'Business Name',
  image: 'https://example.com/logo.jpg',
  '@id': 'https://example.com',
  url: 'https://example.com',
  telephone: '+1-123-456-7890',
  address: {
    '@type': 'PostalAddress',
    streetAddress: '123 Main St',
    addressLocality: 'City',
    addressRegion: 'State',
    postalCode: '12345',
    addressCountry: 'US',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: 40.7128,
    longitude: -74.0060,
  },
  openingHoursSpecification: {
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    opens: '09:00',
    closes: '17:00',
  },
};
```

## Content Strategy

### Keyword Research

- Use tools: Google Keyword Planner, Ahrefs, SEMrush
- Target long-tail keywords
- Focus on user intent
- Use natural language (avoid keyword stuffing)

### Content Quality

- Write for users first, search engines second
- Provide value and answer questions
- Use natural language
- Update content regularly
- Ensure uniqueness and originality

### Title Tag Best Practices

```typescript
// Good title tags
- Primary Keyword | Brand Name (50-60 characters)
- How to [Action] | Guide to [Topic]
- [Number] Best [Things] for [Purpose] in [Year]

// Format
const title = `${primaryKeyword} | ${brandName}`;
```

## SEO Checklist

Before launching or updating a page:

- [ ] Unique, descriptive title tag (50-60 characters)
- [ ] Meta description (150-160 characters)
- [ ] Proper heading hierarchy (H1, H2, H3)
- [ ] Alt text on all images
- [ ] Internal linking structure
- [ ] Canonical URL set
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags
- [ ] Structured data (JSON-LD) implemented
- [ ] Mobile-responsive design
- [ ] Fast page load times (< 3 seconds)
- [ ] HTTPS enabled
- [ ] XML sitemap generated and submitted
- [ ] robots.txt configured
- [ ] No broken links
- [ ] Semantic HTML structure
- [ ] URL structure is clean and descriptive
- [ ] Content is original and valuable

## Tools & Resources

### Testing Tools

- **Google Search Console**: Monitor search performance
- **Google PageSpeed Insights**: Test page speed
- **Schema Markup Validator**: Validate structured data
- **Mobile-Friendly Test**: Check mobile optimization

### Analytics

- **Google Analytics 4**: Track user behavior
- **Google Search Console**: Monitor search queries and rankings
- **Bing Webmaster Tools**: For Bing optimization

### SEO Plugins/Libraries

- **Next.js**: Built-in SEO features (Metadata API)
- **react-helmet**: For React apps (legacy)
- **next-seo**: Next.js SEO package (alternative)

## Best Practices

### Do's

- ✅ Use descriptive, keyword-rich URLs
- ✅ Write unique, valuable content
- ✅ Optimize images with alt text
- ✅ Use proper heading hierarchy
- ✅ Implement structured data
- ✅ Build internal linking structure
- ✅ Ensure mobile responsiveness
- ✅ Monitor Core Web Vitals

### Don'ts

- ❌ Keyword stuffing
- ❌ Duplicate content
- ❌ Hidden text or links
- ❌ Thin or low-quality content
- ❌ Slow page load times
- ❌ Broken links
- ❌ Missing alt text on images
- ❌ Poor mobile experience

## Common Patterns

### SEO Component (Next.js)

```typescript
// components/SEO.tsx
interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url?: string;
  type?: string;
}

export function SEO({ title, description, image, url, type = 'website' }: SEOProps) {
  const fullTitle = `${title} | Site Name`;
  const fullUrl = url ? `https://example.com${url}` : 'https://example.com';
  const fullImage = image ? `https://example.com${image}` : 'https://example.com/og-default.jpg';

  return (
    <>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={fullUrl} />
      
      {/* Open Graph */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={fullUrl} />
      <meta property="og:image" content={fullImage} />
      
      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullImage} />
    </>
  );
}
```

### Generate Metadata Function

```typescript
// utils/seo.ts
export function generateMetadata({
  title,
  description,
  path = '/',
  image,
}: {
  title: string;
  description: string;
  path?: string;
  image?: string;
}): Metadata {
  const url = `https://example.com${path}`;
  const ogImage = image || 'https://example.com/og-default.jpg';

  return {
    title: `${title} | Site Name`,
    description,
    openGraph: {
      title,
      description,
      url,
      images: [ogImage],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [ogImage],
    },
    alternates: {
      canonical: url,
    },
  };
}
```
